from collections.abc import Generator

from sqlalchemy.orm import sessionmaker
from sqlmodel import Session, create_engine

from backend.config.settings import settings

engine = create_engine(settings.DATABASE_URL, echo=True)

# Provide a session factory for services that prefer explicit sessionmaker usage.
SessionLocal = sessionmaker(bind=engine, class_=Session, expire_on_commit=False)


def get_session() -> Generator[Session, None, None]:
    """Yield a SQLModel Session bound to the configured engine.

    Using ``Session`` directly keeps compatibility with tests that monkeypatch the
    Session class and ensures the context manager semantics remain identical to
    the pre-refactor behavior.
    """

    with Session(engine) as session:
        yield session
