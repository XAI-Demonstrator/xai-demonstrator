import logging
import sys

from fastapi import FastAPI
from xaidemo import tracing, http_client, tracking


from xaidemo.routers import vue_frontend

from .api import api
from .config import settings

logging.getLogger("uvicorn").propagate = False
logging.basicConfig(stream=sys.stdout, level=logging.INFO)

tracing.set_up()

app = FastAPI(root_path=settings.root_path)
tracking.instrument(app)
app.include_router(api, prefix=settings.path_prefix)
app.include_router(vue_frontend(__file__), prefix=settings.path_prefix)

tracing.instrument_app(app)
