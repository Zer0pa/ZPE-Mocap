#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

from _common import DEFAULT_SEED, ensure_output_dir, roundtrip_bvh, write_json, write_minimal_bvh


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Compress and roundtrip a BVH file with ZPE-Mocap.")
    parser.add_argument("--input", type=Path, help="Path to a BVH file. Defaults to a minimal local fixture.")
    parser.add_argument("--output-dir", help="Directory for emitted demo artifacts.")
    parser.add_argument("--clip-id", default="example_bvh")
    parser.add_argument("--label", default="walk")
    parser.add_argument("--seed", type=int, default=DEFAULT_SEED)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    output_dir = ensure_output_dir(args.output_dir, prefix="zpe_mocap_bvh_")
    source_path = args.input or (output_dir / "minimal_walk.bvh")
    if args.input is None:
        write_minimal_bvh(source_path)

    summary = roundtrip_bvh(source_path, clip_id=args.clip_id, label=args.label, seed=args.seed)
    summary["summary_path"] = str(output_dir / "bvh_compress_summary.json")
    write_json(Path(summary["summary_path"]), summary)
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
