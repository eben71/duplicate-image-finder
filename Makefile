# Makefile for Dev Workflow
# - Docker tasks manage containers and the app.
# - Local tasks (lint/format/typecheck) *optionally* use a venv if it exists.
# - CI doesn't create .venv; commands run from PATH (installed by the workflow).

# ---------- Config ----------
VENV_DIR ?= .venv
FRONTEND_DIR ?= frontend
NPM ?= npm
# Activate venv only if it exists (safe no-op in CI)
ACTIVATE := if [ -f "$(VENV_DIR)/bin/activate" ]; then . "$(VENV_DIR)/bin/activate"; fi
PYTHON := python3.12
PY ?= python3
PIP := $(PYTHON) -m pip
COV = $(PY) -m coverage

.PHONY: build up down restart logs health \
        reset-db init-db alembic migrate shell celery \
    tests-unit tests-int tests-debug tests-smoke tests-all tests tests-coverage tests-dedupe \
    install-deps install-dev-deps check-versions \
    format lint typecheck ci update-python repomix \
    frontend-install frontend-dev frontend-test frontend-storybook frontend-coverage

# ---------- Docker: App Lifecycle ----------
build:
	docker compose build

up:
	docker compose up --build -d

down:
	docker compose down

restart: down up

logs:
	docker compose logs -f

health:
	# Update if your health path differs
	curl -f http://localhost:8000/health || echo "Health check failed"

# ---------- Docker: Database ----------
reset-db:
	docker compose down -v
	rm -f backend/alembic/versions/*.py || true
	docker compose up -d postgres
	docker compose exec -T postgres psql -U postgres -d postgres -c "CREATE DATABASE app;" || true
	docker compose exec -T app python -c "from sqlmodel import SQLModel; from backend.db import engine; SQLModel.metadata.create_all(engine)"

init-db:
	docker compose exec -T app alembic -c /app/backend/alembic.ini upgrade head

# usage: make alembic m="add new table"
alembic:
	docker compose exec -T app alembic -c /app/backend/alembic.ini revision --autogenerate -m "$(m)"

migrate:
	docker compose exec -T app alembic -c /app/backend/alembic.ini upgrade head

# ---------- Docker: Dev helpers ----------
shell:
	docker compose exec -T app bash

celery:
	docker compose exec -T worker celery -A backend.services.worker.celery_app worker --loglevel=info

# ---------- Tests ----------
# Fast unit tests (no docker). Pytest default markers from pytest.ini apply.
tests-unit:
        $(ACTIVATE); pytest -m "not integration and not e2e and not debug"

tests-dedupe:
        $(ACTIVATE); pytest tests/unit/test_pdq_filter.py tests/unit/test_siglip2_encoder.py tests/unit/test_pgvector_store.py

# Integration tests via your existing compose recipe
tests-int:
	docker compose up -d db
	docker compose exec -T db sh -c "while ! pg_isready -U postgres -d duplicatefinder; do sleep 1; done"
	docker compose run --rm app pytest tests --cov=backend --cov=frontend --disable-warnings
	docker compose stop db

# Debug-only tests (override default filter)
tests-debug:
	$(ACTIVATE); pytest -m debug -s -vv

# Smoke-only tests (override default filter)
tests-smoke:
	$(ACTIVATE); pytest -m smoke -s -vv

# Run the full suite (unit + integration)
tests-all:
	$(MAKE) tests-unit
	$(MAKE) tests-int

# Coverage across backend/core/frontend modules
tests-unit-cov:
	# Write raw DB as .coverage.unit and an XML for inspection
	COVERAGE_FILE=.coverage.unit $(COV) erase
	COVERAGE_FILE=.coverage.unit pytest -q \
		--cov=backend --cov=core \
		--cov-report=xml:coverage.unit.xml

tests-int-cov:
	docker compose up -d db
	docker compose exec -T db sh -c 'while ! pg_isready -U postgres -d duplicatefinder; do sleep 1; done'
	# Ensure the app container has pytest-cov + coverage installed and the repo is mounted at /app
	docker compose run --rm \
		-e COVERAGE_FILE=.coverage.integration \
		app pytest -m integration --disable-warnings \
			--cov=backend --cov=core \
			--cov-report=xml:coverage.integration.xml
	docker compose stop db

tests-coverage-merge:
	# Combine RAW DBs, then produce total XML + console report
	$(COV) erase
	$(COV) combine .coverage.unit .coverage.integration
	$(COV) xml -o coverage.total.xml
	$(COV) report -m
	$(MAKE) frontend-coverage

# ---------- Local deps (optional venv) ----------
install-deps:
	$(PYTHON) -m venv $(VENV_DIR)
	$(ACTIVATE); $(PIP) install --upgrade pip
	$(ACTIVATE); $(PIP) install -r requirements.txt

install-dev-deps:
	$(PYTHON) -m venv $(VENV_DIR)
	$(ACTIVATE); $(PIP) install --upgrade pip
	$(ACTIVATE); $(PIP) install -r requirements-dev.txt

check-versions:
	@echo "Local (venv if present):"
	@$(ACTIVATE); $(PIP) list || true
	@echo "\nDocker app container:"
	@docker compose exec -T app pip list || true

# ---------- Lint / Format / Typecheck ----------
format:
	$(ACTIVATE); ruff format .
	$(ACTIVATE); black .

lint:
	$(ACTIVATE); ruff check . --output-format=github

typecheck:
	$(ACTIVATE); mypy .

# ---------- CI bundle (called by GitHub Actions) ----------
ci:
	$(ACTIVATE); ruff check . --output-format=github
	$(ACTIVATE); ruff format --check .
	$(ACTIVATE); black --check .
	$(ACTIVATE); mypy .
# --	coverage run -m pytest -q
# --	coverage xml
# --	coverage report

# ---------- Misc ----------
update-python:
	@echo "Updating Homebrew and Python to 3.12..."
	@brew update
	@brew install python@3.12 || brew upgrade python@3.12
	@echo "Recreating virtual environment..."
	@rm -rf $(VENV_DIR)
	@$(PYTHON) -m venv $(VENV_DIR)

repomix:
	npx repomix

# ---------- Frontend (Next.js) ----------
.PHONY: frontend-install frontend-dev frontend-test frontend-storybook frontend-coverage

frontend-install:
	cd $(FRONTEND_DIR) && $(NPM) install

frontend-dev:
	cd $(FRONTEND_DIR) && $(NPM) run dev

frontend-test:
	cd $(FRONTEND_DIR) && $(NPM) run test

frontend-storybook:
	cd $(FRONTEND_DIR) && $(NPM) run storybook

frontend-coverage:
	cd $(FRONTEND_DIR) && $(NPM) run test:coverage
	cp -f coverage/frontend/coverage-summary.json coverage.frontend.vitest-summary.json
