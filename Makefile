# ✅ Makefile for Dev Workflow

.PHONY: build up down restart logs web worker bash test

build:
	docker-compose build

up:
	docker-compose up --build

down:
	docker-compose down -v

restart: down up

logs:
	docker-compose logs -f

web:
	docker exec -it fastapi_app bash

worker:
	docker exec -it celery_worker bash

bash:
	docker exec -it fastapi_app bash

test:
	docker exec -it fastapi_app pytest

health:
	curl -f http://localhost:8000/health