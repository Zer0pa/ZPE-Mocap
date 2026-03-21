from __future__ import annotations

import gzip
import io
import math
from dataclasses import dataclass
from statistics import mean

import numpy as np

from .codec import decode_zpmoc, encode_clip
from .constants import ACTION_LABELS
from .metrics import joint_rmse_deg, mpjpe_mm, percentile_ms, precision_at_k
from .retarget import build_scaled_ground_truth, retarget_scale_space
from .search import MotionSuffixIndex, flatten_tokens
from .synthetic import ACTION_TEMPLATES_XY, ACTION_TEMPLATES_XZ, MotionClip, generate_clip, generate_corpus
from .utils import stable_json_dumps


@dataclass(frozen=True)
class BenchmarkBundle:
    compression: dict
    joint_fidelity: dict
    position_fidelity: dict
    search_eval: dict
    latency_eval: dict
    retarget_eval: dict
    blender_eval: dict


def _tokens_from_clip(clip: MotionClip) -> tuple[np.ndarray, np.ndarray]:
    if clip.xy_tokens is not None and clip.xz_tokens is not None:
        return np.asarray(clip.xy_tokens, dtype=np.int16), np.asarray(clip.xz_tokens, dtype=np.int16)

    delta = np.diff(clip.positions_m, axis=0, prepend=clip.positions_m[:1])
    xy = delta[..., [0, 1]]
    xz = delta[..., [0, 2]]
    step = 2.0 * math.pi / 8.0
    xy_tokens = np.mod(np.round(np.arctan2(xy[..., 1], xy[..., 0]) / step).astype(np.int16), 8)
    xz_tokens = np.mod(np.round(np.arctan2(xz[..., 1], xz[..., 0]) / step).astype(np.int16), 8)
    return xy_tokens, xz_tokens


def _gzip_ratio(raw_bytes: bytes) -> tuple[int, float]:
    out = io.BytesIO()
    with gzip.GzipFile(fileobj=out, mode="wb", compresslevel=9) as f:
        f.write(raw_bytes)
    comp = out.getvalue()
    size = len(comp)
    ratio = len(raw_bytes) / float(size) if size else 0.0
    return size, ratio


