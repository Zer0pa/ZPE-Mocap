from __future__ import annotations

import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

CODE_ROOT = Path(__file__).resolve().parents[1]
ROOT = CODE_ROOT.parent
WORKSPACE_ROOT = ROOT.parent
SRC = CODE_ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from zpe_mocap.constants import CHECKPOINT_DIR, OUTPUT_ROOT  # noqa: E402
from zpe_mocap.utils import append_line, ensure_dir, sha256_path, write_json  # noqa: E402

REPO_VENV_PYTHON = ROOT / ".venv" / "bin" / "python"
WORKSPACE_VENV_PYTHON = WORKSPACE_ROOT / ".venv" / "bin" / "python"
REPO_VENV_CMAKE = ROOT / ".venv" / "bin" / "cmake"
WORKSPACE_VENV_CMAKE = WORKSPACE_ROOT / ".venv" / "bin" / "cmake"
EXTERNAL_ROOT = Path(os.environ.get("ZPE_MOCAP_EXTERNAL_ROOT", str(WORKSPACE_ROOT / "external")))

COMMAND_LOG = OUTPUT_ROOT / "command_log.txt"


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def init_output_root() -> None:
    ensure_dir(OUTPUT_ROOT)
    ensure_dir(CHECKPOINT_DIR)


def log_command(cmd: str) -> None:
    append_line(COMMAND_LOG, f"[{now_iso()}] {cmd}")


def write_checkpoint(gate: str, status: str, details: dict[str, Any]) -> None:
    payload = {
        "gate": gate,
        "status": status,
        "timestamp_utc": now_iso(),
        "details": details,
    }
    write_json(CHECKPOINT_DIR / f"{gate}.json", payload)


def gate_file(path: str) -> Path:
    return OUTPUT_ROOT / path


def collect_hashes(paths: list[Path]) -> dict[str, str]:
    out: dict[str, str] = {}
    for path in paths:
        if path.exists():
            out[str(path)] = sha256_path(path)
    return out


def write_text(path: Path, text: str) -> None:
    ensure_dir(path.parent)
    path.write_text(text, encoding="utf-8")


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def load_env_file(path: Path | None = None) -> dict[str, Any]:
    env_path = path or (ROOT / ".env")
    report: dict[str, Any] = {
        "path": str(env_path),
        "exists": env_path.exists(),
        "loaded_keys": [],
        "parse_errors": [],
    }
    if not env_path.exists():
        return report

    for lineno, raw_line in enumerate(env_path.read_text(encoding="utf-8").splitlines(), start=1):
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if "=" not in line:
            report["parse_errors"].append({"line": lineno, "reason": "missing_equals"})
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip()
        if not key:
            report["parse_errors"].append({"line": lineno, "reason": "empty_key"})
            continue
        if (value.startswith('"') and value.endswith('"')) or (value.startswith("'") and value.endswith("'")):
            value = value[1:-1]
        os.environ[key] = value
        report["loaded_keys"].append(key)
    return report


def preferred_python() -> str:
    for candidate in (REPO_VENV_PYTHON, WORKSPACE_VENV_PYTHON):
        if candidate.exists():
            return str(candidate)
    return sys.executable


def preferred_cmake_candidates() -> list[str]:
    return [
        "cmake",
        str(REPO_VENV_CMAKE),
        str(WORKSPACE_VENV_CMAKE),
    ]


def run_command(cmd: list[str], timeout_sec: int = 120, cwd: Path | None = None) -> dict[str, Any]:
    try:
        proc = subprocess.run(
            cmd,
            cwd=str(cwd or ROOT),
            capture_output=True,
            text=True,
            timeout=timeout_sec,
            check=False,
        )
        stdout = proc.stdout[-4000:]
        stderr = proc.stderr[-4000:]
        return {
            "cmd": " ".join(cmd),
            "cwd": str(cwd or ROOT),
            "exit_code": proc.returncode,
            "stdout_tail": stdout,
            "stderr_tail": stderr,
            "timed_out": False,
        }
    except subprocess.TimeoutExpired as exc:
        return {
            "cmd": " ".join(cmd),
            "cwd": str(cwd or ROOT),
            "exit_code": None,
            "stdout_tail": (exc.stdout or "")[-4000:] if isinstance(exc.stdout, str) else "",
            "stderr_tail": (exc.stderr or "")[-4000:] if isinstance(exc.stderr, str) else "",
            "timed_out": True,
        }
    except FileNotFoundError as exc:
        return {
            "cmd": " ".join(cmd),
            "cwd": str(cwd or ROOT),
            "exit_code": None,
            "stdout_tail": "",
            "stderr_tail": str(exc),
            "timed_out": False,
        }
