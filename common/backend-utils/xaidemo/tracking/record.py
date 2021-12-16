import asyncio
import logging
import threading
from collections import defaultdict
from typing import Dict, Any
from typing import Optional, List

from opentelemetry import trace
from pydantic import BaseModel
from xaidemo.tracing import traced, get_tracer

from .config import settings
from ..http_client import AioHttpClientSession

logger = logging.getLogger(__name__)


class SourceInformation(BaseModel):
    service: str = settings.service_name
    provider: str = settings.service_name

    class Config:
        extra = "forbid"


class PartialRecordRequest(BaseModel):
    id: str
    source: SourceInformation
    part: Dict[str, Dict[str, Any]]
    label: str

    class Config:
        extra = "forbid"


class TaskMemory:
    lock: threading.Lock = threading.Lock()
    memory: Dict[str, List[PartialRecordRequest]] = defaultdict(list)

    @classmethod
    def add_task(cls, record_id, task):
        with cls.lock:
            cls.memory[record_id].append(task)

    @classmethod
    def get_tasks_and_erase_memory(cls, record_id):
        with cls.lock:
            list_of_tasks = cls.memory[record_id]
            del cls.memory[record_id]
            return list_of_tasks


def initialize_record(label: Optional[str] = None):
    span = trace.get_current_span()

    if label is None:
        if hasattr(span, "name"):
            label = span.name
        else:
            raise ValueError("No 'label' provided and could not determine label from OpenTelemetry span.")

    return get_record_id(span), label


def get_record_id(span: Optional[trace.Span] = None):
    if span is None:
        span = trace.get_current_span()
    trace_id = span.get_span_context().trace_id
    return f"{trace_id:x}"


@traced
def record_data(key: str, value: Dict[str, Any], label: Optional[str] = None):
    if not settings.experiment:
        return

    record_id, label = initialize_record(label)

    partial_record = PartialRecordRequest(id=record_id,
                                          source=SourceInformation(),
                                          part={key: value},
                                          label=label)
    TaskMemory.add_task(record_id, partial_record)


async def send_record(partial_record: PartialRecordRequest):
    logger.info(f"Recording data for {partial_record.source.service}: {partial_record.label} "
                f"(ID: {partial_record.id})")

    with get_tracer().start_as_current_span("send_record"):
        async with AioHttpClientSession() as session:
            try:
                async with session.post(settings.collector_url + "/record",
                                        timeout=settings.collector_timeout,
                                        json=partial_record.dict()) as response:
                    if response.status != 200:
                        logger.error(f"Request to collector service failed with: {response.status}")
            except asyncio.exceptions.TimeoutError:
                logger.error(f"Request to collector timed out.")
