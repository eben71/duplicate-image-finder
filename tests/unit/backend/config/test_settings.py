from typing import Any

import pytest

from backend.config import settings as settings_module
from backend.config.settings import Settings


def _settings_kwargs(**overrides: Any) -> dict[str, Any]:
    base = {
        "DATABASE_URL": "sqlite:///test.db",
        "CELERY_BROKER_URL": "redis://localhost:6379/0",
        "CELERY_BACKEND_URL": "redis://localhost:6379/1",
        "GOOGLE_PHOTOS_URL": "https://photos.example.com",
        "GOOGLE_SEARCH_URL": "https://photos.example.com/search",
        "GOOGLE_USERINFO_URL": "https://photos.example.com/userinfo",
        "FASTAPI_ENDPOINT": "http://localhost:8000",
        "GOOGLE_CLIENT_ID": "client-id",
        "GOOGLE_CLIENT_SECRET": "client-secret",  # pragma: allowlist secret
        "GOOGLE_REDIRECT_URI": "http://localhost:8000/callback",
        "ENCRYPTION_KEY": "a" * 44,
    }
    base.update(overrides)
    return base


def test_require_env_success() -> None:
    settings = Settings(**_settings_kwargs())

    assert settings.require_env("database_url") == "sqlite:///test.db"


def test_require_env_raises_for_blank() -> None:
    settings = Settings(**_settings_kwargs(GOOGLE_CLIENT_ID=""))

    with pytest.raises(ValueError):
        settings.require_env("google_client_id")


def test_get_settings_exits_on_validation_error(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("DATABASE_URL", raising=False)
    exit_called: dict[str, Any] = {}

    def fake_exit(code: int) -> None:
        exit_called["code"] = code
        raise SystemExit(code)

    monkeypatch.setattr(settings_module.sys, "exit", fake_exit)

    with pytest.raises(SystemExit):
        settings_module.get_settings()

    assert exit_called["code"] == 1
