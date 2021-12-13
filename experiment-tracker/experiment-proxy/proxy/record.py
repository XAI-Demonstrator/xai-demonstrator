from typing import Dict, Any, Optional
from pydantic import BaseModel, root_validator

import aiohttp

from .config import settings
from .http_client import AioHttpClientSession

collector_timeout = aiohttp.ClientTimeout(settings.collector_timeout)


class RequestData(BaseModel):
    raw: Optional[str]
    content_type: Optional[str]
    decoded: Optional[dict]

    @root_validator
    def all_or_nothing(cls, values):
        entries = [values.get("raw"), values.get("content_type"), values.get("decoded")]
        is_none = [entry is None for entry in entries]
        if not all(is_none) and any(is_none):
            raise ValueError("Either all or none of the values have to be set.")
        return values


class ResponseData(BaseModel):
    raw: Optional[str]
    status_code: int
    decoded: Optional[dict]

    @root_validator
    def all_or_nothing(cls, values):
        entries = [values.get("raw"), values.get("decoded")]
        is_none = [entry is None for entry in entries]
        if not all(is_none) and any(is_none):
            raise ValueError("Either both 'raw' and 'decoded' are set or neither is.")
        return values


class TrackedData(BaseModel):
    request: RequestData
    response: ResponseData


class SourceInformation(BaseModel):
    name: str = settings.backend_service
    location: str = settings.backend_url
    endpoint: str


class PartialRecordRequest(BaseModel):
    id: str
    source: SourceInformation
    part: Dict[str, Any]


async def record_data(trace_id: str,
                      endpoint: str,
                      key: str,
                      value: Dict[str, Any]):
    """Send the data to the collector."""
    if key == "id":
        raise ValueError("Key cannot be 'id'")

    partial = PartialRecordRequest(id=trace_id,
                                   source=SourceInformation(endpoint=endpoint),
                                   part = {"tracked": value})

    async with AioHttpClientSession() as session:
        await session.post(settings.collector_url + "/record",
                           timeout=collector_timeout,
                           json=partial.dict())
