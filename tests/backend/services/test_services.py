from backend.services.ingestion import fake_scrape_images

def test_fake_scrape_images_creates_and_returns(session):
    images = fake_scrape_images(user_id=1)
    assert len(images) == 3
    for img in images:
        assert img.file_name.endswith(".jpg")
