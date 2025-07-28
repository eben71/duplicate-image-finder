from fastapi import FastAPI
from backend.api.routes import api_router
from backend.config.settings import settings
from fastapi.middleware.cors import CORSMiddleware
from core.logging_config import configure_logging
from typing import Any

app = FastAPI(title="Duplicate Image Finder")
app.include_router(api_router, prefix="/api")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Allow frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

configure_logging()


@app.get("/", response_model=dict[str, Any])
def read_root() -> dict[str, Any]:
    return {"status": "running", "mode": settings.INGESTION_MODE}
