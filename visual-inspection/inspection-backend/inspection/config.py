from pydantic import BaseSettings


class Settings(BaseSettings):
    service_name: str = "inspection-service"
    # Explanation configuration
    default_explainer: str = "lime"


settings = Settings()
