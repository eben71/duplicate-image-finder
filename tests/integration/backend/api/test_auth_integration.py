from unittest import mock

import httpx
import pytest
from httpx import AsyncClient
from sqlmodel import Session

from backend.api import routes as api_routes
from core import google_oauth

# Constants for readability and maintainability
FAKE_CODE = "fakecode"
TOKEN_RESPONSE: dict[str, str | int] = {
    "access_token": "abc123",
    "refresh_token": "refresh456",
    "expires_in": 3600,
}

USERINFO_RESPONSE: dict[str, str] = {
    "email": "testuser@example.com",
    "full_name": "Test User",
    "profile_picture": "https://example.com/pic.jpg",
}


@pytest.mark.asyncio
@pytest.mark.integration
async def test_auth_callback_creates_user(
    app_client: AsyncClient,
    session: Session,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """
    Test that the auth callback successfully creates a user with valid OAuth code.

    Args:
        mock_exchange: Mock for exchange_code_for_token
        mock_get: Mock for httpx.AsyncClient.get
        client: Test client (e.g., from FastAPI TestClient)
        mocker: Pytest fixture for additional mocking if needed
    """

    async def fake_exchange(code: str, client: AsyncClient) -> dict[str, str | int]:
        return TOKEN_RESPONSE

    async def fake_get(
        self: httpx.AsyncClient,
        url: str,
        *,
        headers: dict[str, str] | None = None,
    ) -> mock.Mock:
        response = mock.Mock(status_code=200)
        response.json = mock.Mock(return_value=USERINFO_RESPONSE)
        response.raise_for_status = mock.Mock()
        return response

    monkeypatch.setattr(api_routes, "exchange_code_for_token", fake_exchange)
    monkeypatch.setattr(google_oauth, "exchange_code_for_token", fake_exchange)
    monkeypatch.setattr(httpx.AsyncClient, "get", fake_get)
    assert api_routes.exchange_code_for_token is fake_exchange

    response = await app_client.get(f"/api/auth/callback?code={FAKE_CODE}")

    assert response.status_code == 200
    data = response.json()
    assert data["email"] == USERINFO_RESPONSE["email"]
    assert data["full_name"] == USERINFO_RESPONSE["full_name"]
    assert data["profile_picture"] == USERINFO_RESPONSE["profile_picture"]

    session.expire_all()


@pytest.mark.asyncio
@pytest.mark.integration
async def test_auth_callback_handles_invalid_code(
    app_client: AsyncClient, monkeypatch: pytest.MonkeyPatch
) -> None:
    async def fake_exchange(*_: object, **__: object) -> dict[str, str | int]:
        raise ValueError("Invalid code")

    monkeypatch.setattr(api_routes, "exchange_code_for_token", fake_exchange)
    monkeypatch.setattr(google_oauth, "exchange_code_for_token", fake_exchange)

    response = await app_client.get(f"/api/auth/callback?code={FAKE_CODE}")

    assert response.status_code == 400
    assert response.json() == {"detail": "Invalid code"}
