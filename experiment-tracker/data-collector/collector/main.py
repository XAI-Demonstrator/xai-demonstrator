import time
from typing import Dict, Any, Optional, List

import couchdb
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, ValidationError
from starlette.status import HTTP_404_NOT_FOUND, HTTP_409_CONFLICT, HTTP_500_INTERNAL_SERVER_ERROR
from xaidemo import tracing
from xaidemo.tracking.data_models import PartialRecordRequest

from .repository import repo

tracing.set_up()

app = FastAPI()


class Record(BaseModel):
    id: str
    timestamp: float = time.time()
    service: str
    data: Dict[str, Dict[str, Any]]

    _id: Optional[str]
    _rev: Optional[str]

    class Config:
        extra = "ignore"


class PartialRecord(BaseModel):
    data: Dict[str, Any]
    label: str
    provider: str


class Dump(BaseModel):
    records: List[Record]


@app.post("/record")
def record(partial_record_request: PartialRecordRequest):
    id_ = partial_record_request.id
    if id_ in repo:
        current_record = Record(**repo[id_])

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
        current_record.data.update(partial_record)
        repo[id_] = current_record.dict()
    else:
        partial_record = create_partial_record(partial_record_request)
        repo[id_] = Record(id=id_,
                           service=partial_record_request.source.service,
                           data=partial_record).dict()


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
