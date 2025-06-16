import logging
from playwright.async_api import async_playwright, TimeoutError
from backend.playwright_scraper.cookie_manager import load_cookies, save_cookies
from backend.config.settings import settings


logger = logging.getLogger(__name__)


async def scrape_google_photos():
    async with async_playwright() as pw:
        browser = await pw.chromium.launch(headless=settings.HEADLESS_MODE)
        context = await browser.new_context()

        session_valid = False

        await load_cookies(context, settings.SESSION_COOKIE_PATH)
        page = await context.new_page()
        await page.goto(settings.GOOGLE_PHOTOS_URL, wait_until="load")

        try:
            await page.wait_for_selector('[aria-label="Account"]', timeout=5000)
            session_valid = True
            logger.info("✅ Session is valid – user is logged in.")

        except TimeoutError:
            logger.warning("❌ Session invalid or expired – manual login required.")

        if not session_valid:
            print("🔑 Please complete login in the browser window, then press ENTER...")
            input()
            await save_cookies(context, settings.SESSION_COOKIE_PATH)
            logger.info("✅ New cookies saved after manual login.")

        logger.info("🔍 Ready to begin image scraping...")
