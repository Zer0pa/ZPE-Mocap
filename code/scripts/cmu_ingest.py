#!/usr/bin/env python3
from __future__ import annotations

import re
import shutil
import urllib.request
import zipfile
from pathlib import Path

import numpy as np

from _common import EXTERNAL_ROOT, log_command, now_iso, write_text
from zpe_mocap.benchmark import _tokens_from_clip
from zpe_mocap.cmu import CMU_BVH_ROOT, CMU_INDEX_ROOT, CMU_MANIFEST, build_manifest, load_cmu_clips
from zpe_mocap.constants import ACTION_LABELS

CGSPEED_PAGE = "https://sites.google.com/a/cgspeed.com/cgspeed/motion-capture/cmu-bvh-conversions"


def _download_zip(url: str, dest: Path) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    with urllib.request.urlopen(url) as resp, open(dest, "wb") as f:
        shutil.copyfileobj(resp, f)


def _find_cgspeed_zip() -> str | None:
    with urllib.request.urlopen(CGSPEED_PAGE) as resp:
        html = resp.read().decode("utf-8", errors="ignore")
    matches = re.findall(r"https?://[^\"]+\\.zip", html)
    return matches[0] if matches else None


def main() -> None:
    log_command("python3 code/scripts/cmu_ingest.py")

    CMU_BVH_ROOT.mkdir(parents=True, exist_ok=True)
    zip_url = _find_cgspeed_zip()
    if zip_url is None:
        raise RuntimeError("Unable to locate CMU BVH zip on cgspeed page.")

    zip_path = EXTERNAL_ROOT / "cmu" / "cmu_bvh.zip"
    _download_zip(zip_url, zip_path)

    with zipfile.ZipFile(zip_path, "r") as zf:
        zf.extractall(CMU_BVH_ROOT)

    zip_path.unlink(missing_ok=True)

    entries = build_manifest(max_files=None)
    if len(entries) < 500:
        raise RuntimeError(f"CMU ingest found {len(entries)} clips; need at least 500.")

    clips = load_cmu_clips(max_clips=500, required_labels=ACTION_LABELS)
    CMU_INDEX_ROOT.mkdir(parents=True, exist_ok=True)
    for clip in clips:
        xy_tokens, xz_tokens = _tokens_from_clip(clip)
        out = CMU_INDEX_ROOT / f"{clip.clip_id}.npz"
        np.savez_compressed(out, xy_tokens=xy_tokens, xz_tokens=xz_tokens, label=clip.label)

    write_text(
        CMU_MANIFEST.parent / "ingest_log.txt",
        f"[{now_iso()}] CMU ingest complete: {len(entries)} files, indexed {len(clips)} clips\n",
    )


if __name__ == "__main__":
    main()
