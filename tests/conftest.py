import tempfile
from collections.abc import AsyncGenerator, Generator

import pytest
from httpx import ASGITransport, AsyncClient
from sqlmodel import Session, SQLModel, create_engine

import backend.models.embedding
import backend.models.image

# 🧩 Import all models to ensure they're registered
import backend.models.user
from backend.db.session import get_session
from backend.main import app

# make imports for data fixtures "used"
_ = (backend.models.user, backend.models.image, backend.models.embedding)

# 🔧 Create a temporary SQLite file-based DB (works with async apps like FastAPI)
tmp_db = tempfile.NamedTemporaryFile(suffix=".db")
DATABASE_URL = f"sqlite:///{tmp_db.name}"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})


# 🧪 Provide a clean DB session per test
@pytest.fixture(name="session")
def session_fixture() -> Generator[Session, None, None]:
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session
    SQLModel.metadata.drop_all(engine)


@pytest.fixture(name="client")
async def client_fixture(session: Session) -> AsyncGenerator[AsyncClient, None]:
    def override_get_session() -> Session:
        return session

    app.dependency_overrides[get_session] = override_get_session
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        yield client
    app.dependency_overrides.clear()
