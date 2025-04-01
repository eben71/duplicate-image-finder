from fastapi import FastAPI
from backend.api.routes import router
from backend.config.settings import settings
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Duplicate Image Finder")
app.include_router(tasks.router, prefix="/api")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or set your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"status": "running", "mode": settings.ingestion_mode}

