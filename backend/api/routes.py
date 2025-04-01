from fastapi import APIRouter
from celery.result import AsyncResult
from backend.services.worker.celery import celery
from backend.services.worker.tasks import debug_task

router = APIRouter()

@router.get("/health")
def health():
    return {"status": "ok"}

@router.get("/debug-task")
def run_task(x: int = 1):
    task = debug_task.delay(x)
    return {"task_id": task.id}