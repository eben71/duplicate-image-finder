from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional


class Image(SQLModel, table=True):  # type: ignore
    model_config = {
        "validate_default": True,
        "validate_assignment": True,
    }
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    file_name: str
    file_path: str
    uploaded_at: datetime = Field(default_factory=datetime.utcnow)
