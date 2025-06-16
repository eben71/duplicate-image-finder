import logging
from playwright.async_api import async_playwright
from cookie_manager import load_cookies, save_cookies
from backend.config.settings import settings


logger = logging.getLogger(__name__)


async def scrape_google_photos():
    async with async_playwright() as pw:
        browser = await pw.chromium.launch(headless=settings.HEADLESS_MODE)
        context = await browser.new_context()

        cookies_loaded = await load_cookies(context, settings.COOKIE_FILE)
        page = await context.new_page()
        await page.goto(settings.GOOGLE_PHOTOS_URL, wait_until="load")

        if not cookies_loaded:
            logger.warning("No cookies loaded. Prompting for manual login...")
            print("🔑 Please login in the browser window. Press ENTER once complete.")
            input()
            await save_cookies(context, settings.COOKIE_FILE)

        logger.info("Browser is ready and session is active.")
        # Future: Add scrolling and image extraction logic here.
