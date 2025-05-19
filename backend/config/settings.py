from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    database_url: str
    celery_broker_url: str
    celery_backend_url: str
    session_cookie_path: Optional[str] = "~/.gp_session.json"
    ingestion_mode: str = "scrape"
    google_photos_url: str
    batch_size: int = 50
    timeout: int = 30000
    scroll_depth: int = 5
    fastapi_endpoint: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
