from pydantic import BaseSettings

__all__ = ["settings"]


class Settings(BaseSettings):
    # proxy
    backend_url: str = ""
    backend_timeout: int = 300
    backend_service: str = "undefined"
    # experiment data collector
    collector_url: str = ""
    collector_timeout: int = 60
    # aiohttp
    connection_limit: int = 100
    connection_limit_per_host: int = 100


settings = Settings()
