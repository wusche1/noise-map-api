# noise-map

Queries noise levels for German addresses from the UBA Lärmkartierung ArcGIS MapServer. Has both a CLI tool and a static web UI (GitHub Pages).

## Running

```bash
poetry run python -m noise_map.cli "Alexanderplatz 1, Berlin"
```

## Tests

```bash
pytest tests/
```

## Architecture

- `noise_map/api.py` — ArcGIS REST API queries, layer definitions, coordinate transformer
- `noise_map/geocode.py` — address → coordinates via Nominatim (normalizes "strasse" → "Straße" etc.)
- `noise_map/parse.py` — parse raw noise level strings (e.g. "Lden5559" → "55-59 dB(A)")
- `noise_map/lookup.py` — core lookup function: address → dict of all noise levels
- `noise_map/cli.py` — CLI entrypoint (single + batch CSV mode)
- `docs/index.html` — static web UI (GitHub Pages), same logic reimplemented in JS

## Key details

- MapServer base URL: `https://datahub.uba.de/server/rest/services/VeLa/LK/MapServer`
- Coordinates must be in EPSG:3857 (Web Mercator) for the API
- Each noise source has a day (Lden) and night (Lnight) layer
- Queries run in parallel via ThreadPoolExecutor
- Batch mode respects Nominatim's 1 req/sec rate limit
- CSV uses semicolons as delimiter (German Excel compatibility)
