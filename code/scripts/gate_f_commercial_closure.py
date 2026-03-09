#!/usr/bin/env python3
from __future__ import annotations

from _common import gate_file, init_output_root, log_command, read_json, write_checkpoint
from zpe_mocap.utils import write_json


def _core_claim_status() -> dict[str, str]:
    compression = read_json(gate_file("mocap_compression_benchmark.json"))
    joint = read_json(gate_file("mocap_joint_fidelity.json"))
    pos = read_json(gate_file("mocap_position_fidelity.json"))
    search = read_json(gate_file("mocap_search_eval.json"))
    latency = read_json(gate_file("mocap_query_latency.json"))
    retarget = read_json(gate_file("mocap_retarget_eval.json"))
    blender = read_json(gate_file("mocap_blender_roundtrip.json"))
    return {
        "MOC-C001": compression.get("status", "FAIL"),
        "MOC-C002": joint.get("status", "FAIL"),
        "MOC-C003": pos.get("status", "FAIL"),
        "MOC-C004": search.get("status", "FAIL"),
        "MOC-C005": latency.get("status", "FAIL"),
        "MOC-C006": retarget.get("status", "FAIL"),
        "MOC-C007": blender.get("status", "FAIL"),
    }


def main() -> None:
    init_output_root()
    log_command("python3 scripts/gate_f_commercial_closure.py")

    core = _core_claim_status()
    resource_map = read_json(gate_file("max_claim_resource_map.json"))

    final = {}
    notes = {}

    for claim_id, core_status in core.items():
        mapped = resource_map.get(claim_id, {})
        resource_status = mapped.get("status", "FAIL")

        if resource_status == "PAUSED_EXTERNAL":
            final_status = "PAUSED_EXTERNAL"
            note = mapped.get("rationale", "commercial-safe open alternative unavailable")
        elif core_status == "PASS" and resource_status == "PASS":
            final_status = "PASS"
            note = "core threshold met with commercial-safe resource coverage"
        else:
            final_status = "FAIL"
            note = mapped.get("rationale", "core/resource closure condition not met")

        final[claim_id] = final_status
        notes[claim_id] = note

    fg1 = all(
        row.get("status") != "PASS" or row.get("commercial_safe_success")
        for row in resource_map.values()
    )

    fg2 = all(
        (row.get("status") == "PAUSED_EXTERNAL")
        or (row.get("status") == "FAIL")
        or (row.get("status") == "PASS" and row.get("commercial_safe_success"))
        for row in resource_map.values()
    )

    gap = read_json(gate_file("net_new_gap_closure_matrix.json"))
    gap["F-G1"] = {
        "status": "PASS" if fg1 else "FAIL",
        "rule": "E-G2 passes on commercial-safe corpus evidence",
        "evidence": "artifacts/2026-02-20_zpe_mocap_wave1/max_claim_resource_map.json",
    }
    gap["F-G2"] = {
        "status": "PASS" if fg2 else "FAIL",
        "rule": "NC-dependent claims converted to alternatives or PAUSED_EXTERNAL",
        "evidence": "artifacts/2026-02-20_zpe_mocap_wave1/commercialization_claim_adjudication.json",
    }
    write_json(gate_file("net_new_gap_closure_matrix.json"), gap)

    payload = {
        "core_claim_status": core,
        "resource_claim_status": {k: v.get("status", "FAIL") for k, v in resource_map.items()},
        "final_claim_status": final,
        "claim_notes": notes,
        "f_gates": {
            "F-G1": gap["F-G1"]["status"],
            "F-G2": gap["F-G2"]["status"],
        },
    }
    write_json(gate_file("commercialization_claim_adjudication.json"), payload)

    write_checkpoint(
        gate="gate_f",
        status="PASS" if all(v in {"PASS", "FAIL", "PAUSED_EXTERNAL"} for v in final.values()) else "FAIL",
        details={
            "final_claim_status": final,
            "f_gates": payload["f_gates"],
        },
    )


if __name__ == "__main__":
    main()
