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

| Command           | Description                      |
|------------------|----------------------------------|
| `make up`        | Start all services               |
| `make down`      | Stop and remove containers       |
| `make restart`   | Rebuild and restart everything   |
| `make logs`      | Tail logs                        |
| `make web`       | Bash into FastAPI container      |
| `make worker`    | Bash into Celery worker          |
| `make test`      | Run pytest inside web container  |
| `make health`    | Hit the /health endpoint         |

---

## 🧪 Testing

Add test files under `tests/` and run:
```bash
make test
```

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
