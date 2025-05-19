from backend.services.worker.tasks import generate_embedding
from backend.models.embedding import ImageEmbedding
from backend.models.image import Image
from datetime import datetime


def test_generate_embedding_creates_vector(session):
    image = Image(
        user_id=1, file_name="test.jpg", file_path="/x", uploaded_at=datetime.utcnow()
    )
    session.add(image)
    session.commit()
    session.refresh(image)

    generate_embedding(image.id)

    embedding = (
        session.query(ImageEmbedding)
        .filter(ImageEmbedding.image_id == image.id)
        .first()
    )
    assert embedding is not None
    assert isinstance(embedding.vector, bytes)
    assert len(embedding.vector) > 100  # Not empty


def test_generate_embedding_skips_if_image_missing(session):
    try:
        generate_embedding(9999)
        assert True  # doesn't crash
    except Exception:
        assert False, "generate_embedding should not raise an error on missing image"
