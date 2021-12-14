import time
from typing import Dict, Any, Optional, List

import couchdb
from fastapi import FastAPI, HTTPException, Response
from pydantic import BaseModel, ValidationError
from starlette.status import HTTP_404_NOT_FOUND, HTTP_409_CONFLICT, HTTP_500_INTERNAL_SERVER_ERROR
from xaidemo import tracing

from .repository import repo

tracing.set_up()

app = FastAPI()


class SourceInformation(BaseModel):
    name: Optional[str]
    location: Optional[str]
    endpoint: Optional[str]

    class Config:
        extra = "forbid"


class Record(BaseModel):
    id: str
    timestamp: float = time.time()
    source: SourceInformation
    data: Dict[str, Dict[str, Any]]

    _id: Optional[str]
    _rev: Optional[str]

    class Config:
        extra = "ignore"


class PartialRecord(BaseModel):
    id: str
    source: SourceInformation
    part: Dict[str, Dict[str, Any]]

    class Config:
        extra = "forbid"


class Dump(BaseModel):
    records: List[Record]


@app.post("/record")
def record(partial_record: PartialRecord):
    id_ = partial_record.id
    if id_ in repo:
        current_record = Record(**repo[id_])

        # TODO: Check that there is no conflicting source information

        for key in partial_record.part:
            if key in current_record.data:
                raise HTTPException(
                    status_code=HTTP_409_CONFLICT,
                    detail=f"Key {key} already set for item {id_}.")

        current_record.data.update(partial_record.part)
        repo[id_] = current_record.dict()

    else:
        # TODO: Check that complete source information is given

        repo[id_] = Record(id=id_,
                           source=partial_record.source.dict(),
                           data=partial_record.part).dict()


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
