import json
import logging
from pathlib import Path


logger = logging.getLogger(__name__)

async def load_cookies(context, path: str) -> bool:
    path_obj = Path(path).expanduser()
    if not path_obj.exists():
        logger.info(f"No cookie file found at {path_obj}")
        return False

    try:
        with path_obj.open("r") as f:
            cookies = json.load(f)

        await context.add_cookies(cookies)
        logger.info(f"Loaded cookies from {path_obj}")
        return True

    except Exception as ex:
        logger.error(f"Failed to load cookies: {ex}", exc_info=True)
        return False


async def save_cookies(context, path: str):
    path_obj = Path(path).expanduser()
    try:
        cookies = await context.cookies()
        with path_obj.open("w") as f:
            json.dump(cookies, f, indent=2)
        logger.info(f"Saved cookies to {path_obj}")

    except Exception as ex:
        logger.error(f"Failed to save cookies: {ex}", exc_info=True)
