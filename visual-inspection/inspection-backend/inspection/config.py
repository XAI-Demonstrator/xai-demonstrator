import pathlib
from pydantic import BaseSettings, validator


class Settings(BaseSettings):
    service_name: str = "inspection-service"
    root_path: str = ""
    path_prefix: str = ""
    # Explanation configuration
    default_explainer: str = "lime"
    # Monitoring
    log_input: bool = False
    log_path: pathlib.Path = "./log"

    @validator('log_path')
    def log_path_must_exist(cls, v):
        v.mkdir(parents=True, exist_ok=True)
        return v


settings = Settings()
