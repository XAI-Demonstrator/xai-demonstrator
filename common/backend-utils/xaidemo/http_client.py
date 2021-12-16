"""An async HTTP client based on aiohttp for use in FastAPI backends.

Inspired by
https://github.com/raphaelauv/fastAPI-aiohttp-example/blob/master/src/fastAPI_aiohttp/fastAPI.py
"""
from typing import Optional

import aiohttp
from fastapi import FastAPI
from opentelemetry.instrumentation.aiohttp_client import (
    AioHttpClientInstrumentor
)
from pydantic import BaseSettings


__all__ = ["set_up", "AioHttpClientSession"]


class AioHttpSettings(BaseSettings):
    connection_limit: int = 100
    connection_limit_per_host: int = 100


settings = AioHttpSettings()


async def close_session():
    await AioHttpClientSession.close_client_session()


def set_up(app: FastAPI):
    AioHttpClientInstrumentor().instrument()
    app.router.on_shutdown.append(close_session)


class AioHttpClientSession:
    client: Optional[aiohttp.ClientSession] = None

    def __init__(self):
        self.conn = aiohttp.TCPConnector(limit=settings.connection_limit,
                                         limit_per_host=settings.connection_limit_per_host)

    @classmethod
    async def __aenter__(cls):
        if cls.client is None:
            cls.client = aiohttp.ClientSession()

        return cls.client

    @classmethod
    async def __aexit__(cls, exc_type, exc_value, exc_traceback):
        pass

    @classmethod
    async def close_client_session(cls):
        if cls.client is not None:
            await cls.client.close()
            cls.client = None
