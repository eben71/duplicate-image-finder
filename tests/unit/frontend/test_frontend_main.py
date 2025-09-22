import pytest
from httpx import ASGITransport, AsyncClient

from frontend.main import app as frontend_app


@pytest.mark.asyncio
async def test_frontend_welcome_page() -> None:
    transport = ASGITransport(app=frontend_app)

    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/")

    assert response.status_code == 200
    assert "Duplicate Image Finder" in response.text
