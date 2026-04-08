from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
from typing import Iterable

from .bvh_loader import BvhMetadata, load_bvh_metadata, load_bvh_motion_clip
from .constants import ACTION_LABELS, REPO_ROOT
from .utils import write_json

CMU_ROOT = Path(os.environ.get("ZPE_MOCAP_CMU_ROOT", str(REPO_ROOT.parent / "external" / "cmu")))
CMU_BVH_ROOT = CMU_ROOT / "bvh"
CMU_INDEX_ROOT = CMU_ROOT / "indexed"
CMU_MANIFEST = CMU_ROOT / "manifest.json"


def _manifest_error(detail: str) -> ValueError:
    return ValueError(f"Invalid CMU manifest {CMU_MANIFEST}: {detail}")


def _clip_reference_error(filename: str, detail: str) -> ValueError:
    return _manifest_error(f"clip entry ({filename}) {detail}")


def _manifest_entry_name(entry: object, index: int) -> str:
    if isinstance(entry, dict):
        filename = entry.get("filename")
        if isinstance(filename, str) and filename:
            return f"clip entry[{index}] ({filename})"
    return f"clip entry[{index}]"


def _validate_manifest_entry(entry: object, index: int) -> dict:
    entry_name = _manifest_entry_name(entry, index)
    if not isinstance(entry, dict):
        raise _manifest_error(f"{entry_name} must be an object, got {type(entry).__name__}.")

    filename = entry.get("filename")
    if not isinstance(filename, str) or not filename.strip():
        raise _manifest_error(f"{entry_name} has invalid 'filename': {filename!r}.")

    action_label = entry.get("action_label")
    if action_label is not None and not isinstance(action_label, str):
        raise _manifest_error(f"{entry_name} has invalid 'action_label': {action_label!r}.")

    return entry


def infer_action_label(name: str, labels: Iterable[str] = ACTION_LABELS) -> str:
    lowered = name.lower()
    for label in labels:
        if label in lowered:
            return label
    return "unknown"


def bvh_files() -> list[Path]:
    if not CMU_BVH_ROOT.exists():
        return []
    return sorted([p for p in CMU_BVH_ROOT.rglob("*.bvh") if p.is_file()])


def build_manifest(max_files: int | None = None) -> list[dict]:
    entries: list[dict] = []
    for path in bvh_files():
        if max_files and len(entries) >= max_files:
            break
        sha = hashlib.sha256(path.read_bytes()).hexdigest()
        meta: BvhMetadata = load_bvh_metadata(path)
        label = infer_action_label(path.stem)
        entries.append(
            {
                "filename": str(path.relative_to(CMU_ROOT)),
                "sha256": sha,
                "frames": meta.frames,
                "joints": meta.joints,
                "fps": meta.fps,
                "action_label": label,
                "license": "CMU-commercial-safe",
            }
        )
    CMU_ROOT.mkdir(parents=True, exist_ok=True)
    write_json(CMU_MANIFEST, entries)
    return entries


def load_manifest() -> list[dict]:
    if not CMU_MANIFEST.exists():
        return []

    try:
        entries = json.loads(CMU_MANIFEST.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise _manifest_error(f"could not be parsed at line {exc.lineno} column {exc.colno}: {exc.msg}.") from exc

    if not isinstance(entries, list):
        raise _manifest_error(f"expected a list of clip entries, got {type(entries).__name__}.")

    return [_validate_manifest_entry(entry, index) for index, entry in enumerate(entries)]


def load_cmu_clips(max_clips: int | None = None, required_labels: Iterable[str] | None = None) -> list:
    entries = load_manifest()
    if not entries:
        raise RuntimeError("CMU manifest missing; run build_manifest first.")

    required = set(required_labels) if required_labels else None
    selected = []
    for entry in entries:
        if required and entry.get("action_label") not in required:
            continue
        selected.append(entry)
        if max_clips and len(selected) >= max_clips:
            break

    clips = []
    for entry in selected:
        filename = entry["filename"]
        path = CMU_ROOT / filename
        if not path.is_file():
            raise _clip_reference_error(filename, f"points to missing file: {path}.")
        label = entry.get("action_label", "unknown")
        clip_id = Path(filename).stem
        clips.append(load_bvh_motion_clip(path, clip_id=clip_id, label=label))
    return clips
