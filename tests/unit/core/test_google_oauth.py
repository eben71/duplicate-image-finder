from unittest.mock import AsyncMock, patch

import httpx
import pytest
from httpx import Request, Response
from sqlalchemy.orm import Session

import core.google_oauth as oauth

from tests.utils.factories import make_test_user


@pytest.mark.asyncio
@patch("httpx.AsyncClient.post", new_callable=AsyncMock)
async def test_refresh_token_success(
    mock_post: AsyncMock, http_client: httpx.AsyncClient
) -> None:
    user = make_test_user()
    user.set_google_tokens("expired_token", "valid_refresh_token", expires_in=-10)

    session = AsyncMock(spec=Session)

    mock_post.return_value = Response(
        200,
        json={"access_token": "tok", "expires_in": 3600, "refresh_token": "r1"},
        request=Request("POST", oauth.GOOGLE_TOKEN_URL),
    )

    await oauth.refresh_access_token(user, session, http_client)

    assert user.get_google_access_token() == "tok"
    assert user.get_google_refresh_token() == "r1"
    assert user.token_expiry is not None

    mock_post.assert_awaited_once_with(
        oauth.GOOGLE_TOKEN_URL,
        data={
            "client_id": oauth.settings.GOOGLE_CLIENT_ID,
            "client_secret": oauth.settings.GOOGLE_CLIENT_SECRET,
            "refresh_token": "valid_refresh_token",
            "grant_type": "refresh_token",
        },
    )


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
@patch("httpx.AsyncClient.post", new_callable=AsyncMock)
async def test_refresh_token_rejected_by_google(
    mock_post: AsyncMock, http_client: httpx.AsyncClient
) -> None:
    user = make_test_user()
    user.set_google_tokens("expired", "revoked", expires_in=-10)
    session = AsyncMock(spec=Session)

    mock_post.return_value = Response(
        status_code=400,
        content=b'{"error":"invalid_grant","error_description":"Bad token"}',
        request=Request("POST", oauth.GOOGLE_TOKEN_URL),
    )

    with pytest.raises(Exception) as exc:
        await oauth.refresh_access_token(user, session, http_client)

    assert "re-authenticate" in str(exc.value).lower()
    assert user.requires_reauth is True
    mock_post.assert_awaited_once()


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
