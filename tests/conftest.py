# tests/conftest.py
from __future__ import annotations

import os
import tempfile
from collections.abc import AsyncGenerator, Generator

import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy.engine import Engine
from sqlmodel import Session, SQLModel, create_engine


# --- Make sure a valid Fernet key exists for tests (no real secrets needed) ---
def _ensure_encryption_key() -> None:
    if os.environ.get("ENCRYPTION_KEY"):
        return
    try:
        from cryptography.fernet import Fernet

        os.environ["ENCRYPTION_KEY"] = Fernet.generate_key().decode()
    except Exception:
        # Fallback without cryptography (rare)
        import base64
        import os as _os

        os.environ["ENCRYPTION_KEY"] = base64.urlsafe_b64encode(_os.urandom(32)).decode()


_ensure_encryption_key()

# --- Import the app and models AFTER the key is set ---
# Import models so SQLModel.metadata is populated
import backend.models.embedding  # noqa: E402,F401
import backend.models.image  # noqa: E402,F401
import backend.models.user  # noqa: E402,F401
from backend.db.session import get_session  # noqa: E402
from backend.main import app  # noqa: E402


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
async def client_fixture(session: Session) -> AsyncGenerator[AsyncClient, None]:
    """HTTP client with app dependency overridden to use the test session."""

    def override_get_session() -> Session:
        return session

    app.dependency_overrides[get_session] = override_get_session
    try:
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
            yield client
    finally:
        app.dependency_overrides.clear()
