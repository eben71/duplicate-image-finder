import pytest
from pydantic import ValidationError
from datetime import datetime, timedelta, timezone
from backend.models.user import IngestionMode
from core.google_oauth import is_token_expired
from tests.utils.factories import make_test_user


@pytest.mark.unit
def test_create_user():
    user = make_test_user(
        email="test@example.com", full_name="Test", ingestion_mode=IngestionMode.SCRAPE
    )
    assert user.email == "test@example.com"
    assert user.full_name == "Test"
    assert user.ingestion_mode == IngestionMode.SCRAPE


@pytest.mark.unit
def test_create_user_from_google_login():
    user = make_test_user(
        email="test@example.com",
        full_name="Test",
        profile_picture="https://example.com/pic.jpg",
    )

    user.set_google_tokens("abc123", "refresh123", expires_in=3600)

    assert user.get_google_access_token() == "abc123"
    assert user.get_google_refresh_token() == "refresh123"
    assert user.token_expiry > datetime.now(timezone.utc)
    assert user.requires_reauth is False


def test_create_user_with_default_ingestion():
    user = make_test_user(email="test@example.com")
    assert user.email == "test@example.com"
    assert user.full_name == "Test User"
    assert user.ingestion_mode == IngestionMode.API


def test_invalid_email_rejected():
    with pytest.raises(ValidationError):
        make_test_user(email="invalid-email")


def test_token_encryption_decryption():
    user = make_test_user()
    access_token = "mock_access"
    refresh_token = "mock_refresh"

    user.set_google_tokens(access_token, refresh_token)

    assert user.get_google_access_token() == access_token
    assert user.get_google_refresh_token() == refresh_token


def test_created_at_is_utc_by_default():
    user = make_test_user()
    assert user.created_at.tzinfo is not None
    assert user.created_at.tzinfo.utcoffset(user.created_at) == timedelta(0)


def test_token_expiry_is_set_to_utc():
    user = make_test_user()
    user.set_google_tokens("abc", "xyz", expires_in=3600)
    assert user.token_expiry is not None
    assert user.token_expiry.tzinfo == timezone.utc


def test_token_expired_logic():
    user = make_test_user(with_tokens=True)

    # simulate expiry in the past
    user.token_expiry = datetime.now(timezone.utc) - timedelta(minutes=5)
    assert is_token_expired(user) is True

    # simulate valid token in the future
    user.token_expiry = datetime.now(timezone.utc) + timedelta(hours=1)
    assert is_token_expired(user) is False

    # no expiry set
    user.token_expiry = None
    assert is_token_expired(user) is True


def test_reject_non_utc_datetime():
    # Build a naive datetime (no tzinfo)
    non_utc = datetime.now()
    with pytest.raises(ValidationError):
        make_test_user(
            email="updated@example.com", full_name="Updated User", updated_at=non_utc
        )


def test_updated_at_must_be_utc():
    utc_now = datetime.now(timezone.utc)
    user = make_test_user(
        email="updated@example.com",
        full_name="Updated User",
        updated_at=utc_now,
    )
    assert user.updated_at == utc_now
    assert user.updated_at.tzinfo == timezone.utc


def test_deleted_at_must_be_utc():
    utc_now = datetime.now(timezone.utc)
    user = make_test_user(
        email="deleted@example.com",
        full_name="Deleted User",
        deleted_at=utc_now,
    )
    assert user.deleted_at == utc_now
    assert user.deleted_at.tzinfo == timezone.utc


def test_reject_non_utc_updated_at():
    naive_time = datetime.now()
    with pytest.raises(ValidationError):
        make_test_user(
            email="bad@example.com",
            full_name="Bad User",
            updated_at=naive_time,
        )
