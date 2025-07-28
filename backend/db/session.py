from sqlmodel import create_engine, Session
from backend.config.settings import settings
from typing import Generator

engine = create_engine(settings.DATABASE_URL, echo=True)


def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session
