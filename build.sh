#!/usr/bin/env bash
set -Eeuo pipefail

ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT"

if [[ ! -x "$ROOT/build.sh" ]]; then
  echo "ERROR: the original build.sh was not found or is not executable." >&2
  exit 2
fi
if [[ ! -d "$ROOT/src/svg" || ! -d "$ROOT/src/svg-cyan" ]]; then
  echo "ERROR: expected both src/svg/ and src/svg-cyan/." >&2
  exit 2
fi
if ! grep -qx 'create svg' "$ROOT/build.sh"; then
  echo "ERROR: could not find the expected final 'create svg' command in build.sh." >&2
  echo "The upstream build.sh may have changed; refusing to guess how to build the cyan variant." >&2
  exit 2
fi
for tool in inkscape xcursorgen python3; do
  if ! command -v "$tool" >/dev/null 2>&1; then
    echo "ERROR: required command '$tool' was not found. Install it and rerun this script." >&2
    exit 2
  fi
done

# First build the original/default variant and then add its scalable SVG tree.
echo "==> Building default Future Cursors variant (src/svg)"
"$ROOT/build.sh"
python3 "$ROOT/build-svg-cursors.py" \
  --svg-dir src/svg \
  --dist-dir dist \
  --theme-name "Future Cursors"

# Build the cyan variant in an isolated copy so its rasterized PNG/Xcursor files
# cannot overwrite the default variant's output or working files.
TMP_ROOT="$(mktemp -d "${TMPDIR:-/tmp}/future-cursors-cyan.XXXXXX")"
trap 'rm -rf "$TMP_ROOT"' EXIT
cp -a "$ROOT/src" "$TMP_ROOT/src"
# Clear PNG intermediates copied from the default build so cyan uses only its own SVGs.
rm -rf "$TMP_ROOT/src/x1" "$TMP_ROOT/src/x1_25" "$TMP_ROOT/src/x1_5" "$TMP_ROOT/src/x2"
cp "$ROOT/build-svg-cursors.py" "$TMP_ROOT/build-svg-cursors.py"
sed 's/^create svg$/create svg-cyan/' "$ROOT/build.sh" > "$TMP_ROOT/build.sh"
chmod +x "$TMP_ROOT/build.sh"

echo
echo "==> Building cyan Future Cursors variant (src/svg-cyan)"
(
  cd "$TMP_ROOT"
  ./build.sh
  python3 ./build-svg-cursors.py \
    --svg-dir src/svg-cyan \
    --dist-dir dist \
    --theme-name "Future Cursors Cyan"
)

# Replace the previous cyan output only after the new variant built successfully.
if [[ -d "$ROOT/dist-cyan" ]]; then
  rm -rf "$ROOT/dist-cyan"
fi
mv "$TMP_ROOT/dist" "$ROOT/dist-cyan"

echo
echo "Build finished. Generated themes:"
echo "  Default: $ROOT/dist"
echo "  Cyan:    $ROOT/dist-cyan"
echo "Install both with ./install-gnome51.sh (or sudo ./install-gnome51.sh for system-wide installation)."
