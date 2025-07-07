import pytest
import httpx
from sqlmodel import Session
from datetime import datetime, timezone
from unittest.mock import AsyncMock, patch
from tests.common.test_user_factory import make_test_user
from core.google_oauth import (
    refresh_access_token,
    get_fresh_access_token,
)


@pytest.mark.asyncio
async def test_refresh_token_success():
    user = make_test_user()
    user.set_google_tokens("expired_token", "valid_refresh_token", expires_in=-10)

    session = AsyncMock(spec=Session)
    mock_response = {
        "access_token": "new_access_token",
        "expires_in": 3600,
    }

    with patch(
        "core.google_oauth.httpx.AsyncClient.post",
        return_value=AsyncMock(
            status_code=200, json=AsyncMock(return_value=mock_response)
        ),
    ):
        await refresh_access_token(user, session)

    assert not user.requires_reauth
    assert user.get_google_access_token() == "new_access_token"
    assert user.token_expiry > datetime.now(timezone.utc)


@pytest.mark.asyncio
async def test_refresh_token_missing():
    user = make_test_user()
    user.encrypted_refresh_token = None  # Simulate no refresh token
    session = AsyncMock(spec=Session)

    with pytest.raises(Exception) as exc:
        await refresh_access_token(user, session)

    assert "re-authenticate" in str(exc.value)
    assert user.requires_reauth is True


@pytest.mark.asyncio
async def test_refresh_token_rejected_by_google():
    user = make_test_user()
    user.set_google_tokens("expired", "revoked", expires_in=-10)

    session = AsyncMock(spec=Session)

    # Simulate HTTP 400 error from Google
    error_content = b'{"error": "invalid_grant", "error_description": "Bad token"}'
    response = httpx.Response(
        status_code=400,
        content=error_content,
        request=httpx.Request("POST", "https://oauth2.googleapis.com/token"),
    )

    with patch("core.google_oauth.httpx.AsyncClient.post", return_value=response):
        with pytest.raises(Exception) as exc:
            await refresh_access_token(user, session)

    assert "re-authenticate" in str(exc.value)
    assert user.requires_reauth is True


@pytest.mark.asyncio
async def test_get_fresh_access_token_triggers_refresh():
    user = make_test_user()
    user.set_google_tokens("expired", "refresh123", expires_in=-10)

    session = AsyncMock(spec=Session)

    with patch("core.google_oauth.refresh_access_token", new=AsyncMock()):
        token = await get_fresh_access_token(user, session)

    assert isinstance(token, str)
