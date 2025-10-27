import logging
from functools import lru_cache
from typing import Annotated, Any

import httpx
from fastapi import APIRouter, Depends, File, HTTPException, Query, Request, UploadFile
from sqlmodel import Session, select
from starlette.responses import RedirectResponse

from backend.config.settings import settings
from backend.db.session import SessionLocal, get_session
from backend.deps import get_http_client
from backend.models.enums import IngestionMode
from backend.models.schemas.user import UserRead
from backend.models.user import User
from backend.services.ingestion.google_photos import fetch_images_by_year
from backend.services.vector import VectorStore
from backend.services.embeddings import SigLIP2Encoder
from backend.services.dedupe import DedupePipeline, PDQFilter
from backend.models.media_item import MediaItem
from core.google_oauth import exchange_code_for_token, get_google_auth_url

try:  # pragma: no cover - optional dependency
    import multipart  # type: ignore

    HAS_MULTIPART = True
except ModuleNotFoundError:  # pragma: no cover - optional dependency
    HAS_MULTIPART = False

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
    client: Annotated[httpx.AsyncClient, Depends(get_http_client)],
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
        token_data = await exchange_code_for_token(code, client)
        logger.debug(f"Token data: {token_data}")

        # Fetch user's Google Profile data
        logger.debug(f"Making POST to {settings.GOOGLE_USERINFO_URL}")
        userinfo_response = await client.get(
            settings.GOOGLE_USERINFO_URL,
            headers={"Authorization": f"Bearer {token_data['access_token']}"},
        )

        logger.debug("POST completed")
        userinfo_response.raise_for_status()
        profile = userinfo_response.json()
        logger.debug(f"Profile: {profile}")

    except ValueError as e:
        logger.debug(f"ValueError in google_callback: {e}")
        raise HTTPException(status_code=400, detail=str(e)) from e
    except Exception as e:
        logger.debug(f"Unexpected error in google_callback: {e}")
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
        user.requires_reauth = False
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
        user.requires_reauth = False
        session.add(user)

    session.commit()

    user_read = UserRead.model_validate(user)
    return user_read


# --- Ingestion Routes ---
@api_router.post("/ingest", response_model=dict[str, Any])
def ingest_images(
    user_id: int,
    session: Annotated[Session, Depends(get_session)],
    mode: Annotated[IngestionMode, Query()] = IngestionMode.SCRAPE,
) -> dict[str, Any]:
    if user_id <= 0:
        raise HTTPException(status_code=400, detail="user_id must be a positive integer")

    user = session.get(User, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

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
    client: Annotated[httpx.AsyncClient, Depends(get_http_client)],
) -> dict[str, Any]:
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    images = await fetch_images_by_year(
        user,
        session,
        client,
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


@lru_cache()
def get_siglip2_encoder() -> SigLIP2Encoder:
    return SigLIP2Encoder()


@lru_cache()
def get_vector_store() -> VectorStore:
    return VectorStore(session_factory=SessionLocal)


if HAS_MULTIPART:

    @api_router.post("/ingest/media/{media_item_id}/embed", response_model=dict[str, Any])
    async def embed_media_item(
        media_item_id: int,
        session: Annotated[Session, Depends(get_session)],
        file: UploadFile = File(...),
    ) -> dict[str, Any]:
        media_item = session.get(MediaItem, media_item_id)
        if media_item is None:
            raise HTTPException(status_code=404, detail="Media item not found")

        payload = await file.read()
        if not payload:
            raise HTTPException(status_code=400, detail="Uploaded file is empty")

        pdq_filter = PDQFilter(method="auto")
        pdq_hash, quality, method = pdq_filter.compute_hash(payload)

        encoder = get_siglip2_encoder()
        embedding = encoder.embed_bytes(payload)

        vector_store = get_vector_store()
        vector_store.upsert_embedding(media_item_id=media_item_id, embedding=embedding, pdq_hash=pdq_hash)

        return {
            "status": "ok",
            "pdq_hash": pdq_hash,
            "pdq_quality": quality,
            "pdq_method": method,
            "embedding_dim": len(embedding),
        }


    @api_router.post("/dedupe/search/{user_id}", response_model=dict[str, Any])
    async def dedupe_search(
        user_id: int,
        session: Annotated[Session, Depends(get_session)],
        file: UploadFile = File(...),
    ) -> dict[str, Any]:
        user = session.get(User, user_id)
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")

        payload = await file.read()
        if not payload:
            raise HTTPException(status_code=400, detail="Uploaded file is empty")

        pipeline = DedupePipeline(vector_store=get_vector_store(), encoder=get_siglip2_encoder())
        matches = pipeline.find_candidates(payload, user_id=user_id)
        return {"results": matches}
else:  # pragma: no cover - optional dependency guard
    logger.warning(
        "python-multipart is not installed; media upload and dedupe endpoints are disabled.",
    )
