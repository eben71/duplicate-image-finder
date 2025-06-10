import pytest
from backend.playwright_scraper.scraper import scrape_images


@pytest.mark.asyncio
async def test_scrape_images_empty():
    class DummyPage:
        async def query_selector_all(self, _):
            return []

    images = await scrape_images(DummyPage())
    assert isinstance(images, list)
    assert len(images) == 0
