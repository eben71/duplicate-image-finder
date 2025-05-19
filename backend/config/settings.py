# backend/config/settings.py
from __future__ import annotations

import sys
from pathlib import Path
from typing import Optional

from pydantic import Field, ValidationError
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # ───────────────────────── Required (no defaults) ──────────────────────────
    database_url: str = Field(env="DATABASE_URL")
    celery_broker_url: str = Field(env="CELERY_BROKER_URL")
    celery_backend_url: str = Field(env="CELERY_BACKEND_URL")
    google_photos_url: str = Field(env="GOOGLE_PHOTOS_URL")
    fastapi_endpoint: str = Field(env="FASTAPI_ENDPOINT")

    # ───────────────────────── Optional / defaults ─────────────────────────────
    session_cookie_path: Optional[Path] = Field(
        Path("~/.gp_session.json").expanduser(), env="SESSION_COOKIE_PATH"
    )
    ingestion_mode: str = Field("scrape", env="INGESTION_MODE")
    batch_size: int = Field(50, env="BATCH_SIZE")
    timeout: int = Field(30_000, env="TIMEOUT")  # ms
    scroll_depth: int = Field(5, env="SCROLL_DEPTH")

    # Pydantic v2 config
    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "case_sensitive": False,
    }


def get_settings() -> Settings:
    """Return a validated Settings instance or exit with a helpful message."""
    try:
        return Settings()  # pulls values from env and `.env` automatically
    except ValidationError as exc:
        # Pretty-print and exit non-zero so Docker / CI fails fast
        print("❌  Configuration error:\n", exc, file=sys.stderr)
        sys.exit(1)


# Singleton used by the rest of the app
settings: Settings = get_settings()
