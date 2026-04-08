from __future__ import annotations

import json
import shutil
import tempfile
import urllib.request
from math import sin
from pathlib import Path
from typing import Any

from zpe_mocap.bvh_loader import load_bvh_motion_clip
from zpe_mocap.codec import decode_zpmoc, encode_clip
from zpe_mocap.metrics import joint_rmse_deg, mpjpe_mm

DEFAULT_CMU_SAMPLE_URL = (
    "https://raw.githubusercontent.com/una-dinosauria/cmu-mocap/master/data/001/01_01.bvh"
)
DEFAULT_SEED = 20260220


def _minimal_bvh_text(frame_count: int = 96) -> str:
    lines = [
        "HIERARCHY",
        "ROOT Hips",
        "{",
        "  OFFSET 0.00 0.00 0.00",
        "  CHANNELS 6 Xposition Yposition Zposition Zrotation Xrotation Yrotation",
        "  JOINT Chest",
        "  {",
        "    OFFSET 0.00 10.00 0.00",
        "    CHANNELS 3 Zrotation Xrotation Yrotation",
        "    End Site",
        "    {",
        "      OFFSET 0.00 10.00 0.00",
        "    }",
        "  }",
        "}",
        "MOTION",
        f"Frames: {frame_count}",
        "Frame Time: 0.0333333",
    ]
    for frame_index in range(frame_count):
        root_y = 0.15 * frame_index
        hips_z = 8.0 * sin(frame_index / 8.0)
        chest_z = 4.0 * sin(frame_index / 10.0)
        lines.append(f"0.00 {root_y:.4f} 0.00 {hips_z:.4f} 0.00 0.00 {chest_z:.4f} 0.00 0.00")
    return "\n".join(lines) + "\n"


MINIMAL_BVH_TEXT = _minimal_bvh_text()


def ensure_output_dir(output_dir: str | None, prefix: str) -> Path:
    if output_dir:
        path = Path(output_dir)
        path.mkdir(parents=True, exist_ok=True)
        return path
    return Path(tempfile.mkdtemp(prefix=prefix))


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_minimal_bvh(path: Path) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(MINIMAL_BVH_TEXT, encoding="utf-8")
    return path


def download_file(url: str, destination: Path) -> Path:
    destination.parent.mkdir(parents=True, exist_ok=True)
    with urllib.request.urlopen(url, timeout=60) as response, destination.open("wb") as handle:
        shutil.copyfileobj(response, handle)
    return destination


def roundtrip_bvh(path: Path, clip_id: str, label: str, seed: int) -> dict[str, Any]:
    clip = load_bvh_motion_clip(path, clip_id=clip_id, label=label)
    encoded = encode_clip(clip, seed=seed)
    decoded = decode_zpmoc(encoded.payload)
    return {
        "clip_id": clip.clip_id,
        "label": clip.label,
        "source_bvh": str(path),
        "fps": int(clip.fps),
        "frames": int(clip.positions_m.shape[0]),
        "joints": int(len(clip.joint_names)),
        "compression_ratio": float(encoded.compression_ratio),
        "encoded_size_bytes": int(encoded.encoded_size_bytes),
        "raw_bvh_float32_bytes": int(encoded.raw_bvh_float32_bytes),
        "payload_hash": encoded.payload_hash,
        "joint_angle_rmse_deg": float(joint_rmse_deg(clip.angles_deg, decoded.angles_deg)),
        "mpjpe_mm": float(mpjpe_mm(clip.positions_m, decoded.positions_m)),
    }
