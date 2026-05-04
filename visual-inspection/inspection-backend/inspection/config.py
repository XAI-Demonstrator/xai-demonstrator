import pathlib
from pydantic import Field, field_validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    service_name: str = "inspection-service"
    # Allow reading env vars in both UPPERCASE and lowercase by providing explicit env names.
    root_path: str = Field("", env="ROOT_PATH")
    path_prefix: str = Field("", env="PATH_PREFIX")
    # Model configuration
    default_model: str = Field("my_model", env="DEFAULT_MODEL")
    # Explanation configuration
    default_explainer: str = Field("tcav", env="DEFAULT_EXPLAINER")
    # Monitoring
    log_input: bool = Field(False, env="LOG_INPUT")
    log_path: pathlib.Path = Field(pathlib.Path("./log"), env="LOG_PATH")

    @field_validator('log_path')
    def log_path_must_exist(cls, v):
        v.mkdir(parents=True, exist_ok=True)
        return v


settings = Settings()
