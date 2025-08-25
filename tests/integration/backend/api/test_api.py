import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
@pytest.mark.integration
@pytest.mark.smoke
async def test_health(client: AsyncClient) -> None:
    r = await client.get("/api/health")
    assert r.status_code == 200
