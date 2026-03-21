from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

import numpy as np

from .constants import ACTION_LABELS, JOINT_NAMES, PARENTS, REST_OFFSETS, TOKEN_VECTORS_2D
from .validation import validate_skeleton


@dataclass(frozen=True)
class MotionClip:
    clip_id: str
    label: str
    fps: int
    joint_names: list[str]
    parents: list[int]
    positions_m: np.ndarray  # [frames, joints, 3]
    angles_deg: np.ndarray  # [frames, joints, 3]
    xy_tokens: np.ndarray | None = None  # [frames, joints]
    xz_tokens: np.ndarray | None = None  # [frames, joints]
    magnitudes_mm: np.ndarray | None = None  # [frames, joints]
    rest_pose_m: np.ndarray | None = None  # [joints, 3]


ACTION_TEMPLATES_XY = {
    "walk": [1, 0, 1, 0, 1, 0, 1, 0],
    "turn_left": [2, 3, 3, 2, 3, 2, 3, 2],
    "turn_right": [2, 1, 1, 2, 1, 2, 1, 2],
    "run": [1, 0, 1, 0, 7, 0, 7, 0],
    "jump": [2, 2, 2, 2, 6, 6, 6, 6],
    "punch": [0, 0, 1, 0, 0, 1, 0, 0],
    "crouch": [6, 6, 6, 2, 2, 2, 6, 2],
    "sidestep": [0, 0, 4, 4, 0, 0, 4, 4],
    "idle": [2, 2, 6, 6, 2, 2, 6, 6],
    "fall_recover": [6, 6, 6, 6, 6, 2, 2, 2],
}

ACTION_TEMPLATES_XZ = {
    "walk": [2, 2, 2, 2, 2, 2, 2, 2],
    "turn_left": [3, 3, 2, 2, 1, 1, 2, 2],
    "turn_right": [1, 1, 2, 2, 3, 3, 2, 2],
    "run": [2, 2, 1, 1, 2, 2, 3, 3],
    "jump": [2, 2, 2, 2, 2, 2, 2, 2],
    "punch": [0, 0, 2, 2, 4, 4, 2, 2],
    "crouch": [2, 2, 2, 2, 2, 2, 2, 2],
    "sidestep": [0, 0, 0, 0, 4, 4, 4, 4],
    "idle": [2, 2, 2, 2, 6, 6, 6, 6],
    "fall_recover": [2, 2, 2, 2, 6, 6, 6, 6],
}

ACTION_MAG_MM = {
    "walk": 12.0,
    "turn_left": 11.0,
    "turn_right": 11.0,
    "run": 22.0,
    "jump": 26.0,
    "punch": 16.0,
    "crouch": 10.0,
    "sidestep": 14.0,
    "idle": 4.0,
    "fall_recover": 20.0,
}


def _token_to_delta(xy_token: int, xz_token: int, magnitude_m: float) -> np.ndarray:
    xy = TOKEN_VECTORS_2D[xy_token]
    xz = TOKEN_VECTORS_2D[xz_token]
    x = (xy[0] + xz[0]) * 0.5 * magnitude_m
    y = xy[1] * magnitude_m
    z = xz[1] * magnitude_m
    return np.array([x, y, z], dtype=np.float64)


def _build_rest_pose(scale: float) -> np.ndarray:
    joint_count = len(JOINT_NAMES)
    pose = np.zeros((joint_count, 3), dtype=np.float64)
    offsets = np.asarray(REST_OFFSETS, dtype=np.float64) * scale
    for joint in range(joint_count):
        parent = PARENTS[joint]
        if parent == -1:
            pose[joint] = offsets[joint]
        else:
            pose[joint] = pose[parent] + offsets[joint]
    return pose


def _angles_from_local_delta(local_delta: np.ndarray) -> np.ndarray:
    x = local_delta[..., 0]
    y = local_delta[..., 1]
    z = local_delta[..., 2]
    yaw = np.degrees(np.arctan2(x, z + 1e-9))
    pitch = np.degrees(np.arctan2(y, np.sqrt(x * x + z * z) + 1e-9))
    roll = np.degrees(np.arctan2(z, x + 1e-9))
    return np.stack([pitch, yaw, roll], axis=-1)


