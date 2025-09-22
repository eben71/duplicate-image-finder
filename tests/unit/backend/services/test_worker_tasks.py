from sqlmodel import Session, select

from backend.models.embedding import ImageEmbedding
from backend.models.image import Image
from backend.services.worker.tasks import generate_embedding
from tests.utils.factories import make_test_user


def test_generate_embedding_uses_existing_session(session: Session) -> None:
    user = make_test_user()
    session.add(user)
    session.commit()
    session.refresh(user)

    image = Image(user_id=user.id, file_name="one.jpg", file_path="/tmp/one.jpg")
    session.add(image)
    session.commit()
    session.refresh(image)

    generate_embedding(image_id=image.id, session_override=session)

    stored = session.exec(select(ImageEmbedding)).all()
    assert len(stored) == 1
    assert stored[0].image_id == image.id
    assert len(stored[0].vector) > 0
