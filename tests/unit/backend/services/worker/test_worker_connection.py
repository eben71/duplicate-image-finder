from backend.services.worker.celery_app import celery_app


def test_celery_app_configured() -> None:
    assert "backend.services.worker.tasks.*" in celery_app.conf.task_routes
    assert celery_app.conf.task_routes["backend.services.worker.tasks.*"]["queue"] == "default"
