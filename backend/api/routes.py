from fastapi import Request, HTTPException, APIRouter, Query
from fastapi.responses import RedirectResponse
from backend.models.enums import IngestionMode
from core.google_oauth import get_google_auth_url, exchange_code_for_token

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


@api_router.get("/auth/callback")
async def google_callback(request: Request):
    code = request.query_params.get("code")
    if not code:
        raise HTTPException(status_code=400, detail="Missing code parameter")

    token_data = await exchange_code_for_token(code)

    # TODO: link token_data to user in DB (we'll do this next step)
    return {"tokens": token_data}


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
