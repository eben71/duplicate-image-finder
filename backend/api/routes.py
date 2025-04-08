from fastapi import APIRouter, Query
from celery.result import AsyncResult
from backend.services.worker.celery_app import celery_app
from backend.services.ingestion import fake_scrape_images

router = APIRouter()

@router.get("/health")
def health():
    return {"status": "ok"}

@router.post("/ingest")
def ingest_images(user_id: int, mode: str = Query("scrape")):
    """
    Simulates scraping or API ingestion and pushes images to Celery.
    """
    images = fake_scrape_images(user_id)
    return {"message": f"Ingested {len(images)} images", "images": [img.id for img in images]}
