from __future__ import annotations

import numpy as np

from .synthetic import MotionClip


def retarget_scale_space(source: MotionClip, target_scale: float) -> MotionClip:
    """Scale local joint vectors from root to produce a target-skeleton motion."""
    src = source.positions_m
    root = src[:, [0], :]
    relative = src - root
    retargeted = root + relative * target_scale

    return MotionClip(
        clip_id=f"retarget_{source.clip_id}",
        label=source.label,
        fps=source.fps,
        joint_names=list(source.joint_names),
        parents=list(source.parents),
        positions_m=retargeted,
        angles_deg=source.angles_deg.copy(),
    )


def build_scaled_ground_truth(source: MotionClip, target_scale: float) -> MotionClip:
    return retarget_scale_space(source, target_scale)


def retarget_clip(source: MotionClip, target_scale: float) -> MotionClip:
    return retarget_scale_space(source, target_scale)
