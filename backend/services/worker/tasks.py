from backend.services.worker.celery import celery

@celery.task
def debug_task(x):
    print(f"Processing debug task with arg: {x}")
    return x * 2   
