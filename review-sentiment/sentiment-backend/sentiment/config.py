from pydantic import BaseSettings


class Settings(BaseSettings):
    service_name: str = "sentiment-service"
    environment: str = "local"
    # OpenTelemetry exporter configuration
    agent_host_name: str = "localhost"
    agent_port: int = 6831
    # Explanation configuration
    default_explainer: str = "integrated_gradients"
    default_target: int = 4


settings = Settings()
