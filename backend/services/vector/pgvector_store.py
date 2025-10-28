"""pgvector-backed persistence helpers."""

from __future__ import annotations

from collections.abc import Callable, Sequence
from math import sqrt
from typing import Any

from sqlalchemy import func, select, text
from sqlmodel import Session

from backend.models.media_item import MediaItem


class VectorStore:
    """Persist and query embeddings stored in PostgreSQL/pgvector."""

    def __init__(self, session_factory: Callable[[], Session]):
        self._session_factory = session_factory

    def upsert_embedding(
        self,
        media_item_id: int,
        embedding: Sequence[float],
        pdq_hash: str | None = None,
    ) -> None:
        with self._session_factory() as session:
            item = session.get(MediaItem, media_item_id)
            if item is None:
                raise ValueError(f"MediaItem {media_item_id} not found")

            item.embedding = list(map(float, embedding))  # type: ignore[assignment]
            if pdq_hash is not None:
                item.pdq_hash = pdq_hash

            session.add(item)
            session.commit()

    def search(
        self,
        embedding: Sequence[float],
        user_id: int,
        top_k: int = 50,
    ) -> list[dict[str, Any]]:
        vector = list(map(float, embedding))
        with self._session_factory() as session:
            bind = session.get_bind()
            if bind is not None and bind.dialect.name != "postgresql":
                return self._search_python(
                    session=session,
                    vector=vector,
                    user_id=user_id,
                    top_k=top_k,
                )

            query = (
                select(
                    MediaItem.id,
                    MediaItem.filename,
                    MediaItem.base_url,
                    MediaItem.mime_type,
                    MediaItem.creation_time,
                    (1 - func.cosine_distance(MediaItem.embedding, vector)).label("similarity"),
                )
                .where(MediaItem.user_id == user_id)
                .where(MediaItem.embedding.is_not(None))
                .order_by(text("similarity DESC"))
                .limit(top_k)
            )

            rows = session.execute(query).all()

        results: list[dict[str, Any]] = []
        for row in rows:
            similarity = row.similarity
            results.append(
                {
                    "id": row.id,
                    "filename": row.filename,
                    "base_url": row.base_url,
                    "mime_type": row.mime_type,
                    "creation_time": row.creation_time,
                    "similarity": float(similarity) if similarity is not None else None,
                }
            )
        return results

    def _search_python(
        self,
        *,
        session: Session,
        vector: Sequence[float],
        user_id: int,
        top_k: int,
    ) -> list[dict[str, Any]]:
        query = (
            select(MediaItem)
            .where(MediaItem.user_id == user_id)
            .where(MediaItem.embedding.is_not(None))
        )
        items = session.execute(query).scalars().all()

        scored: list[dict[str, Any]] = []
        for item in items:
            stored = item.embedding or []
            if not stored:
                continue
            similarity = self._cosine_similarity(vector, stored)
            scored.append(
                {
                    "id": item.id,
                    "filename": item.filename,
                    "base_url": item.base_url,
                    "mime_type": item.mime_type,
                    "creation_time": item.creation_time,
                    "similarity": similarity,
                }
            )

        scored.sort(key=lambda entry: entry["similarity"] or -1.0, reverse=True)
        return scored[:top_k]

    @staticmethod
    def _cosine_similarity(
        vec_a: Sequence[float],
        vec_b: Sequence[float],
    ) -> float | None:
        if not vec_a or not vec_b:
            return None

        dot = sum(a * b for a, b in zip(vec_a, vec_b, strict=True))
        norm_a = sqrt(sum(a * a for a in vec_a))
        norm_b = sqrt(sum(b * b for b in vec_b))
        if norm_a == 0 or norm_b == 0:
            return None
        return dot / (norm_a * norm_b)

    def fetch_pdq_candidates(self, user_id: int, limit: int = 200) -> list[dict[str, Any]]:
        with self._session_factory() as session:
            query = (
                select(
                    MediaItem.id,
                    MediaItem.filename,
                    MediaItem.base_url,
                    MediaItem.pdq_hash,
                    MediaItem.creation_time,
                )
                .where(MediaItem.user_id == user_id)
                .where(MediaItem.pdq_hash.is_not(None))
                .order_by(MediaItem.creation_time.desc())
                .limit(limit)
            )

            rows = session.execute(query).all()

        return [
            {
                "id": row.id,
                "filename": row.filename,
                "base_url": row.base_url,
                "pdq_hash": row.pdq_hash,
                "creation_time": row.creation_time,
            }
            for row in rows
        ]
