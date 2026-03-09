#!/usr/bin/env python3
from __future__ import annotations

import subprocess
import sys

from _common import ROOT, gate_file, init_output_root, log_command, read_json, write_checkpoint, write_text
from zpe_mocap.utils import write_json


def main() -> None:
    init_output_root()
    log_command("python3 scripts/gate_e_runpod_readiness.py")

    impracticality_path = gate_file("impracticality_decisions.json")
    decisions = read_json(impracticality_path).get("decisions", []) if impracticality_path.exists() else []

    imp_compute = [d for d in decisions if d.get("code") == "IMP-COMPUTE"]
    required = len(imp_compute) > 0
    lock_path = gate_file("runpod_requirements_lock.txt")

    freeze = subprocess.run(
        [sys.executable, "-m", "pip", "freeze"],
        cwd=str(ROOT),
        capture_output=True,
        text=True,
        check=False,
    )
    if freeze.returncode == 0 and freeze.stdout.strip():
        lock_path.write_text(freeze.stdout, encoding="utf-8")
    else:
        lock_path.write_text("# failed to generate pip freeze lock\n", encoding="utf-8")

    command_chain = [
        "python3 scripts/gate_a_setup.py",
        "python3 scripts/gate_b_build.py",
        "python3 scripts/gate_c_benchmarks.py",
        "python3 scripts/gate_d_falsification.py",
        "python3 scripts/gate_m3_corpus_stress.py",
        "python3 scripts/gate_m4_replay_core_claims.py",
        "python3 scripts/gate_f_commercial_closure.py",
        "python3 scripts/gate_e_package.py",
    ]
    expected_manifest = [
        "handoff_manifest.json",
        "before_after_metrics.json",
        "falsification_results.md",
        "claim_status_delta.md",
        "command_log.txt",
        "quality_gate_scorecard.json",
        "net_new_gap_closure_matrix.json",
        "impracticality_decisions.json",
        "runpod_readiness_manifest.json",
        "runpod_exec_plan.md",
        "runpod_requirements_lock.txt",
    ]

    manifest = {
        "required": required,
        "gpu_path": "CONDITIONAL",
        "reason": "IMP-COMPUTE present" if required else "No IMP-COMPUTE items recorded",
        "tasks": [
            {
                "resource": item.get("resource"),
                "failure_signature": item.get("failure_signature"),
                "fallback": item.get("fallback"),
            }
            for item in imp_compute
        ],
        "image": "runpod/pytorch:2.3.1-cuda12.1-cudnn8-devel",
        "entrypoint": "python3 scripts/gate_m3_corpus_stress.py && python3 scripts/gate_m4_replay_core_claims.py",
        "determinism_seed": 20260220,
        "deps_lock_file": "artifacts/2026-02-20_zpe_mocap_wave1/runpod_requirements_lock.txt",
        "exact_command_chain": command_chain,
        "expected_artifact_manifest": expected_manifest,
    }
    write_json(gate_file("runpod_readiness_manifest.json"), manifest)

    plan_lines = [
        "# RunPod Execution Plan",
        "",
        f"- required: `{required}`",
        f"- reason: {manifest['reason']}",
        "- container_image: runpod/pytorch:2.3.1-cuda12.1-cudnn8-devel",
        "- execution_steps:",
        "  1. checkout lane repo snapshot",
        "  2. install Python deps from `.venv` parity list",
        "  3. install pinned dependencies from `runpod_requirements_lock.txt`",
        "  4. run exact command chain listed in runpod_readiness_manifest.json",
        "  5. upload expected artifact manifest to lane output root",
        "- lock_file: artifacts/2026-02-20_zpe_mocap_wave1/runpod_requirements_lock.txt",
        "- exact_command_chain:",
    ]
    for cmd in command_chain:
        plan_lines.append(f"  - `{cmd}`")
    plan_lines.append("- expected_artifact_manifest:")
    for item in expected_manifest:
        plan_lines.append(f"  - `{item}`")
    if required:
        plan_lines.append("- deferred_items:")
        for item in imp_compute:
            plan_lines.append(f"  - {item.get('resource')}: {item.get('failure_signature')}")

    write_text(gate_file("runpod_exec_plan.md"), "\n".join(plan_lines) + "\n")

    gap_path = gate_file("net_new_gap_closure_matrix.json")
    gap = read_json(gap_path) if gap_path.exists() else {}
    eg5_status = "PASS" if (not required or gate_file("runpod_readiness_manifest.json").exists()) else "FAIL"
    gap["E-G5"] = {
        "status": eg5_status,
        "rule": "RunPod artifacts required for IMP-COMPUTE",
        "evidence": "artifacts/2026-02-20_zpe_mocap_wave1/runpod_readiness_manifest.json; artifacts/2026-02-20_zpe_mocap_wave1/runpod_exec_plan.md",
    }
    write_json(gap_path, gap)

    write_checkpoint(
        gate="gate_e_g5",
        status=eg5_status,
        details={
            "required": required,
            "imp_compute_count": len(imp_compute),
        },
    )


if __name__ == "__main__":
    main()
