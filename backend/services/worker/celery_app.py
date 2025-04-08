from backend.config.settings import settings
from celery import Celery 

celery_app = Celery(
    "duplicate_finder",
    broker=settings.celery_broker_url,
    backend=settings.celery_backend_url,
)

celery_app.conf.task_routes = {
    "backend.services.worker.tasks.*": {"queue": "default"},
}