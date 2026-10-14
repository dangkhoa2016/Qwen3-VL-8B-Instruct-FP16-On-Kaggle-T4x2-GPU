#!/usr/bin/env bash
set -euo pipefail
ROOT="${1:-.}"
OUT="$ROOT/examples/vision"
mkdir -p "$OUT"
curl -L --fail --retry 3 "https://upload.wikimedia.org/wikipedia/commons/4/48/Street_market_-_Hanoi%2C_Vietnam_-_DSC03475.JPG" -o "$OUT/vision-real-hanoi-street-market-cc0.jpg"
curl -L --fail --retry 3 "https://upload.wikimedia.org/wikipedia/commons/4/4f/Kitchen_table.jpg" -o "$OUT/vision-real-kitchen-table-public-domain.jpg"
curl -L --fail --retry 3 "https://upload.wikimedia.org/wikipedia/commons/5/59/People_on_street_market_in_urban_part_of_town.jpg" -o "$OUT/vision-real-urban-market-public-domain.jpg"
echo "Fetched three real-world public-domain/CC0 images."
