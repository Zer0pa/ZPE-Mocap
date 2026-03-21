from __future__ import annotations

import json
import struct
import zlib
from dataclasses import dataclass
from typing import Any

import numpy as np

from .constants import MIRROR_PAIRS, TOKEN_MIRROR, TOKEN_VECTORS_2D
from .synthetic import MotionClip
from .utils import sha256_bytes, stable_json_dumps
from .validation import validate_skeleton

MAGIC = b"ZPM1"


@dataclass(frozen=True)
class EncodedMotion:
    payload: bytes
    encoded_size_bytes: int
    raw_bvh_float32_bytes: int
    compression_ratio: float
    payload_hash: str


def _quantize_delta_to_tokens(delta: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    xy = delta[..., [0, 1]]
    xz = delta[..., [0, 2]]

    xy_angles = np.arctan2(xy[..., 1], xy[..., 0])
    xz_angles = np.arctan2(xz[..., 1], xz[..., 0])

    step = 2.0 * np.pi / 8.0
    xy_tokens = np.mod(np.round(xy_angles / step).astype(np.int16), 8)
    xz_tokens = np.mod(np.round(xz_angles / step).astype(np.int16), 8)

    mag = np.sqrt(np.sum(delta * delta, axis=-1))
    mag_mm = np.round(mag * 1000.0).astype(np.int16)
    return xy_tokens, xz_tokens, mag_mm


def _tokens_to_delta(xy_tokens: np.ndarray, xz_tokens: np.ndarray, mag_mm: np.ndarray) -> np.ndarray:
    frames, joints = xy_tokens.shape
    delta = np.zeros((frames, joints, 3), dtype=np.float64)
    for token in range(8):
        mask_xy = xy_tokens == token
        if np.any(mask_xy):
            vx, vy = TOKEN_VECTORS_2D[token]
            delta[..., 0][mask_xy] += vx
            delta[..., 1][mask_xy] = vy
    for token in range(8):
        mask_xz = xz_tokens == token
        if np.any(mask_xz):
            vx, vz = TOKEN_VECTORS_2D[token]
            delta[..., 0][mask_xz] += vx
            delta[..., 2][mask_xz] = vz
    delta[..., 0] *= 0.5
    magnitudes = mag_mm.astype(np.float64) / 1000.0
    delta *= magnitudes[..., np.newaxis]
    return delta


def _angles_from_local_delta(local_delta: np.ndarray) -> np.ndarray:
    x = local_delta[..., 0]
    y = local_delta[..., 1]
    z = local_delta[..., 2]
    yaw = np.degrees(np.arctan2(x, z + 1e-9))
    pitch = np.degrees(np.arctan2(y, np.sqrt(x * x + z * z) + 1e-9))
    roll = np.degrees(np.arctan2(z, x + 1e-9))
    return np.stack([pitch, yaw, roll], axis=-1)


def _detect_periodicity(stream: np.ndarray, min_period: int = 8, max_period: int = 64) -> dict[str, Any]:
    n = int(stream.shape[0])
    if n < min_period * 2:
        return {"period": 0, "confidence": 0.0}

    best_period = 0
    best_score = 0.0
    upper = min(max_period, n // 2)
    for period in range(min_period, upper + 1):
        lhs = stream[:-period]
        rhs = stream[period:]
        score = float(np.mean(lhs == rhs))
        if score > best_score:
            best_score = score
            best_period = period
    if best_score < 0.72:
        return {"period": 0, "confidence": best_score}
    return {"period": int(best_period), "confidence": best_score}


def _detect_mirror_groups(
    joint_names: list[str],
    xy_tokens: np.ndarray,
    xz_tokens: np.ndarray,
) -> list[dict[str, Any]]:
    name_to_index = {name: idx for idx, name in enumerate(joint_names)}
    groups: list[dict[str, Any]] = []
    for left_name, right_name in MIRROR_PAIRS:
        if left_name not in name_to_index or right_name not in name_to_index:
            continue
        li = name_to_index[left_name]
        ri = name_to_index[right_name]
        left_xy = xy_tokens[:, li]
        right_xy = xy_tokens[:, ri]
        mirrored_xy = np.vectorize(TOKEN_MIRROR.get)(left_xy)
        left_xz = xz_tokens[:, li]
        right_xz = xz_tokens[:, ri]
        mirrored_xz = np.vectorize(TOKEN_MIRROR.get)(left_xz)
        score_xy = float(np.mean(mirrored_xy == right_xy))
        score_xz = float(np.mean(mirrored_xz == right_xz))
        score = (score_xy + score_xz) * 0.5
        if score >= 0.75:
            groups.append(
                {
                    "left": left_name,
                    "right": right_name,
                    "mirror_similarity": round(score, 6),
                }
            )
    return groups


def _apply_parent_relative_tokens(tokens: np.ndarray, parents: list[int]) -> np.ndarray:
    relative = tokens.copy()
    for joint, parent in enumerate(parents):
        if parent == -1:
            continue
        relative[:, joint] = (tokens[:, joint] - tokens[:, parent]) % 8
    return relative


def _restore_absolute_tokens(relative: np.ndarray, parents: list[int]) -> np.ndarray:
    absolute = relative.copy()
    for joint, parent in enumerate(parents):
        if parent == -1:
            continue
        absolute[:, joint] = (absolute[:, joint] + absolute[:, parent]) % 8
    return absolute


def _positions_to_local_deltas(positions: np.ndarray, parents: list[int]) -> np.ndarray:
    frames, joints, _ = positions.shape
    local_deltas = np.zeros_like(positions)
    for t in range(1, frames):
        frame_delta = positions[t] - positions[t - 1]
        for joint, parent in enumerate(parents):
            if parent == -1:
                local_deltas[t, joint] = frame_delta[joint] / 0.25
            else:
                local_deltas[t, joint] = (frame_delta[joint] - frame_delta[parent]) / 0.08
    return local_deltas


def _reconstruct_positions(local_delta: np.ndarray, parents: list[int], rest_frame: np.ndarray) -> np.ndarray:
    frames, joints, _ = local_delta.shape
    out = np.zeros((frames, joints, 3), dtype=np.float64)
    out[0] = rest_frame
    local_states = np.zeros((joints, 3), dtype=np.float64)

    for t in range(1, frames):
        for joint, parent in enumerate(parents):
            local_states[joint] += local_delta[t, joint]
            if parent == -1:
                out[t, joint] = out[t - 1, joint] + local_delta[t, joint] * 0.25
            else:
                rest_offset = rest_frame[joint] - rest_frame[parent]
                out[t, joint] = out[t, parent] + rest_offset + local_states[joint] * 0.08
    return out


def _read_segment(payload: bytes, offset: int) -> tuple[bytes, int]:
    if offset + 4 > len(payload):
        raise ValueError("segment header truncated")
    (size,) = struct.unpack_from("<I", payload, offset)
    offset += 4
    end = offset + size
    if end > len(payload):
        raise ValueError("segment payload truncated")
    return payload[offset:end], end


def encode_clip(clip: MotionClip, seed: int) -> EncodedMotion:
    validate_skeleton(clip.joint_names, clip.parents)

    if clip.xy_tokens is not None and clip.xz_tokens is not None and clip.magnitudes_mm is not None:
        xy_tokens = np.asarray(clip.xy_tokens, dtype=np.int16)
        xz_tokens = np.asarray(clip.xz_tokens, dtype=np.int16)
        mag_mm = np.asarray(clip.magnitudes_mm, dtype=np.int16)
    else:
        local_delta = _positions_to_local_deltas(clip.positions_m, clip.parents)
        xy_tokens, xz_tokens, mag_mm = _quantize_delta_to_tokens(local_delta)

    rel_xy = _apply_parent_relative_tokens(xy_tokens, clip.parents).astype(np.uint8, copy=False)
    rel_xz = _apply_parent_relative_tokens(xz_tokens, clip.parents).astype(np.uint8, copy=False)
    mag_mm_i2 = np.asarray(mag_mm, dtype="<i2")

    periodicity = _detect_periodicity(rel_xy[:, 0])
    mirror_groups = _detect_mirror_groups(clip.joint_names, xy_tokens, xz_tokens)

    rest_frame = clip.rest_pose_m if clip.rest_pose_m is not None else clip.positions_m[0]
    rest_frame_f32 = np.asarray(rest_frame, dtype="<f4")

    header = {
        "magic": "ZPMOC",
        "version": "1.0.0",
        "seed": int(seed),
        "fps": int(clip.fps),
        "num_frames": int(xy_tokens.shape[0]),
        "num_joints": len(clip.joint_names),
        "joint_names": list(clip.joint_names),
        "parents": list(clip.parents),
    }

    meta = {
        "header": header,
        "periodicity": periodicity,
        "mirror_groups": mirror_groups,
        "segments": ["rest_f32", "rel_xy_u8", "rel_xz_u8", "mag_mm_i16"],
    }
    meta_bytes = stable_json_dumps(meta).encode("utf-8")

    payload = bytearray()
    payload += struct.pack("<I", len(meta_bytes))
    payload += meta_bytes

    for arr in (rest_frame_f32, rel_xy, rel_xz, mag_mm_i2):
        blob = arr.tobytes(order="C")
        payload += struct.pack("<I", len(blob))
        payload += blob

    raw_payload = bytes(payload)
    compressed = zlib.compress(raw_payload, level=9)
    digest_hex = sha256_bytes(raw_payload)
    digest = bytes.fromhex(digest_hex)
    out_bytes = MAGIC + digest + compressed

    # Raw BVH float32 proxy: rotation channels + position channels.
    raw_bvh_bytes = int(clip.angles_deg.astype(np.float32).nbytes + clip.positions_m.astype(np.float32).nbytes)
    encoded_size = len(out_bytes)
    ratio = float(raw_bvh_bytes / encoded_size) if encoded_size else 0.0

    return EncodedMotion(
        payload=out_bytes,
        encoded_size_bytes=encoded_size,
        raw_bvh_float32_bytes=raw_bvh_bytes,
        compression_ratio=ratio,
        payload_hash=sha256_bytes(out_bytes),
    )


def decode_zpmoc(data: bytes) -> MotionClip:
    if len(data) < 36:
        raise ValueError("payload too short")
    if data[:4] != MAGIC:
        raise ValueError("invalid zpmoc magic")

    expected_digest = data[4:36]
    compressed = data[36:]
    raw_payload = zlib.decompress(compressed)

    digest = bytes.fromhex(sha256_bytes(raw_payload))
    if digest != expected_digest:
        raise ValueError("payload checksum mismatch")

    offset = 0
    if len(raw_payload) < 4:
        raise ValueError("missing metadata length")
    (meta_len,) = struct.unpack_from("<I", raw_payload, offset)
    offset += 4

    meta_end = offset + meta_len
    if meta_end > len(raw_payload):
        raise ValueError("metadata truncated")

    meta = json.loads(raw_payload[offset:meta_end].decode("utf-8"))
    offset = meta_end

    header = meta.get("header", {})
    required = ["magic", "version", "seed", "fps", "num_frames", "num_joints", "joint_names", "parents"]
    missing = [k for k in required if k not in header]
    if missing:
        raise ValueError(f"missing header fields: {missing}")
    if header["magic"] != "ZPMOC":
        raise ValueError("invalid header magic")

    frames = int(header["num_frames"])
    joints = int(header["num_joints"])
    joint_names = list(header["joint_names"])
    parents = list(header["parents"])
    validate_skeleton(joint_names, parents)

    segment_blobs = []
    for _ in range(4):
        blob, offset = _read_segment(raw_payload, offset)
        segment_blobs.append(blob)

    rest_frame = np.frombuffer(segment_blobs[0], dtype="<f4").reshape(joints, 3).astype(np.float64)
    rel_xy = np.frombuffer(segment_blobs[1], dtype=np.uint8).reshape(frames, joints).astype(np.int16)
    rel_xz = np.frombuffer(segment_blobs[2], dtype=np.uint8).reshape(frames, joints).astype(np.int16)
    mag_mm = np.frombuffer(segment_blobs[3], dtype="<i2").reshape(frames, joints).astype(np.int16)

    abs_xy = _restore_absolute_tokens(rel_xy, parents)
    abs_xz = _restore_absolute_tokens(rel_xz, parents)
    local_delta = _tokens_to_delta(abs_xy, abs_xz, mag_mm)

    positions = _reconstruct_positions(local_delta, parents, rest_frame)
    angles = _angles_from_local_delta(local_delta)

    return MotionClip(
        clip_id=f"decoded_{header['seed']}",
        label="decoded",
        fps=int(header["fps"]),
        joint_names=joint_names,
        parents=parents,
        positions_m=positions,
        angles_deg=angles,
        xy_tokens=abs_xy,
        xz_tokens=abs_xz,
        magnitudes_mm=mag_mm,
        rest_pose_m=rest_frame,
    )
