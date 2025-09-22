from unittest.mock import AsyncMock, patch

import pytest
from httpx import AsyncClient
from sqlmodel import Session

from backend.models.enums import IngestionMode
from tests.utils.factories import make_test_user


@pytest.mark.asyncio
async def test_ingest_endpoint_with_valid_user(app_client: AsyncClient, session: Session) -> None:
    # Arrange: create a user the route can find
    u = make_test_user()
    session.add(u)
    session.commit()
    session.refresh(u)

    # Act
    resp = await app_client.post("/api/ingest", params={"user_id": u.id})

    # Assert
    assert resp.status_code == 200


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "mode,expected",
    [
        (IngestionMode.SCRAPE, "scraped images"),
        (IngestionMode.API, "fetched via API"),
        (IngestionMode.UPLOAD, "uploaded manually"),
    ],
)
async def test_ingest_endpoint_mode_branches(
    app_client: AsyncClient, session: Session, mode: IngestionMode, expected: str
) -> None:
    user = make_test_user()
    session.add(user)
    session.commit()
    session.refresh(user)

    resp = await app_client.post("/api/ingest", params={"user_id": user.id, "mode": mode.value})

    assert resp.status_code == 200
    assert resp.json() == {"status": expected}


@pytest.mark.asyncio
async def test_ingest_with_invalid_user_id(app_client: AsyncClient) -> None:
    resp = await app_client.post("/api/ingest", params={"user_id": -1})
    assert resp.status_code == 400


@pytest.mark.asyncio
async def test_ingest_with_not_found_user_id(app_client: AsyncClient) -> None:
    resp = await app_client.post("/api/ingest", params={"user_id": 9999999})
    assert resp.status_code == 404


@pytest.mark.asyncio
@patch("backend.api.routes.fetch_images_by_year", new_callable=AsyncMock)
async def test_ingest_dev_happy_path(
    mock_fetch: AsyncMock, app_client: AsyncClient, session: Session
) -> None:
    user = make_test_user()
    session.add(user)
    session.commit()
    session.refresh(user)

    mock_fetch.return_value = [
        {"id": "1", "filename": "one.jpg"},
        {"id": "2", "filename": "two.jpg"},
        {"id": "3", "filename": "three.jpg"},
        {"id": "4", "filename": "four.jpg"},
    ]

    response = await app_client.get("/api/ingest/dev", params={"user_id": user.id})

    assert response.status_code == 200
    payload = response.json()
    assert payload["total_images"] == 4
    assert len(payload["sample"]) == 3
    mock_fetch.assert_awaited_once()


@pytest.mark.asyncio
async def test_ingest_dev_user_not_found(app_client: AsyncClient) -> None:
    response = await app_client.get("/api/ingest/dev", params={"user_id": 9999})

    assert response.status_code == 404
    assert response.json() == {"detail": "User not found"}
