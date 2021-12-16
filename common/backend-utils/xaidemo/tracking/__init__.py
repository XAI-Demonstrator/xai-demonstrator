from fastapi import FastAPI

from .config import settings
from .middleware import ExperimentTrackerMiddleware

from .record import record_data
from ..http_client import set_up as _set_up_http_client


__all__ = ["instrument_app", "record_data"]


def instrument_app(app: FastAPI):
    if settings.experiment:
        _set_up_http_client(app)
        app.add_middleware(ExperimentTrackerMiddleware)
