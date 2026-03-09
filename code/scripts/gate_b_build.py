#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path

import numpy as np

from _common import ROOT, gate_file, init_output_root, log_command, write_checkpoint
from zpe_mocap.codec import decode_zpmoc, encode_clip
from zpe_mocap.metrics import joint_rmse_deg, mpjpe_mm
from zpe_mocap.retarget import build_scaled_ground_truth, retarget_scale_space
from zpe_mocap.search import MotionSuffixIndex
from zpe_mocap.synthetic import generate_clip


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def main() -> None:
    init_output_root()
    log_command("python3 scripts/gate_b_build.py")

    clip = generate_clip(
        clip_id="gate_b_smoke",
        label="walk",
        frames=180,
        fps=60,
        seed=20260220,
        noise_scale=0.0002,
    )

    enc1 = encode_clip(clip, seed=20260220)
    enc2 = encode_clip(clip, seed=20260220)
    _require(enc1.payload == enc2.payload, "deterministic encode mismatch")

    dec = decode_zpmoc(enc1.payload)
    rmse = joint_rmse_deg(clip.angles_deg, dec.angles_deg)
    pos = mpjpe_mm(clip.positions_m, dec.positions_m)
    _require(rmse <= 1.0, f"joint RMSE smoke failed: {rmse}")
    _require(pos <= 5.0, f"MPJPE smoke failed: {pos}")

    idx = MotionSuffixIndex(k=6)
    tokens = [0, 1, 2, 3, 4, 5, 6, 7] * 10
    idx.add("a", tokens, "walk")
    res, latency = idx.query(tokens, top_k=1)
    _require(res == ["a"], "search smoke mismatch")
    _require(latency < 100.0, "search smoke latency too high")

    retargeted = retarget_scale_space(clip, target_scale=1.15)
    gt = build_scaled_ground_truth(clip, target_scale=1.15)
    rt_err = mpjpe_mm(gt.positions_m, retargeted.positions_m)
    _require(rt_err <= 10.0, f"retarget smoke failed: {rt_err}")

    summary = {
        "compression_ratio": enc1.compression_ratio,
        "joint_rmse_deg": rmse,
        "mpjpe_mm": pos,
        "retarget_mpjpe_mm": rt_err,
        "search_latency_ms": latency,
    }
    gate_file("gate_b_smoke.json").write_text(
        __import__("json").dumps(summary, indent=2) + "\n", encoding="utf-8"
    )

    write_checkpoint(
        gate="gate_b",
        status="PASS",
        details={
            "smoke_file": "artifacts/2026-02-20_zpe_mocap_wave1/gate_b_smoke.json",
            "summary": summary,
        },
    )


if __name__ == "__main__":
    main()
