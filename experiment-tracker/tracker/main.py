import datetime
import uuid
from typing import Dict, Any, Optional

import couchdb

from fastapi import FastAPI
from pydantic import BaseModel, ValidationError

from .config import settings

couch = couchdb.Server(f"{settings.db_user}:{settings.db_password}@{settings.db_server}:{settings.db_port}")

db = couch[settings.db_name]

app = FastAPI()


class Request(BaseModel):
    service_name: str
    request_id: uuid.UUID
    timestamp: datetime.datetime = datetime.datetime.now()
    request: Optional[Dict[str, Any]]
    response: Optional[Dict[str, Any]]


@app.put("/record")
def record(request: Request):
    db[request.request_id] = request.dict()


@app.get("/get/{identifier}")
def retrieve(identifier: uuid.UUID) -> Request:
    try:
        return Request(**db[identifier])
    except ValidationError:
        print("Invalid DB entry")
    except couchdb.ResourceNotFound:
        print("Not found")
