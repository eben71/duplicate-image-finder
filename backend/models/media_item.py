"""Media item SQLModel definition."""

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Any

from sqlmodel import Column, Field, SQLModel

if TYPE_CHECKING:  # pragma: no cover - typing import
    from pgvector.sqlalchemy import Vector  # type: ignore
else:  # pragma: no cover - runtime import with fallback
    try:
        from pgvector.sqlalchemy import Vector  # type: ignore
    except ModuleNotFoundError:
        from sqlalchemy.types import JSON, TypeDecorator

        class Vector(TypeDecorator):  # type: ignore[type-arg]
            impl = JSON
            cache_ok = True

            def __init__(self, dim: int):
                super().__init__()
                self.dim = dim

            def process_bind_param(self, value: Any, dialect: Any) -> Any:
                return value

            def process_result_value(self, value: Any, dialect: Any) -> Any:
                return value


class MediaItem(SQLModel, table=True):  # type: ignore[misc]
    __tablename__ = "media_items"

    model_config = {
        "validate_assignment": True,
        "validate_default": True,
    }

    id: int | None = Field(default=None, primary_key=True)
    user_id: int = Field(index=True)
    google_media_item_id: str = Field(index=True, unique=True)
    filename: str | None = Field(default=None)
    base_url: str | None = Field(default=None)
    mime_type: str | None = Field(default=None)
    creation_time: datetime | None = Field(default=None, index=True)

    embedding: list[float] | None = Field(
        default=None,
        sa_column=Column(Vector(dim=768)),
    )
    pdq_hash: str | None = Field(default=None, index=True)
