#!/usr/bin/env python3
from __future__ import annotations

import re
from pathlib import Path

import numpy as np

from _common import (
    EXTERNAL_ROOT,
    ROOT,
    gate_file,
    init_output_root,
    load_env_file,
    log_command,
    preferred_cmake_candidates,
    preferred_python,
    run_command,
    write_checkpoint,
)
from zpe_mocap.codec import encode_clip
from zpe_mocap.constants import ACTION_LABELS
from zpe_mocap.synthetic import MotionClip, generate_corpus
from zpe_mocap.utils import write_json


def _pick_cmake(evidence: list[dict]) -> str:
    for candidate in preferred_cmake_candidates():
        check = run_command([candidate, "--version"], timeout_sec=30)
        evidence.append(check)
        if check["exit_code"] == 0:
            return candidate
    return ""


def _find_acl_tool(build_dir: Path) -> str:
    direct = build_dir / "tools" / "acl_compressor" / "main_generic" / "acl_compressor"
    if direct.exists():
        return str(direct)
    for candidate in build_dir.rglob("acl_compressor"):
        if candidate.is_file():
            return str(candidate)
    for candidate in build_dir.rglob("acl_compressor.exe"):
        if candidate.is_file():
            return str(candidate)
    return ""


def _write_acl_sjson(clip: MotionClip, path: Path) -> None:
    positions = clip.positions_m
    lines: list[str] = []
    lines.append("version = 5")
    lines.append("")
    lines.append("clip =")
    lines.append("{")
    lines.append(f'  name = "{clip.clip_id}"')
    lines.append(f"  num_samples = {positions.shape[0]}")
    lines.append(f"  sample_rate = {clip.fps}")
    lines.append("  is_binary_exact = false")
    lines.append("}")
    lines.append("")
    lines.append("settings =")
    lines.append("{")
    lines.append('  algorithm_name = "uniformly_sampled"')
    lines.append('  rotation_format = "quatf_full"')
    lines.append('  translation_format = "vector3f_full"')
    lines.append('  scale_format = "vector3f_full"')
    lines.append("}")
    lines.append("")
    lines.append("bones =")
    lines.append("[")
    for joint_idx, name in enumerate(clip.joint_names):
        parent_idx = clip.parents[joint_idx]
        parent_name = "" if parent_idx < 0 else clip.joint_names[parent_idx]
        lines.append("  {")
        lines.append(f'    name = "{name}"')
        lines.append(f'    parent = "{parent_name}"')
        lines.append("    vertex_distance = 1.0")
        lines.append("    bind_rotation = [ 0.0, 0.0, 0.0, 1.0 ]")
        lines.append("    bind_translation = [ 0.0, 0.0, 0.0 ]")
        lines.append("    bind_scale = [ 1.0, 1.0, 1.0 ]")
        lines.append("  }")
    lines.append("]")
    lines.append("")
    lines.append("tracks =")
    lines.append("[")
    for joint_idx, name in enumerate(clip.joint_names):
        parent_idx = clip.parents[joint_idx]
        if parent_idx < 0:
            local = positions[:, joint_idx, :]
        else:
            local = positions[:, joint_idx, :] - positions[:, parent_idx, :]

        lines.append("  {")
        lines.append(f'    name = "{name}"')
        lines.append("    rotations =")
        lines.append("    [")
        for _ in range(local.shape[0]):
            lines.append("      [ 0.0, 0.0, 0.0, 1.0 ]")
        lines.append("    ]")
        lines.append("    translations =")
        lines.append("    [")
        for row in local:
            lines.append(f"      [ {row[0]:.9f}, {row[1]:.9f}, {row[2]:.9f} ]")
        lines.append("    ]")
        lines.append("    scales =")
        lines.append("    [")
        for _ in range(local.shape[0]):
            lines.append("      [ 1.0, 1.0, 1.0 ]")
        lines.append("    ]")
        lines.append("  }")
    lines.append("]")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def _parse_acl_ratio(stats_path: Path) -> float | None:
    if not stats_path.exists():
        return None
    text = stats_path.read_text(encoding="utf-8", errors="ignore")
    match = re.search(r"compression_ratio\\s*=\\s*([-+0-9eE.]+)", text)
    if not match:
        return None
    return float(match.group(1))


