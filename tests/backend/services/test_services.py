import pytest
from backend.models.user import User, IngestionMode
from backend.services.ingestion import fake_scrape_images
from unittest.mock import patch


@patch("backend.services.ingestion.generate_embedding.delay")
def test_fake_scrape_images_creates_and_returns(mock_delay, session):
    user = User(email="test@example.com", full_name="Test", mode=IngestionMode.SCRAPE)
    session.add(user)
    session.commit()
    session.refresh(user)

    images = fake_scrape_images(user_id=user.id, session=session)

    assert len(images) == 3
    for img in images:
        assert img.file_name.endswith(".jpg")
    assert mock_delay.call_count == 3
