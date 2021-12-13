from pydantic import BaseSettings


class Settings(BaseSettings):
    service_name: str = "experiment-collector"
    # Database settings
    db_server: str = "localhost"
    db_port: int = 5984
    db_user: str = "user"
    db_password: str = "pw"
    db_name: str = "xaidemo"


settings = Settings()
