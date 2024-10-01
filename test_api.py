from fastapi.testclient import TestClient
from api import app

client = TestClient(app)


def test_get_ram_usage():
    response = client.get("/ram-usage?limit=5")
    assert response.status_code == 200
    data = response.json()

    assert isinstance(data, list)
    assert len(data) <= 5

    for item in data:
        assert "total" in item
        assert "used" in item
        assert "free" in item
        assert "timestamp" in item
