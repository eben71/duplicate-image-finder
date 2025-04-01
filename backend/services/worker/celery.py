from celery import Celery
from backend.config.settings import settings

celery = Celery(
    "duplicate_finder",
    broker=settings.celery_broker_url,
    backend="settings.celery_backend_url
)

celery.conf.task_routes = {
    "backend.worker.tasks.*": {"queue": "default"},
}