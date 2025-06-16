# tests/test_cookie_manager.py
import pytest
import json
from unittest.mock import AsyncMock, mock_open, patch
from backend.playwright_scraper import cookie_manager


@pytest.mark.asyncio
async def test_load_cookies_success():
    mock_context = AsyncMock()
    fake_cookies = [{"name": "test", "value": "123"}]
    m_open = mock_open(read_data=json.dumps(fake_cookies))

    with (
        patch(
            "backend.playwright_scraper.cookie_manager.Path.exists", return_value=True
        ),
        patch("backend.playwright_scraper.cookie_manager.Path.open", m_open),
    ):
        result = await cookie_manager.load_cookies(mock_context, "dummy/path.json")

    assert result is True
    mock_context.add_cookies.assert_called_once_with(fake_cookies)


@pytest.mark.asyncio
async def test_load_cookies_missing_file():
    mock_context = AsyncMock()
    with patch(
        "backend.playwright_scraper.cookie_manager.Path.exists", return_value=False
    ):
        result = await cookie_manager.load_cookies(mock_context, "missing.json")
    assert result is False


@pytest.mark.asyncio
async def test_save_cookies():
    mock_context = AsyncMock()
    mock_context.cookies = AsyncMock(return_value=[{"name": "test", "value": "456"}])
    m_open = mock_open()

    with patch("backend.playwright_scraper.cookie_manager.Path.open", m_open):
        await cookie_manager.save_cookies(mock_context, "some/path.json")

    handle = m_open()
    written = "".join(call.args[0] for call in handle.write.call_args_list)
    assert '"name": "test"' in written
