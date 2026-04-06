from __future__ import annotations

import json
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

from .bvh_loader import BvhMetadata, load_bvh_metadata, load_bvh_motion_clip
from .constants import CODE_ROOT, REPO_ROOT
from .utils import sha256_path, write_json

CMU_FIXTURE_ROOT = Path(os.environ.get("ZPE_MOCAP_CMU_FIXTURE_ROOT", str(CODE_ROOT / "fixtures" / "cmu")))
CMU_FIXTURE_BVH_ROOT = CMU_FIXTURE_ROOT / "bvh"
CMU_FIXTURE_INDEX_ROOT = CMU_FIXTURE_ROOT / "indexed"
CMU_FIXTURE_MANIFEST = CMU_FIXTURE_ROOT / "manifest.json"

CMU_EXTERNAL_ROOT = Path(os.environ.get("ZPE_MOCAP_CMU_ROOT", str(REPO_ROOT.parent / "external" / "cmu")))
CMU_EXTERNAL_BVH_ROOT = CMU_EXTERNAL_ROOT / "bvh"
CMU_EXTERNAL_INDEX_ROOT = CMU_EXTERNAL_ROOT / "indexed"
CMU_EXTERNAL_MANIFEST = CMU_EXTERNAL_ROOT / "manifest.json"

# Backward-compatible aliases for the historical external-corpus path.
CMU_ROOT = CMU_EXTERNAL_ROOT
CMU_BVH_ROOT = CMU_EXTERNAL_BVH_ROOT
CMU_INDEX_ROOT = CMU_EXTERNAL_INDEX_ROOT
CMU_MANIFEST = CMU_EXTERNAL_MANIFEST

DEFAULT_CMU_MODE = os.environ.get("ZPE_MOCAP_CMU_MODE", "auto")


@dataclass(frozen=True)
class CmuLayout:
    mode: str
    root: Path
    bvh_root: Path
    index_root: Path
    manifest_path: Path


def _coerce_path(path: str | Path | None) -> Path | None:
    if path is None:
        return None
    return Path(path)


def _root_from_mode(mode: str) -> Path:
    if mode == "fixture":
        return CMU_FIXTURE_ROOT
    if mode == "external":
        return CMU_EXTERNAL_ROOT
    raise ValueError(f"unsupported CMU mode {mode!r}")


def resolve_cmu_layout(
    mode: str | None = None,
    root: str | Path | None = None,
    manifest_path: str | Path | None = None,
) -> CmuLayout:
    explicit_root = _coerce_path(root)
    explicit_manifest = _coerce_path(manifest_path)
    resolved_mode = mode or DEFAULT_CMU_MODE

    if resolved_mode == "auto":
        if explicit_root is not None:
            resolved_mode = "fixture" if explicit_root == CMU_FIXTURE_ROOT else "external"
        elif explicit_manifest is not None and explicit_manifest.exists():
            resolved_mode = "fixture" if explicit_manifest.parent == CMU_FIXTURE_ROOT else "external"
        elif CMU_FIXTURE_MANIFEST.exists():
            resolved_mode = "fixture"
        elif CMU_EXTERNAL_MANIFEST.exists():
            resolved_mode = "external"
        else:
            resolved_mode = "fixture"

    if resolved_mode not in {"fixture", "external"}:
        raise ValueError(f"unsupported CMU mode {resolved_mode!r}")

    resolved_root = explicit_root or _root_from_mode(resolved_mode)
    resolved_manifest = explicit_manifest or (resolved_root / "manifest.json")
    return CmuLayout(
        mode=resolved_mode,
        root=resolved_root,
        bvh_root=resolved_root / "bvh",
        index_root=resolved_root / "indexed",
        manifest_path=resolved_manifest,
    )


def bvh_files(mode: str | None = None, root: str | Path | None = None) -> list[Path]:
    layout = resolve_cmu_layout(mode=mode, root=root)
    if not layout.bvh_root.exists():
        return []
    return sorted(path for path in layout.bvh_root.rglob("*.bvh") if path.is_file())


def _manifest_entries(payload: object) -> list[dict]:
    if isinstance(payload, list):
        return [entry for entry in payload if isinstance(entry, dict)]
    if isinstance(payload, dict):
        for key in ("clips", "entries", "motions"):
            entries = payload.get(key)
            if isinstance(entries, list):
                return [entry for entry in entries if isinstance(entry, dict)]
    raise RuntimeError("CMU manifest must be a list of objects or an object with a clips/entries list.")


def _entry_path_field(entry: dict) -> str | None:
    for key in ("relative_path", "filename", "path"):
        value = entry.get(key)
        if isinstance(value, str) and value:
            return value
    return None


def _entry_subject_trial(entry: dict) -> str:
    for key in ("subject_trial", "clip_id", "id"):
        value = entry.get(key)
        if isinstance(value, str) and value:
            return value

    relative_path = _entry_path_field(entry)
    if relative_path:
        return Path(relative_path).stem

    raise RuntimeError("CMU manifest entry missing subject_trial/clip_id and relative path.")


