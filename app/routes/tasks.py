from fastapi import APIRouter
from app.worker.tasks import add
from celery.result import AsyncResult
from app.worker.celery import celery

router = APIRouter()

@router.get("/health")
def health():
    return {"status": "ok"}

@router.post("/add")
def run_add(x: int, y: int):
    task = add.delay(x, y)
    return {"task_id": task.id}

@router.get("/status/{task_id}")
def get_status(task_id: str):
    result = AsyncResult(task_id, app=celery)
    return {
        "task_id": task_id,
        "status": result.status,
        "result": result.result
    }
