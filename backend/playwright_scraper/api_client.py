"""
Encapsulates HTTP interactions with FastAPI endpoint.
"""

import httpx
import logging
from typing import List, Dict
from .config import config

logger = logging.getLogger(__name__)


def send_to_api(data: List[Dict]) -> None:
    """
    POST scraped image metadata to the FastAPI service.
    """
    try:
        response = httpx.post(
            config.FASTAPI_ENDPOINT, json=data, timeout=config.TIMEOUT / 1000
        )
        response.raise_for_status()
        logger.info(f"Sent {len(data)} records successfully")

    except Exception as e:
        logger.error(f"API request failed: {e}")
