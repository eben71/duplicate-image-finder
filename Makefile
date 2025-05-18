# ✅ Makefile for Dev Workflow

.PHONY: build up down restart logs alembic migrate shell celery test reset-db init-db

build:
	docker-compose build

up:
	docker-compose up --build

down:
	docker-compose down -v

restart: down up

logs:
	docker-compose logs -f

health:
	curl -f http://localhost:8000/health

reset-db:
	docker-compose down -v
	rm -f backend/alembic/versions/*.py
	docker-compose up -d
	docker compose wait postgres
	docker-compose exec app python -c "from sqlmodel import SQLModel; from backend.db import engine; SQLModel.metadata.create_all(engine)"

alembic:
	docker-compose exec app alembic -c /app/backend/alembic.ini revision --autogenerate -m "$(m)"

migrate:
	docker-compose exec app alembic -c /app/backend/alembic.ini upgrade head

shell:
	docker-compose exec app bash

celery:
	docker-compose exec worker celery -A backend.services.worker.celery_app worker --loglevel=info

test:
	docker-compose run --rm app pytest tests --cov=backend --disable-warnings

