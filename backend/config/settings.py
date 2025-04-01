from pydantic import BaseSettings, FilePath
from typing import Optional

class Settings(BaseSettings):
    database_url: str
    celery_broker_url: str
    celery_result_backend: str
    session_cookie_path: Optional[str] = "~/.gp_session.json"
    ingestion_mode: str = "scrape"

    class Config:
        env_file = ".env"

settings = Settings()
