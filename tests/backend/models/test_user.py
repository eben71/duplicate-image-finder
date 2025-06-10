from backend.models.user import User, IngestionMode


def test_create_user():
    user = User(email="test@example.com", full_name="Test", mode=IngestionMode.SCRAPE)
    assert user.email == "test@example.com"
    assert user.mode == IngestionMode.SCRAPE
