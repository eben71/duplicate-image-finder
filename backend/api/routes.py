import httpx
from fastapi import Request, Depends, HTTPException, APIRouter, Query
from fastapi.responses import RedirectResponse
from sqlmodel import Session, select
from backend.models.enums import IngestionMode
from backend.config.settings import settings
from core.google_oauth import get_google_auth_url, exchange_code_for_token
from backend.db.session import get_session
from backend.models.user import User
from backend.models.schemas.user import UserRead
from backend.services.ingestion.google_photos import fetch_images_by_year

api_router = APIRouter()


# --- Health Routes ---
@api_router.get("/health")
def health():
    return {"status": "ok"}


# --- User Routes ---


# --- Auth Routes ---
@api_router.get("/auth/login")
def google_login():
    auth_url = get_google_auth_url()
    return RedirectResponse(url=auth_url)


@api_router.get("/auth/callback", response_model=UserRead)
async def google_callback(request: Request, session: Session = Depends(get_session)):
    code = request.query_params.get("code")
    error = request.query_params.get("error")
    if error:
        raise HTTPException(status_code=400, detail=f"OAuth error: {error}")
    if not code:
        raise HTTPException(status_code=400, detail="Missing code parameter")

    try:
        token_data = await exchange_code_for_token(code)

        # Fetch user's Google Profile data
        async with httpx.AsyncClient() as client:
            userinfo_response = await client.get(
                settings.GOOGLE_USERINFO_URL,
                headers={"Authorization": f"Bearer {token_data['access_token']}"},
            )

            userinfo_response.raise_for_status()
            profile = await userinfo_response.json()

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

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

    return user


# --- Ingestion Routes ---
@api_router.post("/ingest")
def ingest_images(
    user_id: int, mode: IngestionMode = Query(default=IngestionMode.SCRAPE)
):
    if mode == IngestionMode.SCRAPE:
        return {"status": "scraped images"}
    elif mode == IngestionMode.API:
        return {"status": "fetched via API"}
    elif mode == IngestionMode.UPLOAD:
        return {"status": "uploaded manually"}


@api_router.get("/ingest/dev", tags=["Ingestion"])
async def ingest_photos_for_dev(
    user_id: int,
    session: Session = Depends(get_session),
):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    images = await fetch_images_by_year(
        user,
        session,
        year=settings.ingestion_year,
        start_page=settings.ingestion_start_page,
        end_page=settings.ingestion_end_page,
    )

    return {
        "year": settings.ingestion_year,
        "pages": {
            "start": settings.ingestion_start_page,
            "end": settings.ingestion_end_page,
        },
        "total_images": len(images),
        "sample": images[:3],  # return first 3 images for preview
    }
