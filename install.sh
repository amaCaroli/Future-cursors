#!/usr/bin/env bash
set -Eeuo pipefail

ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
if [[ "$EUID" -eq 0 ]]; then
  DEST_DIR="/usr/share/icons"
else
  DEST_DIR="${XDG_DATA_HOME:-$HOME/.local/share}/icons"
fi

for theme_dir in dist dist-cyan; do
  if [[ ! -f "$ROOT/$theme_dir/index.theme" || ! -d "$ROOT/$theme_dir/cursors_scalable" ]]; then
    echo "ERROR: $theme_dir is missing or incomplete. Run ./build-gnome51.sh first." >&2
    exit 2
  fi
done

mkdir -p "$DEST_DIR"
for item in "Future-cursors:dist" "Future-cursors-cyan:dist-cyan"; do
  theme_name="${item%%:*}"
  source_dir="${item#*:}"
  rm -rf -- "$DEST_DIR/$theme_name"
  cp -a -- "$ROOT/$source_dir" "$DEST_DIR/$theme_name"
  echo "Installed $theme_name -> $DEST_DIR/$theme_name"
done

echo
echo "Select 'Future-cursors' or 'Future-cursors-cyan' in GNOME Tweaks or your desktop's cursor-theme settings."
