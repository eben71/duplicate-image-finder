# backend/config/settings.py
from __future__ import annotations

import logging
import os
import sys
from pathlib import Path
from typing import no_type_check

from pydantic import Field, ValidationError
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # ───────────────────────── Required (no defaults) ──────────────────────────
    DATABASE_URL: str = Field(..., validation_alias="DATABASE_URL")
    CELERY_BROKER_URL: str = Field(..., validation_alias="CELERY_BROKER_URL")
    CELERY_BACKEND_URL: str = Field(..., validation_alias="CELERY_BACKEND_URL")
    GOOGLE_PHOTOS_URL: str = Field(..., validation_alias="GOOGLE_PHOTOS_URL")
    GOOGLE_SEARCH_URL: str = Field(..., validation_alias="GOOGLE_SEARCH_URL")
    GOOGLE_USERINFO_URL: str = Field(..., validation_alias="GOOGLE_USERINFO_URL")
    FASTAPI_ENDPOINT: str = Field(..., validation_alias="FASTAPI_ENDPOINT")
    GOOGLE_CLIENT_ID: str = Field(..., validation_alias="GOOGLE_CLIENT_ID")
    GOOGLE_CLIENT_SECRET: str = Field(..., validation_alias="GOOGLE_CLIENT_SECRET")
    GOOGLE_REDIRECT_URI: str = Field(..., validation_alias="GOOGLE_REDIRECT_URI")
    ENCRYPTION_KEY: str = Field(..., validation_alias="ENCRYPTION_KEY")

    # ───────────────────────── Optional / defaults ─────────────────────────────
    SESSION_COOKIE_PATH: Path | None = Field(
        Path("~/.gp_session.json").expanduser(), validation_alias="SESSION_COOKIE_PATH"
    )
    INGESTION_MODE: str = Field("api", validation_alias="INGESTION_MODE")
    INGESTION_YEAR: int | None = None
    INGESTION_START_PAGE: int = Field(1, validation_alias="INGESTION_START_PAGE")
    INGESTION_END_PAGE: int | None = None
    INGESTION_PAGE_SIZE: int = Field(100, validation_alias="INGESTION_PAGE_SIZE")
    LOG_LEVEL: int = logging.DEBUG

    # Pydantic v2 config
    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "case_sensitive": False,
    }

    def require_env(self, var_name: str) -> str:
        """
        Retrieve an environment variable or raise an error if it's missing.
        """
        value = self.__getattribute__(var_name.upper())
        if value is None or (isinstance(value, str) and value.strip() == ""):
            raise ValueError(f"{var_name} environment variable is required")
        return value


@no_type_check
def get_settings() -> Settings:
    """Return a validated Settings instance or exit with a helpful message."""
    try:
        env_file = (
            None if "PYTEST_CURRENT_TEST" in os.environ else Settings.model_config.get("env_file")
        )
        settings = Settings(_env_file=env_file)
        # Validate required fields
        settings.require_env("DATABASE_URL")
        settings.require_env("CELERY_BROKER_URL")
        settings.require_env("CELERY_BACKEND_URL")
        settings.require_env("GOOGLE_PHOTOS_URL")
        settings.require_env("GOOGLE_SEARCH_URL")
        settings.require_env("GOOGLE_USERINFO_URL")
        settings.require_env("FASTAPI_ENDPOINT")
        settings.require_env("GOOGLE_CLIENT_ID")
        settings.require_env("GOOGLE_CLIENT_SECRET")
        settings.require_env("GOOGLE_REDIRECT_URI")
        settings.require_env("ENCRYPTION_KEY")
        return settings

    except ValidationError as exc:
        # Pretty-print and exit non-zero so Docker / CI fails fast
        print("❌  Configuration error:\n", exc, file=sys.stderr)
        sys.exit(1)


# Singleton used by the rest of the app
settings: Settings = get_settings()
