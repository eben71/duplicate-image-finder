# ------------------------------------------------------------------------------------------------
# ✅ README.md

# Duplicate Image Finder Backend (FastAPI + Celery + Redis + Postgres)

This is a boilerplate backend stack for building a scalable image processing app.

## 🔧 Tech Stack
- FastAPI (web API)
- Celery (background task queue)
- Redis (broker & result backend)
- PostgreSQL (data persistence)
- Docker Compose (container orchestration)

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
project-root/
├── backend/          # FastAPI app and Celery tasks
├── tests/            # Test cases (pytest)
├── Dockerfile
├── docker-compose.yml
├── Makefile
├── README.md
```

---

## 🧼 Extras
- Update `.env` file for custom config
- Create DB models in `backend/models`
- Add new tasks in `backend/worker/tasks.py`

---

## ❤️ Contributions Welcome
Feel free to submit issues or PRs if you're building on top of this boilerplate!

---

## License
MIT