def generate_clip(
    clip_id: str,
    label: str,
    frames: int,
    fps: int,
    seed: int,
    skeleton_scale: float = 1.0,
    noise_scale: float = 0.0,
) -> MotionClip:
    if label not in ACTION_LABELS:
        raise ValueError(f"unknown label {label}")

    validate_skeleton(JOINT_NAMES, PARENTS)
    rng = np.random.default_rng(seed)
    joint_count = len(JOINT_NAMES)

    base_xy = ACTION_TEMPLATES_XY[label]
    base_xz = ACTION_TEMPLATES_XZ[label]
    base_mag = ACTION_MAG_MM[label] / 1000.0

    rest_pose = _build_rest_pose(skeleton_scale)
    positions = np.zeros((frames, joint_count, 3), dtype=np.float64)
    positions[0] = rest_pose

    local_states = np.zeros((joint_count, 3), dtype=np.float64)
    local_deltas = np.zeros((frames, joint_count, 3), dtype=np.float64)
    xy_tokens = np.zeros((frames, joint_count), dtype=np.int16)
    xz_tokens = np.zeros((frames, joint_count), dtype=np.int16)
    magnitudes_mm = np.zeros((frames, joint_count), dtype=np.int16)

    for t in range(1, frames):
        phase = t % len(base_xy)
        for joint in range(joint_count):
            joint_phase = (phase + joint) % len(base_xy)
            xy_token = base_xy[joint_phase]
            xz_token = base_xz[(joint_phase + joint // 3) % len(base_xz)]

            if "Left" in JOINT_NAMES[joint]:
                xy_token = (xy_token + 1) % 8
            elif "Right" in JOINT_NAMES[joint]:
                xy_token = (xy_token - 1) % 8

            if label == "punch" and JOINT_NAMES[joint] in {"RightArm", "RightForeArm", "RightHand"}:
                xy_token = 0
                xz_token = 0
            if label == "jump" and JOINT_NAMES[joint] in {"LeftFoot", "RightFoot", "LeftToe", "RightToe"}:
                xy_token = 2 if t % 16 < 8 else 6

            magnitude = base_mag * (1.0 + (joint % 4) * 0.05)
            if noise_scale > 0.0:
                magnitude += float(rng.normal(0.0, noise_scale))
                magnitude = max(magnitude, 0.0005)

            delta = _token_to_delta(xy_token, xz_token, magnitude)
            local_states[joint] += delta
            local_deltas[t, joint] = delta
            xy_tokens[t, joint] = xy_token
            xz_tokens[t, joint] = xz_token
            magnitudes_mm[t, joint] = int(round(magnitude * 1000.0))

        for joint in range(joint_count):
            parent = PARENTS[joint]
            if parent == -1:
                positions[t, joint] = positions[t - 1, joint] + local_deltas[t, joint] * 0.25
            else:
                positions[t, joint] = positions[t, parent] + rest_pose[joint] - rest_pose[parent] + local_states[joint] * 0.08

    angles = _angles_from_local_delta(local_deltas)
    return MotionClip(
        clip_id=clip_id,
        label=label,
        fps=fps,
        joint_names=list(JOINT_NAMES),
        parents=list(PARENTS),
        positions_m=positions,
        angles_deg=angles,
        xy_tokens=xy_tokens,
        xz_tokens=xz_tokens,
        magnitudes_mm=magnitudes_mm,
        rest_pose_m=rest_pose,
    )


def generate_corpus(
    labels: Iterable[str],
    clips_per_label: int,
    frames: int,
    fps: int,
    seed: int,
    skeleton_scale: float = 1.0,
    noise_scale: float = 0.0,
) -> list[MotionClip]:
    clips: list[MotionClip] = []
    index = 0
    for label in labels:
        for n in range(clips_per_label):
            clip_seed = seed + index * 17 + n
            clips.append(
                generate_clip(
                    clip_id=f"{label}_{n:04d}",
                    label=label,
                    frames=frames,
                    fps=fps,
                    seed=clip_seed,
                    skeleton_scale=skeleton_scale,
                    noise_scale=noise_scale,
                )
            )
            index += 1
    return clips
