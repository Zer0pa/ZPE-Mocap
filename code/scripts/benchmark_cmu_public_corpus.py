#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import shutil
import sys
import time
import urllib.request
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path
from typing import Any

from _common import EXTERNAL_ROOT, ROOT, now_iso, write_text
from zpe_mocap.bvh_loader import load_bvh_motion_clip
from zpe_mocap.cmu_benchmark import (
    CMU_GITHUB_RAW_ROOT,
    CMU_GITHUB_TREE_URL,
    baseline_table_rows,
    benchmark_table_rows,
    gzip_ratio,
    list_cmu_bvh_paths,
    select_round_robin_subset,
    select_successful_rows,
    subject_id_for_path,
    summarize_clip_rows,
)
from zpe_mocap.codec import decode_zpmoc, encode_clip
from zpe_mocap.metrics import joint_rmse_deg, mpjpe_mm
from zpe_mocap.utils import ensure_dir, write_json

DEFAULT_ARTIFACT_ROOT = ROOT / "proofs" / "artifacts" / "2026-04-08_cmu_public_corpus_benchmark"
DEFAULT_TIMEOUT_SEC = 180


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Benchmark ZPE-Mocap on a reproducible public CMU BVH subset.")
    parser.add_argument("--target-sequences", type=int, default=120, help="Successful CMU BVH sequences required.")
    parser.add_argument("--extra-candidates", type=int, default=40, help="Additional candidates to cover failures.")
    parser.add_argument("--workers", type=int, default=4, help="Parallel worker count for clip benchmarking.")
    parser.add_argument("--seed", type=int, default=20260408, help="Base seed for deterministic encoding.")
    parser.add_argument(
        "--cache-root",
        default=str(EXTERNAL_ROOT / "cmu_github_mirror"),
        help="Local cache for downloaded CMU BVH files.",
    )
    parser.add_argument(
        "--artifact-root",
        default=str(DEFAULT_ARTIFACT_ROOT),
        help="Artifact directory for emitted benchmark outputs.",
    )
    parser.add_argument("--timeout-sec", type=int, default=DEFAULT_TIMEOUT_SEC, help="Network timeout per request.")
    parser.add_argument("--retry-count", type=int, default=3, help="Retry count for transient network failures.")
    return parser.parse_args()


def _urlopen(request: urllib.request.Request, timeout_sec: int, retry_count: int):
    last_error: Exception | None = None
    for attempt in range(retry_count):
        try:
            return urllib.request.urlopen(request, timeout=timeout_sec)
        except Exception as exc:  # pragma: no cover - network failures are environment-specific
            last_error = exc
            if attempt + 1 >= retry_count:
                break
            time.sleep(1.0 + attempt)
    if last_error is None:  # pragma: no cover - defensive fallback
        raise RuntimeError("urlopen failed without an exception.")
    raise last_error


def _fetch_json(url: str, timeout_sec: int, retry_count: int) -> dict[str, Any]:
    request = urllib.request.Request(url, headers={"User-Agent": "codex-zpe-mocap-phase3"})
    with _urlopen(request, timeout_sec=timeout_sec, retry_count=retry_count) as response:
        return json.load(response)


def _download_file(url: str, destination: Path, timeout_sec: int, retry_count: int) -> Path:
    request = urllib.request.Request(url, headers={"User-Agent": "codex-zpe-mocap-phase3"})
    destination.parent.mkdir(parents=True, exist_ok=True)
    with _urlopen(request, timeout_sec=timeout_sec, retry_count=retry_count) as response, destination.open("wb") as handle:
        shutil.copyfileobj(response, handle)
    return destination


def _cache_path(cache_root: Path, cmu_path: str) -> Path:
    return cache_root / cmu_path


