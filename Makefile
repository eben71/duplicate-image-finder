# ✅ Makefile for Dev Workflow

.PHONY: build up down restart logs alembic migrate shell celery test

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

alembic:
	alembic -c backend/alembic.ini revision --autogenerate -m "$(m)"

migrate:
	alembic -c backend/alembic.ini upgrade head

shell:
	docker-compose exec app bash

celery:
	docker-compose exec worker celery -A backend.services.worker.celery worker --loglevel=info

test:
	docker-compose run --rm app pytest tests --cov=backend --disable-warnings

