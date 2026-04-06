from __future__ import annotations

import importlib.util
import tempfile
import unittest
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
UTILS_PATH = ROOT / "zpe_mocap" / "utils.py"
SPEC = importlib.util.spec_from_file_location("zpe_mocap_utils", UTILS_PATH)
if SPEC is None or SPEC.loader is None:  # pragma: no cover - import bootstrap guard
    raise RuntimeError(f"Unable to load utils module from {UTILS_PATH}")
UTILS = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(UTILS)

extract_zip_safely = UTILS.extract_zip_safely


class ZipExtractSafetyTests(unittest.TestCase):
    def test_extracts_safe_members(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            archive_path = tmp / "safe.zip"
            destination = tmp / "out"
            expected = b"mock clip data"

            with zipfile.ZipFile(archive_path, "w") as archive:
                archive.writestr("clips/walk/001.bvh", expected)

            with zipfile.ZipFile(archive_path, "r") as archive:
                extract_zip_safely(archive, destination)

            self.assertEqual((destination / "clips" / "walk" / "001.bvh").read_bytes(), expected)

    def test_rejects_parent_traversal_members(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            archive_path = tmp / "unsafe.zip"
            destination = tmp / "out"

            with zipfile.ZipFile(archive_path, "w") as archive:
                archive.writestr("safe.txt", b"ok")
                archive.writestr("../escape.txt", b"nope")

            with zipfile.ZipFile(archive_path, "r") as archive:
                with self.assertRaisesRegex(ValueError, r"Unsafe archive entry: \.\./escape\.txt"):
                    extract_zip_safely(archive, destination)

            self.assertFalse((destination / "safe.txt").exists())
            self.assertFalse((tmp / "escape.txt").exists())

    def test_rejects_absolute_members(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            archive_path = tmp / "absolute.zip"
            destination = tmp / "out"

            with zipfile.ZipFile(archive_path, "w") as archive:
                archive.writestr("/absolute.txt", b"nope")

            with zipfile.ZipFile(archive_path, "r") as archive:
                with self.assertRaisesRegex(ValueError, r"Unsafe archive entry: /absolute\.txt"):
                    extract_zip_safely(archive, destination)


if __name__ == "__main__":
    unittest.main()
