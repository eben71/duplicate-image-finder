from sqlmodel import SQLModel, Field
from sqlalchemy import Column, Enum as SAEnum
from datetime import datetime
from backend.models.enums import IngestionMode


class User(SQLModel, table=True):  # type: ignore
    id: int = Field(default=None, primary_key=True)
    email: str = Field(index=True, nullable=False, unique=True)
    full_name: str
    mode: IngestionMode = Field(
        sa_column=Column(SAEnum(IngestionMode, name="ingestionmode"))
    )
    created_at: datetime = Field(default_factory=datetime.utcnow)
