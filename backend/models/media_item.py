"""Media item SQLModel definition."""

from __future__ import annotations

from datetime import datetime
from typing import Optional

from sqlmodel import Column, Field, SQLModel

try:  # pragma: no cover - optional dependency
    from pgvector.sqlalchemy import Vector  # type: ignore
except ModuleNotFoundError:  # pragma: no cover - optional dependency
    from sqlalchemy.types import JSON, TypeDecorator

    class Vector(TypeDecorator):  # type: ignore[type-arg]
        impl = JSON
        cache_ok = True

        def __init__(self, dim: int):
            super().__init__()
            self.dim = dim

        def process_bind_param(self, value, dialect):
            return value

        def process_result_value(self, value, dialect):
            return value


class MediaItem(SQLModel, table=True):  # type: ignore[misc]
    __tablename__ = "media_items"

    model_config = {
        "validate_assignment": True,
        "validate_default": True,
    }

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(index=True)
    google_media_item_id: str = Field(index=True, unique=True)
    filename: Optional[str] = Field(default=None)
    base_url: Optional[str] = Field(default=None)
    mime_type: Optional[str] = Field(default=None)
    creation_time: Optional[datetime] = Field(default=None, index=True)

    embedding: Optional[list[float]] = Field(
        default=None,
        sa_column=Column(Vector(dim=768)),
    )
    pdq_hash: Optional[str] = Field(default=None, index=True)

