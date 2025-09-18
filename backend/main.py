# backend/main.py
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from typing import Any

import httpx
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.api.routes import api_router
from backend.config.settings import settings
from core.logging_config import configure_logging


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    async with httpx.AsyncClient(timeout=10.0) as client:
        app.state.http = client  # type: ignore[attr-defined]
        yield


def create_app() -> FastAPI:
    configure_logging()

    app = FastAPI(title="Duplicate Image Finder", lifespan=lifespan)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:3000"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(api_router, prefix="/api")

    @app.get("/", response_model=dict[str, Any])
    def read_root() -> dict[str, Any]:
        return {"status": "running", "mode": settings.INGESTION_MODE}

    return app


# for `uvicorn backend.main:app --reload`
app = create_app()
