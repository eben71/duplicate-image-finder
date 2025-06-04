# backend/config/settings.py
from __future__ import annotations

import sys
from pathlib import Path
from typing import Optional, no_type_check
from pydantic_settings import BaseSettings
from pydantic import ValidationError, Field


class Settings(BaseSettings):
    # ───────────────────────── Required (no defaults) ──────────────────────────
    database_url: str = Field(..., validation_alias="DATABASE_URL")
    celery_broker_url: str = Field(..., validation_alias="CELERY_BROKER_URL")
    celery_backend_url: str = Field(..., validation_alias="CELERY_BACKEND_URL")
    google_photos_url: str = Field(..., validation_alias="GOOGLE_PHOTOS_URL")
    fastapi_endpoint: str = Field(..., validation_alias="FASTAPI_ENDPOINT")

    # ───────────────────────── Optional / defaults ─────────────────────────────
    session_cookie_path: Optional[Path] = Field(
        Path("~/.gp_session.json").expanduser(), validation_alias="SESSION_COOKIE_PATH"
    )
    ingestion_mode: str = Field("scrape", validation_alias="INGESTION_MODE")
    batch_size: int = Field(50, validation_alias="BATCH_SIZE")
    timeout: int = Field(30_000, validation_alias="TIMEOUT")  # ms
    scroll_depth: int = Field(5, validation_alias="SCROLL_DEPTH")

    # Pydantic v2 config
    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "case_sensitive": False,
    }


@no_type_check
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
