#!/usr/bin/env python3
from __future__ import annotations

from _common import gate_file, init_output_root, log_command, write_checkpoint
from zpe_mocap.benchmark import run_core_benchmarks
from zpe_mocap.utils import write_json


def main() -> None:
    init_output_root()
    log_command("python3 scripts/gate_c_benchmarks.py")

    bundle = run_core_benchmarks(seed=20260220)

    write_json(gate_file("mocap_compression_benchmark.json"), bundle.compression)
    write_json(gate_file("mocap_joint_fidelity.json"), bundle.joint_fidelity)
    write_json(gate_file("mocap_position_fidelity.json"), bundle.position_fidelity)
    write_json(gate_file("mocap_search_eval.json"), bundle.search_eval)
    write_json(gate_file("mocap_query_latency.json"), bundle.latency_eval)
    write_json(gate_file("mocap_retarget_eval.json"), bundle.retarget_eval)
    write_json(gate_file("mocap_blender_roundtrip.json"), bundle.blender_eval)

    statuses = {
        "MOC-C001": bundle.compression["status"],
        "MOC-C002": bundle.joint_fidelity["status"],
        "MOC-C003": bundle.position_fidelity["status"],
        "MOC-C004": bundle.search_eval["status"],
        "MOC-C005": bundle.latency_eval["status"],
        "MOC-C006": bundle.retarget_eval["status"],
        "MOC-C007": bundle.blender_eval["status"],
    }

    write_checkpoint(
        gate="gate_c",
        status="PASS" if all(v == "PASS" for v in statuses.values()) else "FAIL",
        details={
            "claim_statuses": statuses,
        },
    )


if __name__ == "__main__":
    main()
