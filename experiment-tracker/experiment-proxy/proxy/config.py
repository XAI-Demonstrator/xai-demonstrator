from pydantic_settings import BaseSettings


class ProxySettings(BaseSettings):
    backend_url: str
    backend_timeout: int = 300
    backend_service: str
    # This environment variable is handled by the xaidemo package,
    # where it is defined as an optional configuration parameter
    # We keep this here to ensure that it is set in all cases
    collector_url: str  # pragma: no cover


settings = ProxySettings()
