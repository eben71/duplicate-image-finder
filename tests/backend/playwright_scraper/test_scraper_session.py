# tests/test_scraper_session.py

import pytest
from unittest.mock import AsyncMock, patch
from backend.playwright_scraper import scraper


@pytest.mark.asyncio
async def test_scrape_google_photos_valid_session():
    # Mocks
    mock_page = AsyncMock()
    mock_page.goto = AsyncMock()
    mock_page.wait_for_selector = AsyncMock()

    mock_context = AsyncMock()
    mock_context.new_page = AsyncMock(return_value=mock_page)

    mock_browser = AsyncMock()
    mock_browser.new_context = AsyncMock(return_value=mock_context)

    mock_pw = AsyncMock()
    mock_pw.chromium.launch = AsyncMock(return_value=mock_browser)

    with (
        patch("backend.playwright_scraper.scraper.async_playwright") as mock_pw_context,
        patch("backend.playwright_scraper.scraper.load_cookies", return_value=True),
        patch("backend.playwright_scraper.scraper.save_cookies") as mock_save,
    ):
        mock_pw_context.return_value.__aenter__.return_value = mock_pw
        await scraper.scrape_google_photos()

        mock_page.wait_for_selector.assert_called_with(
            '[aria-label="Account"]', timeout=5000
        )
        mock_save.assert_not_called()
