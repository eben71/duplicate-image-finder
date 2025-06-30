from typing import List, Dict
import logging

logger = logging.getLogger(__name__)


async def extract_images(page, scroll_limit: int = 10) -> List[Dict]:
    logger.info(f"📜 Starting scroll + scrape up to {scroll_limit} times...")
    results = set()

    for i in range(scroll_limit):
        logger.debug(f"🌀 Scroll iteration {i + 1}/{scroll_limit}")
        await page.mouse.wheel(0, 10000)
        await page.wait_for_timeout(1000)

        elements = await page.query_selector_all(
            'img[src^="https://lh3.googleusercontent.com/"]'
        )

        for img in elements:
            src = await img.get_attribute("src")
            alt = await img.get_attribute("alt")
            if src:
                results.add((src, alt))

    logger.info(f"✅ Found {len(results)} unique images")

    return [{"url": url, "alt": alt or ""} for url, alt in results]
