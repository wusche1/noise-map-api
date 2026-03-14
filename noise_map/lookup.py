from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor

from noise_map.api import LAYERS, query_layer, transformer
from noise_map.geocode import geocode
from noise_map.parse import parse_db


def lookup_address(address: str) -> dict | None:
    result = geocode(address)
    if not result:
        return None

    resolved, lon, lat = result
    x, y = transformer.transform(lon, lat)

    with ThreadPoolExecutor(max_workers=8) as pool:
        futures = {lid: pool.submit(query_layer, lid, x, y)
                   for pair in LAYERS.values() for lid in pair}

    row = {"address_input": address, "address_resolved": resolved, "lat": lat, "lon": lon}
    for name, (day_id, night_id) in LAYERS.items():
        day_val = futures[day_id].result()
        night_val = futures[night_id].result()
        row[f"{name} (day)"] = parse_db(day_val) if day_val else ""
        row[f"{name} (night)"] = parse_db(night_val) if night_val else ""
    return row
