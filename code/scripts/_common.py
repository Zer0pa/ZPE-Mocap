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
if str(CODE_ROOT) not in sys.path:
    sys.path.insert(0, str(CODE_ROOT))

from zpe_mocap.constants import CHECKPOINT_DIR, OUTPUT_ROOT  # noqa: E402
from zpe_mocap.utils import append_line, ensure_dir, sha256_path, write_json  # noqa: E402

REPO_VENV_PYTHON = ROOT / ".venv" / "bin" / "python"
WORKSPACE_VENV_PYTHON = WORKSPACE_ROOT / ".venv" / "bin" / "python"
REPO_VENV_CMAKE = ROOT / ".venv" / "bin" / "cmake"
WORKSPACE_VENV_CMAKE = WORKSPACE_ROOT / ".venv" / "bin" / "cmake"
EXTERNAL_ROOT = Path(os.environ.get("ZPE_MOCAP_EXTERNAL_ROOT", str(WORKSPACE_ROOT / "external")))

COMMAND_LOG = OUTPUT_ROOT / "command_log.txt"
RUN_MANIFEST = OUTPUT_ROOT / "RUN_MANIFEST.json"

COMET_PROJECT_NAME = "zpe-mocap"
COMET_WORKSPACE = "zer0pa"


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def init_output_root() -> None:
    ensure_dir(OUTPUT_ROOT)
    ensure_dir(CHECKPOINT_DIR)


def log_command(cmd: str) -> None:
    append_line(COMMAND_LOG, f"[{now_iso()}] {cmd}")


def write_checkpoint(
    gate: str,
    status: str,
    details: dict[str, Any],
    comet_url: str | None = None,
) -> None:
    payload = {
        "gate": gate,
        "status": status,
        "timestamp_utc": now_iso(),
        "details": details,
    }
    if comet_url:
        payload["comet_experiment_url"] = comet_url
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


def init_comet_context(gate_name: str, corpus: str) -> dict[str, Any]:
    env_report = load_env_file()
    api_key = os.environ.get("COMET_API_KEY")
    if not api_key:
        return {"enabled": False, "reason": "missing_api_key", "env_report": env_report}

    try:
        import comet_ml  # type: ignore
    except Exception as exc:  # pragma: no cover - optional dependency
        return {"enabled": False, "reason": f"comet_import_failed:{exc}", "env_report": env_report}

    experiment = comet_ml.Experiment(
        project_name=COMET_PROJECT_NAME,
        workspace=COMET_WORKSPACE,
        auto_log_co2=False,
    )
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    experiment.set_name(f"gate_{gate_name}_{corpus}_{timestamp}")
    experiment.add_tag("zpe-mocap")
    experiment.add_tag(corpus)
    return {"enabled": True, "experiment": experiment, "env_report": env_report}


def comet_log_metrics(context: dict[str, Any], metrics: dict[str, Any]) -> None:
    if not context.get("enabled"):
        return
    experiment = context["experiment"]
    for key, value in metrics.items():
        experiment.log_metric(key, value)


def comet_log_asset(context: dict[str, Any], path: Path) -> None:
    if not context.get("enabled"):
        return
    if path.exists():
        context["experiment"].log_asset(str(path))


def finalize_comet(context: dict[str, Any]) -> str | None:
    if not context.get("enabled"):
        return None
    experiment = context["experiment"]
    url = getattr(experiment, "get_url", lambda: None)()
    if not url:
        url = getattr(experiment, "url", None)
    experiment.end()
    return url


def update_run_manifest(entry: dict[str, Any]) -> None:
    payload = {"runs": []}
    if RUN_MANIFEST.exists():
        payload = read_json(RUN_MANIFEST)
        if not isinstance(payload, dict):
            payload = {"runs": []}
    runs = payload.get("runs")
    if not isinstance(runs, list):
        runs = []
    runs.append(entry)
    payload["runs"] = runs
    write_json(RUN_MANIFEST, payload)


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


def resolve_corpus(default: str = "synthetic") -> str:
    return os.environ.get("ZPE_MOCAP_CORPUS", default)


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
