#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import shlex
import sys
from pathlib import Path
from statistics import mean, median
from time import perf_counter_ns

CODE_ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = CODE_ROOT.parent
if str(CODE_ROOT) not in sys.path:
    sys.path.insert(0, str(CODE_ROOT))

from zpe_mocap.bvh_loader import bvhio, load_bvh_motion_clip
from zpe_mocap.codec import decode_zpmoc, encode_clip
from zpe_mocap.cmu import load_manifest, resolve_cmu_layout, select_manifest_entries
from zpe_mocap.constants import GLOBAL_SEED
from zpe_mocap.metrics import joint_rmse_deg, mpjpe_mm

DEFAULT_ARTIFACT_DIR = REPO_ROOT / "proofs" / "artifacts" / "cmu_benchmarks"
DEFAULT_OUTPUT = DEFAULT_ARTIFACT_DIR / "cmu_benchmark_results.json"


def now_iso() -> str:
    from datetime import datetime, timezone

    return datetime.now(timezone.utc).isoformat()


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Benchmark ZPE-Mocap on committed CMU fixture clips.")
    parser.add_argument("--mode", choices=("fixture", "external", "auto"), default="fixture")
    parser.add_argument("--root", default=None, help="CMU root containing bvh/ and manifest.json")
    parser.add_argument("--manifest", default=None, help="manifest path override")
    parser.add_argument(
        "--subject-trial",
        action="append",
        dest="subject_trials",
        default=None,
        help="specific subject_trial ids to include; repeat for multiple ids",
    )
    parser.add_argument("--seed", type=int, default=GLOBAL_SEED)
    parser.add_argument("--latency-repeats", type=int, default=5, help="number of encode/decode timing repeats per clip")
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT), help="results JSON path or '-' for stdout")
    parser.add_argument("--dry-run", action="store_true", help="print resolved selection and exit")
    return parser.parse_args()


def _missing_files(entries: list[dict], root: Path) -> list[str]:
    missing: list[str] = []
    for entry in entries:
        relative_path = entry.get("relative_path")
        if isinstance(relative_path, str):
            candidate = root / relative_path
            if not candidate.exists():
                missing.append(str(candidate))
    return missing


def _load_selection(args: argparse.Namespace) -> tuple[dict, list[dict], list[dict]]:
    layout = resolve_cmu_layout(mode=args.mode, root=args.root, manifest_path=args.manifest)
    entries = load_manifest(mode=layout.mode, root=layout.root, manifest_path=layout.manifest_path)
    selected = select_manifest_entries(
        entries,
        subject_trials=args.subject_trials,
    )
    if not args.subject_trials:
        selected = list(entries)
    return {
        "mode": layout.mode,
        "root": str(layout.root),
        "manifest_path": str(layout.manifest_path),
    }, entries, selected


def _dry_run_report(args: argparse.Namespace) -> dict:
    try:
        layout_info, entries, selected = _load_selection(args)
    except Exception as exc:
        return {
            "timestamp_utc": now_iso(),
            "ready": False,
            "error": str(exc),
        }

    root = Path(layout_info["root"])
    manifest_path = Path(layout_info["manifest_path"])
    missing_files = _missing_files(selected, root)
    return {
        "timestamp_utc": now_iso(),
        "mode": layout_info["mode"],
        "root": layout_info["root"],
        "manifest_path": layout_info["manifest_path"],
        "manifest_exists": manifest_path.exists(),
        "available_clip_count": len(entries),
        "selected_clip_count": len(selected),
        "selected_subject_trials": [entry["subject_trial"] for entry in selected],
        "missing_files": missing_files,
        "bvhio_available": bvhio is not None,
        "ready": manifest_path.exists() and bool(selected) and not missing_files and bvhio is not None,
    }


def _write_output(path: str, payload: dict) -> None:
    if path == "-":
        print(json.dumps(payload, indent=2, sort_keys=True))
        return
    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(
        json.dumps(
            {
                "status": "ok",
                "output": str(output_path),
                "clip_count": payload["summary"]["clip_count"],
            },
            indent=2,
            sort_keys=True,
        )
    )


def _measure_ms(func, repeats: int) -> tuple[object, list[float]]:
    result = None
    samples_ms: list[float] = []
    for _ in range(repeats):
        started = perf_counter_ns()
        result = func()
        elapsed_ns = perf_counter_ns() - started
        samples_ms.append(elapsed_ns / 1_000_000.0)
    return result, samples_ms


def _load_clip(entry: dict, root: Path):
    source_path = root / entry["relative_path"]
    label = entry.get("benchmark_category") or entry.get("published_description") or "unknown"
    return load_bvh_motion_clip(source_path, clip_id=entry["subject_trial"], label=label)


