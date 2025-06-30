from fastapi import FastAPI
from backend.api.routes import router
from backend.config.settings import settings
from fastapi.middleware.cors import CORSMiddleware
from core.logging_config import configure_logging
from core.version_check import check_playwright_version

app = FastAPI(title="Duplicate Image Finder")
app.include_router(router, prefix="/api")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Allow frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

configure_logging()
check_playwright_version()


@app.get("/")
def read_root():
    return {"status": "running", "mode": settings.INGESTION_MODE}
