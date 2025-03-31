from fastapi import FastAPI
from app.routes import tasks
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.include_router(tasks.router, prefix="/api")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or set your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