def _download_selected(
    cache_root: Path,
    selected_paths: list[str],
    timeout_sec: int,
    retry_count: int,
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for cmu_path in selected_paths:
        raw_url = CMU_GITHUB_RAW_ROOT + cmu_path
        local_path = _cache_path(cache_root, cmu_path)
        if not local_path.exists():
            _download_file(raw_url, local_path, timeout_sec=timeout_sec, retry_count=retry_count)
        rows.append(
            {
                "cmu_path": cmu_path,
                "raw_url": raw_url,
                "local_path": str(local_path),
                "size_bytes": int(local_path.stat().st_size),
            }
        )
    return rows


def _benchmark_one(local_path_str: str, cmu_path: str, seed: int) -> dict[str, Any]:
    try:
        local_path = Path(local_path_str)
        clip = load_bvh_motion_clip(
            local_path,
            clip_id=Path(cmu_path).stem,
            label=subject_id_for_path(cmu_path),
        )
        encoded = encode_clip(clip, seed=seed)
        decoded = decode_zpmoc(encoded.payload)
        raw_float_bytes = (
            clip.angles_deg.astype("float32").tobytes() + clip.positions_m.astype("float32").tobytes()
        )
        return {
            "status": "ok",
            "cmu_path": cmu_path,
            "fps": int(clip.fps),
            "frames": int(clip.positions_m.shape[0]),
            "joints": int(len(clip.joint_names)),
            "zpe_ratio": float(encoded.compression_ratio),
            "gzip_ratio": float(gzip_ratio(raw_float_bytes)),
            "joint_angle_rmse_deg": float(joint_rmse_deg(clip.angles_deg, decoded.angles_deg)),
            "mpjpe_mm": float(mpjpe_mm(clip.positions_m, decoded.positions_m)),
            "encoded_size_bytes": int(encoded.encoded_size_bytes),
            "raw_bvh_float32_bytes": int(encoded.raw_bvh_float32_bytes),
            "payload_hash": encoded.payload_hash,
        }
    except Exception as exc:  # pragma: no cover - integration failure path
        return {
            "status": "error",
            "cmu_path": cmu_path,
            "error": f"{type(exc).__name__}: {exc}",
        }


def _write_blockers(artifact_root: Path) -> None:
    blender_path = shutil.which("blender")
    lines = [
        "# Phase 3 Blockers",
        "",
        f"- CMU corpus benchmark: executed via public GitHub mirror `{CMU_GITHUB_TREE_URL}`.",
        "- AMASS benchmark: blocked. Registration gate at `https://amass.is.tue.mpg.de/` requires owner-approved access.",
        "- Mixamo benchmark: blocked. Adobe login gate at `https://www.mixamo.com/` requires owner-approved access.",
        "- Blender viewport GIF: blocked. `blender` executable not found on PATH in this workspace.",
    ]
    if blender_path:
        lines[-1] = f"- Blender viewport GIF: executable present at `{blender_path}`, but no GIF run was executed in this phase."
    write_text(artifact_root / "phase3_blockers.md", "\n".join(lines) + "\n")


def main() -> None:
    args = parse_args()
    artifact_root = Path(args.artifact_root)
    cache_root = Path(args.cache_root)
    ensure_dir(artifact_root)
    ensure_dir(cache_root)

    command = "python3 code/scripts/benchmark_cmu_public_corpus.py " + " ".join(sys.argv[1:])
    write_text(artifact_root / "command.txt", command.rstrip() + "\n")

    tree_payload = _fetch_json(CMU_GITHUB_TREE_URL, timeout_sec=args.timeout_sec, retry_count=args.retry_count)
    all_paths = list_cmu_bvh_paths(tree_payload)
    requested_candidates = args.target_sequences + args.extra_candidates
    selected_paths = select_round_robin_subset(all_paths, requested_candidates)
    download_rows = _download_selected(
        cache_root,
        selected_paths,
        timeout_sec=args.timeout_sec,
        retry_count=args.retry_count,
    )

    successful_rows: list[dict[str, Any]] = []
    failure_rows: list[dict[str, Any]] = []
    with ProcessPoolExecutor(max_workers=max(1, args.workers)) as pool:
        future_map = {}
        for index, row in enumerate(download_rows):
            future = pool.submit(_benchmark_one, row["local_path"], row["cmu_path"], args.seed + index)
            future_map[future] = row["cmu_path"]

        for future in as_completed(future_map):
            result = future.result()
            if result["status"] == "ok":
                successful_rows.append(result)
                continue
            if result["status"] == "error":
                failure_rows.append(result)

    if len(successful_rows) < args.target_sequences:
        raise RuntimeError(
            f"Only benchmarked {len(successful_rows)} successful CMU clips; need {args.target_sequences}. "
            f"Failures: {len(failure_rows)}."
        )
    clip_rows = select_successful_rows(
        successful_rows,
        selected_paths=selected_paths,
        target_sequences=args.target_sequences,
    )

    summary = summarize_clip_rows(clip_rows, target_sequences=args.target_sequences)
    output = {
        "generated_at_utc": now_iso(),
        "command": command.rstrip(),
        "dataset": {
            "name": "CMU MoCap public GitHub mirror subset",
            "source_tree_url": CMU_GITHUB_TREE_URL,
            "source_raw_root": CMU_GITHUB_RAW_ROOT,
            "tree_truncated": bool(tree_payload.get("truncated")),
            "available_bvh_files": len(all_paths),
            "candidate_count": len(selected_paths),
            "successful_candidate_count": len(successful_rows),
            "selection_method": "round_robin_by_subject_directory",
        },
        "summary": summary,
        "benchmark_rows": benchmark_table_rows(summary),
        "baseline_rows": baseline_table_rows(summary),
        "downloads": download_rows,
        "clip_metrics": clip_rows,
        "failures": failure_rows,
    }

    write_json(artifact_root / "cmu_public_corpus_benchmark.json", output)
    write_json(artifact_root / "cmu_public_corpus_clip_metrics.json", clip_rows)
    _write_blockers(artifact_root)

    print(json.dumps(output["summary"], indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
