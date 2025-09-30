# tests/conftest.py
from __future__ import annotations

import asyncio
import base64
import inspect
import os
import re
import tempfile
from collections.abc import AsyncGenerator, Generator
from typing import Any, Final, cast

import httpx
import pytest
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient
from sqlalchemy.engine import Engine
from sqlmodel import Session, SQLModel, create_engine

_FERNET_ALLOWED: Final[re.Pattern[str]] = re.compile(r"^[A-Za-z0-9\-_]+=*$")


_DEFAULT_ENV = {
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
}

for key, value in _DEFAULT_ENV.items():
    os.environ.setdefault(key, value)


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
from tests.utils.lifespan import LifespanManager  # noqa: E402


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


@pytest.fixture
def event_loop() -> Generator[asyncio.AbstractEventLoop, None, None]:
    loop = asyncio.new_event_loop()
    try:
        yield loop
    finally:
        loop.run_until_complete(loop.shutdown_asyncgens())
        loop.close()


def pytest_fixture_setup(
    fixturedef: pytest.FixtureDef[Any],
    request: pytest.FixtureRequest,
) -> object | None:
    if fixturedef.argname == "event_loop":
        return None

    func = fixturedef.func

    try:
        is_asyncgen = inspect.isasyncgenfunction(func)
    except OSError:
        # Under Python 3.12 the inspect helpers can raise when a fixture is defined
        # from a C-implemented wrapper (e.g. when coverage wraps callables). Treat
        # it as a regular function and let pytest handle it normally.
        is_asyncgen = False

    if is_asyncgen:
        loop = cast(asyncio.AbstractEventLoop, request.getfixturevalue("event_loop"))
        argnames = fixturedef.argnames or ()

        async def init() -> Any:
            kwargs = {name: request.getfixturevalue(name) for name in argnames}
            agen = func(**kwargs)
            value = await agen.__anext__()

            def finalizer() -> None:
                try:
                    loop.run_until_complete(agen.__anext__())
                except StopAsyncIteration:
                    pass

            request.addfinalizer(finalizer)
            return value

        value = loop.run_until_complete(init())
        fixturedef.cached_result = (value, fixturedef.cache_key(cast(Any, request)), None)
        return value

    try:
        is_coro = inspect.iscoroutinefunction(func)
    except OSError:
        # Coverage/async fixtures may lack retrievable source code; assume they
        # are sync so pytest can fall back to its default handling.
        is_coro = False

    if is_coro:
        loop = cast(asyncio.AbstractEventLoop, request.getfixturevalue("event_loop"))
        argnames = fixturedef.argnames or ()

        async def call() -> Any:
            kwargs = {name: request.getfixturevalue(name) for name in argnames}
            return await func(**kwargs)

        value = loop.run_until_complete(call())
        fixturedef.cached_result = (value, fixturedef.cache_key(cast(Any, request)), None)
        return value

    return None


def pytest_pyfunc_call(pyfuncitem: pytest.Function) -> bool | None:
    func = pyfuncitem.obj
    if asyncio.iscoroutinefunction(func):
        loop_obj = pyfuncitem.funcargs.get("event_loop")
        loop = cast(asyncio.AbstractEventLoop | None, loop_obj)
        argnames = pyfuncitem._fixtureinfo.argnames
        kwargs = {
            name: pyfuncitem.funcargs[name] for name in argnames if name in pyfuncitem.funcargs
        }
        if loop is None:
            loop = asyncio.new_event_loop()
            try:
                asyncio.set_event_loop(loop)
                loop.run_until_complete(func(**kwargs))
                loop.run_until_complete(loop.shutdown_asyncgens())
            finally:
                asyncio.set_event_loop(None)
                loop.close()
        else:
            loop.run_until_complete(func(**kwargs))
        return True
    return None
