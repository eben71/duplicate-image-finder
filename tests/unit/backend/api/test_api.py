import pytest
from httpx import AsyncClient
from sqlmodel import Session

from tests.utils.factories import make_test_user


@pytest.mark.asyncio
async def test_ingest_endpoint_with_valid_user(client: AsyncClient, session: Session) -> None:
    # Arrange: create a user the route can find
    u = make_test_user()
    session.add(u)
    session.commit()
    session.refresh(u)

    # Act
    resp = await client.post("/api/ingest", params={"user_id": u.id})

    # Assert
    assert resp.status_code == 200


@pytest.mark.asyncio
async def test_ingest_with_invalid_user_id(client: AsyncClient) -> None:
    resp = await client.post("/api/ingest", params={"user_id": -1})
    assert resp.status_code == 400


@pytest.mark.asyncio
async def test_ingest_with_not_found_user_id(client: AsyncClient) -> None:
    resp = await client.post("/api/ingest", params={"user_id": 9999999})
    assert resp.status_code == 404
