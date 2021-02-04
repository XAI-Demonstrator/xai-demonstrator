from pydantic import BaseSettings


class Settings(BaseSettings):
    service_name: str = "inspection-service"
    root_path: str = ""
    path_prefix: str = ""
    # Explanation configuration
    default_explainer: str = "lime"


settings = Settings()
