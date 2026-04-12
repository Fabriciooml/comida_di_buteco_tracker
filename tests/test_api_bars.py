from unittest.mock import patch
from fastapi.testclient import TestClient
from api.main import app

client = TestClient(app)

_MOCK_BAR = {
    "id": 1,
    "name": "Bar Teste",
    "latitude": -19.9245,
    "longitude": -43.9352,
    "food_name": "Bolinho",
    "food_image_url": "https://img.example.com/bolinho.jpg",
    "food_description": "Crocante por fora, cremoso por dentro.",
    "food_category": "bolinhos",
    "is_vegan": 0,
    "is_vegetarian": 1,
    "address": "Rua A, 1 - Centro, Belo Horizonte - MG",
    "working_hours": "Seg–Sex 18h–23h",
}


def test_list_bars_returns_200():
    with patch("api.routers.bars.get_bars", return_value=[]):
        resp = client.get("/api/bars")
    assert resp.status_code == 200


def test_list_bars_returns_json_array():
    with patch("api.routers.bars.get_bars", return_value=[]):
        resp = client.get("/api/bars")
    assert resp.json() == []


def test_list_bars_returns_bar_data():
    with patch("api.routers.bars.get_bars", return_value=[_MOCK_BAR]):
        resp = client.get("/api/bars")
    data = resp.json()
    assert len(data) == 1
    assert data[0]["name"] == "Bar Teste"
    assert data[0]["latitude"] == -19.9245
    assert data[0]["longitude"] == -43.9352
    assert data[0]["is_vegetarian"] == 1


def test_list_bars_returns_food_category():
    with patch("api.routers.bars.get_bars", return_value=[_MOCK_BAR]):
        resp = client.get("/api/bars")
    data = resp.json()
    assert data[0]["food_category"] == "bolinhos"
