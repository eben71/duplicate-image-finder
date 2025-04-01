from sqlmodel import SQLModel, Field
from datetime import datetime

class User(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    email: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
