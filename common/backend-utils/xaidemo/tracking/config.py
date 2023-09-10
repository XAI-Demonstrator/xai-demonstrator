from typing import Optional

from pydantic import root_validator
from pydantic_settings import BaseSettings


class TrackingSettings(BaseSettings):
    experiment: bool = False
    service_name: str
    collector_url: Optional[str] = None
    collector_timeout: int = 60

    @root_validator(skip_on_failure=True)
    def experiment_requires_collector(cls, values):
        if values.get("experiment"):
            if not values.get("collector_url", False):
                raise ValueError("If EXPERIMENT is True, COLLECTOR_URL must be set.")
        return values


settings = TrackingSettings()
