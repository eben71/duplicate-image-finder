from collections.abc import Generator

from sqlalchemy.orm import sessionmaker
from sqlmodel import Session, create_engine

from backend.config.settings import settings

engine = create_engine(settings.DATABASE_URL, echo=True)

SessionLocal = sessionmaker(bind=engine, class_=Session, expire_on_commit=False)


def get_session() -> Generator[Session, None, None]:
    with SessionLocal() as session:
        yield session
