# tests/conftest.py
from __future__ import annotations

import base64
import os
import re
import tempfile
from collections.abc import AsyncGenerator, Generator, Iterator
from typing import Final

import httpx
import pytest
import respx
from asgi_lifespan import LifespanManager
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient
from sqlalchemy.engine import Engine
from sqlmodel import Session, SQLModel, create_engine

_FERNET_ALLOWED: Final[re.Pattern[str]] = re.compile(r"^[A-Za-z0-9\-_]+=*$")


def _is_fernet_like(key: str) -> bool:
    if not key or not _FERNET_ALLOWED.match(key):
        return False
    try:
        raw = base64.urlsafe_b64decode(key.encode())
    except Exception:
        return False
    return len(raw) == 32


def _generate_fernet_key_fallback() -> str:
    return base64.urlsafe_b64encode(os.urandom(32)).decode()


# --- Make sure a valid Fernet key exists for tests (no real secrets needed) ---
def _ensure_encryption_key() -> None:
    key = os.environ.get("ENCRYPTION_KEY")

    if key:
        try:
            from cryptography.fernet import Fernet  # type: ignore
        except ImportError:
            if _is_fernet_like(key):
                return
        else:
            try:
                Fernet(key.encode())
            except Exception:
                key = None
            else:
                return

    try:
        from cryptography.fernet import Fernet  # type: ignore

        os.environ["ENCRYPTION_KEY"] = Fernet.generate_key().decode()
    except ImportError:
        os.environ["ENCRYPTION_KEY"] = _generate_fernet_key_fallback()

    if not _is_fernet_like(os.environ["ENCRYPTION_KEY"]):
        raise RuntimeError("Failed to generate Fernet-compatible key fallback.")


_ensure_encryption_key()

# --- Import the app and models AFTER the key is set ---
# Import models so SQLModel.metadata is populated
from backend.db.session import get_session  # noqa: E402
from backend.main import create_app  # noqa: E402
from backend.models import embedding, image, user  # noqa: E402,F401


@pytest.fixture(scope="session")
def _sqlite_file() -> Generator[str, None, None]:
    """Temporary sqlite file path for this test session."""
    fd, path = tempfile.mkstemp(prefix="test-db-", suffix=".sqlite3")
    os.close(fd)
    try:
        yield path
    finally:
        try:
            os.remove(path)
        except FileNotFoundError:
            pass


@pytest.fixture(scope="session")
def engine(_sqlite_file: str) -> Engine:
    return create_engine(f"sqlite:///{_sqlite_file}", connect_args={"check_same_thread": False})


@pytest.fixture
def session(engine: Engine) -> Generator[Session, None, None]:
    """Fresh schema per test; clean and fast."""
    SQLModel.metadata.create_all(engine)
    try:
        with Session(engine) as s:
            yield s
    finally:
        SQLModel.metadata.drop_all(engine)


@pytest.fixture
def token_json() -> dict:
    return {"access_token": "tok", "expires_in": 3600, "refresh_token": "r1"}


@pytest.fixture
def http_mock() -> Iterator[respx.Router]:
    # respx.mock is a synchronous context manager
    with respx.mock(assert_all_called=False) as router:
        yield router


@pytest.fixture(scope="session")
def app() -> FastAPI:
    return create_app()


@pytest.fixture
async def http_client() -> AsyncGenerator[httpx.AsyncClient, None]:
    async with httpx.AsyncClient(timeout=10.0) as client:
        yield client


@pytest.fixture(name="app_client")
async def app_client(app: FastAPI, session: Session) -> AsyncGenerator[AsyncClient, None]:
    """
    Async HTTP client bound to the FastAPI app, with the DB dependency
    overridden to use the per-test SQLModel Session.
    """

    def override_get_session() -> Session:
        return session

    app.dependency_overrides[get_session] = override_get_session
    try:
        async with LifespanManager(app):
            transport = ASGITransport(app=app)
            async with AsyncClient(transport=transport, base_url="http://test") as client:
                yield client
    finally:
        app.dependency_overrides.clear()
