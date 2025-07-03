from backend.models.user import User, IngestionMode


def test_create_user():
    user = User(email="test@example.com", full_name="Test", mode=IngestionMode.SCRAPE)
    assert user.email == "test@example.com"
    assert user.mode == IngestionMode.SCRAPE


def test_create_user_with_default_ingestion():
    user = User(email="test@example.com", full_name="Test")
    assert user.email == "test@example.com"
    assert user.mode == IngestionMode.API


def test_token_encryption_decryption():
    user = User(email="test@example.com")
    access_token = "mock_access"
    refresh_token = "mock_refresh"

    user.set_google_tokens(access_token, refresh_token)

    assert user.get_google_access_token() == access_token
    assert user.get_google_refresh_token() == refresh_token
