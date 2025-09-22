from unittest import mock
import pytest
import httpx
from httpx import AsyncClient
from sqlmodel import Session

from backend.api import routes as api_routes
from backend.config.settings import settings
from core import google_oauth
from tests.utils.factories import make_test_user


@pytest.mark.asyncio
async def test_google_login_redirects(app_client: AsyncClient) -> None:
    response = await app_client.get("/api/auth/login")

    assert response.status_code in {302, 307}
    assert "https://accounts.google.com" in response.headers["location"]


@pytest.mark.asyncio
async def test_google_callback_missing_code(app_client: AsyncClient) -> None:
    response = await app_client.get("/api/auth/callback")

    assert response.status_code == 400
    assert response.json() == {"detail": "Missing code parameter"}


@pytest.mark.asyncio
async def test_google_callback_error_param(app_client: AsyncClient) -> None:
    response = await app_client.get("/api/auth/callback?error=access_denied")

    assert response.status_code == 400
    assert response.json() == {"detail": "OAuth error: access_denied"}


@pytest.mark.asyncio
async def test_google_callback_updates_existing_user(
    app_client: AsyncClient,
    session: Session,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    user = make_test_user(with_tokens=True)
    user.requires_reauth = True
    session.add(user)
    session.commit()
    session.refresh(user)

    token_payload = {
        "access_token": "new-access",
        "refresh_token": "new-refresh",
        "expires_in": 1200,
    }
    profile_payload = {
        "email": user.email,
        "full_name": "Updated User",
        "profile_picture": "https://example.com/avatar.jpg",
    }

    async def fake_exchange(code: str, client: AsyncClient) -> dict:
        return token_payload

    async def fake_get(self, url: str, *, headers: dict | None = None) -> mock.Mock:
        response = mock.Mock(status_code=200)
        response.json = mock.Mock(return_value=profile_payload)
        response.raise_for_status = mock.Mock()
        return response

    monkeypatch.setattr(api_routes, "exchange_code_for_token", fake_exchange)
    monkeypatch.setattr(google_oauth, "exchange_code_for_token", fake_exchange)
    monkeypatch.setattr(httpx.AsyncClient, "get", fake_get)
    assert api_routes.exchange_code_for_token is fake_exchange

    response = await app_client.get("/api/auth/callback?code=valid-code")

    assert response.status_code == 200
    data = response.json()
    assert data["email"] == user.email
    assert data["full_name"] == "Updated User"
    assert data["profile_picture"] == "https://example.com/avatar.jpg"