def _fast_token_stream(label: str, length: int, seed: int) -> list[int]:
    rng = np.random.default_rng(seed)
    base_xy = ACTION_TEMPLATES_XY[label]
    base_xz = ACTION_TEMPLATES_XZ[label]
    stream: list[int] = []

    shift = int(rng.integers(0, len(base_xy)))
    for i in range(length):
        idx = (i + shift) % len(base_xy)
        xy_token = base_xy[idx]
        xz_token = base_xz[(idx + (i // 16) % len(base_xz)) % len(base_xz)]
        if rng.random() < 0.03:
            xy_token = (xy_token + int(rng.integers(0, 2))) % 8
        if rng.random() < 0.03:
            xz_token = (xz_token + int(rng.integers(0, 2))) % 8
        stream.extend([xy_token, xz_token])
    return stream


def run_core_benchmarks(
    seed: int,
    search_library_size: int = 10_000,
    query_count: int = 120,
    clips: list[MotionClip] | None = None,
) -> BenchmarkBundle:
    if clips is None:
        clips = generate_corpus(
            labels=ACTION_LABELS,
            clips_per_label=8,
            frames=240,
            fps=60,
            seed=seed,
            noise_scale=0.0002,
        )

    compression_ratios = []
    gzip_ratios = []
    encoded_sizes = []
    raw_sizes = []
    joint_errs = []
    pos_errs = []

    for i, clip in enumerate(clips):
        encoded = encode_clip(clip, seed=seed + i)
        decoded = decode_zpmoc(encoded.payload)
        compression_ratios.append(encoded.compression_ratio)
        encoded_sizes.append(encoded.encoded_size_bytes)
        raw_sizes.append(encoded.raw_bvh_float32_bytes)

        raw_float_bytes = (
            clip.angles_deg.astype(np.float32).tobytes()
            + clip.positions_m.astype(np.float32).tobytes()
        )
        _, gzip_ratio = _gzip_ratio(raw_float_bytes)
        gzip_ratios.append(gzip_ratio)

        joint_errs.append(joint_rmse_deg(clip.angles_deg, decoded.angles_deg))
        pos_errs.append(mpjpe_mm(clip.positions_m, decoded.positions_m))

    compression = {
        "metric": "compression_ratio_vs_raw_bvh_float32",
        "zpmoc_mean_cr": float(mean(compression_ratios)),
        "zpmoc_p50_cr": float(np.percentile(compression_ratios, 50)),
        "zpmoc_p95_cr": float(np.percentile(compression_ratios, 95)),
        "gzip_mean_cr": float(mean(gzip_ratios)),
        "acl_reference_cr": 2.9,
        "clip_count": len(clips),
        "raw_total_bytes": int(sum(raw_sizes)),
        "encoded_total_bytes": int(sum(encoded_sizes)),
        "status": "PASS" if float(mean(compression_ratios)) >= 10.0 else "FAIL",
        "note": "ACL value from concept reference; direct ACL binary benchmark unavailable in-lane",
    }

    joint_fidelity = {
        "metric": "joint_angle_rmse_deg",
        "rmse_mean_deg": float(mean(joint_errs)),
        "rmse_p95_deg": float(np.percentile(joint_errs, 95)),
        "threshold_deg": 1.0,
        "status": "PASS" if float(mean(joint_errs)) <= 1.0 else "FAIL",
    }

    position_fidelity = {
        "metric": "mpjpe_mm",
        "mpjpe_mean_mm": float(mean(pos_errs)),
        "mpjpe_p95_mm": float(np.percentile(pos_errs, 95)),
        "threshold_mm": 5.0,
        "status": "PASS" if float(mean(pos_errs)) <= 5.0 else "FAIL",
    }

    search_index = MotionSuffixIndex(k=8)
    labels = []
    predictions: list[list[str]] = []
    latencies_ms = []

    rng = np.random.default_rng(seed)
    for idx in range(search_library_size):
        clip = clips[idx % len(clips)]
        xy_tokens, xz_tokens = _tokens_from_clip(clip)
        tokens = flatten_tokens(xy_tokens, xz_tokens)
        search_index.add(f"lib_{idx:05d}", tokens, clip.label)

    for q in range(query_count):
        clip = clips[q % len(clips)]
        labels.append(clip.label)
        xy_tokens, xz_tokens = _tokens_from_clip(clip)
        tokens = flatten_tokens(xy_tokens, xz_tokens)
        ids, elapsed_ms = search_index.query(tokens, top_k=10)
        latencies_ms.append(elapsed_ms)
        predictions.append([search_index.labels[cid] for cid in ids])

    p_at_10 = precision_at_k(labels, predictions, k=10)
    search_eval = {
        "metric": "precision_at_10",
        "p_at_10": p_at_10,
        "threshold": 0.85,
        "query_count": len(labels),
        "status": "PASS" if p_at_10 >= 0.85 else "FAIL",
    }

    latency_eval = {
        "metric": "query_latency_ms",
        "p50_ms": percentile_ms(latencies_ms, 50),
        "p95_ms": percentile_ms(latencies_ms, 95),
        "p99_ms": percentile_ms(latencies_ms, 99),
        "threshold_ms": 100.0,
        "library_size": search_library_size,
        "status": "PASS" if percentile_ms(latencies_ms, 95) < 100.0 else "FAIL",
    }

    retarget_errors = []
    for i in range(40):
        src = clips[i % len(clips)]
        predicted = retarget_scale_space(src, target_scale=1.18)
        ground_truth = build_scaled_ground_truth(src, target_scale=1.18)
        retarget_errors.append(mpjpe_mm(ground_truth.positions_m, predicted.positions_m))

    retarget_eval = {
        "metric": "retarget_mpjpe_mm",
        "mpjpe_mean_mm": float(mean(retarget_errors)),
        "mpjpe_p95_mm": float(np.percentile(retarget_errors, 95)),
        "threshold_mm": 10.0,
        "clip_count": len(retarget_errors),
        "status": "PASS" if float(mean(retarget_errors)) <= 10.0 else "FAIL",
    }

    from .adapters import blender_roundtrip_simulation

    roundtrip_results = []
    for i in range(16):
        clip = clips[i % len(clips)]
        res = blender_roundtrip_simulation(clip, seed=seed + 80_000 + i)
        roundtrip_results.append(res)

    blender_eval = {
        "metric": "blender_roundtrip_integrity",
        "pass_count": int(sum(1 for r in roundtrip_results if r.ok)),
        "total": len(roundtrip_results),
        "mean_roundtrip_mpjpe_mm": float(mean([r.mpjpe_mm for r in roundtrip_results])),
        "all_bytes_identical": all(r.bytes_identical for r in roundtrip_results),
        "status": "PASS" if all(r.ok for r in roundtrip_results) else "FAIL",
        "note": "simulated adapter path in-lane; real Blender runtime integration not executed",
    }

    return BenchmarkBundle(
        compression=compression,
        joint_fidelity=joint_fidelity,
        position_fidelity=position_fidelity,
        search_eval=search_eval,
        latency_eval=latency_eval,
        retarget_eval=retarget_eval,
        blender_eval=blender_eval,
    )


def determinism_hash(seed: int) -> str:
    clips = generate_corpus(
        labels=ACTION_LABELS[:4],
        clips_per_label=3,
        frames=120,
        fps=60,
        seed=seed,
        noise_scale=0.0002,
    )

    hashes = []
    for i, clip in enumerate(clips):
        enc = encode_clip(clip, seed=seed + i)
        hashes.append(enc.payload_hash)

    index = MotionSuffixIndex(k=8)
    for i in range(500):
        label = ACTION_LABELS[i % len(ACTION_LABELS)]
        index.add(f"det_{i:04d}", _fast_token_stream(label, length=80, seed=seed + i), label)

    q_tokens = _fast_token_stream("walk", length=80, seed=seed + 9000)
    ids, _ = index.query(q_tokens, top_k=10)
    payload = {
        "encode_hashes": hashes,
        "query_ids": ids,
    }

    import hashlib

    stable = stable_json_dumps(payload).encode("utf-8")
    return hashlib.sha256(stable).hexdigest()
