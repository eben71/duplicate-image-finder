from unittest import mock
from unittest.mock import AsyncMock, patch

import pytest
from httpx import AsyncClient

# Constants for readability and maintainability
FAKE_CODE = "fakecode"
TOKEN_RESPONSE = {
    "access_token": "abc123",
    "refresh_token": "refresh456",
    "expires_in": 3600,
}

USERINFO_RESPONSE = {
    "email": "testuser@example.com",
    "full_name": "Test User",
    "profile_picture": "https://example.com/pic.jpg",
}


@pytest.mark.asyncio
@pytest.mark.integration
@patch("backend.api.routes.exchange_code_for_token", new_callable=AsyncMock)
@patch("httpx.AsyncClient.get", new_callable=AsyncMock)
async def test_auth_callback_creates_user(
    mock_get: AsyncMock,
    mock_exchange: AsyncMock,
    app_client: AsyncClient,
) -> None:
    """
    Test that the auth callback successfully creates a user with valid OAuth code.

    Args:
        mock_exchange: Mock for exchange_code_for_token
        mock_get: Mock for httpx.AsyncClient.get
        client: Test client (e.g., from FastAPI TestClient)
        mocker: Pytest fixture for additional mocking if needed
    """
    # Configure mocks
    mock_exchange.return_value = TOKEN_RESPONSE

    mock_response = AsyncMock(status_code=200)
    mock_response.json = mock.Mock(return_value=USERINFO_RESPONSE)
    mock_response.raise_for_status = mock.Mock()
    mock_get.return_value = mock_response

    # Perform the request
    response = await app_client.get(f"/api/auth/callback?code={FAKE_CODE}")

    # Assertions
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == USERINFO_RESPONSE["email"]
    assert data["full_name"] == USERINFO_RESPONSE["full_name"]
    assert data["profile_picture"] == USERINFO_RESPONSE["profile_picture"]

    # Verify mocks were called
    mock_exchange.assert_called_once_with(FAKE_CODE, mock.ANY)
    mock_get.assert_called_once()


@pytest.mark.asyncio
@pytest.mark.integration
@patch("backend.api.routes.exchange_code_for_token", new_callable=AsyncMock)
async def test_auth_callback_handles_invalid_code(
    mock_exchange: AsyncMock, client: AsyncClient
) -> None:
    mock_exchange.side_effect = ValueError("Invalid code")

    response = await client.get(f"/api/auth/callback?code={FAKE_CODE}")

    assert response.status_code == 400
    assert response.json() == {"detail": "Invalid code"}
