from __future__ import annotations

from typing import Iterable


class SkeletonValidationError(ValueError):
    """Raised when skeleton topology is invalid."""


def validate_skeleton(joint_names: list[str], parents: list[int]) -> None:
    if len(joint_names) != len(parents):
        raise SkeletonValidationError("joint_names and parents length mismatch")
    if len(set(joint_names)) != len(joint_names):
        raise SkeletonValidationError("duplicate joint names")

    n = len(parents)
    root_count = sum(1 for p in parents if p == -1)
    if root_count != 1:
        raise SkeletonValidationError("exactly one root required")

    for idx, parent in enumerate(parents):
        if parent == -1:
            continue
        if parent < 0 or parent >= n:
            raise SkeletonValidationError(f"parent out of range at joint {idx}")
        if parent == idx:
            raise SkeletonValidationError(f"self cycle at joint {idx}")

    # Detect directed cycles.
    state = [0] * n  # 0=unvisited, 1=visiting, 2=done

    def visit(node: int) -> None:
        if state[node] == 1:
            raise SkeletonValidationError(f"cyclic parent graph at joint {node}")
        if state[node] == 2:
            return
        state[node] = 1
        parent = parents[node]
        if parent != -1:
            visit(parent)
        state[node] = 2

    for node in range(n):
        visit(node)


def require_fields(payload: dict, required: Iterable[str]) -> None:
    missing = [field for field in required if field not in payload]
    if missing:
        raise ValueError(f"missing required fields: {missing}")