def main() -> None:
    init_output_root()
    log_command("python3 code/scripts/gate_m1_acl_comparator.py")
    env_report = load_env_file()

    external = EXTERNAL_ROOT
    external.mkdir(parents=True, exist_ok=True)
    acl_dir = external / "acl"

    evidence = []

    # Attempt canonical bootstrap command from startup prompt for evidence.
    evidence.append(
        run_command(
            [
                "zsh",
                "-lc",
                "set -a; [ -f .env ] && source .env; set +a; echo BOOTSTRAP_OK",
            ],
            timeout_sec=30,
        )
    )

    evidence.append(run_command([preferred_python(), "-m", "pip", "install", "cmake", "ninja"], timeout_sec=300))

    if acl_dir.exists():
        evidence.append(run_command(["git", "-C", str(acl_dir), "pull", "--ff-only"]))
    else:
        evidence.append(run_command(["git", "clone", "--depth", "1", "https://github.com/nfrechette/acl", str(acl_dir)]))

    evidence.append(run_command(["git", "-C", str(acl_dir), "submodule", "update", "--init", "--recursive"], timeout_sec=600))

    cmake_exe = _pick_cmake(evidence)
    build_ok = False
    acl_tool_exists = False
    acl_tool_path = ""

    if cmake_exe and acl_dir.exists():
        build_dir = acl_dir / "build_make"
        evidence.append(
            run_command(
                [
                    cmake_exe,
                    "-S",
                    str(acl_dir),
                    "-B",
                    str(build_dir),
                    "-G",
                    "Unix Makefiles",
                    "-DCMAKE_C_COMPILER=/usr/bin/clang",
                    "-DCMAKE_CXX_COMPILER=/usr/bin/clang++",
                    "-DUSE_SIMD_INSTRUCTIONS=OFF",
                ],
                timeout_sec=240,
            )
        )
        if build_dir.exists():
            acl_tool_path = _find_acl_tool(build_dir)
            acl_tool_exists = bool(acl_tool_path)

        if acl_tool_exists:
            build_ok = True
            evidence.append(
                {
                    "cmd": "skip full ACL rebuild; acl_compressor already present",
                    "cwd": str(build_dir),
                    "exit_code": 0,
                    "stdout_tail": acl_tool_path,
                    "stderr_tail": "",
                    "timed_out": False,
                }
            )
        else:
            build_result = run_command(
                [cmake_exe, "--build", str(build_dir), "--target", "acl_compressor", "-j2"],
                timeout_sec=900,
            )
            evidence.append(build_result)
            build_ok = build_result["exit_code"] == 0

            if build_dir.exists():
                acl_tool_path = _find_acl_tool(build_dir)
                acl_tool_exists = bool(acl_tool_path)

    if acl_tool_exists:
        evidence.append(run_command([acl_tool_path], timeout_sec=30))

    comparator_rows: list[dict] = []
    acl_ratios_from_stats: list[float] = []
    acl_ratios_same_raw: list[float] = []
    zpmoc_ratios: list[float] = []

    if acl_tool_exists:
        corpus = generate_corpus(
            labels=ACTION_LABELS,
            clips_per_label=1,
            frames=120,
            fps=60,
            seed=20260220,
            noise_scale=0.0002,
        )
        raw_dir = gate_file("tmp/acl_direct_raw")
        stats_dir = gate_file("tmp/acl_direct_stats")
        out_dir = gate_file("tmp/acl_direct_out")
        raw_dir.mkdir(parents=True, exist_ok=True)
        stats_dir.mkdir(parents=True, exist_ok=True)
        out_dir.mkdir(parents=True, exist_ok=True)

        for idx, clip in enumerate(corpus):
            acl_input = raw_dir / f"{clip.clip_id}.acl.sjson"
            acl_stats = stats_dir / f"{clip.clip_id}_stats.sjson"
            acl_out = out_dir / f"{clip.clip_id}.acl"

            _write_acl_sjson(clip, acl_input)
            run = run_command(
                [
                    acl_tool_path,
                    f"-acl={acl_input}",
                    f"-stats={acl_stats}",
                    f"-out={acl_out}",
                    "-level=medium",
                ],
                timeout_sec=120,
            )
            evidence.append(run)
            if run["exit_code"] != 0 or not acl_out.exists():
                continue

            encoded = encode_clip(clip, seed=20260220 + idx)
            acl_size = acl_out.stat().st_size
            if acl_size <= 0:
                continue

            acl_ratio_same_raw = float(encoded.raw_bvh_float32_bytes) / float(acl_size)
            acl_ratio_stats = _parse_acl_ratio(acl_stats)
            if acl_ratio_stats is not None:
                acl_ratios_from_stats.append(float(acl_ratio_stats))
            acl_ratios_same_raw.append(acl_ratio_same_raw)
            zpmoc_ratios.append(float(encoded.compression_ratio))
            comparator_rows.append(
                {
                    "clip_id": clip.clip_id,
                    "zpmoc_ratio_vs_raw_bvh32": float(encoded.compression_ratio),
                    "zpmoc_encoded_bytes": int(encoded.encoded_size_bytes),
                    "raw_bvh32_bytes": int(encoded.raw_bvh_float32_bytes),
                    "acl_compressed_bytes": int(acl_size),
                    "acl_ratio_vs_same_raw_bvh32": acl_ratio_same_raw,
                    "acl_ratio_reported_by_acl": acl_ratio_stats,
                    "acl_input_path": str(acl_input),
                    "acl_output_path": str(acl_out),
                    "acl_stats_path": str(acl_stats),
                }
            )

    comparator_status = "FAIL"
    impracticality = None
    if not acl_tool_exists:
        impracticality = {
            "resource": "ACL direct comparator",
            "code": "IMP-ACCESS",
            "failure_signature": "acl_compressor binary unavailable after build attempt",
            "fallback": "retain ZPMOC-only benchmark and keep max-wave ACL parity FAIL",
            "claim_impact": "MOC-C001 max-wave comparator parity remains explicit FAIL until direct ACL run exists",
        }
    elif len(comparator_rows) < 5:
        impracticality = {
            "resource": "ACL direct comparator",
            "code": "IMP-NOCODE",
            "failure_signature": "insufficient successful ACL compressions on deterministic corpus",
            "fallback": "retain partial direct-comparator rows and keep max-wave ACL parity FAIL",
            "claim_impact": "MOC-C001 max-wave comparator parity remains explicit FAIL",
        }
    else:
        comparator_status = "PASS"

    summary = {
        "status": comparator_status,
        "clips_attempted": len(ACTION_LABELS),
        "clips_compared": len(comparator_rows),
        "zpmoc_mean_ratio": float(np.mean(zpmoc_ratios)) if zpmoc_ratios else None,
        "acl_mean_ratio_same_raw_bvh32": float(np.mean(acl_ratios_same_raw)) if acl_ratios_same_raw else None,
        "acl_mean_ratio_reported_by_acl": float(np.mean(acl_ratios_from_stats)) if acl_ratios_from_stats else None,
        "same_corpus": True,
    }

    table = {
        "gate": "M1",
        "acl_repo_present": acl_dir.exists(),
        "acl_build_ok": build_ok,
        "acl_tool_path": acl_tool_path,
        "direct_comparator_status": comparator_status,
        "direct_comparator_summary": summary,
        "direct_comparator_rows": comparator_rows,
        "impracticality": impracticality,
        "env_report": {
            "exists": env_report.get("exists"),
            "loaded_keys": env_report.get("loaded_keys", []),
            "parse_errors": env_report.get("parse_errors", []),
        },
        "attempt_evidence": evidence,
    }

    write_json(gate_file("acl_direct_comparator_table.json"), table)

    write_checkpoint(
        gate="gate_m1",
        status="PASS" if comparator_status == "PASS" else "FAIL",
        details={
            "comparator_status": comparator_status,
            "acl_tool_path": acl_tool_path,
            "clips_compared": len(comparator_rows),
            "impracticality": impracticality,
        },
    )


if __name__ == "__main__":
    main()
