import pytest
from httpx import AsyncClient

BASE = "/api"


@pytest.mark.unit
async def test_ingest_endpoint(client: AsyncClient) -> None:
    response = await client.post(f"{BASE}/ingest?user_id=1")
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_ingest_with_invalid_user_id(client: AsyncClient) -> None:
    response = await client.post(f"{BASE}/ingest?user_id=9999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Not Found"}
