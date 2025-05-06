from fastapi import APIRouter, Query
from celery.result import AsyncResult
from backend.services.worker.celery_app import celery_app
from backend.services.ingestion import fake_scrape_images
from backend.models.enums import IngestionMode

router = APIRouter()

@router.get("/health")
def health():
    return {"status": "ok"}

@router.post("/ingest")
def ingest_images(user_id: int, mode: IngestionMode = Query(default=IngestionMode.SCRAPE)):
    if mode == IngestionMode.SCRAPE:
        return {"status": "scraped images"}
    elif mode == IngestionMode.API:
        return {"status": "fetched via API"}
    elif mode == IngestionMode.UPLOAD:
        return {"status": "uploaded manually"}