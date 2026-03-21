from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

import numpy as np

try:  # optional dependency for real BVH ingestion
    import bvhio  # type: ignore
except Exception as exc:  # pragma: no cover - optional dependency
    bvhio = None
    _BVH_IMPORT_ERROR = str(exc)
else:
    _BVH_IMPORT_ERROR = ""

from .synthetic import MotionClip


@dataclass(frozen=True)
class BvhMetadata:
    frames: int
    fps: int
    joints: int


def _estimate_scale(joints: Iterable[object]) -> float:
    ys = [float(j.PositionWorld.y) for j in joints]  # type: ignore[attr-defined]
    height = max(ys) - min(ys) if ys else 0.0
    if height > 10.0:
        return 0.01
    if height > 3.0:
        return 0.0254
    return 1.0


def load_bvh_metadata(path: Path) -> BvhMetadata:
    if bvhio is None:  # pragma: no cover - optional dependency
        raise RuntimeError(f"bvhio unavailable: {_BVH_IMPORT_ERROR}")
    bvh = bvhio.readAsBvh(str(path), loadKeyFrames=False)
    fps = int(round(1.0 / bvh.FrameTime)) if bvh.FrameTime else 60
    root = bvhio.convertBvhToHierarchy(bvh.Root).loadRestPose(recursive=True)
    layout = root.layout()
    joints = [joint for joint, _, _ in layout]
    return BvhMetadata(frames=bvh.FrameCount, fps=fps, joints=len(joints))


def load_bvh_motion_clip(path: Path, clip_id: str, label: str) -> MotionClip:
    if bvhio is None:  # pragma: no cover - optional dependency
        raise RuntimeError(f"bvhio unavailable: {_BVH_IMPORT_ERROR}")

    bvh = bvhio.readAsBvh(str(path), loadKeyFrames=True)
    root = bvhio.convertBvhToHierarchy(bvh.Root).loadRestPose(recursive=True)
    layout = root.layout()
    joints = [joint for joint, _, _ in layout]
    joint_names = [joint.Name for joint in joints]
    index = {joint: idx for idx, joint in enumerate(joints)}
    parents = [index.get(joint.Parent, -1) if getattr(joint, "Parent", None) else -1 for joint in joints]

    fps = int(round(1.0 / bvh.FrameTime)) if bvh.FrameTime else 60
    frames = int(bvh.FrameCount or 0)

    root.loadRestPose(recursive=True)
    scale = _estimate_scale(joints)

    positions = np.zeros((frames, len(joints), 3), dtype=np.float64)
    angles = np.zeros((frames, len(joints), 3), dtype=np.float64)

    for frame in range(frames):
        root.loadPose(frame, recursive=True)
        for j, joint in enumerate(joints):
            pos = joint.PositionWorld  # type: ignore[attr-defined]
            positions[frame, j] = [float(pos.x) * scale, float(pos.y) * scale, float(pos.z) * scale]
            euler = joint.getEuler()  # type: ignore[attr-defined]
            angles[frame, j] = [float(euler.x), float(euler.y), float(euler.z)]

    return MotionClip(
        clip_id=clip_id,
        label=label,
        fps=fps,
        joint_names=joint_names,
        parents=parents,
        positions_m=positions,
        angles_deg=angles,
    )
