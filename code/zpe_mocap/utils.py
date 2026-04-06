from __future__ import annotations

import hashlib
import json
import shutil
import zipfile
from pathlib import Path
from pathlib import PurePosixPath, PureWindowsPath
from typing import Any


def ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def stable_json_dumps(payload: Any) -> str:
    return json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=True)


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_path(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def write_json(path: Path, payload: Any) -> None:
    ensure_dir(path.parent)
    path.write_text(stable_json_dumps(payload) + "\n", encoding="utf-8")


def append_line(path: Path, line: str) -> None:
    ensure_dir(path.parent)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(line.rstrip("\n") + "\n")


def _validated_zip_member_path(destination_root: Path, member_name: str) -> Path:
    if not member_name:
        raise ValueError("Unsafe archive entry: empty path")

    normalized_name = member_name.replace("\\", "/")
    posix_path = PurePosixPath(normalized_name)
    windows_path = PureWindowsPath(member_name)
    if posix_path.is_absolute() or windows_path.is_absolute():
        raise ValueError(f"Unsafe archive entry: {member_name}")

    target_path = (destination_root / Path(*posix_path.parts)).resolve()
    if target_path != destination_root and destination_root not in target_path.parents:
        raise ValueError(f"Unsafe archive entry: {member_name}")

    return target_path


def extract_zip_safely(archive: zipfile.ZipFile, destination: Path) -> None:
    destination_root = destination.resolve()
    members = [
        (member, _validated_zip_member_path(destination_root, member.filename))
        for member in archive.infolist()
    ]

    for member, target_path in members:
        if member.is_dir():
            target_path.mkdir(parents=True, exist_ok=True)
            continue

        target_path.parent.mkdir(parents=True, exist_ok=True)
        with archive.open(member, "r") as src, target_path.open("wb") as dst:
            shutil.copyfileobj(src, dst)
