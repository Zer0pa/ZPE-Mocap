#!/usr/bin/env python3
from __future__ import annotations

import gzip

import numpy as np
import zstandard as zstd

from _common import (
    comet_log_asset,
    comet_log_metrics,
    finalize_comet,
    gate_file,
    init_comet_context,
    init_output_root,
    log_command,
    now_iso,
    resolve_corpus,
    update_run_manifest,
    write_checkpoint,
)
from zpe_mocap.cmu import load_cmu_clips
from zpe_mocap.codec import encode_clip
from zpe_mocap.constants import ACTION_LABELS
from zpe_mocap.utils import write_json


def _gzip_ratio(raw_bytes: bytes) -> float:
    comp = gzip.compress(raw_bytes, compresslevel=9)
    return len(raw_bytes) / float(len(comp)) if comp else 0.0


def _zstd_ratio(raw_bytes: bytes) -> float:
    comp = zstd.ZstdCompressor(level=19).compress(raw_bytes)
    return len(raw_bytes) / float(len(comp)) if comp else 0.0


def main() -> None:
    init_output_root()
    log_command("python3 code/scripts/gate_m1_acl_comparator.py")
    corpus = resolve_corpus("cmu")
    comet = init_comet_context("gate_m1", corpus)

    clips = load_cmu_clips(max_clips=500, required_labels=ACTION_LABELS)
    zpe_ratios = []
    gzip_ratios = []
    zstd_ratios = []

    for idx, clip in enumerate(clips):
        encoded = encode_clip(clip, seed=20260220 + idx)
        zpe_ratios.append(encoded.compression_ratio)
        raw_bytes = (
            clip.angles_deg.astype(np.float32).tobytes()
            + clip.positions_m.astype(np.float32).tobytes()
        )
        gzip_ratios.append(_gzip_ratio(raw_bytes))
        zstd_ratios.append(_zstd_ratio(raw_bytes))

    output = {
        "corpus": "CMU-500-commercial-safe",
        "zpe_vs_raw_bvh_float32_mean": float(np.mean(zpe_ratios)) if zpe_ratios else None,
        "gzip_l9_vs_raw_bvh_float32_mean": float(np.mean(gzip_ratios)) if gzip_ratios else None,
        "zstd_l19_vs_raw_bvh_float32_mean": float(np.mean(zstd_ratios)) if zstd_ratios else None,
        "acl_v2_literature_cmu_2534clips": 21.77,
        "acl_source": "Frechette 2022, ACL v2.0 benchmark",
        "framing": "ZPE-MoCap compresses vs raw BVH float32. ACL uses variable-bitrate quantization targeting sub-0.01cm error; ZPE tokens are a searchable index stream, not a quality-competitive compression codec.",
        "note": "ACL binary not run in-lane; literature value used. gzip/zstd provide in-lane general-purpose comparators on same corpus.",
    }

    write_json(gate_file("acl_direct_comparator_table.json"), output)

    comet_log_metrics(
        comet,
        {
            "zpe_vs_raw_bvh_float32_mean": output["zpe_vs_raw_bvh_float32_mean"],
            "gzip_l9_vs_raw_bvh_float32_mean": output["gzip_l9_vs_raw_bvh_float32_mean"],
            "zstd_l19_vs_raw_bvh_float32_mean": output["zstd_l19_vs_raw_bvh_float32_mean"],
            "corpus_type": 1,
        },
    )
    comet_log_asset(comet, gate_file("acl_direct_comparator_table.json"))

    comet_url = finalize_comet(comet)
    write_checkpoint(
        gate="gate_m1",
        status="PASS" if output["zpe_vs_raw_bvh_float32_mean"] else "FAIL",
        details=output,
        comet_url=comet_url,
    )
    update_run_manifest(
        {
            "gate": "gate_m1",
            "corpus": corpus,
            "status": "PASS" if output["zpe_vs_raw_bvh_float32_mean"] else "FAIL",
            "timestamp_utc": now_iso(),
            "comet_experiment_url": comet_url,
        }
    )


if __name__ == "__main__":
    main()
