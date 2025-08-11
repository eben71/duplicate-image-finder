from typing import Any

from backend.services.worker.tasks import generate_embedding


def test_generate_embedding_creates_vector(session: Any) -> None:
    # Assume test DB already has image with ID 123
    image_id = 123
    # Insert a dummy image row if needed...

    generate_embedding(image_id=image_id, session_override=session)

    from backend.models.embedding import ImageEmbedding

    stored = session.query(ImageEmbedding).filter_by(image_id=image_id).first()

    assert stored is not None
    assert len(stored.vector) == 512 * 4  # float32 = 4 bytes
