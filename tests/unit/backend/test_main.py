import pytest
from httpx import ASGITransport, AsyncClient

from backend.main import create_app
from tests.utils.lifespan import LifespanManager


@pytest.mark.asyncio
async def test_create_app_root_reports_status() -> None:
    app = create_app()

    async with LifespanManager(app):
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            response = await client.get("/")

    assert response.status_code == 200
    assert response.json()["status"] == "running"
