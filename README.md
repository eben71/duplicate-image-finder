# ✅ README.md

# Duplicate Image Finder Backend (FastAPI + Celery + Redis + Postgres)

This is a boilerplate backend stack for building a scalable image processing app.

## 🔧 Tech Stack
- **FastAPI**: Backend API (`/api`-prefixed endpoints)
- **Celery + Redis**: Background processing for image embeddings
- **PostgreSQL**: Stores users, image metadata, embeddings
- **Docker + Makefile**: Development and CI-ready environment
- **SQLModel + Alembic**: Declarative models with migration support

---

## 🚀 Quickstart

### 1. Clone the Repo
```bash
git clone <repo-url>
cd duplicate-image-finder-backend
```

### 2. Build & Start Services
```bash
make up
```

Access FastAPI docs: [http://localhost:8000/docs](http://localhost:8000/docs)

---

## 🛠️ Common Commands

| Command           | Description                                      |
|------------------|--------------------------------------------------|
| `make build`     | Build all Docker images                         |
| `make up`        | Start all services (app, db, redis, worker)     |
| `make down`      | Stop and remove containers and volumes          |
| `make restart`   | Rebuild and restart everything                  |
| `make logs`      | Tail logs from all running containers           |
| `make health`    | Ping the FastAPI `/health` endpoint             |
| `make alembic`   | Create new Alembic migration (use `m="msg"`)   |
| `make migrate`   | Apply latest Alembic migrations                 |
| `make shell`     | Open bash shell in the app container            |
| `make celery`    | Start Celery worker in the worker container     |
| `make test`      | Run tests with coverage inside app container    |

---

## 🧪 Testing

Run your tests inside the container:

```bash
make test
```

This runs `pytest` with coverage inside the `app` container.
Make sure all test files are located in the `tests/` folder.

---

## 🔍 Health Check
Ensure the app is up:
```bash
curl http://localhost:8000/health
```

---

## 📦 Folder Structure

```
.
├── backend/
│   ├── api/                  # Routes
│   ├── models/               # SQLModel models
│   ├── services/             # Business logic
│   ├── config/               # Enums and constants
│   ├── alembic.ini
│   ├── alembic/              # DB migrations
│   │   ├── versions/
│   │   └── env.py
├── docker-compose.yml
├── Makefile
├── SETUP.md
├── README.md
```
---

### Database Models:
- `User`: Represents registered users.
- `Image`: Stores user image metadata and file paths.
- `IngestionMode`: Enum with `SCRAPE`, `API`, and `UPLOAD`.

---

## 🧠 Lessons Learned

### Alembic + SQLModel:
- Define `target_metadata = SQLModel.metadata` in `env.py`
- Use absolute imports (e.g., `from backend.models import User`)
- Alembic fails if database isn't upgraded before generating new revisions

### File Structure Best Practices:
- Place `alembic.ini` under `backend/`
- Run Alembic commands from `/app` in Docker using:  
  `alembic -c /app/backend/alembic.ini ...`
- Ensure `/backend/alembic/versions/` exists and is writable

### Common Errors Avoided:
- `NameError: Optional not defined`: Ensure `from typing import Optional`
- `ModuleNotFoundError: No module named 'backend'`: Set `PYTHONPATH=/app`
- Git ignores empty dirs — add a `.gitkeep` or dummy file to `versions/`

---

## 🧼 Extras
- Update `.env` file for custom config
   (To get the localhost IP address for DB: docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' duplicate-image-finder-db-1
)
- Create DB models in `backend/models`
- Add new tasks in `backend/worker/tasks.py`

---

## ❤️ Contributions Welcome
Feel free to submit issues or PRs if you're building on top of this boilerplate!

---

## License
MIT
