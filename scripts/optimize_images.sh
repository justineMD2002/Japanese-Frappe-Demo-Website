#!/usr/bin/env bash
# Convert source photos into the WebP sizes the site templates reference.
# Usage: scripts/optimize_images.sh <dir with <name>.jpg files>
# Names must match those used in templates (hero, banner-about, service-erp, ...).
# Needs macOS `sips` and `cwebp` (brew install webp). Widths larger than the source are skipped.
set -euo pipefail

SRC_DIR="${1:?usage: $0 <source-dir>}"
OUT_DIR="$(cd "$(dirname "$0")/.." && pwd)/japanese_demo_website/public/images"
WIDTHS=(480 960 1600)
QUALITY=78

mkdir -p "$OUT_DIR"
tmp="$(mktemp -d)"
trap 'rm -rf "$tmp"' EXIT

for src in "$SRC_DIR"/*.jpg; do
	name="$(basename "$src" .jpg)"
	src_width="$(sips -g pixelWidth "$src" | awk '/pixelWidth/ {print $2}')"
	for width in "${WIDTHS[@]}"; do
		# always emit 480 and 960 so templates can rely on them; upscale only those two
		if (( width > src_width )) && (( width > 960 )); then
			continue
		fi
		sips -s format jpeg --resampleWidth "$width" "$src" --out "$tmp/$name.jpg" >/dev/null
		cwebp -quiet -q "$QUALITY" -metadata none "$tmp/$name.jpg" -o "$OUT_DIR/$name-$width.webp"
	done
	echo "$name"
done
