from __future__ import annotations

import json
import tempfile
import unittest

from pathlib import Path
from unittest.mock import patch

from zpe_mocap import cmu


class CmuManifestDiagnosticTests(unittest.TestCase):
    def test_invalid_json_reports_manifest_path(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            manifest_path = Path(tmp_dir) / "manifest.json"
            manifest_path.write_text("{broken", encoding="utf-8")

            with patch.object(cmu, "CMU_MANIFEST", manifest_path):
                with self.assertRaises(ValueError) as ctx:
                    cmu.load_manifest()

        self.assertEqual(
            str(ctx.exception),
            f"Invalid CMU manifest {manifest_path}: could not be parsed at line 1 column 2: "
            "Expecting property name enclosed in double quotes.",
        )

    def test_invalid_filename_reports_entry_index(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            manifest_path = Path(tmp_dir) / "manifest.json"
            manifest_path.write_text(json.dumps([{"filename": 42}]), encoding="utf-8")

            with patch.object(cmu, "CMU_MANIFEST", manifest_path):
                with self.assertRaises(ValueError) as ctx:
                    cmu.load_manifest()

        self.assertEqual(
            str(ctx.exception),
            f"Invalid CMU manifest {manifest_path}: clip entry[0] has invalid 'filename': 42.",
        )

    def test_invalid_action_label_reports_filename(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            manifest_path = Path(tmp_dir) / "manifest.json"
            manifest_path.write_text(
                json.dumps([{"filename": "bvh/08/08_02.bvh", "action_label": 5}]),
                encoding="utf-8",
            )

            with patch.object(cmu, "CMU_MANIFEST", manifest_path):
                with self.assertRaises(ValueError) as ctx:
                    cmu.load_manifest()

        self.assertEqual(
            str(ctx.exception),
            f"Invalid CMU manifest {manifest_path}: clip entry[0] (bvh/08/08_02.bvh) "
            "has invalid 'action_label': 5.",
        )

    def test_missing_clip_file_reports_filename(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            root_path = Path(tmp_dir)
            manifest_path = root_path / "manifest.json"
            missing_clip = root_path / "bvh" / "08" / "08_02.bvh"
            manifest_path.write_text(
                json.dumps([{"filename": "bvh/08/08_02.bvh", "action_label": "walk"}]),
                encoding="utf-8",
            )

            with patch.object(cmu, "CMU_MANIFEST", manifest_path), patch.object(cmu, "CMU_ROOT", root_path):
                with self.assertRaises(ValueError) as ctx:
                    cmu.load_cmu_clips()

        self.assertEqual(
            str(ctx.exception),
            f"Invalid CMU manifest {manifest_path}: clip entry (bvh/08/08_02.bvh) "
            f"points to missing file: {missing_clip}.",
        )


if __name__ == "__main__":
    unittest.main()
