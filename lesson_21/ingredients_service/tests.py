from fastapi.testclient import TestClient
from ingredients_service.main import app

client = TestClient(app)


def test_get_ingredients():
    response = client.get("/ingredients")
    assert response.status_code == 200
    assert response.json() == {
        "flour": 1000,
        "milk": 500,
        "sugar": 100,
        "salt": 20,
        "eggs": 10,
    }
