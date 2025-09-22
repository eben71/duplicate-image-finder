from fastapi import FastAPI
from starlette.requests import Request

from backend.deps import get_http_client


def test_get_http_client_returns_app_state() -> None:
    app = FastAPI()
    sentinel = object()
    app.state.http = sentinel  # type: ignore[attr-defined]

    scope = {"type": "http", "app": app}
    request = Request(scope)

    assert get_http_client(request) is sentinel
