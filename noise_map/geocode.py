from __future__ import annotations

import re

from geopy.geocoders import Nominatim

_STREET_PATTERNS = [
    (r"(?i)\bstrasse\b", "Straße"),
    (r"(?i)\bstr\b\.?", "Straße"),
    (r"(?i)\bplatz\b", "Platz"),
]


def _normalize(address: str) -> str:
    for pattern, replacement in _STREET_PATTERNS:
        address = re.sub(pattern, replacement, address)
    return address


def geocode(address: str) -> tuple[str, float, float] | None:
    geolocator = Nominatim(user_agent="noise-map-cli")
    location = geolocator.geocode(_normalize(address), country_codes="de")
    if not location:
        return None
    return location.address, location.longitude, location.latitude
