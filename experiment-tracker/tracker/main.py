import time
import uuid
from typing import Dict, Any, Optional

import couchdb

from fastapi import FastAPI
from pydantic import BaseModel, ValidationError

from .config import settings

couch = couchdb.Server(f"http://{settings.db_user}:{settings.db_password}"
                       f"@{settings.db_server}:{settings.db_port}")

try:
    db = couch.create(settings.db_name)
except couchdb.PreconditionFailed:
    db = couch[settings.db_name]

app = FastAPI()


class Request(BaseModel):
    service_name: str
    request_id: uuid.UUID
    timestamp: float = time.time()
    request: Optional[Dict[str, Any]]
    response: Optional[Dict[str, Any]]


@app.put("/record")
def record(request: Request):
    db[str(request.request_id)] = request.dict(exclude={'request_id'})


@app.get("/get/{identifier}")
def retrieve(identifier: uuid.UUID) -> Request:
    try:
        return Request(**db[str(identifier)],
                       request_id=identifier)
    except ValidationError:
        print("Invalid DB entry")
    except couchdb.ResourceNotFound:
        print("Not found")
