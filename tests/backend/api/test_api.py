def test_ingest_endpoint(client, session):
    response = client.post("/ingest?user_id=1")
    assert response.status_code == 200
    data = response.json()
    assert "images" in data
    assert len(data["images"]) == 3


def test_ingest_with_invalid_user_id(client):
    response = client.post("/ingest?user_id=9999")
    assert response.status_code == 200  # still 200, just no user validation yet
    data = response.json()
    assert "images" in data
    assert len(data["images"]) == 3  # still works since we don’t check user existence

