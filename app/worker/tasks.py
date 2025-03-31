from app.worker.celery import celery

@celery.task
def add(x, y):
    print(f"Adding {x} + {y}")
    return x + y
