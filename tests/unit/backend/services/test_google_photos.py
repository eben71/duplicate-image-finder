from datetime import datetime
from unittest.mock import AsyncMock, Mock, patch

import pytest
from sqlmodel import Session

from backend.services.ingestion.google_photos import fetch_images_by_year
from tests.utils.factories import make_test_user


def _response(payload: dict) -> Mock:
    stub = Mock()
    stub.json = Mock(return_value=payload)
    stub.raise_for_status = Mock()
    return stub


@pytest.mark.asyncio
async def test_fetch_images_by_year_collects_only_images(session: Session) -> None:
    user = make_test_user(with_tokens=True)
    session.add(user)
    session.commit()
    session.refresh(user)

    client = AsyncMock()
    client.post = AsyncMock(
        side_effect=
        [
            _response(
                {
                    "mediaItems": [
                        {
                            "id": "img-1",
                            "filename": "one.jpg",
                            "mimeType": "image/jpeg",
                            "baseUrl": "https://example.com/one",
                        }
                    ],
                    "nextPageToken": "page-2",
                }
            ),
            _response(
                {
                    "mediaItems": [
                        {
                            "id": "vid-2",
                            "filename": "two.mp4",
                            "mimeType": "video/mp4",
                        },
                        {
                            "id": "img-3",
                            "filename": "three.png",
                            "mimeType": "image/png",
                            "baseUrl": "https://example.com/three",
                        },
                    ],
                    "nextPageToken": "unused-token",
                }
            ),
        ]
    )

    with patch(
        "backend.services.ingestion.google_photos.get_fresh_access_token",
        new=AsyncMock(return_value="token"),
    ) as token_mock:
        images = await fetch_images_by_year(
            user,
            session,
            client,
            year=2024,
            start_page=1,
            end_page=2,
        )

    assert len(images) == 2
    assert {img["id"] for img in images} == {"img-1", "img-3"}
    token_mock.assert_awaited_once_with(user, session, client)
    assert client.post.await_count == 2


@pytest.mark.asyncio
async def test_fetch_images_by_year_defaults_year_and_stops_at_end(session: Session) -> None:
    user = make_test_user(with_tokens=True)
    session.add(user)
    session.commit()
    session.refresh(user)

    client = AsyncMock()
    client.post = AsyncMock(
        side_effect=
        [
            _response({"mediaItems": [], "nextPageToken": "page-2"}),
            _response({"mediaItems": [], "nextPageToken": "page-3"}),
            _response({"mediaItems": []}),
        ]
    )

    with patch(
        "backend.services.ingestion.google_photos.get_fresh_access_token",
        new=AsyncMock(return_value="token"),
    ):
        images = await fetch_images_by_year(
            user,
            session,
            client,
            year=None,
            start_page=2,
            end_page=2,
        )

    assert images == []
    # Ensure we broke out when current_page exceeded end_page (third call never made)
    assert client.post.await_count == 1

    first_call = client.post.await_args_list[0]
    payload = first_call.kwargs["json"]
    current_year = datetime.now().year
    year_filter = payload["filters"]["dateFilter"]["ranges"][0]["startDate"]["year"]
    assert year_filter == current_year
    assert "pageToken" not in payload

    payload = client.post.await_args_list[0].kwargs["json"]
    assert "pageToken" not in payload
