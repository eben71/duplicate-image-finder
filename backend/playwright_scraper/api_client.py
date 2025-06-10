"""
Encapsulates HTTP interactions with FastAPI endpoint.
"""

import httpx
import logging
from typing import List, Dict
from backend.config.settings import settings

logger = logging.getLogger(__name__)


def send_to_api(data: List[Dict]) -> None:
    """
    POST scraped image metadata to the FastAPI service.
    """
    try:
        response = httpx.post(
            settings.fastapi_endpoint, json=data, timeout=settings.timeout / 1000
        )
        response.raise_for_status()
        logger.info(f"Sent {len(data)} records successfully")

    except Exception as e:
        logger.error(f"API request failed: {e}")
