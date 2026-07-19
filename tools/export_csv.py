#!/usr/bin/env python3
"""Export ready scenes from scripts/*.json into Canva Bulk Create CSV files.

Usage:
    tools/export_csv.py [TOPIC_FILES...] [--manifest sprites/manifest.json]
                         [--output-dir output/csv] [--max-rows 300] [--max-cols 150]

With no TOPIC_FILES, exports every scripts/*.json in the repo.

Only scenes with status == "ready" are exported (see MASTER_SPEC.md section 6).
Sprite sequences are mapped to fixed sprite_1..sprite_N columns matching the
Canva master template's placeholder slots. Sprite cells contain the image
filename (not a URL) — the corresponding files must be uploaded to Canva's
Bulk Create media library alongside the CSV so filenames resolve to images
(see pipeline/CANVA_UPLOAD_CHECKLIST.md).
"""
from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent


class ExportError(Exception):
    pass


def load_manifest(manifest_path: Path) -> dict:
    return json.loads(manifest_path.read_text())


def load_ready_scenes(topic_path: Path) -> tuple[str, list[dict]]:
    data = json.loads(topic_path.read_text())
    topic = data.get("topic", topic_path.stem)
    scenes = [s for s in data.get("scenes", []) if s.get("status") == "ready"]
    return topic, scenes


def sprite_columns(scenes: list[dict]) -> list[str]:
    max_len = max((len(s.get("sprite_sequence", [])) for s in scenes), default=0)
    return [f"sprite_{i + 1}" for i in range(max_len)]


def build_rows(scenes: list[dict], manifest: dict, columns: list[str]) -> list[dict]:
    rows = []
    for scene in scenes:
        sequence = scene.get("sprite_sequence", [])
        row = {"page_id": scene["page_id"]}
        for i, col in enumerate(columns):
            if i >= len(sequence):
                row[col] = ""
                continue
            sprite_id = sequence[i]
            if sprite_id not in manifest:
                raise ExportError(
                    f"scene {scene['page_id']}: sprite id '{sprite_id}' not found in manifest"
                )
            row[col] = Path(manifest[sprite_id]["file"]).name
        row["incoming"] = scene.get("incoming", "")
        row["outgoing"] = scene.get("outgoing", "")
        rows.append(row)
    return rows


def chunk(items: list, size: int) -> list[list]:
    if size <= 0:
        return [items] if items else []
    return [items[i:i + size] for i in range(0, len(items), size)]


def export_topic(topic_path: Path, manifest: dict, output_dir: Path,
                  max_rows: int, max_cols: int) -> list[Path]:
    topic, scenes = load_ready_scenes(topic_path)
    if not scenes:
        print(f"{topic}: no ready scenes, skipping")
        return []

    columns = sprite_columns(scenes)
    header = ["page_id"] + columns + ["incoming", "outgoing"]
    if len(header) > max_cols:
        raise ExportError(
            f"{topic}: {len(header)} columns exceeds Canva Bulk Create limit of {max_cols}"
        )

    rows = build_rows(scenes, manifest, columns)
    batches = chunk(rows, max_rows)

    output_dir.mkdir(parents=True, exist_ok=True)
    written: list[Path] = []
    part_suffix = lambda i: f"_part{i}" if len(batches) > 1 else ""
    for i, batch in enumerate(batches, start=1):
        out_path = output_dir / f"{topic}{part_suffix(i)}.csv"
        with out_path.open("w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=header)
            writer.writeheader()
            writer.writerows(batch)
        written.append(out_path)
        print(f"wrote {out_path} ({len(batch)} rows, {len(header)} columns)")
    return written


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("files", nargs="*", help="scripts/*.json topic files to export")
    parser.add_argument("--manifest", default=str(REPO_ROOT / "sprites" / "manifest.json"))
    parser.add_argument("--output-dir", default=str(REPO_ROOT / "output" / "csv"))
    parser.add_argument("--max-rows", type=int, default=300)
    parser.add_argument("--max-cols", type=int, default=150)
    args = parser.parse_args()

    manifest = load_manifest(Path(args.manifest))
    files = [Path(f) for f in args.files] if args.files else sorted((REPO_ROOT / "scripts").glob("*.json"))
    output_dir = Path(args.output_dir)

    try:
        for path in files:
            export_topic(path, manifest, output_dir, args.max_rows, args.max_cols)
    except ExportError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
