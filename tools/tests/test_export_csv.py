#!/usr/bin/env python3
"""Unit tests for tools/export_csv.py.

Run with: python3 -m unittest discover -s tools/tests
"""
import csv
import json
import sys
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(REPO_ROOT / "tools"))

import export_csv  # noqa: E402


class ExportSampleTopicTest(unittest.TestCase):
    """Exercises export_csv.py against the real sample topic in the repo."""

    def setUp(self):
        self.manifest = export_csv.load_manifest(REPO_ROOT / "sprites" / "manifest.json")
        self.tmp_dir = tempfile.TemporaryDirectory()
        self.output_dir = Path(self.tmp_dir.name)

    def tearDown(self):
        self.tmp_dir.cleanup()

    def test_only_ready_scenes_are_exported(self):
        written = export_csv.export_topic(
            REPO_ROOT / "scripts" / "forward-proxy.json",
            self.manifest, self.output_dir, max_rows=300, max_cols=150,
        )
        self.assertEqual(len(written), 1)
        with written[0].open() as f:
            rows = list(csv.DictReader(f))
        # fp-001, fp-002, fp-004 are "ready"; fp-003, fp-005 are "draft"
        self.assertEqual({r["page_id"] for r in rows}, {"fp-001", "fp-002", "fp-004"})

    def test_sprite_columns_hold_filenames_not_urls(self):
        written = export_csv.export_topic(
            REPO_ROOT / "scripts" / "forward-proxy.json",
            self.manifest, self.output_dir, max_rows=300, max_cols=150,
        )
        with written[0].open() as f:
            rows = list(csv.DictReader(f))
        row = next(r for r in rows if r["page_id"] == "fp-001")
        self.assertEqual(row["sprite_1"], "client_idle_neutral.png")
        self.assertEqual(row["sprite_2"], "client_action_neutral.png")
        self.assertFalse(row["sprite_1"].startswith("http"))


class ExportSyntheticTest(unittest.TestCase):
    """Uses synthetic fixtures to exercise batching and limit-enforcement logic."""

    def setUp(self):
        self.manifest = {
            "a": {"file": "sprites/x/a.png"},
            "b": {"file": "sprites/x/b.png"},
        }
        self.tmp_dir = tempfile.TemporaryDirectory()
        self.tmp_path = Path(self.tmp_dir.name)
        self.output_dir = self.tmp_path / "csv"

    def tearDown(self):
        self.tmp_dir.cleanup()

    def _write_topic(self, name: str, n_scenes: int) -> Path:
        scenes = [
            {
                "page_id": f"{name}-{i:03d}",
                "status": "ready",
                "visual_action": "x",
                "sprite_sequence": ["a", "b"],
                "incoming": "in",
                "outgoing": "out",
            }
            for i in range(n_scenes)
        ]
        path = self.tmp_path / f"{name}.json"
        path.write_text(json.dumps({"topic": name, "scenes": scenes}))
        return path

    def test_splits_into_parts_over_row_limit(self):
        topic_path = self._write_topic("big-topic", 7)
        written = export_csv.export_topic(topic_path, self.manifest, self.output_dir,
                                           max_rows=3, max_cols=150)
        self.assertEqual(len(written), 3)  # 3 + 3 + 1
        self.assertTrue(written[0].name.endswith("_part1.csv"))
        row_counts = []
        for path in written:
            with path.open() as f:
                row_counts.append(len(list(csv.DictReader(f))))
        self.assertEqual(row_counts, [3, 3, 1])

    def test_single_batch_has_no_part_suffix(self):
        topic_path = self._write_topic("small-topic", 2)
        written = export_csv.export_topic(topic_path, self.manifest, self.output_dir,
                                           max_rows=300, max_cols=150)
        self.assertEqual(len(written), 1)
        self.assertEqual(written[0].name, "small-topic.csv")

    def test_raises_when_column_limit_exceeded(self):
        topic_path = self._write_topic("wide-topic", 1)
        with self.assertRaises(export_csv.ExportError):
            export_csv.export_topic(topic_path, self.manifest, self.output_dir,
                                      max_rows=300, max_cols=3)

    def test_raises_on_unknown_sprite_id(self):
        path = self.tmp_path / "bad-topic.json"
        path.write_text(json.dumps({
            "topic": "bad-topic",
            "scenes": [{
                "page_id": "bt-001", "status": "ready", "visual_action": "x",
                "sprite_sequence": ["a", "does_not_exist"],
                "incoming": "in", "outgoing": "out",
            }],
        }))
        with self.assertRaises(export_csv.ExportError):
            export_csv.export_topic(path, self.manifest, self.output_dir,
                                      max_rows=300, max_cols=150)

    def test_no_ready_scenes_writes_nothing(self):
        path = self.tmp_path / "empty-topic.json"
        path.write_text(json.dumps({
            "topic": "empty-topic",
            "scenes": [{
                "page_id": "et-001", "status": "draft", "visual_action": "x",
                "sprite_sequence": ["a", "b"], "incoming": "in", "outgoing": "out",
            }],
        }))
        written = export_csv.export_topic(path, self.manifest, self.output_dir,
                                            max_rows=300, max_cols=150)
        self.assertEqual(written, [])


if __name__ == "__main__":
    unittest.main()
