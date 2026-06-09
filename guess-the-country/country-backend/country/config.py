from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    service_name: str = "country-service"
    root_path: str = ""
    path_prefix: str = ""
    # Google Maps API access
    google_maps_api_token: str = ""
    batch_size: int = 32


settings = Settings()
