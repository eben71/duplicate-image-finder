from datetime import datetime
from typing import Annotated

import httpx
from fastapi import Depends
from sqlmodel import Session

from backend.config.settings import settings
from backend.deps import get_http_client
from backend.models.user import User
from core.google_oauth import get_fresh_access_token


async def fetch_images_by_year(
    user: User,
    session: Session,
    client: Annotated[httpx.AsyncClient, Depends(get_http_client)],
    year: int | None = settings.INGESTION_YEAR,
    start_page: int = settings.INGESTION_START_PAGE,
    end_page: int | None = settings.INGESTION_END_PAGE,
) -> list[dict]:
    access_token = await get_fresh_access_token(user, session, client)
    headers = {"Authorization": f"Bearer {access_token}"}
    images: list[dict] = []

    if not year:
        # Fallback to current year
        # TODO - what if user's latest photos is not in current year?
        year = datetime.now().year

    # TODO What if we don't want to limit it to only a year or span years?
    payload = {
        "pageSize": settings.INGESTION_PAGE_SIZE,
        "filters": {
            "dateFilter": {"ranges": [{"startDate": {"year": year}, "endDate": {"year": year}}]}
        },
    }

    # TODO - Initializing current_page to start_page causes the very first API response to be
    # treated  as that page, meaning you can’t skip the earlier pages.
    # Start counting at 1 (or track actual page index separately)
    #  so start_page/end_page act as documented.
    current_page = start_page
    next_page_token = None

    while True:
        if next_page_token:
            payload["pageToken"] = next_page_token
        else:
            payload.pop("pageToken", None)

        response = await client.post(settings.GOOGLE_SEARCH_URL, headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()

        if current_page >= start_page:
            for item in data.get("mediaItems", []):
                if item.get("mimeType", "").startswith("image/"):
                    images.append(
                        {
                            "id": item["id"],
                            "filename": item.get("filename"),
                            "mimeType": item.get("mimeType"),
                            "baseUrl": item.get("baseUrl"),
                        }
                    )

        current_page += 1
        next_page_token = data.get("nextPageToken")

        if not next_page_token:
            break
        if end_page and current_page > end_page:
            break

    return images
