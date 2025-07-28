from pydantic import BaseModel, EmailStr
from typing import Optional
from backend.models.enums import IngestionMode


class UserRead(BaseModel):
    id: int
    email: EmailStr
    full_name: str
    profile_picture: Optional[str] = None
    ingestion_mode: IngestionMode
    requires_reauth: Optional[bool] = False

    model_config = {"from_attributes": True}
