from pydantic import BaseModel, EmailStr

from backend.models.enums import IngestionMode


class UserRead(BaseModel):
    id: int
    email: EmailStr
    full_name: str
    profile_picture: str | None = None
    ingestion_mode: IngestionMode
    requires_reauth: bool

    model_config = {"from_attributes": True}
