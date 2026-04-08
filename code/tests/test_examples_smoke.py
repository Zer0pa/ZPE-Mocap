from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
EXAMPLES = ROOT / "examples"
MINIMAL_BVH = """HIERARCHY
ROOT Hips
{
  OFFSET 0.00 0.00 0.00
  CHANNELS 6 Xposition Yposition Zposition Zrotation Xrotation Yrotation
  JOINT Chest
  {
    OFFSET 0.00 10.00 0.00
    CHANNELS 3 Zrotation Xrotation Yrotation
    End Site
    {
      OFFSET 0.00 10.00 0.00
    }
  }
}
MOTION
Frames: 3
Frame Time: 0.0333333
0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00
0.00 0.50 0.00 5.00 0.00 0.00 2.00 0.00 0.00
0.00 1.00 0.00 10.00 0.00 0.00 4.00 0.00 0.00
"""


def _run_example(name: str, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(EXAMPLES / name), *args],
        cwd=str(ROOT),
        capture_output=True,
        text=True,
        check=False,
    )


class ExampleSmokeTests(unittest.TestCase):
    def test_bvh_compress_runs(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            proc = _run_example("bvh_compress.py", "--output-dir", tmpdir)
            self.assertEqual(proc.returncode, 0, proc.stderr)
            payload = json.loads(proc.stdout)
            self.assertGreater(payload["compression_ratio"], 1.0)
            self.assertTrue((Path(tmpdir) / "bvh_compress_summary.json").exists())

    def test_blender_preview_generates_script(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            proc = _run_example("blender_preview.py", "--output-dir", tmpdir)
            self.assertEqual(proc.returncode, 0, proc.stderr)
            payload = json.loads(proc.stdout)
            self.assertTrue(Path(payload["decoded_json"]).exists())
            self.assertTrue(Path(payload["blender_script"]).exists())

    def test_cmu_offline_demo_runs_with_file_url(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            local_bvh = Path(tmpdir) / "sample.bvh"
            local_bvh.write_text(MINIMAL_BVH, encoding="utf-8")
            proc = _run_example(
                "cmu_offline_demo.py",
                "--sample-url",
                local_bvh.as_uri(),
                "--output-dir",
                tmpdir,
                "--cache-dir",
                str(Path(tmpdir) / "cache"),
            )
            self.assertEqual(proc.returncode, 0, proc.stderr)
            payload = json.loads(proc.stdout)
            self.assertEqual(payload["source_url"], local_bvh.as_uri())
            self.assertTrue((Path(tmpdir) / "cmu_offline_demo_summary.json").exists())


if __name__ == "__main__":
    unittest.main()
