from unittest.mock import patch, Mock

from noise_map.api import query_layer


def _mock_response(features):
    mock = Mock()
    mock.json.return_value = {"features": features}
    return mock


def test_query_layer_returns_value():
    features = [{"attributes": {"Lärmpegelklasse": "Lden5559"}}]
    with patch("noise_map.api.requests.get", return_value=_mock_response(features)):
        assert query_layer(4210, 1097816.0, 6858914.0) == "Lden5559"


def test_query_layer_returns_none_when_empty():
    with patch("noise_map.api.requests.get", return_value=_mock_response([])):
        assert query_layer(4210, 0.0, 0.0) is None
