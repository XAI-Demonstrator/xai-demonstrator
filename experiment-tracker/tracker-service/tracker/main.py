import time
import uuid
from typing import Dict, Any, Optional

import couchdb
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, ValidationError

from .repository import repo

app = FastAPI()


class Request(BaseModel):
    service_name: str
    request_id: uuid.UUID
    timestamp: float = time.time()
    request: Optional[Dict[str, Any]]
    response: Optional[Dict[str, Any]]


@app.put("/record", status_code=201)
def record(request: Request):
    repo[str(request.request_id)] = request.dict(exclude={'request_id'})


@app.get("/get/{identifier}")
def retrieve(identifier: uuid.UUID) -> Request:
    try:
        return Request(**repo[str(identifier)],
                       request_id=identifier)
    except ValidationError:
        raise HTTPException(status_code=500,
                            detail="Corrupted database.")
    except (KeyError, couchdb.ResourceNotFound):
        raise HTTPException(status_code=404,
                            detail=f"No record {str(identifier)} in database.")
