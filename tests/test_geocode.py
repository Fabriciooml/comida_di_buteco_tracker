import json
from unittest.mock import patch, MagicMock


def _make_mock_urlopen(payload: list) -> MagicMock:
    mock_resp = MagicMock()
    mock_resp.read.return_value = json.dumps(payload).encode()
    mock_resp.__enter__ = lambda s: s
    mock_resp.__exit__ = MagicMock(return_value=False)
    return mock_resp


def test_build_query_combines_all_fields():
    from geocode import build_query
    row = ("Rua das Flores", "100", "Savassi", "Belo Horizonte", "MG")
    assert build_query(row) == "Rua das Flores 100, Savassi, Belo Horizonte, MG"


def test_build_query_skips_none_street():
    from geocode import build_query
    row = (None, None, "Centro", "Belo Horizonte", "MG")
    assert build_query(row) == "Centro, Belo Horizonte, MG"


def test_build_query_strips_whitespace_in_street_part():
    from geocode import build_query
    row = ("Rua X", None, "Lourdes", "Belo Horizonte", "MG")
    assert build_query(row) == "Rua X, Lourdes, Belo Horizonte, MG"


def test_geocode_address_returns_coords_on_hit():
    from geocode import geocode_address
    payload = [{"lat": "-19.9245", "lon": "-43.9352"}]
    with patch("urllib.request.urlopen", return_value=_make_mock_urlopen(payload)):
        result = geocode_address("Rua X, Savassi, Belo Horizonte, MG")
    assert result == (-19.9245, -43.9352)


def test_geocode_address_returns_none_on_empty_results():
    from geocode import geocode_address
    with patch("urllib.request.urlopen", return_value=_make_mock_urlopen([])):
        result = geocode_address("nowhere special")
    assert result is None
