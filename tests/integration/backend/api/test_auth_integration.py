from unittest.mock import AsyncMock, patch
import pytest

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
@patch("backend.api.routes.exchange_code_for_token", new_callable=AsyncMock)
@patch("httpx.AsyncClient")
@patch("httpx.AsyncClient.post", new_callable=AsyncMock)
async def test_auth_callback_creates_user(
    mock_post, mock_userinfo, mock_exchange, client
):
    """
    Test that the auth callback successfully creates a user with valid OAuth code.

    Args:
        mock_userinfo: Mock for httpx.AsyncClient.get
        mock_exchange: Mock for exchange_code_for_token
        mock_post: Mock for httpx.AsyncClient.post
        client: Test client (e.g., from FastAPI TestClient)
        mocker: Pytest fixture for additional mocking if needed
    """
    # Configure mocks
    mock_exchange.return_value = TOKEN_RESPONSE

    mock_post.return_value = AsyncMock(
        status_code=200,
        json=lambda: TOKEN_RESPONSE,
    )

    mock_client = AsyncMock()
    mock_response = AsyncMock()
    mock_response.status_code = 200
    mock_response.raise_for_status = lambda: None
    mock_response.json = AsyncMock(return_value=USERINFO_RESPONSE)

    mock_client.__aenter__.return_value.get.return_value = mock_response
    mock_userinfo.return_value = mock_client

    # Perform the request
    response = client.get(f"/api/auth/callback?code={FAKE_CODE}")

    # Assertions
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == USERINFO_RESPONSE["email"]
    assert data["full_name"] == USERINFO_RESPONSE["full_name"]
    assert data["profile_picture"] == USERINFO_RESPONSE["profile_picture"]

    # Verify mocks were called
    mock_exchange.assert_called_once_with(FAKE_CODE)
    mock_post.assert_called_once()
    mock_userinfo.assert_called_once()


@pytest.mark.asyncio
@patch("backend.api.routes.exchange_code_for_token", new_callable=AsyncMock)
@patch("httpx.AsyncClient.get", new_callable=AsyncMock)
async def test_auth_callback_handles_invalid_code(mock_get, mock_exchange, client):
    """Test that the auth callback handles an invalid OAuth code."""
    mock_exchange.side_effect = ValueError("Invalid code")

    response = client.get(f"/api/auth/callback?code={FAKE_CODE}")

    assert response.status_code == 400
    assert response.json()["detail"] == "Invalid code"
