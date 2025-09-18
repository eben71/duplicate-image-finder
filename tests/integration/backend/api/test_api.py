import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
@pytest.mark.integration
@pytest.mark.smoke
async def test_health(app_client: AsyncClient) -> None:
    r = await app_client.get("/api/health")
    assert r.status_code == 200
