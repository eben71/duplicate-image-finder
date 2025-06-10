from backend.models.user import User, IngestionMode
from backend.services.ingestion import fake_scrape_images


def test_fake_scrape_images_creates_and_returns(session):
    user = User(email="test@example.com", full_name="Test", mode=IngestionMode.SCRAPE)
    session.add(user)
    session.commit()
    session.refresh(user)

    images = fake_scrape_images(user_id=user.id, session=session)

    assert len(images) == 3
    for img in images:
        assert img.file_name.endswith(".jpg")
