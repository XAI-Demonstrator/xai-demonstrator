from fastapi import FastAPI
from xaidemo import tracing
from xaidemo.routers import vue_frontend

from .api import api
from .config import settings

tracing.set_up()

app = FastAPI(root_path=settings.root_path)
app.include_router(api, prefix=settings.path_prefix)
app.include_router(vue_frontend(__file__), prefix=settings.path_prefix)

tracing.instrument_app(app)
