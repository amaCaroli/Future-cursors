#!/usr/bin/env python3
"""Generate GNOME 51 / KDE Plasma 6.2+ scalable SVG cursors.

Run this from the root of yeyushengfan258/Future-cursors after its original
build.sh has generated the selected dist directory. The script uses only the
Python standard library.
"""
from __future__ import annotations

import argparse
import json
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
HASH_NAME = re.compile(r"^[0-9a-fA-F]{32}$")


def number(value: str) -> int | float:
    parsed = float(value)
    return int(parsed) if parsed.is_integer() else parsed


def read_cursor_config(path: Path, svg_dir: Path, root: Path) -> list[dict]:
    """Read xcursorgen entries, retaining the first scale's data per SVG frame."""
    frames: list[dict] = []
    seen: set[str] = set()
    for line_number, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        columns = line.split()
        if len(columns) < 4:
            raise ValueError(f"{path.relative_to(root)}:{line_number}: expected 4+ columns")
        size, hotspot_x, hotspot_y, png_path = columns[:4]
        delay = columns[4] if len(columns) >= 5 else None
        # x1/foo.png, x1_25/foo.png, etc. all map back to the selected SVG tree.
        frame_stem = Path(png_path).stem
        if frame_stem in seen:
            continue
        seen.add(frame_stem)
        frame = {
            "source": svg_dir / f"{frame_stem}.svg",
            "filename": f"{frame_stem}.svg",
            "hotspot_x": number(hotspot_x),
            "hotspot_y": number(hotspot_y),
            "nominal_size": number(size),
        }
        if delay is not None:
            frame["delay"] = number(delay)
        frames.append(frame)
    return frames


def read_aliases(path: Path) -> list[tuple[str, str]]:
    """Read source cursorList and discard Xcursor's content-hash aliases."""
    aliases: list[tuple[str, str]] = []
    if not path.exists():
        return aliases
    for raw in path.read_text(encoding="utf-8").splitlines():
        columns = raw.split()
        if len(columns) < 2:
            continue
        alias, target = columns[:2]
        if HASH_NAME.fullmatch(alias):
            continue
        aliases.append((alias, target))
    return aliases


def create_symlink(alias_path: Path, target_name: str) -> None:
    alias_path.symlink_to(target_name, target_is_directory=True)


