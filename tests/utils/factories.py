import random
from datetime import datetime

from backend.models.user import IngestionMode, User


def make_test_user(
    id: int | None = None,
    email: str = "user@example.com",
    full_name: str = "Test User",
    profile_picture: str | None = None,
    ingestion_mode: IngestionMode = IngestionMode.API,
    with_tokens: bool = False,
    expires_in: int = 3600,
    updated_at: datetime | None = None,
    deleted_at: datetime | None = None,
) -> User:
    user = User(
        id=id or random.randint(1000, 9999),
        email=email,
        full_name=full_name,
        profile_picture=profile_picture,
        ingestion_mode=ingestion_mode,
        updated_at=updated_at,
        deleted_at=deleted_at,
    )
    if with_tokens:
        user.set_google_tokens("mock_access_token", "mock_refresh_token", expires_in)
    return user
