import json
import logging
from pathlib import Path
from typing import List
from playwright.async_api import BrowserContext

COOKIE_FILE = Path(__file__).parent / "cookies.json"
logger = logging.getLogger(__name__)


async def load_cookies(context: BrowserContext) -> None:
    """
    Load cookies from disk into Playwright context.
    """
    if COOKIE_FILE.exists():
        try:
            cookies = json.loads(COOKIE_FILE.read_text())
            await context.add_cookies(cookies)
            logger.info(f"Loaded {len(cookies)} cookies from {COOKIE_FILE}")
        except Exception as e:
            logger.error(f"Failed to load cookies: {e}")
    else:
        logger.info(f"No cookie file at {COOKIE_FILE}, login required.")


async def save_cookies(context: BrowserContext) -> None:
    """
    Persist current context cookies to disk.
    """
    try:
        cookies = await context.cookies()
        COOKIE_FILE.write_text(json.dumps(cookies, indent=2))
        logger.info(f"Saved {len(cookies)} cookies to {COOKIE_FILE}")
    except Exception as e:
        logger.error(f"Failed to save cookies: {e}")