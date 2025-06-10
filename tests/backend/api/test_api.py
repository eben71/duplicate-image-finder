BASE = "/api"


def test_ingest_endpoint(client):
    response = client.post(f"{BASE}/ingest?user_id=1")
    assert response.status_code == 200


def test_ingest_with_invalid_user_id(client):
    response = client.post(f"{BASE}/ingest?user_id=9999")
    assert response.status_code == 200
