import pytest
from backend.playwright_scraper.scraper import scrape_google_photos


@pytest.mark.asyncio
async def test_scrape_images_empty():
    class DummyPage:
        async def query_selector_all(self, _):
            return []

    images = await scrape_google_photos(DummyPage())
    assert isinstance(images, list)
    assert len(images) == 0
