#!/usr/bin/env python3
from __future__ import annotations

from _common import gate_file, init_output_root, log_command, read_json, write_checkpoint
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

    write_checkpoint(
        gate="gate_m4",
        status=payload["status"],
        details={"max_replay_claims": final},
    )


if __name__ == "__main__":
    main()
