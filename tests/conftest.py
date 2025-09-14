# tests/conftest.py
from __future__ import annotations

import base64
import os
import tempfile
from collections.abc import AsyncGenerator, Generator

import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy.engine import Engine
from sqlmodel import Session, SQLModel, create_engine


# --- Make sure a valid Fernet key exists for tests (no real secrets needed) ---
def _ensure_encryption_key() -> None:
    key = os.environ.get("ENCRYPTION_KEY")

    if key:
        try:
            from cryptography.fernet import Fernet

            Fernet(key.encode())
            return
        except ImportError:
            # Without cryptography, do a light heuristic check (length 44)
            if len(key) == 44:
                return
            # else fall through to regenerate a valid-looking key
        except ValueError:
            pass

    try:
        from cryptography.fernet import Fernet
    except ImportError:
        os.environ["ENCRYPTION_KEY"] = base64.urlsafe_b64encode(os.urandom(32)).decode()
    else:
        os.environ["ENCRYPTION_KEY"] = Fernet.generate_key().decode()


_ensure_encryption_key()

# --- Import the app and models AFTER the key is set ---
# Import models so SQLModel.metadata is populated
from backend.db.session import get_session  # noqa: E402
from backend.main import app  # noqa: E402
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
    """Session-scoped engine bound to a temp sqlite file."""
    url = f"sqlite:///{_sqlite_file}"
    engine = create_engine(url, connect_args={"check_same_thread": False})
    return engine


@pytest.fixture
def session(engine: Engine) -> Generator[Session, None, None]:
    """Fresh schema per test; clean and fast."""
    SQLModel.metadata.create_all(engine)
    try:
        with Session(engine) as s:
            yield s
    finally:
        SQLModel.metadata.drop_all(engine)


@pytest.fixture(name="client")
async def async_client_fixture(session: Session) -> AsyncGenerator[AsyncClient, None]:
    """
    Async HTTP client bound to the FastAPI app, with the DB dependency
    overridden to use the per-test SQLModel Session.
    """

    def override_get_session() -> Session:
        return session

    app.dependency_overrides[get_session] = override_get_session
    try:
        async with AsyncClient(
            transport=ASGITransport(app=app),
            base_url="http://test",
        ) as client:
            yield client
    finally:
        app.dependency_overrides.clear()


def test_fallback_key_format() -> None:
    k = base64.urlsafe_b64encode(os.urandom(32)).decode()
    assert len(k) == 44  # Fernet base64 length
    assert all(c.isalnum() or c in "-_" for c in k.rstrip("="))  # urlsafe


def test_ensure_sets_key(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("ENCRYPTION_KEY", raising=False)
    _ensure_encryption_key()
    assert "ENCRYPTION_KEY" in os.environ
