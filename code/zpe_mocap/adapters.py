from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from .codec import decode_zpmoc, encode_clip
from .metrics import mpjpe_mm
from .synthetic import MotionClip


@dataclass(frozen=True)
class AdapterRoundtripResult:
    ok: bool
    mpjpe_mm: float
    bytes_identical: bool
    note: str


def blender_roundtrip_simulation(clip: MotionClip, seed: int) -> AdapterRoundtripResult:
    """Blender-path surrogate: export(.zpmoc) -> import -> export idempotence check."""
    first = encode_clip(clip, seed=seed)
    decoded = decode_zpmoc(first.payload)
    second = encode_clip(decoded, seed=seed)

    err = mpjpe_mm(clip.positions_m, decoded.positions_m)
    identical = first.payload == second.payload
    return AdapterRoundtripResult(
        ok=bool(err <= 5.0),
        mpjpe_mm=err,
        bytes_identical=identical,
        note="simulated adapter path; real Blender runtime not invoked in this lane",
    )


def usd_adapter_smoke(clip: MotionClip, seed: int) -> dict:
    encoded = encode_clip(clip, seed=seed)
    decoded = decode_zpmoc(encoded.payload)
    return {
        "status": "PASS" if np.allclose(decoded.positions_m[0], clip.positions_m[0], atol=1e-9) else "FAIL",
        "note": "usdBVHAnim integration simulated via schema-preserving decode",
    }
