import pytest
import tempfile
from fastapi.testclient import TestClient
from sqlmodel import SQLModel, Session, create_engine

from backend.main import app
from backend.db.session import get_session

# 🧩 Import all models to ensure they're registered
import backend.models.user
import backend.models.image
import backend.models.embedding

# make imports for data fixtures "used"
_ = (backend.models.user, backend.models.image, backend.models.embedding)

# 🔧 Create a temporary SQLite file-based DB (works with async apps like FastAPI)
tmp_db = tempfile.NamedTemporaryFile(suffix=".db")
DATABASE_URL = f"sqlite:///{tmp_db.name}"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})


# 🧪 Provide a clean DB session per test
@pytest.fixture(name="session")
def session_fixture():
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session
    SQLModel.metadata.drop_all(engine)


# ⚙️ Provide FastAPI test client with overridden DB session
@pytest.fixture(name="client")
def client_fixture(session: Session):
    def override_get_session():
        return session

    app.dependency_overrides[get_session] = override_get_session
    return TestClient(app)
