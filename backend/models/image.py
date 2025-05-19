from sqlmodel import SQLModel, Field
from datetime import datetime


class Image(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    file_name: str
    file_path: str
    uploaded_at: datetime = Field(default_factory=datetime.utcnow)
