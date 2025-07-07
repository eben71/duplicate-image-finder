from sqlmodel import SQLModel, Field
from typing import Optional


class ImageEmbedding(SQLModel, table=True):  # type: ignore
    model_config = {
        "validate_default": True,
        "validate_assignment": True,
    }
    id: Optional[int] = Field(default=None, primary_key=True)

    image_id: int = Field(foreign_key="image.id")
    vector: bytes
