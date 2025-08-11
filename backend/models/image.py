from datetime import datetime

from sqlmodel import Field, SQLModel


class Image(SQLModel, table=True):  # type: ignore
    model_config = {
        "validate_default": True,
        "validate_assignment": True,
    }
    id: int | None = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    file_name: str
    file_path: str
    uploaded_at: datetime = Field(default_factory=datetime.utcnow)
