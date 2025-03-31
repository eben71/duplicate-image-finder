from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_add_task():
    response = client.post("/add", json={"x": 1, "y": 2})
    assert response.status_code == 200
    assert "task_id" in response.json()
