from datetime import datetime
from backend.models.user import User, IngestionMode
from backend.models.image import Image
from backend.models.embedding import ImageEmbedding
from backend.services.worker.tasks import generate_embedding


def test_generate_embedding_creates_vector(session):
    # Create a user first
    user = User(
        email="test2@example.com", full_name="Test User", mode=IngestionMode.SCRAPE
    )
    session.add(user)
    session.commit()
    session.refresh(user)

    # Now create image referencing that user
    image = Image(
        user_id=user.id,
        file_name="test.jpg",
        file_path="/x",
        uploaded_at=datetime.utcnow(),
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
    assert len(embedding.vector) > 100
