from __future__ import annotations

import pytest
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel, Session, create_engine

from backend.models.media_item import MediaItem
from backend.services.vector.pgvector_store import VectorStore


def _build_embedding(value: float = 1.0) -> list[float]:
    vec = [0.0] * 768
    vec[0] = value
    vec[1] = value / 2
    return vec


def test_vector_store_round_trip() -> None:
    engine = create_engine("sqlite:///:memory:", echo=False)
    SQLModel.metadata.create_all(engine)
    SessionLocal = sessionmaker(bind=engine, class_=Session, expire_on_commit=False)

    with SessionLocal() as session:
        media = MediaItem(
            user_id=1,
            google_media_item_id="item-1",
            filename="one.png",
        )
        session.add(media)
        session.commit()
        media_id = media.id

    store = VectorStore(session_factory=SessionLocal)
    embedding = _build_embedding()

    store.upsert_embedding(media_item_id=media_id, embedding=embedding, pdq_hash="abcd")

    results = store.search(embedding=embedding, user_id=1, top_k=5)
    assert results
    assert results[0]["id"] == media_id
    assert results[0]["similarity"] == pytest.approx(1.0, rel=1e-6)

    candidates = store.fetch_pdq_candidates(user_id=1, limit=5)
    assert candidates
    assert candidates[0]["pdq_hash"] == "abcd"
