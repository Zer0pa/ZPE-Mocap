#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
from urllib.parse import urlparse

from _common import DEFAULT_CMU_SAMPLE_URL, DEFAULT_SEED, download_file, ensure_output_dir, roundtrip_bvh, write_json


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Download one CMU BVH sample, compress it, and verify roundtrip.")
    parser.add_argument("--sample-url", default=DEFAULT_CMU_SAMPLE_URL, help="CMU BVH source URL.")
    parser.add_argument("--cache-dir", help="Cache directory for downloaded BVH files.")
    parser.add_argument("--output-dir", help="Directory for emitted demo artifacts.")
    parser.add_argument("--clip-id", default="cmu_01_01")
    parser.add_argument("--label", default="walk")
    parser.add_argument("--seed", type=int, default=DEFAULT_SEED)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    output_dir = ensure_output_dir(args.output_dir, prefix="zpe_mocap_cmu_demo_")
    cache_dir = Path(args.cache_dir) if args.cache_dir else (output_dir / "cache")
    source_name = Path(urlparse(args.sample_url).path).name or "cmu_sample.bvh"
    cached_bvh = cache_dir / source_name
    if not cached_bvh.exists():
        download_file(args.sample_url, cached_bvh)

    summary = roundtrip_bvh(cached_bvh, clip_id=args.clip_id, label=args.label, seed=args.seed)
    summary["source_url"] = args.sample_url
    summary["cached_bvh"] = str(cached_bvh)
    summary["summary_path"] = str(output_dir / "cmu_offline_demo_summary.json")
    write_json(Path(summary["summary_path"]), summary)
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
