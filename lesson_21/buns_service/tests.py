from fastapi.testclient import TestClient
import pytest
from buns_service.main import app

client = TestClient(app)


@pytest.mark.asyncio
async def test_calculate_buns(monkeypatch):
    async def mock_get(*args, **kwargs):
        class Response:
            def json(self):
                return {
                    "flour": 1000,
                    "milk": 500,
                    "sugar": 100,
                    "salt": 20,
                    "eggs": 10,
                }

        return Response()

    monkeypatch.setattr("httpx.AsyncClient.get", mock_get)

    response = client.get("/buns")
    assert response.status_code == 200
    assert response.json() == {"buns": 5}


@pytest.mark.asyncio
async def test_calculate_buns_not_enough_ingredients(monkeypatch):
    async def mock_get(*args, **kwargs):
        class Response:
            def json(self):
                return {
                    "flour": 100,
                    "milk": 50,
                    "sugar": 10,
                    "salt": 2,
                    "eggs": 1,
                }

        return Response()

    monkeypatch.setattr("httpx.AsyncClient.get", mock_get)

    response = client.get("/buns")
    assert response.status_code == 200
    assert response.json() == {
        "error": "Not enough ingredients even for one bun. Please resupply!"
    }
