#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import shlex
import sys
from datetime import datetime, timezone
from pathlib import Path
from statistics import mean

CODE_ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = CODE_ROOT.parent
if str(CODE_ROOT) not in sys.path:
    sys.path.insert(0, str(CODE_ROOT))

from zpe_mocap.benchmark import _tokens_from_clip  # noqa: E402
from zpe_mocap.bvh_loader import bvhio, load_bvh_motion_clip  # noqa: E402
from zpe_mocap.metrics import mean_reciprocal_rank, median_rank, percentile_ms, recall_at_k  # noqa: E402
from zpe_mocap.search import MotionSuffixIndex, flatten_tokens  # noqa: E402

DEFAULT_CORPUS_ROOT = REPO_ROOT.parent / "external" / "cmu_github_mirror"
DEFAULT_ARTIFACT_DIR = REPO_ROOT / "proofs" / "artifacts" / "2026-04-24_cmu_retrieval_benchmark"
DEFAULT_RESULTS = DEFAULT_ARTIFACT_DIR / "results.json"
DEFAULT_SUMMARY = DEFAULT_ARTIFACT_DIR / "summary.md"


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Benchmark real-corpus CMU retrieval on held-out non-overlapping windows."
    )
    parser.add_argument("--corpus-root", default=str(DEFAULT_CORPUS_ROOT))
    parser.add_argument("--window-frames", type=int, default=48)
    parser.add_argument("--library-windows-per-clip", type=int, default=2)
    parser.add_argument("--query-windows-per-clip", type=int, default=1)
    parser.add_argument("--max-clips", type=int, default=None)
    parser.add_argument("--top-k", type=int, default=10)
    parser.add_argument("--candidate-cap", type=int, default=64)
    parser.add_argument("--results-json", default=str(DEFAULT_RESULTS))
    parser.add_argument("--summary-md", default=str(DEFAULT_SUMMARY))
    parser.add_argument("--stdout", action="store_true")
    return parser.parse_args()


def scan_bvh_files(root: Path, max_clips: int | None) -> list[Path]:
    files = sorted(path for path in root.rglob("*.bvh") if path.is_file())
    if max_clips is not None:
        files = files[:max_clips]
    return files


def non_overlapping_window_starts(frame_count: int, window_frames: int, window_count: int) -> list[int]:
    required = window_frames * window_count
    if frame_count < required:
        return []

    slack = frame_count - required
    gap = slack // (window_count + 1)
    position = gap
    starts: list[int] = []
    for _ in range(window_count):
        starts.append(position)
        position += window_frames + gap
    return starts


def window_tokens(xy_tokens, xz_tokens, start: int, stop: int) -> list[int]:
    return flatten_tokens(xy_tokens[start:stop], xz_tokens[start:stop])


def build_summary(report: dict) -> str:
    summary = report["summary"]
    lines = [
        "# ZPE-Mocap CMU Retrieval Benchmark Summary",
        "",
        "## Scope",
        "",
        f"- corpus root: `{report['corpus_root']}`",
        f"- scanned BVH files: `{summary['scanned_bvh_file_count']}`",
        f"- clips used: `{summary['clip_count_used']}`",
        f"- clips skipped for short duration: `{summary['clip_count_skipped_short']}`",
        f"- window frames: `{summary['window_frames']}`",
        f"- library windows per clip: `{summary['library_windows_per_clip']}`",
        f"- query windows per clip: `{summary['query_windows_per_clip']}`",
        "",
        "## Retrieval Metrics",
        "",
        f"- recall@1: `{summary['recall_at_1']:.6f}`",
        f"- recall@5: `{summary['recall_at_5']:.6f}`",
        f"- recall@10: `{summary['recall_at_10']:.6f}`",
        f"- mean reciprocal rank: `{summary['mean_reciprocal_rank']:.6f}`",
        f"- median rank: `{summary['median_rank']}`",
        f"- latency p50: `{summary['latency_p50_ms']:.6f} ms`",
        f"- latency p95: `{summary['latency_p95_ms']:.6f} ms`",
        "",
        "## Interpretation",
        "",
        "- This benchmark is real-data retrieval over non-overlapping held-out windows from committed BVH corpus files.",
        "- The relevance target is source-clip identity, not action-level semantic labeling.",
        "- This strengthens the retrieval/indexing wedge without promoting playback-grade reconstruction.",
    ]
    return "\n".join(lines) + "\n"


