from typing import Optional

from pydantic import BaseModel, root_validator
from xaidemo.tracking.record import initialize_record, PartialRecordRequest, SourceInformation

from .config import settings


class RequestData(BaseModel):
    raw: Optional[str]
    content_type: Optional[str]
    decoded: Optional[dict]

    @root_validator(skip_on_failure=True)
    def all_or_nothing(cls, values):
        entries = [values.get("raw"), values.get("content_type"), values.get("decoded")]
        is_none = [(entry is None or not entry) for entry in entries]
        if not all(is_none) and any(is_none):
            raise ValueError("Either all or none of the values have to be set.")
        return values


class ResponseData(BaseModel):
    raw: Optional[str]
    status_code: int
    decoded: Optional[dict]

    @root_validator(skip_on_failure=True)
    def all_or_nothing(cls, values):
        entries = [values.get("raw"), values.get("decoded")]
        is_none = [(entry is None or not entry) for entry in entries]
        if not all(is_none) and any(is_none):
            raise ValueError("Either both 'raw' and 'decoded' are set or neither is.")
        return values


class TrackedData(BaseModel):
    request: RequestData
    response: ResponseData


def prepare_record(endpoint: str,
                   key: str,
                   value: TrackedData) -> PartialRecordRequest:
    record_id, label = initialize_record(label=endpoint)
    source_info = SourceInformation(service=settings.backend_service)

    return PartialRecordRequest(id=record_id,
                                source=source_info,
                                part={key: value.dict()},
                                label=label)
