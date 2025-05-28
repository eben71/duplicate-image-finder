# Makefile for Dev Workflow
# - Docker tasks manage containers and the app (no virtual environment needed).
# - Local tasks (linting, formatting) require a virtual environment (`source .venv/bin/activate`).
# - Run `make <task>` to execute.
# - SDLC phases: Development (coding, prototyping), Testing (unit/integration tests), Deployment (CI/CD, production), Maintenance (updates, debugging).

.PHONY: build up down restart logs health shell test reset-db init-db alembic migrate celery install-deps install-dev-deps check-versions format ci

# --- Docker: App Lifecycle ---
# Build Docker images
# SDLC: Development (initial setup), Testing (before tests), Deployment (CI/CD pipeline)
build:
	docker-compose build

# Start containers (builds images first)
# SDLC: Development (run app locally), Testing (test environment), Deployment (local staging)
up:
	docker-compose up --build -d

# Stop and remove containers and volumes
# SDLC: Development (cleanup), Testing (reset environment), Maintenance (stop services)
down:
	docker-compose down -v

# Restart containers (stop, then start)
# SDLC: Development (apply changes), Testing (reset for tests), Maintenance (restart services)
restart: down up

# View container logs
# SDLC: Development (debugging), Testing (check test failures), Maintenance (monitor issues)
logs:
	docker-compose logs -f

# Check app health (requires app running at localhost:8000)
# SDLC: Testing (verify app), Deployment (post-deployment check), Maintenance (monitor health)
health:
	curl -f http://localhost:8000/health || echo "Health check failed"

# --- Docker: Database Management ---
# Reset database: Stop containers, remove migrations, recreate tables
# SDLC: Development (reset DB for new schema), Testing (clean DB for tests)
reset-db:
	docker-compose down -v
	rm -f backend/alembic/versions/*.py
	docker-compose up -d postgres
	docker-compose exec -T postgres psql -U postgres -d postgres -c "CREATE DATABASE app;"
	docker-compose exec app python -c "from sqlmodel import SQLModel; from backend.db import engine; SQLModel.metadata.create_all(engine)"

# Initialize database (run migrations)
# SDLC: Development (apply initial schema), Deployment (setup production DB)
init-db:
	docker-compose exec app alembic -c /app/backend/alembic.ini upgrade head

# Generate new Alembic migration (usage: make alembic m="migration_name")
# SDLC: Development (after schema changes)
alembic:
	docker-compose exec app alembic -c /app/backend/alembic.ini revision --autogenerate -m "$(m)"

# Apply migrations
# SDLC: Development (apply schema updates), Deployment (update production DB)
migrate:
	docker-compose exec app alembic -c /app/backend/alembic.ini upgrade head

# --- Docker: Development ---
# Open a shell in the app container
# SDLC: Development (debugging, manual checks), Maintenance (troubleshooting)
shell:
	docker-compose exec app bash

# Run Celery worker
# SDLC: Development (test background tasks), Testing (task integration), Deployment (run workers)
celery:
	docker-compose exec worker celery -A backend.services.worker.celery_app worker --loglevel=info

# Run tests in container with coverage
# SDLC: Development (verify code), Testing (unit/integration tests), Deployment (CI pipeline)
test:
	docker-compose run --rm app pytest tests --cov=backend --disable-warnings

# --- Local: Dependency Management (requires virtual environment) ---
# Install production dependencies locally (in virtual environment)
# SDLC: Development (setup local env), Testing (local testing outside Docker)
install-deps:
	python -m venv .venv
	. .venv/bin/activate && pip install -r requirements.txt

# Install development dependencies locally (in virtual environment)
# SDLC: Development (setup linting/formatting tools), Testing (pre-CI checks)
install-dev-deps:
	python -m venv .venv
	. .venv/bin/activate && pip install -r requirements-dev.txt

# Check package versions in local virtual environment and Docker
# SDLC: Development (debug version mismatches), Testing (ensure consistency), Maintenance (verify environments)
check-versions:
	@echo "Local versions (virtual environment):"
	@. .venv/bin/activate && pip list
	@echo "\nDocker versions (app container):"
	@docker-compose exec app pip list

# --- Local: Linting and Formatting (requires virtual environment) ---
# Format code with ruff and black
# SDLC: Development (before committing code), Testing (pre-CI formatting)
format:
	. .venv/bin/activate && ruff format .
	. .venv/bin/activate && black .

# Run linting and type checking (CI simulation)
# SDLC: Development (code quality checks), Testing (pre-CI validation), Deployment (CI pipeline)
ci:
	. .venv/bin/activate && ruff check .
	. .venv/bin/activate && ruff format --check .
	. .venv/bin/activate && black --check .
	. .venv/bin/activate && mypy .