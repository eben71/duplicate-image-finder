import numpy as np
from backend.services.worker.celery_app import celery_app
from backend.models.embedding import ImageEmbedding
from backend.db.session import engine
from sqlmodel import Session


@celery_app.task
def generate_embedding(image_id: int, session_override: Session = None):
    """
    Simulates generating a 512-dim embedding and stores it.
    Allows session override for test injection.
    """
    fake_vector = np.random.rand(512).astype(np.float32).tobytes()

    if session_override:
        session = session_override
        owns_session = False
    else:
        session = Session(engine)
        owns_session = True

    try:
        embedding = ImageEmbedding(image_id=image_id, vector=fake_vector)
        session.add(embedding)
        session.commit()
    finally:
        if owns_session:
            session.close()
