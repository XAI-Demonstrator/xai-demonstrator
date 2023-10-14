import logging
import sys

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from xaidemo import tracing, tracking
from xaidemo.routers import vue_frontend

from .api import api
from .config import settings

logging.getLogger("uvicorn").propagate = False
logging.basicConfig(stream=sys.stdout, level=logging.INFO)

tracing.set_up()

origins = [
    "http://localhost:3000",
]

app = FastAPI(root_path=settings.root_path)
tracking.instrument_app(app)
app.include_router(api, prefix=settings.path_prefix)
app.include_router(vue_frontend(__file__), prefix=settings.path_prefix)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

tracing.instrument_app(app)
