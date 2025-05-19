"""
Configuration for the Playwright scraper.
Loads environment variables from the project root `.env`.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

dotenv_path = Path(__file__).parents[1] / ".env"
load_dotenv(dotenv_path=dotenv_path)


def require_env(var_name: str) -> str:
    """
    Retrieve an environment variable or raise an error if it's missing.
    """
    value = os.getenv(var_name)
    if value is None or value.strip() == "":
        raise ValueError(f"{var_name} environment variable is required")
    return value


class ScraperConfig:
    GOOGLE_PHOTOS_URL: str = require_env("GOOGLE_PHOTOS_URL")
    FASTAPI_ENDPOINT: str = require_env(
        "FASTAPI_ENDPOINT"
    )  # FastAPI endpoint to POST scraped metadata

    BATCH_SIZE: int = int(
        os.getenv("BATCH_SIZE", 50)
    )  # Number of images to fetch per run
    TIMEOUT: int = int(
        os.getenv("TIMEOUT", 30000)
    )  # Playwright timeout for page loads & requests (in milliseconds)
    SCROLL_DEPTH: int = int(
        os.getenv("SCROLL_DEPTH", 5)
    )  # Number of scroll iterations to load more thumbnails


config = ScraperConfig()