def _normalize_entry(entry: dict) -> dict:
    normalized = dict(entry)
    relative_path = _entry_path_field(entry)
    if not relative_path:
        clip_id = _entry_subject_trial(entry)
        relative_path = f"bvh/{clip_id}.bvh"

    clip_id = _entry_subject_trial(entry)
    published_description = entry.get("published_description")
    if not isinstance(published_description, str):
        published_description = entry.get("description")
    benchmark_category = entry.get("benchmark_category")
    if not isinstance(benchmark_category, str):
        benchmark_category = entry.get("chosen_benchmark_category")
    if not isinstance(benchmark_category, str):
        benchmark_category = entry.get("category")
    if not isinstance(benchmark_category, str):
        benchmark_category = entry.get("action_label")
    selection_rationale = entry.get("selection_rationale")
    if not isinstance(selection_rationale, str):
        selection_rationale = entry.get("rationale")

    normalized.update(
        {
            "subject_trial": clip_id,
            "clip_id": clip_id,
            "relative_path": relative_path,
            "filename": relative_path,
            "sha256": entry.get("sha256"),
            "frames": entry.get("frames"),
            "joints": entry.get("joints"),
            "fps": entry.get("fps"),
            "published_description": published_description,
            "benchmark_category": benchmark_category,
            "selection_rationale": selection_rationale,
            "license": entry.get("license", "CMU-commercial-safe"),
        }
    )
    return normalized


def _normalize_curated_map(payload: object) -> dict[str, dict]:
    if isinstance(payload, dict) and not any(key in payload for key in ("clips", "entries", "motions")):
        normalized: dict[str, dict] = {}
        for subject_trial, metadata in payload.items():
            if isinstance(subject_trial, str) and isinstance(metadata, dict):
                normalized[subject_trial] = _normalize_entry({"subject_trial": subject_trial, **metadata})
        return normalized

    normalized = {}
    for entry in _manifest_entries(payload):
        manifest_entry = _normalize_entry(entry)
        normalized[manifest_entry["subject_trial"]] = manifest_entry
    return normalized


def load_curated_metadata(path: str | Path | None) -> dict[str, dict]:
    curated_path = _coerce_path(path)
    if curated_path is None or not curated_path.exists():
        return {}
    payload = json.loads(curated_path.read_text(encoding="utf-8"))
    return _normalize_curated_map(payload)


def build_manifest(
    max_files: int | None = None,
    *,
    mode: str | None = None,
    root: str | Path | None = None,
    manifest_path: str | Path | None = None,
    curated_manifest_path: str | Path | None = None,
) -> list[dict]:
    layout = resolve_cmu_layout(mode=mode, root=root, manifest_path=manifest_path)
    curated_metadata = load_curated_metadata(curated_manifest_path)

    entries: list[dict] = []
    for path in bvh_files(mode=layout.mode, root=layout.root):
        if max_files is not None and len(entries) >= max_files:
            break

        clip_id = path.stem
        meta: BvhMetadata = load_bvh_metadata(path)
        curated = curated_metadata.get(clip_id, {})
        entries.append(
            {
                **curated,
                "subject_trial": clip_id,
                "clip_id": clip_id,
                "relative_path": str(path.relative_to(layout.root)),
                "filename": str(path.relative_to(layout.root)),
                "sha256": sha256_path(path),
                "frames": meta.frames,
                "joints": meta.joints,
                "fps": meta.fps,
                "published_description": curated.get("published_description"),
                "benchmark_category": curated.get("benchmark_category"),
                "selection_rationale": curated.get("selection_rationale"),
                "license": curated.get("license", "CMU-commercial-safe"),
            }
        )

    layout.root.mkdir(parents=True, exist_ok=True)
    write_json(layout.manifest_path, entries)
    return entries


def load_manifest(
    mode: str | None = None,
    root: str | Path | None = None,
    manifest_path: str | Path | None = None,
) -> list[dict]:
    layout = resolve_cmu_layout(mode=mode, root=root, manifest_path=manifest_path)
    if not layout.manifest_path.exists():
        return []
    payload = json.loads(layout.manifest_path.read_text(encoding="utf-8"))
    return [_normalize_entry(entry) for entry in _manifest_entries(payload)]


def select_manifest_entries(
    entries: Iterable[dict],
    *,
    max_clips: int | None = None,
    required_labels: Iterable[str] | None = None,
    subject_trials: Iterable[str] | None = None,
    exclude_unmapped: bool = False,
) -> list[dict]:
    required = {label for label in required_labels or ()}
    requested_subject_trials = {clip_id for clip_id in subject_trials or ()}

    selected: list[dict] = []
    for entry in entries:
        clip_id = entry.get("subject_trial")
        category = entry.get("benchmark_category")

        if requested_subject_trials and clip_id not in requested_subject_trials:
            continue
        if exclude_unmapped and not category:
            continue
        if required and category not in required:
            continue

        selected.append(entry)
        if max_clips is not None and len(selected) >= max_clips:
            break
    return selected


def load_cmu_clips(
    max_clips: int | None = None,
    required_labels: Iterable[str] | None = None,
    *,
    mode: str | None = None,
    root: str | Path | None = None,
    manifest_path: str | Path | None = None,
    subject_trials: Iterable[str] | None = None,
    exclude_unmapped: bool = False,
) -> list:
    layout = resolve_cmu_layout(mode=mode, root=root, manifest_path=manifest_path)
    entries = load_manifest(mode=layout.mode, root=layout.root, manifest_path=layout.manifest_path)
    if not entries:
        raise RuntimeError(f"CMU manifest missing at {layout.manifest_path}; run build_manifest first.")

    selected = select_manifest_entries(
        entries,
        max_clips=max_clips,
        required_labels=required_labels,
        subject_trials=subject_trials,
        exclude_unmapped=exclude_unmapped,
    )

    clips = []
    for entry in selected:
        relative_path = entry["relative_path"]
        path = layout.root / relative_path
        if not path.exists():
            raise RuntimeError(f"CMU manifest entry {entry['subject_trial']} points to missing file {path}.")
        label = entry.get("benchmark_category") or entry.get("published_description") or "unknown"
        clip_id = entry.get("subject_trial") or Path(relative_path).stem
        clips.append(load_bvh_motion_clip(path, clip_id=clip_id, label=label))
    return clips
