from unittest.mock import AsyncMock, patch

import httpx
import pytest
import respx
from httpx import Request, Response
from sqlalchemy.orm import Session

import core.google_oauth as oauth

# Adjust these imports to your project:
# - make_test_user: wherever your test user factory lives
# - oauth module path: you used "core.google_oauth" in your patch path, so import that
from tests.utils.factories import make_test_user  # or wherever this is


@pytest.mark.asyncio
async def test_refresh_token_success(
    http_mock: respx.Router, http_client: httpx.AsyncClient
) -> None:
    user = make_test_user()
    user.set_google_tokens("expired_token", "valid_refresh_token", expires_in=-10)

    session = AsyncMock(spec=Session)

    # RESPX intercepts the POST and returns a real httpx.Response
    route = http_mock.post("https://oauth2.googleapis.com/token").mock(
        return_value=Response(
            200,
            json={"access_token": "tok", "expires_in": 3600, "refresh_token": "r1"},
        )
    )

    # Call without passing a client; any httpx client (module-level or new) is intercepted by respx
    await oauth.refresh_access_token(user, session, http_client)

    assert user.get_google_access_token() == "tok"
    assert user.get_google_refresh_token() == "r1"
    assert user.token_expiry is not None

    # Optional: assert our route was actually hit
    assert route.called


@pytest.mark.asyncio
async def test_refresh_token_missing(http_client: httpx.AsyncClient) -> None:
    user = make_test_user()
    user.encrypted_refresh_token = None  # Simulate no refresh token
    session = AsyncMock(spec=Session)

    with pytest.raises(Exception) as exc:
        await oauth.refresh_access_token(user, session, http_client)

    assert "re-authenticate" in str(exc.value).lower()
    assert user.requires_reauth is True


@pytest.mark.asyncio
async def test_refresh_token_rejected_by_google(
    http_mock: respx.Router, http_client: httpx.AsyncClient
) -> None:
    user = make_test_user()
    user.set_google_tokens("expired", "revoked", expires_in=-10)
    session = AsyncMock(spec=Session)

    # Simulate HTTP 400 from Google
    route = http_mock.post("https://oauth2.googleapis.com/token").mock(
        return_value=Response(
            status_code=400,
            content=b'{"error":"invalid_grant","error_description":"Bad token"}',
            request=Request("POST", "https://oauth2.googleapis.com/token"),
        )
    )

    with pytest.raises(Exception) as exc:
        await oauth.refresh_access_token(user, session, http_client)

    assert "re-authenticate" in str(exc.value).lower()
    assert user.requires_reauth is True
    assert route.called


@pytest.mark.asyncio
async def test_get_fresh_access_token_triggers_refresh(http_client: httpx.AsyncClient) -> None:
    user = make_test_user()
    user.set_google_tokens("expired", "refresh123", expires_in=-10)

    session = AsyncMock(spec=Session)

    # Patch the refresh call so we only test that it is invoked from get_fresh_access_token
    with patch("core.google_oauth.refresh_access_token", new=AsyncMock()) as mocked_refresh:
        token = await oauth.get_fresh_access_token(user, session, http_client)

    # Should return a string (either the refreshed token or existing one post-refresh)
    assert isinstance(token, str)
    mocked_refresh.assert_awaited_once_with(user, session, http_client)
