import logging
import threading
import time
from typing import Dict, Any, List

import couchdb
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, ValidationError
from starlette.status import HTTP_404_NOT_FOUND, HTTP_409_CONFLICT, HTTP_500_INTERNAL_SERVER_ERROR
from xaidemo import tracing
from xaidemo.tracing import traced
from xaidemo.tracking.record import PartialRecordRequest

from .config import settings
from .repository import repo

logger = logging.getLogger(__name__)

tracing.set_up()

app = FastAPI()


class Record(BaseModel):
    id: str
    timestamp: float = time.time()
    service: str
    data: Dict[str, Dict[str, Any]]

    class Config:
        extra = "ignore"


class PartialRecord(BaseModel):
    data: Dict[str, Any]
    label: str
    provider: str


class Dump(BaseModel):
    records: List[Record]


creation_lock = threading.Lock()


@app.post("/record")
def record(partial_record_request: PartialRecordRequest):
    if partial_record_request.id in repo:
        update_record(partial_record_request)
    else:
        with creation_lock:
            if partial_record_request.id not in repo:
                partial_record = create_partial_record(partial_record_request)
                repo[partial_record_request.id] = Record(id=partial_record_request.id,
                                                         service=partial_record_request.source.service,
                                                         data=partial_record).dict()
                return  # return early to allow the logical "else" to be outside the lock context
        # else
        update_record(partial_record_request)


@traced
def update_record(partial_record_request):
    id_ = partial_record_request.id

    for attempt in range(settings.retries):
        try:
            _update_record(id_, partial_record_request)
        except couchdb.http.ResourceConflict:
            logger.warning("Resource conflict, try again...")
        else:
            break
    else:
        logger.error(f"Could not submit update to {id_} within {settings.retries} attempts.")


def _update_record(id_, partial_record_request):
    current_doc = repo[id_]

    current_record = Record(**current_doc)
    if current_record.service != partial_record_request.source.service:
        raise HTTPException(
            status_code=HTTP_409_CONFLICT,
            detail=f"Key {id_} is already associated with {current_record.service}, "
                   f"received partial request allegedly from {partial_record_request.source.service}"
        )
    for key in partial_record_request.part:
        if key in current_record.data:
            raise HTTPException(
                status_code=HTTP_409_CONFLICT,
                detail=f"Key {key} already set for item {id_}.")

    partial_record = create_partial_record(partial_record_request)
    current_doc["data"].update(partial_record)
    repo[id_] = current_doc


def create_partial_record(partial_record_request: PartialRecordRequest):
    return {
        key: PartialRecord(
            data=partial_record_request.part[key],
            label=partial_record_request.label,
            provider=partial_record_request.source.provider
        ).dict() for key in partial_record_request.part}


@app.get("/get/{identifier}")
def retrieve(identifier: str) -> Record:
    try:
        return Record(**repo[identifier])
    except ValidationError:
        raise HTTPException(status_code=HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Cannot parse record from database.")
    except (KeyError, couchdb.ResourceNotFound):
        raise HTTPException(status_code=HTTP_404_NOT_FOUND,
                            detail=f"No record {str(identifier)} in database.")


@app.get("/dump")
def dump() -> Dump:
    # TODO: How large can this response be? We might need to return data in chunks

    return Dump(records=[Record(**repo[doc_id])
                         for doc_id in repo])


tracing.instrument_app(app)
