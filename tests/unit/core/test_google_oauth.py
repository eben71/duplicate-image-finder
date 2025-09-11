from unittest.mock import AsyncMock, Mock, patch

import pytest
from httpx import Request, Response
from sqlmodel import Session

import core.google_oauth as oauth
from tests.utils.factories import make_test_user


@pytest.mark.asyncio
async def test_refresh_token_success(monkeypatch: pytest.MonkeyPatch) -> None:
    user = make_test_user()
    user.set_google_tokens("expired_token", "valid_refresh_token", expires_in=-10)

    session = AsyncMock(spec=Session)

    # Mock httpx.Response
    mock_response = Mock(spec=Response)
    mock_response.status_code = 200
    mock_response.raise_for_status = Mock()  # <-- sync, not async
    mock_response.json = Mock(
        return_value={"access_token": "tok", "expires_in": 3600, "refresh_token": "r1"}
    )

    # Mock httpx.AsyncClient
    mock_client = AsyncMock()
    mock_client.post = AsyncMock(return_value=mock_response)

    # Patch the module-level client
    monkeypatch.setattr(oauth, "async_client", mock_client, raising=True)

    await oauth.refresh_access_token(user, session)

    assert user.get_google_access_token() == "tok"
    assert user.get_google_refresh_token() == "r1"
    assert user.token_expiry is not None
    mock_response.raise_for_status.assert_called_once()


@pytest.mark.asyncio
async def test_refresh_token_missing() -> None:
    user = make_test_user()
    user.encrypted_refresh_token = None  # Simulate no refresh token
    session = AsyncMock(spec=Session)

    with pytest.raises(Exception) as exc:
        await oauth.refresh_access_token(user, session)

    assert "re-authenticate" in str(exc.value)
    assert user.requires_reauth is True


@pytest.mark.asyncio
async def test_refresh_token_rejected_by_google() -> None:
    user = make_test_user()
    user.set_google_tokens("expired", "revoked", expires_in=-10)

    session = AsyncMock(spec=Session)

    # Simulate HTTP 400 error from Google
    error_content = b'{"error": "invalid_grant", "error_description": "Bad token"}'
    response = Response(
        status_code=400,
        content=error_content,
        request=Request("POST", "https://oauth2.googleapis.com/token"),
    )

    with patch("core.google_oauth.httpx.AsyncClient.post", return_value=response):
        with pytest.raises(Exception) as exc:
            await oauth.refresh_access_token(user, session)

    assert "re-authenticate" in str(exc.value)
    assert user.requires_reauth is True


@pytest.mark.asyncio
async def test_get_fresh_access_token_triggers_refresh() -> None:
    user = make_test_user()
    user.set_google_tokens("expired", "refresh123", expires_in=-10)

    session = AsyncMock(spec=Session)

    with patch("core.google_oauth.refresh_access_token", new=AsyncMock()):
        token = await oauth.get_fresh_access_token(user, session)

    assert isinstance(token, str)