def update_theme_index(index_path: Path, theme_name: str) -> None:
    existing_lines = index_path.read_text(encoding="utf-8").splitlines() if index_path.exists() else []
    if not any(line.strip() == "[Icon Theme]" for line in existing_lines):
        existing_lines = ["[Icon Theme]"] + existing_lines
    section_start = next((i for i, line in enumerate(existing_lines) if line.strip() == "[Icon Theme]"), 0)
    section_end = next(
        (i for i in range(section_start + 1, len(existing_lines)) if existing_lines[i].startswith("[")),
        len(existing_lines),
    )
    theme_section = existing_lines[section_start + 1:section_end]
    other_before = existing_lines[:section_start]
    other_after = existing_lines[section_end:]
    theme_section = [line for line in theme_section if not line.startswith(("Name=", "Inherits="))]
    theme_section.extend([f"Name={theme_name}", "Inherits=Adwaita"])
    new_lines = [*other_before, "[Icon Theme]", *theme_section]
    if other_after:
        new_lines.extend(["", *other_after])
    index_path.write_text("\n".join(new_lines).rstrip() + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--svg-dir", default="src/svg", help="selected source SVG directory (default: src/svg)")
    parser.add_argument("--dist-dir", default="dist", help="build output directory (default: dist)")
    parser.add_argument("--theme-name", default="Future Cursors", help="display name in index.theme")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = ROOT
    config_dir = root / "src" / "config"
    svg_dir = (root / args.svg_dir).resolve()
    dist = (root / args.dist_dir).resolve()
    output = dist / "cursors_scalable"

    if not config_dir.is_dir() or not svg_dir.is_dir():
        print(f"ERROR: expected {config_dir.relative_to(root)}/ and {svg_dir}; check --svg-dir.", file=sys.stderr)
        return 2
    if not dist.is_dir():
        print(f"ERROR: {dist} does not exist. Run ./build.sh first.", file=sys.stderr)
        return 2

    config_files = sorted(config_dir.glob("*.cursor"))
    if not config_files:
        print(f"ERROR: no *.cursor files found in {config_dir}", file=sys.stderr)
        return 2

    # Build in a temporary directory so a missing SVG won't leave a half-generated tree.
    temp_output = dist / ".cursors_scalable.tmp"
    if temp_output.exists() or temp_output.is_symlink():
        if temp_output.is_dir() and not temp_output.is_symlink():
            shutil.rmtree(temp_output)
        else:
            temp_output.unlink()
    temp_output.mkdir(parents=True)

    missing: list[str] = []
    cursor_count = 0
    frame_count = 0
    for config_path in config_files:
        frames = read_cursor_config(config_path, svg_dir, root)
        if not frames:
            print(f"WARNING: {config_path.name} has no usable entries; skipping", file=sys.stderr)
            continue
        absent = [str(frame["source"]) for frame in frames if not frame["source"].is_file()]
        if absent:
            missing.extend(absent)
            continue

        cursor_dir = temp_output / config_path.stem
        cursor_dir.mkdir(parents=True)
        metadata: list[dict] = []
        for frame in frames:
            shutil.copy2(frame["source"], cursor_dir / frame["filename"])
            metadata_frame = {
                "filename": frame["filename"],
                "hotspot_x": frame["hotspot_x"],
                "hotspot_y": frame["hotspot_y"],
                "nominal_size": frame["nominal_size"],
            }
            if "delay" in frame:
                metadata_frame["delay"] = frame["delay"]
            metadata.append(metadata_frame)
        (cursor_dir / "metadata.json").write_text(
            json.dumps(metadata, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )
        cursor_count += 1
        frame_count += len(frames)

    if missing:
        shutil.rmtree(temp_output, ignore_errors=True)
        print("ERROR: source SVGs referenced by src/config/*.cursor were not found:", file=sys.stderr)
        for name in sorted(set(missing)):
            print(f"  - {name}", file=sys.stderr)
        return 1

    aliases = read_aliases(root / "src" / "cursorList")
    remaining = aliases[:]
    made_aliases: set[str] = set()
    for _ in range(len(aliases) + 1):
        unresolved: list[tuple[str, str]] = []
        progress = False
        for alias, target in remaining:
            link = temp_output / alias
            target_path = temp_output / target
            if link.exists() or link.is_symlink():
                continue
            if target_path.exists() or target_path.is_symlink():
                create_symlink(link, target)
                made_aliases.add(alias)
                progress = True
            else:
                unresolved.append((alias, target))
        remaining = unresolved
        if not progress:
            break

    required_aliases = {
        "all-resize": ("fleur", "size_all", "move"),
        "dnd-ask": ("context-menu", "help", "pointer"),
    }
    for alias, candidates in required_aliases.items():
        link = temp_output / alias
        if link.exists() or link.is_symlink():
            continue
        target = next((candidate for candidate in candidates
                       if (temp_output / candidate).exists() or (temp_output / candidate).is_symlink()), None)
        if target is not None:
            create_symlink(link, target)
            made_aliases.add(alias)
        else:
            print(f"WARNING: unable to create required alias {alias!r}; no target was generated", file=sys.stderr)

    if output.exists() or output.is_symlink():
        if output.is_dir() and not output.is_symlink():
            shutil.rmtree(output)
        else:
            output.unlink()
    temp_output.rename(output)
    update_theme_index(dist / "index.theme", args.theme_name)

    print(f"Generated {cursor_count} SVG cursor shapes and {frame_count} frame(s) in:")
    print(f"  {output.relative_to(root)}")
    print(f"Created {len(made_aliases)} aliases from cursorList and GNOME compatibility aliases.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
