from celery import Celery

from backend.config.settings import settings

celery_app = Celery(
    "duplicate_finder",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_BACKEND_URL,
)

celery_app.conf.task_routes = {
    "backend.services.worker.tasks.*": {"queue": "default"},
}
