"""create media items table and vector index"""

from typing import TYPE_CHECKING, Any

import sqlalchemy as sa
from alembic import op

if TYPE_CHECKING:  # pragma: no cover - typing import
    from pgvector.sqlalchemy import Vector  # type: ignore

    HAS_VECTOR = True
else:  # pragma: no cover - runtime import with fallback
    try:
        from pgvector.sqlalchemy import Vector  # type: ignore

        HAS_VECTOR = True
    except ModuleNotFoundError:
        HAS_VECTOR = False

        class Vector(sa.types.JSON):  # type: ignore[type-arg]
            def __init__(self, dim: int):  # noqa: D401 - mimic pgvector API
                super().__init__()
                self.dim = dim

            def bind_processor(self, dialect: Any):  # pragma: no cover - fallback helper
                return None


# revision identifiers, used by Alembic.
revision = "20250217_create_media_items_table"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    if HAS_VECTOR:
        op.execute("CREATE EXTENSION IF NOT EXISTS vector")

    op.create_table(
        "media_items",
        sa.Column("id", sa.Integer(), primary_key=True, nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("google_media_item_id", sa.String(), nullable=False),
        sa.Column("filename", sa.String(), nullable=True),
        sa.Column("base_url", sa.String(), nullable=True),
        sa.Column("mime_type", sa.String(), nullable=True),
        sa.Column("creation_time", sa.DateTime(), nullable=True),
        sa.Column("embedding", Vector(dim=768), nullable=True),
        sa.Column("pdq_hash", sa.String(), nullable=True),
    )

    op.create_index("ix_media_items_user_id", "media_items", ["user_id"])
    op.create_index(
        "ix_media_items_google_media_item_id",
        "media_items",
        ["google_media_item_id"],
        unique=True,
    )
    op.create_index("ix_media_items_creation_time", "media_items", ["creation_time"])
    op.create_index("ix_media_items_pdq_hash", "media_items", ["pdq_hash"])
    if HAS_VECTOR:
        op.execute(
            "CREATE INDEX IF NOT EXISTS media_items_embedding_idx "
            "ON media_items USING ivfflat (embedding vector_cosine_ops) WITH (lists = 100)"
        )


def downgrade() -> None:
    if HAS_VECTOR:
        op.execute("DROP INDEX IF EXISTS media_items_embedding_idx")
    op.drop_index("ix_media_items_pdq_hash", table_name="media_items")
    op.drop_index("ix_media_items_creation_time", table_name="media_items")
    op.drop_index("ix_media_items_google_media_item_id", table_name="media_items")
    op.drop_index("ix_media_items_user_id", table_name="media_items")
    op.drop_table("media_items")
