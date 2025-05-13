"""
Orchestrates the Playwright scraping flow:
1. Load cookies
2. Authenticate (or prompt login)
3. Scrape images
4. Persist new cookies
5. Send metadata to API
"""
import asyncio
import logging
from playwright.async_api import async_playwright, BrowserContext, Page, TimeoutError as PlaywrightTimeoutError
from .config import config
from .cookie_manager import load_cookies, save_cookies
from .scraper import scrape_images
from .api_client import send_to_api

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def ensure_authenticated(context: BrowserContext) -> Page:
    """
    Navigate to Google Photos, use cookies if valid or pause for manual login.
    """
    page = await context.new_page()
    await page.goto(config.GOOGLE_PHOTOS_URL, timeout=config.TIMEOUT)
    if 'signin' in page.url:
        logger.info("Login required; please authenticate in browser window.")
        await page.wait_for_timeout(60000)
        await save_cookies(context)
    else:
        logger.info("Authenticated via cookies.")
    return page

async def main() -> None:
    async with async_playwright() as pw:
        browser = await pw.chromium.launch(headless=False)
        context = await browser.new_context()

        await load_cookies(context)
        page = await ensure_authenticated(context)

        try:
            images = await scrape_images(page)
            if images:
                send_to_api(images)

        except PlaywrightTimeoutError as e:
            logger.error(f"Scraping timeout: {e}")
            
        finally:
            await save_cookies(context)
            await browser.close()

if __name__ == '__main__':
    asyncio.run(main())