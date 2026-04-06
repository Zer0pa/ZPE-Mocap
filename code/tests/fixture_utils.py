from __future__ import annotations

import json
from pathlib import Path
import sys

import numpy as np

TEST_ROOT = Path(__file__).resolve().parent
ROOT = TEST_ROOT.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from zpe_mocap.synthetic import MotionClip

FIXTURES_ROOT = TEST_ROOT / "fixtures"
CANONICAL_FIXTURE_SEED = 20260220


def load_fixture_json(name: str) -> dict:
    return json.loads((FIXTURES_ROOT / name).read_text(encoding="utf-8"))


def load_binary_fixture(name: str) -> bytes:
    return (FIXTURES_ROOT / name).read_bytes()


def motion_clip_from_payload(payload: dict) -> MotionClip:
    def _array(name: str, *, dtype) -> np.ndarray | None:
        value = payload.get(name)
        if value is None:
            return None
        return np.asarray(value, dtype=dtype)

    return MotionClip(
        clip_id=payload["clip_id"],
        label=payload["label"],
        fps=int(payload["fps"]),
        joint_names=list(payload["joint_names"]),
        parents=[int(parent) for parent in payload["parents"]],
        positions_m=np.asarray(payload["positions_m"], dtype=np.float64),
        angles_deg=np.asarray(payload["angles_deg"], dtype=np.float64),
        xy_tokens=_array("xy_tokens", dtype=np.int16),
        xz_tokens=_array("xz_tokens", dtype=np.int16),
        magnitudes_mm=_array("magnitudes_mm", dtype=np.int16),
        rest_pose_m=_array("rest_pose_m", dtype=np.float64),
    )


def motion_clip_to_payload(clip: MotionClip) -> dict:
    def _maybe_list(value: np.ndarray | None) -> list | None:
        if value is None:
            return None
        return np.asarray(value).tolist()

    return {
        "clip_id": clip.clip_id,
        "label": clip.label,
        "fps": int(clip.fps),
        "joint_names": list(clip.joint_names),
        "parents": [int(parent) for parent in clip.parents],
        "positions_m": np.asarray(clip.positions_m, dtype=np.float64).tolist(),
        "angles_deg": np.asarray(clip.angles_deg, dtype=np.float64).tolist(),
        "xy_tokens": _maybe_list(clip.xy_tokens),
        "xz_tokens": _maybe_list(clip.xz_tokens),
        "magnitudes_mm": _maybe_list(clip.magnitudes_mm),
        "rest_pose_m": _maybe_list(clip.rest_pose_m),
    }


def load_motion_fixture(name: str) -> MotionClip:
    return motion_clip_from_payload(load_fixture_json(name))
