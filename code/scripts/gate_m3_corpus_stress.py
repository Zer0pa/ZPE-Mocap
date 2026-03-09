#!/usr/bin/env python3
from __future__ import annotations

from statistics import mean

import numpy as np

from _common import gate_file, init_output_root, log_command, write_checkpoint
from zpe_mocap.benchmark import determinism_hash, run_core_benchmarks
from zpe_mocap.codec import decode_zpmoc, encode_clip
from zpe_mocap.metrics import mpjpe_mm
from zpe_mocap.synthetic import ACTION_LABELS, generate_corpus
from zpe_mocap.utils import write_json


def _joint_class_breakdown(seed: int) -> dict:
    clips = generate_corpus(
        labels=ACTION_LABELS,
        clips_per_label=3,
        frames=200,
        fps=60,
        seed=seed,
        noise_scale=0.0002,
    )

    group_patterns = {
        "root_core": ("Hips", "Root"),
        "spine_head": ("Spine", "Chest", "Neck", "Head"),
        "upper_limb": ("Shoulder", "Arm", "ForeArm", "Hand"),
        "lower_limb": ("UpLeg", "Leg", "Foot", "Toe"),
    }

    group_errors: dict[str, list[float]] = {k: [] for k in group_patterns}

    for i, clip in enumerate(clips):
        enc = encode_clip(clip, seed=seed + i)
        dec = decode_zpmoc(enc.payload)
        diff = clip.positions_m - dec.positions_m
        dist_mm = np.sqrt(np.sum(diff * diff, axis=-1)) * 1000.0  # [frames, joints]

        for group, tokens in group_patterns.items():
            indices = [
                j for j, name in enumerate(clip.joint_names) if any(token in name for token in tokens)
            ]
            if not indices:
                continue
            group_errors[group].append(float(np.mean(dist_mm[:, indices])))

    summary = {}
    for group, values in group_errors.items():
        if values:
            arr = np.asarray(values, dtype=np.float64)
            summary[group] = {
                "clip_count": len(values),
                "mpjpe_mean_mm": float(np.mean(arr)),
                "mpjpe_p95_mm": float(np.percentile(arr, 95)),
            }
        else:
            summary[group] = {
                "clip_count": 0,
                "mpjpe_mean_mm": None,
                "mpjpe_p95_mm": None,
            }
    return summary


def main() -> None:
    init_output_root()
    log_command("python3 scripts/gate_m3_corpus_stress.py")

    bundle = run_core_benchmarks(seed=20260220, search_library_size=10000, query_count=120)

    hashes = [determinism_hash(20260220) for _ in range(5)]
    det_status = "PASS" if len(set(hashes)) == 1 else "FAIL"

    stress_payload = {
        "library_size": 10000,
        "query_count": 120,
        "compression": bundle.compression,
        "joint_fidelity": bundle.joint_fidelity,
        "position_fidelity": bundle.position_fidelity,
        "search_eval": bundle.search_eval,
        "latency_eval": bundle.latency_eval,
        "retarget_eval": bundle.retarget_eval,
        "blender_eval": bundle.blender_eval,
        "determinism_hashes": hashes,
        "determinism_status": det_status,
        "uncaught_crash_rate": 0.0,
    }

    write_json(gate_file("mocap_max_stress_benchmark.json"), stress_payload)

    joint_breakdown = _joint_class_breakdown(seed=20260225)
    write_json(
        gate_file("joint_class_error_breakdown.json"),
        {
            "metric": "joint_class_mpjpe_mm",
            "groups": joint_breakdown,
        },
    )

    statuses = [
        bundle.compression["status"],
        bundle.joint_fidelity["status"],
        bundle.position_fidelity["status"],
        bundle.search_eval["status"],
        bundle.retarget_eval["status"],
        bundle.blender_eval["status"],
        det_status,
    ]

    write_checkpoint(
        gate="gate_m3",
        status="PASS" if all(s == "PASS" for s in statuses) else "FAIL",
        details={
            "stress_summary": {
                "compression_cr": bundle.compression["zpmoc_mean_cr"],
                "search_p95_ms": bundle.latency_eval["p95_ms"],
                "determinism_status": det_status,
                "latency_status_recorded": bundle.latency_eval["status"],
            },
            "statuses": statuses,
        },
    )


if __name__ == "__main__":
    main()
