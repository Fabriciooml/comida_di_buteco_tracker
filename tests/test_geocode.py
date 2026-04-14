import json
from unittest.mock import patch, MagicMock


def _make_mock_urlopen(payload: list) -> MagicMock:
    mock_resp = MagicMock()
    mock_resp.read.return_value = json.dumps(payload).encode()
    mock_resp.__enter__ = lambda s: s
    mock_resp.__exit__ = MagicMock(return_value=False)
    return mock_resp


def test_build_params_combines_street_fields():
    from pipeline.geocode import build_params
    result = build_params("Rua das Flores", "100", "Belo Horizonte", "MG")
    assert result == {"street": "Rua das Flores 100", "city": "Belo Horizonte", "state": "MG"}


def test_build_params_skips_none_street():
    from pipeline.geocode import build_params
    result = build_params(None, None, "Belo Horizonte", "MG")
    assert result == {"city": "Belo Horizonte", "state": "MG"}
    assert "street" not in result


def test_build_params_strips_whitespace_in_street_part():
    from pipeline.geocode import build_params
    result = build_params("Rua X", None, "Belo Horizonte", "MG")
    assert result["street"] == "Rua X"


def test_geocode_address_structured_returns_coords():
    from pipeline.geocode import geocode_address
    payload = [{"lat": "-19.9245678", "lon": "-43.9352123"}]
    with patch("urllib.request.urlopen", return_value=_make_mock_urlopen(payload)):
        result = geocode_address({"street": "Rua X 100", "city": "BH", "state": "MG"})
    assert result == (-19.9245678, -43.9352123)


def test_geocode_address_freetext_returns_coords():
    from pipeline.geocode import geocode_address
    payload = [{"lat": "-19.9245000", "lon": "-43.9352000"}]
    with patch("urllib.request.urlopen", return_value=_make_mock_urlopen(payload)):
        result = geocode_address({"q": "Rua X 100, Savassi, Belo Horizonte, MG"})
    assert result == (-19.9245, -43.9352)


def test_geocode_address_rounds_to_7_decimals():
    from pipeline.geocode import geocode_address
    payload = [{"lat": "-19.924567890123", "lon": "-43.935212345678"}]
    with patch("urllib.request.urlopen", return_value=_make_mock_urlopen(payload)):
        result = geocode_address({"street": "Rua X 100", "city": "BH", "state": "MG"})
    lat, lon = result
    assert lat == round(-19.924567890123, 7)
    assert lon == round(-43.935212345678, 7)


def test_geocode_address_returns_none_on_empty_results():
    from pipeline.geocode import geocode_address
    with patch("urllib.request.urlopen", return_value=_make_mock_urlopen([])):
        result = geocode_address({"street": "nowhere special"})
    assert result is None


def test_fallback_params_drops_street_prefix():
    from pipeline.geocode import _fallback_params
    fallbacks = _fallback_params("Rua das Flores", "100", "Palmeiras", "Belo Horizonte", "MG")
    labels = [label for label, _ in fallbacks]
    params_list = [p for _, p in fallbacks]
    assert "without street prefix" in labels
    prefix_params = params_list[labels.index("without street prefix")]
    assert prefix_params["street"] == "das Flores 100"
    assert prefix_params["city"] == "Belo Horizonte"
    assert prefix_params["state"] == "MG"
    assert "q" not in prefix_params


def test_fallback_params_freetext_with_neighborhood():
    from pipeline.geocode import _fallback_params
    fallbacks = _fallback_params("Rua das Flores", "100", "Palmeiras", "Belo Horizonte", "MG")
    labels = [label for label, _ in fallbacks]
    params_list = [p for _, p in fallbacks]
    assert "free-text with neighborhood" in labels
    ft_params = params_list[labels.index("free-text with neighborhood")]
    assert "q" in ft_params
    assert "Palmeiras" in ft_params["q"]
    assert "Rua das Flores 100" in ft_params["q"]


def test_fallback_params_neighborhood_only():
    from pipeline.geocode import _fallback_params
    fallbacks = _fallback_params("Rua das Flores", "100", "Palmeiras", "Belo Horizonte", "MG")
    labels = [label for label, _ in fallbacks]
    params_list = [p for _, p in fallbacks]
    assert "neighborhood only" in labels
    coarse_params = params_list[labels.index("neighborhood only")]
    assert "q" in coarse_params
    assert "Palmeiras" in coarse_params["q"]
    assert "Rua das Flores" not in coarse_params["q"]
