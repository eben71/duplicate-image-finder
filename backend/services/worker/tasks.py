import numpy as np
from backend.services.worker.celery_app import celery_app
from backend.models.embedding import ImageEmbedding
from backend.db.session import engine
from sqlmodel import Session

@celery_app.task
def generate_embedding(image_id: int):
    """
    Simulates generating a 512-dim embedding and stores it.
    """
    fake_vector = np.random.rand(512).astype(np.float32).tobytes()

    with Session(engine) as session:
        embedding = ImageEmbedding(
            image_id=image_id,
            vector=fake_vector
        )
        session.add(embedding)
        session.commit()
