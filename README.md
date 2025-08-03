# ✅ README.md

# Duplicate Image Finder Backend (FastAPI + Celery + Redis + Postgres)

This is a modular backend stack for a SaaS application that identifies duplicate or similar images using AI. It includes a FastAPI backend, background processing with Celery, and a per-user OAuth2 integration with Google Photos for secure, API-based image ingestion. The system is designed for scalability, user isolation, and efficient image analysis with CLIP, YOLO, and perceptual hashing. It supports containerized development with Docker, automated CI/CD, and a robust testing suite.

## 🔧 Tech Stack

- **FastAPI**: Backend API (`/api`-prefixed endpoints) and lightweight frontend
- **Celery + Redis**: Background processing for image embeddings
- **PostgreSQL**: Stores users, image metadata, embeddings
- **Docker + Docker Compose**: Containerized development and CI-ready environment
- **SQLModel + Alembic**: Declarative database models with migration support
- **GitHub Actions**: CI/CD with linting and migration checks
- **Dependabot**: Dependency updates with reviewer assignment
- **Pytest**: Unit and integration testing with coverage
- **Ruff, Black, Mypy**: Linting, formatting, and type checking

## 📋 Features

- **Image Ingestion**: Supports three modes (`SCRAPE`, `API`, `UPLOAD`) for importing images
- **Duplicate Detection**: Generates embeddings for images to identify duplicates
- **Scalable Architecture**: Uses Celery for asynchronous tasks and Redis for task queuing
- **CI/CD Integration**: Automated testing, linting, and dependency management via GitHub Actions
- **Frontend**: Basic HTML welcome page served by FastAPI

---

## 🚀 Quickstart

### Prerequisites

- **Docker** and **Docker Compose** for running services
- **Python 3.12** for local development (optional)
- **Make** for running commands (optional, can run Docker commands directly)

### 1. Clone the Repository

```bash
git clone <repo-url>
cd duplicate-image-finder-backend
```

### 2. Set Up Environment Variables

Copy the example environment file and update it with your configuration:

Key environment variables (see `.env.example`):

| Variable             | Description                                 | Example Value                                 |
| -------------------- | ------------------------------------------- | --------------------------------------------- |
| `DATABASE_URL`       | PostgreSQL connection string                | `postgresql://postgres:pass@db:5432/db`       |
| `CELERY_BROKER_URL`  | Redis URL for Celery broker                 | `redis://redis:6379/0`                        |
| `CELERY_BACKEND_URL` | Redis URL for Celery backend                | `redis://redis:6379/1`                        |
| `GOOGLE_PHOTOS_URL`  | URL for web scraping                        | `https://photos.google.com/`                  |
| `FASTAPI_ENDPOINT`   | FastAPI endpoint for scraped image metadata | `http://localhost:8000/api/v1/images/scraped` |

### 3. Build & Start Services

```bash
make up
```

This starts the following services:

- **Backend API**: http://localhost:8000/docs
- **Frontend UI**: http://localhost:3000
- **PostgreSQL**: Port `5432`
- **Redis**: Port `6379`
- **Celery Worker**: Background task processing

### 4. Initialize Database

Apply database migrations:

```bash
make migrate
```

---

## 🛠️ Makefile Commands

| Command                 | Description                                           |
| ----------------------- | ----------------------------------------------------- |
| `make build`            | Build all Docker images                               |
| `make up`               | Start all services (app, db, redis, worker, frontend) |
| `make down`             | Stop and remove containers and volumes                |
| `make restart`          | Rebuild and restart everything                        |
| `make logs`             | Tail logs from all running containers                 |
| `make health`           | Ping the FastAPI `/health` endpoint                   |
| `make reset-db`         | Drop and reinit DB, removing migrations               |
| `make alembic`          | Create new Alembic migration (use `m="msg"`)          |
| `make migrate`          | Apply latest Alembic migrations                       |
| `make shell`            | Open bash shell in the app container                  |
| `make celery`           | Start Celery worker in the worker container           |
| `make tests`            | Run tests with coverage inside app container          |
| `make format`           | Format code with Ruff and Black (requires venv)       |
| `make ci`               | Run linting and type checking (requires venv)         |
| `make install-deps`     | Install production dependencies (requires venv)       |
| `make install-dev-deps` | Install development dependencies (requires venv)      |
| `make repomix`          | Generate a flattened repo summary                     |