def _measure_clip(root: Path, entry: dict, seed: int, repeats: int) -> dict:
    clip = _load_clip(entry, root)
    encoded, encode_latency_samples_ms = _measure_ms(lambda: encode_clip(clip, seed=seed), repeats)
    decoded, decode_latency_samples_ms = _measure_ms(lambda: decode_zpmoc(encoded.payload), repeats)
    source_path = root / entry["relative_path"]
    source_bvh_bytes = source_path.stat().st_size
    encoded_size_bytes = int(encoded.encoded_size_bytes)
    compression_ratio_vs_source_bvh_file = source_bvh_bytes / float(encoded_size_bytes) if encoded_size_bytes else 0.0

    return {
        "subject_trial": entry["subject_trial"],
        "benchmark_category": entry.get("benchmark_category"),
        "published_description": entry.get("published_description"),
        "selection_rationale": entry.get("selection_rationale"),
        "relative_path": entry.get("relative_path"),
        "fixture_sha256": entry.get("sha256"),
        "source_archive_url": entry.get("source_archive_url"),
        "source_release": entry.get("source_release"),
        "source_bvh_bytes": source_bvh_bytes,
        "frame_count": int(clip.positions_m.shape[0]),
        "joint_count": int(clip.positions_m.shape[1]),
        "fps": int(clip.fps),
        "compression_ratio_vs_raw_bvh_float32": float(encoded.compression_ratio),
        "compression_ratio_vs_source_bvh_file": compression_ratio_vs_source_bvh_file,
        "encoded_size_bytes": encoded_size_bytes,
        "raw_bvh_float32_bytes": int(encoded.raw_bvh_float32_bytes),
        "payload_hash": encoded.payload_hash,
        "mpjpe_mm": float(mpjpe_mm(clip.positions_m, decoded.positions_m)),
        "joint_angle_rmse_deg": float(joint_rmse_deg(clip.angles_deg, decoded.angles_deg)),
        "encode_latency_ms": float(median(encode_latency_samples_ms)),
        "decode_latency_ms": float(median(decode_latency_samples_ms)),
        "encode_latency_samples_ms": encode_latency_samples_ms,
        "decode_latency_samples_ms": decode_latency_samples_ms,
    }


def _aggregate(entries: list[dict]) -> dict:
    ratios = [entry["compression_ratio_vs_raw_bvh_float32"] for entry in entries]
    file_ratios = [entry["compression_ratio_vs_source_bvh_file"] for entry in entries]
    mpjpes = [entry["mpjpe_mm"] for entry in entries]
    joint_rmses = [entry["joint_angle_rmse_deg"] for entry in entries]
    encode_ms = [entry["encode_latency_ms"] for entry in entries]
    decode_ms = [entry["decode_latency_ms"] for entry in entries]
    frame_counts = [entry["frame_count"] for entry in entries]
    joint_counts = [entry["joint_count"] for entry in entries]
    return {
        "clip_count": len(entries),
        "compression_ratio_vs_raw_bvh_float32_mean": float(mean(ratios)),
        "compression_ratio_vs_raw_bvh_float32_median": float(median(ratios)),
        "compression_ratio_vs_raw_bvh_float32_min": float(min(ratios)),
        "compression_ratio_vs_raw_bvh_float32_max": float(max(ratios)),
        "compression_ratio_vs_source_bvh_file_mean": float(mean(file_ratios)),
        "compression_ratio_vs_source_bvh_file_median": float(median(file_ratios)),
        "mpjpe_mean_mm": float(mean(mpjpes)),
        "mpjpe_median_mm": float(median(mpjpes)),
        "mpjpe_max_mm": float(max(mpjpes)),
        "joint_angle_rmse_deg_mean": float(mean(joint_rmses)),
        "joint_angle_rmse_deg_median": float(median(joint_rmses)),
        "encode_latency_mean_ms": float(mean(encode_ms)),
        "encode_latency_median_ms": float(median(encode_ms)),
        "decode_latency_mean_ms": float(mean(decode_ms)),
        "decode_latency_median_ms": float(median(decode_ms)),
        "frame_count_min": int(min(frame_counts)),
        "frame_count_max": int(max(frame_counts)),
        "joint_count_min": int(min(joint_counts)),
        "joint_count_max": int(max(joint_counts)),
    }


def main() -> None:
    args = _parse_args()
    if args.dry_run:
        print(json.dumps(_dry_run_report(args), indent=2, sort_keys=True))
        return
    if args.latency_repeats < 1:
        raise RuntimeError("--latency-repeats must be at least 1.")

    layout_info, entries, selected = _load_selection(args)
    if not entries:
        raise RuntimeError(f"CMU manifest missing or empty at {layout_info['manifest_path']}.")
    if not selected:
        raise RuntimeError("No CMU clips selected for benchmarking.")

    root = Path(layout_info["root"])
    missing_files = _missing_files(selected, root)
    if missing_files:
        raise RuntimeError(f"CMU selection includes missing files: {missing_files[:5]}")

    per_clip = [
        _measure_clip(root, entry, seed=args.seed + index, repeats=args.latency_repeats)
        for index, entry in enumerate(selected)
    ]

    report = {
        "timestamp_utc": now_iso(),
        "python_executable": sys.executable,
        "argv": sys.argv,
        "command_line": shlex.join(sys.argv),
        "mode": layout_info["mode"],
        "root": layout_info["root"],
        "manifest_path": layout_info["manifest_path"],
        "artifact_dir": str(Path(args.output).parent) if args.output != "-" else None,
        "selected_clip_count": len(selected),
        "selected_subject_trials": [entry["subject_trial"] for entry in selected],
        "latency_measurement": {
            "repeats": args.latency_repeats,
            "unit": "ms",
            "statistic": "median",
        },
        "notes": [
            "Compression ratio vs raw BVH float32 is the repo's canonical benchmark basis.",
            "Compression ratio vs source BVH file size is included for transparency but is not comparable to the synthetic benchmark headline.",
            "Oversized source BVHs are committed as documented first-360-frame fixture extracts to keep the offline corpus bounded.",
        ],
        "summary": _aggregate(per_clip),
        "selected_manifest_entries": selected,
        "entries": per_clip,
    }
    _write_output(args.output, report)


if __name__ == "__main__":
    main()
