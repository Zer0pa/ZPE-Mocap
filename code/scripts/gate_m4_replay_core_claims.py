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
    read_json,
    resolve_corpus,
    update_run_manifest,
    write_checkpoint,
)
from zpe_mocap.utils import write_json


def _core_claims() -> dict[str, str]:
    compression = read_json(gate_file("mocap_compression_benchmark.json"))
    joint = read_json(gate_file("mocap_joint_fidelity.json"))
    pos = read_json(gate_file("mocap_position_fidelity.json"))
    search = read_json(gate_file("mocap_search_eval.json"))
    latency = read_json(gate_file("mocap_query_latency.json"))
    retarget = read_json(gate_file("mocap_retarget_eval.json"))
    blender = read_json(gate_file("mocap_blender_roundtrip.json"))

    return {
        "MOC-C001": compression.get("status", "UNTESTED"),
        "MOC-C002": joint.get("status", "UNTESTED"),
        "MOC-C003": pos.get("status", "UNTESTED"),
        "MOC-C004": search.get("status", "UNTESTED"),
        "MOC-C005": latency.get("status", "UNTESTED"),
        "MOC-C006": retarget.get("status", "UNTESTED"),
        "MOC-C007": blender.get("status", "UNTESTED"),
    }


def _stress_claims() -> dict[str, str]:
    stress = read_json(gate_file("mocap_max_stress_benchmark.json"))
    return {
        "MOC-C001": stress.get("compression", {}).get("status", "UNTESTED"),
        "MOC-C002": stress.get("joint_fidelity", {}).get("status", "UNTESTED"),
        "MOC-C003": stress.get("position_fidelity", {}).get("status", "UNTESTED"),
        "MOC-C004": stress.get("search_eval", {}).get("status", "UNTESTED"),
        "MOC-C005": stress.get("latency_eval", {}).get("status", "UNTESTED"),
        "MOC-C006": stress.get("retarget_eval", {}).get("status", "UNTESTED"),
        "MOC-C007": stress.get("blender_eval", {}).get("status", "UNTESTED"),
    }


def main() -> None:
    init_output_root()
    log_command("python3 scripts/gate_m4_replay_core_claims.py")
    corpus = resolve_corpus()
    comet = init_comet_context("gate_m4", corpus)

    core = _core_claims()
    stress = _stress_claims()

    final = {}
    for claim_id in core:
        if core[claim_id] == "PASS" and stress[claim_id] == "PASS":
            final[claim_id] = "PASS"
        else:
            final[claim_id] = "FAIL"

    payload = {
        "core_claims": core,
        "max_stress_claims": stress,
        "max_replay_claims": final,
        "status": "PASS" if all(v == "PASS" for v in final.values()) else "FAIL",
    }
    write_json(gate_file("max_core_claim_replay.json"), payload)

    comet_log_metrics(
        comet,
        {
            "max_replay_pass_count": sum(1 for v in final.values() if v == "PASS"),
            "max_replay_total": len(final),
            "corpus_type": 0 if corpus == "synthetic" else 1,
        },
    )
    comet_log_asset(comet, gate_file("max_core_claim_replay.json"))

    comet_url = finalize_comet(comet)
    write_checkpoint(
        gate="gate_m4",
        status=payload["status"],
        details={"max_replay_claims": final},
        comet_url=comet_url,
    )
    update_run_manifest(
        {
            "gate": "gate_m4",
            "corpus": corpus,
            "status": payload["status"],
            "timestamp_utc": now_iso(),
            "comet_experiment_url": comet_url,
        }
    )


if __name__ == "__main__":
    main()
