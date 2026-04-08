from __future__ import annotations

import os
import subprocess
import sys
import tempfile
import unittest

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CODE_DIR = ROOT / "code"


def _venv_python(venv_dir: Path) -> Path:
    if os.name == "nt":
        return venv_dir / "Scripts" / "python.exe"
    return venv_dir / "bin" / "python"


class CleanInstallTests(unittest.TestCase):
    def test_local_package_installs_in_fresh_venv(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            venv_dir = Path(tmpdir) / "venv"
            subprocess.run([sys.executable, "-m", "venv", str(venv_dir)], check=True, capture_output=True, text=True)
            py = _venv_python(venv_dir)
            subprocess.run([str(py), "-m", "pip", "install", "--upgrade", "pip"], check=True, capture_output=True, text=True)
            subprocess.run([str(py), "-m", "pip", "install", str(CODE_DIR)], check=True, capture_output=True, text=True)
            proc = subprocess.run(
                [str(py), "-c", "import zpe_mocap; print(zpe_mocap.__version__)"],
                check=True,
                capture_output=True,
                text=True,
            )
            self.assertEqual(proc.stdout.strip(), "0.1.0")


if __name__ == "__main__":
    unittest.main()
