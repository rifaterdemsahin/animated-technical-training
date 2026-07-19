#!/usr/bin/env python3
"""Validate scripts/*.json scene files against the DeliveryPilot schema.

Usage:
    tools/validate_scenes.py [FILES...] [--manifest sprites/manifest.json]
                              [--word-cap 20] [--strict-drafts]

With no FILES, validates every scripts/*.json in the repo.

Exit codes:
    0  no blocking errors
    1  at least one blocking error found

A "ready" scene that fails a check is a blocking ERROR (it must not reach
export). A "draft" scene that fails a check is a WARNING, unless
--strict-drafts is passed.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
REQUIRED_FIELDS = [
    "page_id", "status", "visual_action", "sprite_sequence",
    "incoming", "outgoing",
]
VALID_STATUSES = {"draft", "ready", "exported"}


def _normalize(text: str) -> set[str]:
    return set(re.findall(r"[a-z0-9]+", text.lower()))


def _word_count(text: str) -> int:
    return len(text.split())


def _is_redundant(visual_action: str, caption: str) -> bool:
    """Flag near-duplicate wording between visual_action and a caption field."""
    if not visual_action or not caption:
        return False
    va_words = _normalize(visual_action)
    cap_words = _normalize(caption)
    if not va_words or not cap_words:
        return False
    overlap = va_words & cap_words
    jaccard = len(overlap) / len(va_words | cap_words)
    return jaccard > 0.8


class Issue:
    def __init__(self, page_id: str, level: str, message: str):
        self.page_id = page_id
        self.level = level  # "ERROR" or "WARNING"
        self.message = message

    def __str__(self) -> str:
        return f"  [{self.level}] {self.page_id}: {self.message}"


def validate_topic_file(path: Path, manifest: dict, word_cap: int) -> list[Issue]:
    issues: list[Issue] = []
    try:
        data = json.loads(path.read_text())
    except json.JSONDecodeError as exc:
        return [Issue(path.name, "ERROR", f"invalid JSON: {exc}")]

    scenes = data.get("scenes")
    if not isinstance(scenes, list):
        return [Issue(path.name, "ERROR", "missing top-level 'scenes' array")]

    seen_page_ids: set[str] = set()

    for scene in scenes:
        page_id = scene.get("page_id", "<missing page_id>")
        status = scene.get("status")
        scene_issues: list[tuple[str, str]] = []  # (check_message, blocking?)

        missing = [f for f in REQUIRED_FIELDS if f not in scene]
        if missing:
            scene_issues.append((f"missing required field(s): {', '.join(missing)}", True))

        if status not in VALID_STATUSES:
            scene_issues.append((f"invalid status '{status}' (expected one of {sorted(VALID_STATUSES)})", True))

        if page_id in seen_page_ids:
            scene_issues.append((f"duplicate page_id '{page_id}'", True))
        seen_page_ids.add(page_id)

        visual_action = scene.get("visual_action", "")
        if not visual_action.strip():
            scene_issues.append(("visual_action is empty", True))

        incoming = scene.get("incoming", "")
        outgoing = scene.get("outgoing", "")
        if not incoming.strip():
            scene_issues.append(("incoming is empty", True))
        if not outgoing.strip():
            scene_issues.append(("outgoing is empty", True))

        if incoming and _word_count(incoming) > word_cap:
            scene_issues.append((f"incoming exceeds {word_cap}-word cap ({_word_count(incoming)} words)", True))
        if outgoing and _word_count(outgoing) > word_cap:
            scene_issues.append((f"outgoing exceeds {word_cap}-word cap ({_word_count(outgoing)} words)", True))

        if visual_action and _is_redundant(visual_action, incoming):
            scene_issues.append(("visual_action reads as a restatement of incoming (redundancy risk)", True))
        if visual_action and _is_redundant(visual_action, outgoing):
            scene_issues.append(("visual_action reads as a restatement of outgoing (redundancy risk)", True))

        sprite_sequence = scene.get("sprite_sequence", [])
        if len(sprite_sequence) < 2:
            scene_issues.append((f"sprite_sequence has {len(sprite_sequence)} entr(y/ies), minimum 2 required", True))
        unknown_sprites = [s for s in sprite_sequence if s not in manifest]
        if unknown_sprites:
            scene_issues.append((f"unknown sprite id(s) not in manifest: {', '.join(unknown_sprites)}", True))

        for message, _blocking in scene_issues:
            level = "ERROR" if status == "ready" else "WARNING"
            issues.append(Issue(page_id, level, message))

    return issues


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("files", nargs="*", help="scripts/*.json files to validate")
    parser.add_argument("--manifest", default=str(REPO_ROOT / "sprites" / "manifest.json"))
    parser.add_argument("--word-cap", type=int, default=20)
    parser.add_argument("--strict-drafts", action="store_true", help="treat draft-scene warnings as blocking errors")
    args = parser.parse_args()

    manifest_path = Path(args.manifest)
    manifest = json.loads(manifest_path.read_text()) if manifest_path.exists() else {}

    files = [Path(f) for f in args.files] if args.files else sorted((REPO_ROOT / "scripts").glob("*.json"))
    if not files:
        print("No scripts/*.json files found to validate.")
        return 0

    total_errors = 0
    total_warnings = 0
    for path in files:
        issues = validate_topic_file(path, manifest, args.word_cap)
        if args.strict_drafts:
            for issue in issues:
                issue.level = "ERROR"

        errors = [i for i in issues if i.level == "ERROR"]
        warnings = [i for i in issues if i.level == "WARNING"]
        total_errors += len(errors)
        total_warnings += len(warnings)

        print(f"{path.relative_to(REPO_ROOT) if path.is_absolute() else path}: "
              f"{len(errors)} error(s), {len(warnings)} warning(s)")
        for issue in issues:
            print(issue)

    print(f"\nTotal: {total_errors} error(s), {total_warnings} warning(s) across {len(files)} file(s)")
    return 1 if total_errors else 0


if __name__ == "__main__":
    sys.exit(main())
