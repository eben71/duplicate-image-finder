import logging
from playwright.async_api import async_playwright, TimeoutError
from backend.playwright_scraper.cookie_manager import load_cookies, save_cookies
from backend.playwright_scraper.image_scraper import extract_images
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

        session_valid = await is_session_valid(page)

        if not session_valid:
            logger.warning("❌ Session invalid or expired – manual login required.")
            print("🔑 Please complete login in the browser window, then press ENTER...")
            input()

            await save_cookies(context, settings.SESSION_COOKIE_PATH)
            session_valid = await is_session_valid(page)

            if not session_valid:
                logger.error("❌ Login still invalid after manual attempt – aborting.")
                return

            logger.info("✅ Session is valid – continuing to scrape...")
            images = await extract_images(page, scroll_limit=5)

async def is_session_valid(page) -> bool:
    try:
        await page.wait_for_selector('[aria-label="Account"]', timeout=5000)
        return True
    except:
        return False
