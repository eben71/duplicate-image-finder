from sqlmodel import SQLModel, Field


class ImageEmbedding(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    image_id: int = Field(foreign_key="image.id")
    vector: bytes
