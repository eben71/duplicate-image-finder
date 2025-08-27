from datetime import UTC, datetime, timedelta
from typing import Any

from pydantic import EmailStr, field_validator
from sqlalchemy import Column, DateTime
from sqlalchemy import Enum as SAEnum
from sqlmodel import Field, SQLModel

from backend.models.enums import IngestionMode
from core.crypto import decrypt, encrypt


class User(SQLModel, table=True):  # type: ignore
    model_config = {
        "validate_default": True,
        "validate_assignment": True,
    }
    id: int | None = Field(default=None, primary_key=True)
    email: EmailStr = Field(index=True, nullable=False, unique=True, max_length=255)
    full_name: str = Field(max_length=100)
    ingestion_mode: IngestionMode = Field(
        default=IngestionMode.API,
        sa_column=Column(SAEnum(IngestionMode, name="ingestionmode")),
    )
    profile_picture: str | None = Field(default=None, max_length=2048)
    requires_reauth: bool = Field(default=False)

    encrypted_access_token: str | None = Field(default=None, alias="google_access_token")

    encrypted_refresh_token: str | None = Field(default=None, alias="google_refresh_token")

    token_expiry: datetime | None = Field(
        default=None,
        sa_column=Column(DateTime(timezone=True)),  # Enforce UTC in DB
    )

    created_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
        sa_column=Column(DateTime(timezone=True), nullable=False),
    )

    updated_at: datetime | None = Field(default=None, sa_column=Column(DateTime(timezone=True)))

    deleted_at: datetime | None = Field(default=None, sa_column=Column(DateTime(timezone=True)))

    @field_validator("token_expiry", "created_at", "updated_at", "deleted_at", mode="before")
    def ensure_utc(cls, v: datetime | None) -> datetime | None:
        if v is not None and v.tzinfo != UTC:
            raise ValueError("Datetime must be in UTC")
        return v

    def set_google_tokens(
        self,
        access_token: str,
        refresh_token: str | None,
        expires_in: int | None = None,
    ) -> None:
        self.encrypted_access_token = encrypt(access_token)
        if refresh_token:
            self.encrypted_refresh_token = encrypt(refresh_token)
        if expires_in:
            self.token_expiry = datetime.now(UTC) + timedelta(seconds=expires_in)

    def get_google_access_token(self) -> str | None:
        return decrypt(self.encrypted_access_token) if self.encrypted_access_token else None

    def get_google_refresh_token(self) -> str | None:
        return decrypt(self.encrypted_refresh_token) if self.encrypted_refresh_token else None

    def dict(self, *args: Any, **kwargs: Any) -> dict[str, Any]:
        kwargs.setdefault("exclude", {"_encrypted_access_token", "_encrypted_refresh_token"})
        return super().dict(*args, **kwargs)
