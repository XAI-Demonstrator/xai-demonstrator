from pydantic import BaseSettings


class Settings(BaseSettings):
    service_name: str = "country-service"
    root_path: str = ""
    path_prefix: str = ""
    streetview_static_api_token = ""
    streetview_image_size: int = 448
    streetview_max_retries: int = 16
    batch_size: int = 32


settings = Settings()
