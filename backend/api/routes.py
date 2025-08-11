import logging
from typing import Annotated, Any

import httpx
from fastapi import APIRouter, Depends, HTTPException, Query, Request
from sqlmodel import Session, select
from starlette.responses import RedirectResponse

from backend.config.settings import settings
from backend.db.session import get_session
from backend.models.enums import IngestionMode
from backend.models.schemas.user import UserRead
from backend.models.user import User
from backend.services.ingestion.google_photos import fetch_images_by_year
from core.google_oauth import exchange_code_for_token, get_google_auth_url

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

api_router = APIRouter()


# --- Health Routes ---
@api_router.get("/health", response_model=dict[str, str])
def health() -> dict[str, str]:
    return {"status": "ok"}


# --- User Routes ---


# --- Auth Routes ---
@api_router.get("/auth/login", response_model=None)
def google_login() -> RedirectResponse:
    auth_url = get_google_auth_url()
    return RedirectResponse(url=auth_url)


@api_router.get("/auth/callback", response_model=UserRead)
async def google_callback(
    request: Request,
    session: Annotated[Session, Depends(get_session)],
) -> UserRead:
    logger.debug("Entered google_callback")
    code = request.query_params.get("code")
    error = request.query_params.get("error")
    if error:
        logger.debug(f"OAuth error: {error}")
        raise HTTPException(status_code=400, detail=f"OAuth error: {error}")
    if not code:
        logger.debug("Missing code parameter")
        raise HTTPException(status_code=400, detail="Missing code parameter")

    try:
        token_data = await exchange_code_for_token(code)
        logger.debug(f"Token data: {token_data}")

        # Fetch user's Google Profile data
        async with httpx.AsyncClient() as client:
            logger.debug(f"Making POST to {settings.GOOGLE_USERINFO_URL}")
            userinfo_response = await client.post(
                settings.GOOGLE_USERINFO_URL,
                headers={"Authorization": f"Bearer {token_data['access_token']}"},
            )

            logger.debug("POST completed")
            userinfo_response.raise_for_status()
            profile = await userinfo_response.json()
            logger.debug(f"Profile: {profile}")

    except ValueError as e:
        logger.debug("ValueError in google_callback: %s", str(e))
        # B904: preserve original cause for debugging
        raise HTTPException(status_code=400, detail=str(e)) from e
    except Exception as e:
        logger.debug("Unexpected error in google_callback: %s", str(e))
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}") from e

    email = profile["email"]
    full_name = profile.get("full_name", "")
    picture = profile.get("profile_picture")

    user = session.exec(select(User).where(User.email == email)).first()

    if user:
        user.set_google_tokens(
            access_token=token_data["access_token"],
            refresh_token=token_data.get("refresh_token"),
            expires_in=token_data["expires_in"],
        )
    else:
        user = User(
            email=email,
            full_name=full_name,
            profile_picture=picture,
        )
        user.set_google_tokens(
            access_token=token_data["access_token"],
            refresh_token=token_data.get("refresh_token"),
            expires_in=token_data["expires_in"],
        )
        session.add(user)

    session.commit()

    user_read = UserRead.model_validate(user)
    return user_read


# --- Ingestion Routes ---
@api_router.post("/ingest", response_model=dict[str, Any])
def ingest_images(
    user_id: int,
    mode: Annotated[IngestionMode, Query()] = IngestionMode.SCRAPE,
) -> dict[str, Any]:
    if mode == IngestionMode.SCRAPE:
        return {"status": "scraped images"}
    elif mode == IngestionMode.API:
        return {"status": "fetched via API"}
    elif mode == IngestionMode.UPLOAD:
        return {"status": "uploaded manually"}


@api_router.get("/ingest/dev", tags=["Ingestion"], response_model=dict[str, Any])
async def ingest_photos_for_dev(
    user_id: int,
    session: Annotated[Session, Depends(get_session)],
) -> dict[str, Any]:
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    images = await fetch_images_by_year(
        user,
        session,
        year=settings.INGESTION_YEAR,
        start_page=settings.INGESTION_START_PAGE,
        end_page=settings.INGESTION_END_PAGE,
    )

    return {
        "year": settings.INGESTION_YEAR,
        "pages": {
            "start": settings.INGESTION_START_PAGE,
            "end": settings.INGESTION_END_PAGE,
        },
        "total_images": len(images),
        "sample": images[:3],  # return first 3 images for preview
    }