---

## 🧪 Testing

Run tests inside the Docker container:

```bash
make tests
```

This executes `pytest` with coverage in the `app` container. Tests are located in the `tests/` directory, covering:

- **API endpoints** (`tests/backend/api/`)
- **Models** (`tests/backend/models/`)
- **Services** (`tests/backend/services/`)
- **Web scraper** (`tests/backend/backend_scraper/`)

Dependencies: `pytest`, `pytest-asyncio`, `pytest-cov`.

---

## 📁 Folder Structure

```
.
├── backend/
├── core/                     # Shared logic (logging, constants, utils)
│   ├── alembic/              # DB migrations
│   ├── alembic.ini
│   ├── api/                  # API routes
│   ├── config/               # Pydantic settings
│   ├── db/                   # Session + engine
│   ├── models/               # SQLModel ORM (User, Image, Embedding)
│   ├── services/             # Business logic and Celery
│   └── main.py               # FastAPI entrypoint
├── frontend/                 # Uvicorn-hosted welcome page
├── tests/                    # Pytest suite
├── .github/                  # CI workflows, dependabot, reviewers
├── docker-compose.yml
├── Dockerfile
├── Dockerfile.frontend
├── Makefile
├── requirements.txt
├── requirements-dev.txt
└── README.md
```

### Database Models:

- `User`: Registered users with email, name, and ingestion mode
- `Image`: Image metadata (file name, path, upload time)
- `ImageEmbedding`: Image embeddings for duplicate detection
- `IngestionMode`: Enum (`SCRAPE`, `API`, `UPLOAD`)

---

## ⚙️ CI/CD

The project uses GitHub Actions for continuous integration, defined in `.github/workflows/`:

- **CI Pipeline** (`ci.yaml`): Runs linting, testing, and Alembic migration checks on push/pull requests to `main`.
- **Dependabot** (`assign-reviewers.yml`): Automatically assigns reviewers to Dependabot PRs for dependency updates.

Dependencies are updated weekly via Dependabot, configured in `.github/dependabot.yml`.

---

## 🧠 Lessons Learned

### Alembic + SQLModel:

- Set `target_metadata = SQLModel.metadata` in `backend/alembic/env.py`
- Use absolute imports (e.g., `from backend.models import User`)
- Run Alembic commands from `/app` in Docker: `alembic -c /app/backend/alembic.ini ...`
- Ensure database is upgraded before generating new migrations
- Keep `/backend/alembic/versions/` writable and include a `.gitkeep` file

### Development Environment:

- Set `PYTHONPATH=/app` to avoid `ModuleNotFoundError`
- Import `Optional` from `typing` to avoid `NameError`
- Create a virtual environment for local development:
  ```bash
  python3 -m venv .venv
  source .venv/bin/activate
  pip install -r requirements-dev.txt
  ```

---

## 🧼 Extras

- **Dependencies**: Production dependencies in `requirements.txt`; development tools (ruff, black, mypy) in `requirements-dev.txt`
- **Database IP**: Find the database IP with:
  ```bash
  docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' duplicate-image-finder-db-1
  ```
- **New Models**: Add SQLModel models in `backend/models/`
- **New Tasks**: Add Celery tasks in `backend/services/worker/tasks.py`

---

## ❤️ Contributions

Contributions are welcome! Submit issues or PRs to enhance the boilerplate. Follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/xyz`)
3. Commit changes (`git commit -m "Add xyz"`)
4. Push to the branch (`git push origin feature/xyz`)
5. Open a pull request

---

## 📜 License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

---

## 📬 Contact

For questions, check the [GitHub Issues](https://github.com/<owner/repo>/issues) page or file an issue.
