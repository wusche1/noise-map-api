from __future__ import annotations

import csv
import sys
import time

from noise_map.api import LAYERS
from noise_map.lookup import lookup_address

HEADER = (
    ["address_input", "address_resolved", "lat", "lon"]
    + [f"{name} ({period})" for name in LAYERS for period in ("day", "night")]
)


def single(address: str):
    row = lookup_address(address)
    if not row:
        print(f"Could not find address: {address}")
        print("Tip: check spelling and try adding the city (e.g. 'Hauptstr 1, Berlin')")
        sys.exit(1)

    print(f"Found: {row['address_resolved']}")
    print(f"Coordinates: {row['lat']:.6f}, {row['lon']:.6f}\n")

    print(f"{'Source':<25} {'Day':>15} {'Night':>15}")
    print("-" * 57)
    for name in LAYERS:
        day = row.get(f"{name} (day)") or "-"
        night = row.get(f"{name} (night)") or "-"
        print(f"{name:<25} {day:>15} {night:>15}")


def batch(input_path: str, output_path: str, address_column: str = "address"):
    with open(input_path, newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f, delimiter=";")
        if address_column not in reader.fieldnames:
            available = ", ".join(reader.fieldnames)
            print(f"Column '{address_column}' not found. Available: {available}")
            sys.exit(1)
        rows = list(reader)

    print(f"Processing {len(rows)} addresses...\n")

    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=HEADER, delimiter=";")
        writer.writeheader()

        for i, input_row in enumerate(rows, 1):
            address = input_row[address_column].strip()
            if not address:
                continue

            print(f"[{i}/{len(rows)}] {address}...", end=" ", flush=True)
            result = lookup_address(address)
            if result:
                writer.writerow(result)
                print(f"OK ({result['address_resolved'][:50]})")
            else:
                writer.writerow({"address_input": address})
                print("NOT FOUND")

            # Nominatim rate limit: 1 req/sec
            time.sleep(1.1)

    print(f"\nDone! Results saved to {output_path}")


def main():
    if len(sys.argv) < 2:
        print("Usage:")
        print("  noise-map <address>                          Single lookup")
        print("  noise-map --batch input.csv output.csv       Batch from CSV")
        print("  noise-map --batch input.csv output.csv --col address_column")
        sys.exit(1)

    if sys.argv[1] == "--batch":
        if len(sys.argv) < 4:
            print("Usage: noise-map --batch input.csv output.csv [--col address_column]")
            sys.exit(1)
        col = "address"
        if "--col" in sys.argv:
            col = sys.argv[sys.argv.index("--col") + 1]
        batch(sys.argv[2], sys.argv[3], col)
    else:
        single(" ".join(sys.argv[1:]))


if __name__ == "__main__":
    main()