def main() -> None:
    args = parse_args()
    if bvhio is None:
        raise RuntimeError("bvhio is required for real CMU retrieval benchmarking.")
    if args.window_frames < 1:
        raise RuntimeError("--window-frames must be positive.")

    corpus_root = Path(args.corpus_root)
    if not corpus_root.exists():
        raise RuntimeError(f"Corpus root does not exist: {corpus_root}")

    total_windows = args.library_windows_per_clip + args.query_windows_per_clip
    files = scan_bvh_files(corpus_root, args.max_clips)
    if not files:
        raise RuntimeError(f"No BVH files found under {corpus_root}")

    index = MotionSuffixIndex(k=8)
    index.max_candidates = args.candidate_cap

    query_specs: list[dict] = []
    clip_reports: list[dict] = []
    skipped_short: list[dict] = []

    for path in files:
        clip_id = path.stem
        clip = load_bvh_motion_clip(path, clip_id=clip_id, label=clip_id)
        frame_count = int(clip.positions_m.shape[0])
        starts = non_overlapping_window_starts(frame_count, args.window_frames, total_windows)
        if not starts:
            skipped_short.append(
                {
                    "clip_id": clip_id,
                    "relative_path": str(path.relative_to(corpus_root)),
                    "frame_count": frame_count,
                }
            )
            continue

        xy_tokens, xz_tokens = _tokens_from_clip(clip)
        library_starts = starts[: args.library_windows_per_clip]
        query_starts = starts[args.library_windows_per_clip :]
        doc_ids: list[str] = []

        for window_index, start in enumerate(library_starts):
            stop = start + args.window_frames
            doc_id = f"{clip_id}__lib_{window_index:02d}"
            index.add(doc_id, window_tokens(xy_tokens, xz_tokens, start, stop), clip_id)
            doc_ids.append(doc_id)

        for window_index, start in enumerate(query_starts):
            stop = start + args.window_frames
            query_specs.append(
                {
                    "query_id": f"{clip_id}__query_{window_index:02d}",
                    "clip_id": clip_id,
                    "relative_path": str(path.relative_to(corpus_root)),
                    "frame_start": start,
                    "frame_stop": stop,
                    "tokens": window_tokens(xy_tokens, xz_tokens, start, stop),
                }
            )

        clip_reports.append(
            {
                "clip_id": clip_id,
                "relative_path": str(path.relative_to(corpus_root)),
                "frame_count": frame_count,
                "fps": int(clip.fps),
                "library_doc_ids": doc_ids,
                "query_count": len(query_starts),
            }
        )

    if not query_specs:
        raise RuntimeError("No valid query windows were produced.")

    query_results: list[dict] = []
    ranks: list[int | None] = []
    latencies_ms: list[float] = []

    for query in query_specs:
        ids, elapsed_ms = index.query(query["tokens"], top_k=max(args.top_k, index.max_candidates))
        predicted_clip_ids = [index.labels[candidate_id] for candidate_id in ids]
        rank = None
        for offset, predicted_clip_id in enumerate(predicted_clip_ids, start=1):
            if predicted_clip_id == query["clip_id"]:
                rank = offset
                break
        ranks.append(rank)
        latencies_ms.append(elapsed_ms)
        query_results.append(
            {
                "query_id": query["query_id"],
                "clip_id": query["clip_id"],
                "relative_path": query["relative_path"],
                "frame_start": query["frame_start"],
                "frame_stop": query["frame_stop"],
                "rank": rank,
                "latency_ms": elapsed_ms,
                "top_results": [
                    {
                        "doc_id": candidate_id,
                        "clip_id": index.labels[candidate_id],
                    }
                    for candidate_id in ids[: args.top_k]
                ],
            }
        )

    clip_count_used = len(clip_reports)
    random_clip_hit_rate_at_1 = 1.0 / float(clip_count_used)
    random_clip_hit_rate_at_10 = min(float(args.top_k) / float(clip_count_used), 1.0)
    recall_1 = recall_at_k(ranks, 1)
    recall_5 = recall_at_k(ranks, 5)
    recall_10 = recall_at_k(ranks, 10)
    summary = {
        "metric": "heldout_window_clip_retrieval",
        "status": "PASS" if recall_1 > random_clip_hit_rate_at_1 else "FAIL",
        "scanned_bvh_file_count": len(files),
        "clip_count_used": clip_count_used,
        "clip_count_skipped_short": len(skipped_short),
        "library_window_count": len(index.docs),
        "query_window_count": len(query_specs),
        "window_frames": args.window_frames,
        "library_windows_per_clip": args.library_windows_per_clip,
        "query_windows_per_clip": args.query_windows_per_clip,
        "candidate_cap": index.max_candidates,
        "top_k": args.top_k,
        "relevance_definition": "same source clip across held-out non-overlapping windows",
        "random_clip_hit_rate_at_1": random_clip_hit_rate_at_1,
        "random_clip_hit_rate_at_10": random_clip_hit_rate_at_10,
        "recall_at_1": recall_1,
        "recall_at_5": recall_5,
        "recall_at_10": recall_10,
        "mean_reciprocal_rank": mean_reciprocal_rank(ranks),
        "median_rank": median_rank(ranks),
        "mean_rank": float(mean([rank for rank in ranks if rank is not None])) if any(rank is not None for rank in ranks) else None,
        "miss_count": int(sum(1 for rank in ranks if rank is None)),
        "latency_p50_ms": percentile_ms(latencies_ms, 50),
        "latency_p95_ms": percentile_ms(latencies_ms, 95),
        "latency_p99_ms": percentile_ms(latencies_ms, 99),
    }

    report = {
        "timestamp_utc": now_iso(),
        "python_executable": sys.executable,
        "argv": sys.argv,
        "command_line": shlex.join(sys.argv),
        "corpus_root": str(corpus_root),
        "summary": summary,
        "clips_used": clip_reports,
        "clips_skipped_short": skipped_short,
        "queries": query_results,
    }

    results_path = Path(args.results_json)
    summary_path = Path(args.summary_md)
    results_path.parent.mkdir(parents=True, exist_ok=True)
    summary_path.parent.mkdir(parents=True, exist_ok=True)
    results_path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    summary_path.write_text(build_summary(report), encoding="utf-8")

    if args.stdout:
        print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
