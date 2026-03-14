from __future__ import annotations

import requests
from pyproj import Transformer

BASE_URL = "https://datahub.uba.de/server/rest/services/VeLa/LK/MapServer"

LAYERS = {
    "Road (major roads)":   (4110, 4120),
    "Road (urban)":         (4210, 4220),
    "Rail (major lines)":   (5110, 5120),
    "Rail (urban)":         (5210, 5220),
    "Air (major airports)": (6110, 6120),
    "Air (urban)":          (6210, 6220),
    "Industry (urban)":     (7210, 7220),
}

transformer = Transformer.from_crs("EPSG:4326", "EPSG:3857", always_xy=True)


def query_layer(layer_id: int, x: float, y: float) -> str | None:
    resp = requests.get(f"{BASE_URL}/{layer_id}/query", params={
        "geometry": f"{x},{y}",
        "geometryType": "esriGeometryPoint",
        "spatialRel": "esriSpatialRelIntersects",
        "outFields": "Lärmpegelklasse",
        "f": "json",
    })
    features = resp.json().get("features", [])
    if features:
        return features[0]["attributes"]["Lärmpegelklasse"]
    return None
