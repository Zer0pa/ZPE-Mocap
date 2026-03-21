#!/usr/bin/env python3
from __future__ import annotations

from _common import (
    comet_log_asset,
    comet_log_metrics,
    finalize_comet,
    gate_file,
    init_comet_context,
    init_output_root,
    log_command,
    now_iso,
    resolve_corpus,
    update_run_manifest,
    write_checkpoint,
)
from zpe_mocap.benchmark import run_core_benchmarks
from zpe_mocap.cmu import load_cmu_clips
from zpe_mocap.constants import ACTION_LABELS
from zpe_mocap.utils import write_json


def main() -> None:
    init_output_root()
    log_command("python3 scripts/gate_c_benchmarks.py")
    corpus = resolve_corpus()
    comet = init_comet_context("gate_c", corpus)

    clips = None
    if corpus != "synthetic":
        clips = load_cmu_clips(max_clips=500, required_labels=ACTION_LABELS)
    bundle = run_core_benchmarks(seed=20260220, clips=clips)

    write_json(gate_file("mocap_compression_benchmark.json"), bundle.compression)
    write_json(gate_file("mocap_joint_fidelity.json"), bundle.joint_fidelity)
    write_json(gate_file("mocap_position_fidelity.json"), bundle.position_fidelity)
    write_json(gate_file("mocap_search_eval.json"), bundle.search_eval)
    write_json(gate_file("mocap_query_latency.json"), bundle.latency_eval)
    write_json(gate_file("mocap_retarget_eval.json"), bundle.retarget_eval)
    write_json(gate_file("mocap_blender_roundtrip.json"), bundle.blender_eval)

    comet_log_metrics(
        comet,
        {
            "compression_ratio_mean": bundle.compression.get("zpmoc_mean_cr"),
            "joint_rmse_deg_mean": bundle.joint_fidelity.get("rmse_mean_deg"),
            "mpjpe_mm_mean": bundle.position_fidelity.get("mpjpe_mean_mm"),
            "search_p_at_10": bundle.search_eval.get("p_at_10"),
            "search_latency_p50_ms": bundle.latency_eval.get("p50_ms"),
            "search_latency_p95_ms": bundle.latency_eval.get("p95_ms"),
            "search_latency_p99_ms": bundle.latency_eval.get("p99_ms"),
            "retarget_mpjpe_mm": bundle.retarget_eval.get("mpjpe_mean_mm"),
            "corpus_type": 0 if corpus == "synthetic" else 1,
        },
    )
    for name in (
        "mocap_compression_benchmark.json",
        "mocap_joint_fidelity.json",
        "mocap_position_fidelity.json",
        "mocap_search_eval.json",
        "mocap_query_latency.json",
        "mocap_retarget_eval.json",
        "mocap_blender_roundtrip.json",
    ):
        comet_log_asset(comet, gate_file(name))

    statuses = {
        "MOC-C001": bundle.compression["status"],
        "MOC-C002": bundle.joint_fidelity["status"],
        "MOC-C003": bundle.position_fidelity["status"],
        "MOC-C004": bundle.search_eval["status"],
        "MOC-C005": bundle.latency_eval["status"],
        "MOC-C006": bundle.retarget_eval["status"],
        "MOC-C007": bundle.blender_eval["status"],
    }

    comet_url = finalize_comet(comet)
    write_checkpoint(
        gate="gate_c",
        status="PASS" if all(v == "PASS" for v in statuses.values()) else "FAIL",
        details={
            "claim_statuses": statuses,
        },
        comet_url=comet_url,
    )
    update_run_manifest(
        {
            "gate": "gate_c",
            "corpus": corpus,
            "status": "PASS" if all(v == "PASS" for v in statuses.values()) else "FAIL",
            "timestamp_utc": now_iso(),
            "comet_experiment_url": comet_url,
        }
    )


if __name__ == "__main__":
    main()
