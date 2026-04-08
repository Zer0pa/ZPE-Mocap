from __future__ import annotations

import gzip
import io
from pathlib import PurePosixPath
from statistics import mean
from typing import Any

import numpy as np

CMU_GITHUB_TREE_URL = "https://api.github.com/repos/una-dinosauria/cmu-mocap/git/trees/master?recursive=1"
CMU_GITHUB_RAW_ROOT = "https://raw.githubusercontent.com/una-dinosauria/cmu-mocap/master/"


def list_cmu_bvh_paths(tree_payload: dict[str, Any]) -> list[str]:
    tree = tree_payload.get("tree")
    if not isinstance(tree, list):
        raise ValueError("CMU GitHub tree payload must contain a list under 'tree'.")

    paths: list[str] = []
    for entry in tree:
        if not isinstance(entry, dict):
            continue
        path = entry.get("path")
        if entry.get("type") != "blob":
            continue
        if not isinstance(path, str):
            continue
        if path.startswith("data/") and path.endswith(".bvh"):
            paths.append(path)
    return sorted(paths)


def subject_id_for_path(path: str) -> str:
    parts = PurePosixPath(path).parts
    if len(parts) < 3 or parts[0] != "data":
        raise ValueError(f"Unexpected CMU BVH path: {path}")
    return parts[1]


def select_round_robin_subset(paths: list[str], limit: int) -> list[str]:
    if limit < 0:
        raise ValueError("limit must be non-negative")
    if limit == 0:
        return []

    buckets: dict[str, list[str]] = {}
    for path in sorted(paths):
        subject_id = subject_id_for_path(path)
        buckets.setdefault(subject_id, []).append(path)

    selected: list[str] = []
    active_subjects = sorted(buckets)
    while active_subjects and len(selected) < limit:
        next_subjects: list[str] = []
        for subject_id in active_subjects:
            bucket = buckets[subject_id]
            if not bucket:
                continue
            selected.append(bucket.pop(0))
            if bucket:
                next_subjects.append(subject_id)
            if len(selected) >= limit:
                break
        active_subjects = next_subjects
    return selected


def select_successful_rows(
    rows: list[dict[str, Any]],
    selected_paths: list[str],
    target_sequences: int,
) -> list[dict[str, Any]]:
    if target_sequences < 0:
        raise ValueError("target_sequences must be non-negative")

    order = {path: index for index, path in enumerate(selected_paths)}
    ordered_rows = sorted(
        [row for row in rows if str(row.get("cmu_path")) in order],
        key=lambda row: order[str(row["cmu_path"])],
    )
    return ordered_rows[:target_sequences]


def gzip_ratio(raw_bytes: bytes) -> float:
    out = io.BytesIO()
    with gzip.GzipFile(fileobj=out, mode="wb", compresslevel=9) as handle:
        handle.write(raw_bytes)
    compressed = out.getvalue()
    if not compressed:
        return 0.0
    return len(raw_bytes) / float(len(compressed))


def summarize_clip_rows(rows: list[dict[str, Any]], target_sequences: int) -> dict[str, Any]:
    if not rows:
        raise ValueError("Need at least one clip row to summarize.")

    zpe_ratios = np.asarray([float(row["zpe_ratio"]) for row in rows], dtype=np.float64)
    gzip_ratios = np.asarray([float(row["gzip_ratio"]) for row in rows], dtype=np.float64)
    joint_rmse = np.asarray([float(row["joint_angle_rmse_deg"]) for row in rows], dtype=np.float64)
    mpjpe = np.asarray([float(row["mpjpe_mm"]) for row in rows], dtype=np.float64)
    frame_counts = np.asarray([int(row["frames"]) for row in rows], dtype=np.int64)
    joint_counts = np.asarray([int(row["joints"]) for row in rows], dtype=np.int64)
    fps_values = np.asarray([int(row["fps"]) for row in rows], dtype=np.int64)

    total_duration_seconds = float(np.sum(frame_counts / fps_values))
    mean_zpe = float(np.mean(zpe_ratios))
    mean_gzip = float(np.mean(gzip_ratios))
    improvement = mean_zpe / mean_gzip if mean_gzip else None

    return {
        "target_sequences": int(target_sequences),
        "completed_sequences": len(rows),
        "total_frames": int(np.sum(frame_counts)),
        "total_duration_hours": total_duration_seconds / 3600.0,
        "joint_count_mean": float(mean(joint_counts)),
        "joint_count_min": int(np.min(joint_counts)),
        "joint_count_max": int(np.max(joint_counts)),
        "fps_values": sorted({int(value) for value in fps_values}),
        "raw_total_bytes": int(sum(int(row["raw_bvh_float32_bytes"]) for row in rows)),
        "encoded_total_bytes": int(sum(int(row["encoded_size_bytes"]) for row in rows)),
        "zpe_ratio_mean": mean_zpe,
        "zpe_ratio_p50": float(np.percentile(zpe_ratios, 50)),
        "zpe_ratio_p95": float(np.percentile(zpe_ratios, 95)),
        "gzip_ratio_mean": mean_gzip,
        "gzip_ratio_p50": float(np.percentile(gzip_ratios, 50)),
        "gzip_ratio_p95": float(np.percentile(gzip_ratios, 95)),
        "joint_angle_rmse_deg_mean": float(np.mean(joint_rmse)),
        "joint_angle_rmse_deg_p95": float(np.percentile(joint_rmse, 95)),
        "mpjpe_mm_mean": float(np.mean(mpjpe)),
        "mpjpe_mm_p95": float(np.percentile(mpjpe, 95)),
        "zpe_vs_gzip_mean_multiplier": improvement,
        "zpe_beats_gzip_sequences": int(sum(1 for row in rows if float(row["zpe_ratio"]) > float(row["gzip_ratio"]))),
    }


def benchmark_table_rows(summary: dict[str, Any]) -> list[dict[str, str]]:
    dataset_label = f"CMU MoCap public subset ({summary['completed_sequences']} sequences)"
    return [
        {
            "dataset": dataset_label,
            "sequences": str(summary["completed_sequences"]),
            "joints": f"{summary['joint_count_mean']:.2f} mean",
            "frames": str(summary["total_frames"]),
            "ratio": f"{summary['zpe_ratio_mean']:.4f}x",
            "rmse_deg": f"{summary['joint_angle_rmse_deg_mean']:.4f}",
            "mpjpe_mm": f"{summary['mpjpe_mm_mean']:.4f}",
        }
    ]


def baseline_table_rows(summary: dict[str, Any]) -> list[dict[str, str]]:
    multiplier = summary.get("zpe_vs_gzip_mean_multiplier")
    improvement = "n/a" if multiplier is None else f"{float(multiplier):.4f}x"
    dataset_label = f"CMU MoCap public subset ({summary['completed_sequences']} sequences)"
    return [
        {
            "dataset": dataset_label,
            "baseline": "gzip -9 vs raw BVH float32",
            "zpe": f"{summary['zpe_ratio_mean']:.4f}x",
            "ratio": f"{summary['gzip_ratio_mean']:.4f}x",
            "improvement": improvement,
        }
    ]
