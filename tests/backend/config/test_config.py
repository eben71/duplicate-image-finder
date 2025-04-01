import pytest
import os
from fastapi.testclient import TestClient
from sqlmodel import SQLModel, create_engine, Session
from backend.main import app
from backend.db.session import get_session

# Create a test database
TEST_DB = "sqlite:///./test.db"
engine = create_engine(TEST_DB, connect_args={"check_same_thread": False})

@pytest.fixture(name="session")
def session_fixture():
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session
    SQLModel.metadata.drop_all(engine)
    if os.path.exists("./test.db"):
        os.remove("./test.db")

@pytest.fixture(name="client")
def client_fixture(session: Session):
    def get_override():
        yield session
    app.dependency_overrides[get_session] = get_override
    return TestClient(app)
    