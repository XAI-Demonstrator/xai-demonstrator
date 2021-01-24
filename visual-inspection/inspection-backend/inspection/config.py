from pydantic import BaseSettings


class Settings(BaseSettings):
    service_name: str = "inspection-service"
    environment: str = "local"
    # OpenTelemetry exporter configuration
    agent_host_name: str = "localhost"
    agent_port: int = 6831


settings = Settings()
