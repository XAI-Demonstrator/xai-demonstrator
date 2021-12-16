from pydantic import BaseSettings


class Settings(BaseSettings):
    service_name: str = "data-collector"
    # Database settings
    db_host: str
    db_port: int = 5984
    db_name: str = "xaidemo"
    db_user: str
    db_password: str


settings = Settings()
