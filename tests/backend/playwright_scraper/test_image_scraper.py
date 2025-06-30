import pytest
from unittest.mock import AsyncMock
from backend.playwright_scraper.image_scraper import extract_images

@pytest.mark.asyncio
async def test_extract_images_scrolls_and_extracts():
    mock_page = AsyncMock()

    def make_mock_img(src_val, alt_val):
        mock_img = AsyncMock()
        async def get_attribute(attr):
            return src_val if attr == "src" else alt_val
        mock_img.get_attribute.side_effect = get_attribute
        return mock_img

    mock_img_1 = make_mock_img("https://lh3.googleusercontent.com/image1.jpg", "Alt text 1")
    mock_img_2 = make_mock_img("https://lh3.googleusercontent.com/image2.jpg", "Alt text 2")

    mock_page.query_selector_all = AsyncMock(return_value=[mock_img_1, mock_img_2])
    mock_page.mouse.wheel = AsyncMock()
    mock_page.wait_for_timeout = AsyncMock()

    result = await extract_images(mock_page, scroll_limit=2)

    assert isinstance(result, list)
    assert len(result) == 2
    urls = [img["url"] for img in result]
    assert "https://lh3.googleusercontent.com/image1.jpg" in urls
    assert "https://lh3.googleusercontent.com/image2.jpg" in urls
