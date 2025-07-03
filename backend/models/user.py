from sqlmodel import SQLModel, Field
from sqlalchemy import Column, Enum as SAEnum, DateTime
from datetime import datetime, timezone
from backend.models.enums import IngestionMode
from typing import Optional
from pydantic import EmailStr, validator
from core.crypto import encrypt, decrypt


class User(SQLModel, table=True):  # type: ignore
    id: int = Field(default=None, primary_key=True)
    email: EmailStr = Field(index=True, nullable=False, unique=True, max_length=255)
    name: str = Field(max_length=100, regex=r"^[a-zA-Z\s]+$")
    ingestion_mode: IngestionMode = Field(
        default=IngestionMode.API,
        sa_column=Column(SAEnum(IngestionMode, name="ingestionmode")),
    )

    _encrypted_access_token: Optional[str] = Field(
        default=None, alias="google_access_token"
    )
    _encrypted_refresh_token: Optional[str] = Field(
        default=None, alias="google_refresh_token"
    )

    token_expiry: Optional[datetime] = Field(
        default=None,
        sa_column=Column(DateTime(timezone=True)),  # Enforce UTC in DB
    )
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column=Column(DateTime(timezone=True), nullable=False),
    )
    updated_at: Optional[datetime] = Field(
        default=None, sa_column=Column(DateTime(timezone=True))
    )
    deleted_at: Optional[datetime] = Field(
        default=None, sa_column=Column(DateTime(timezone=True))
    )

    @validator("token_expiry", "created_at", "updated_at", "deleted_at")
    def ensure_utc(cls, v):
        if v is not None and v.tzinfo != timezone.utc:
            raise ValueError("Datetime must be in UTC")
        return v

    def set_google_tokens(self, access_token: str, refresh_token: Optional[str]):
        self._encrypted_access_token = encrypt(access_token)
        if refresh_token:
            self._encrypted_refresh_token = encrypt(refresh_token)

    def get_google_access_token(self) -> Optional[str]:
        return (
            decrypt(self._encrypted_access_token)
            if self._encrypted_access_token
            else None
        )

    def get_google_refresh_token(self) -> Optional[str]:
        return (
            decrypt(self._encrypted_refresh_token)
            if self._encrypted_refresh_token
            else None
        )

    def dict(self, *args, **kwargs):
        kwargs.setdefault(
            "exclude", {"_encrypted_access_token", "_encrypted_refresh_token"}
        )
        return super().dict(*args, **kwargs)
