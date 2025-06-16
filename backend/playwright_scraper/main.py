import asyncio
from backend.playwright_scraper.scraper import scrape_google_photos

if __name__ == "__main__":
    from core.logging_config import configure_logging

    configure_logging()
    asyncio.run(scrape_google_photos())
