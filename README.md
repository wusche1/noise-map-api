# noise-map

CLI tool to query noise levels for any German address from the [UBA Lärmkartierung](https://gis.uba.de/maps/resources/apps/laermkartierung/index.html) (German Federal Environment Agency noise map).

Returns day (Lden) and night (Lnight) noise levels across road, rail, air, and industrial sources.

## Prerequisites

- Python 3.9+
- [Poetry](https://python-poetry.org/docs/#installation)

## Setup

```bash
poetry install
```

## Usage

### Single address

```bash
python -m noise_map.cli "Alexanderplatz 1, Berlin"
```

```
Found: Berolinahaus, 1, Alexanderplatz, Mitte, Berlin, 10178, Deutschland
Coordinates: 52.521506, 13.412381

Source                                Day           Night
---------------------------------------------------------
Road (major roads)            55-59 dB(A)               -
Road (urban)                  55-59 dB(A)               -
Rail (major lines)            60-64 dB(A)     50-54 dB(A)
Rail (urban)                  60-64 dB(A)     50-54 dB(A)
Air (major airports)                    -               -
Air (urban)                             -               -
Industry (urban)                        -               -
```

### Batch processing (CSV)

Prepare a CSV with an `address` column (semicolon-separated):

```csv
address
Alexanderplatz 1, Berlin
Hauptbahnhof, München
```

Then run:

```bash
python -m noise_map.cli --batch input.csv output.csv
```

If the address column has a different name:

```bash
python -m noise_map.cli --batch input.csv output.csv --col Adresse
```

Output is a semicolon-separated CSV (opens directly in German Excel) with all noise levels. Processes ~1 address/second due to geocoding rate limits.

## Tests

```bash
pytest tests/
```

## How it works

1. Geocodes the address to coordinates using OpenStreetMap/Nominatim
2. Reprojects to EPSG:3857 (Web Mercator)
3. Queries the UBA ArcGIS MapServer REST API for all noise layers in parallel
4. Returns the noise level classification per source (road, rail, air, industry — day & night)
