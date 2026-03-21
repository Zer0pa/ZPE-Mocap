from __future__ import annotations

import time
from collections import defaultdict

import numpy as np


class MotionSuffixIndex:
    """Pragmatic suffix-like k-gram index for tokenized motion streams."""

    def __init__(self, k: int = 6) -> None:
        self.k = k
        self.max_candidates = 64
        self.docs: dict[str, list[int]] = {}
        self.docs_np: dict[str, np.ndarray] = {}
        self.labels: dict[str, str] = {}
        self.inverted: dict[tuple[int, ...], set[str]] = defaultdict(set)
        self.exact_lookup: dict[tuple[int, ...], list[str]] = defaultdict(list)

    def add(self, clip_id: str, tokens: list[int], label: str) -> None:
        self.docs[clip_id] = tokens
        self.docs_np[clip_id] = np.asarray(tokens, dtype=np.int16)
        self.labels[clip_id] = label
        self.exact_lookup[tuple(tokens)].append(clip_id)
        if len(tokens) < self.k:
            self.inverted[tuple(tokens)].add(clip_id)
            return
        for i in range(len(tokens) - self.k + 1):
            gram = tuple(tokens[i : i + self.k])
            self.inverted[gram].add(clip_id)

    def _candidates(self, query_tokens: list[int]) -> set[str]:
        counts: dict[str, int] = defaultdict(int)
        if len(query_tokens) < self.k:
            for clip_id in self.inverted.get(tuple(query_tokens), set()):
                counts[clip_id] += 1
            return set(counts.keys())
        span = len(query_tokens) - self.k + 1
        stride = 1 if span <= 64 else max(2, span // 64)
        for i in range(0, span, stride):
            gram = tuple(query_tokens[i : i + self.k])
            for clip_id in self.inverted.get(gram, set()):
                counts[clip_id] += 1
        if not counts:
            return set()
        ranked = sorted(counts.items(), key=lambda x: (-x[1], x[0]))
        return {clip_id for clip_id, _ in ranked[: self.max_candidates]}

    def _similarity(self, a: np.ndarray, b: np.ndarray) -> float:
        n = min(a.shape[0], b.shape[0])
        if n == 0:
            return 0.0
        return float(np.mean(a[:n] == b[:n]))

    def query(self, query_tokens: list[int], top_k: int = 10) -> tuple[list[str], float]:
        start = time.perf_counter()
        exact_ids = sorted(self.exact_lookup.get(tuple(query_tokens), []))
        candidates = self._candidates(query_tokens)
        for exact in exact_ids:
            candidates.add(exact)
        if not candidates:
            elapsed_ms = (time.perf_counter() - start) * 1000.0
            return [], elapsed_ms

        query_arr = np.asarray(query_tokens, dtype=np.int16)
        scored = []
        for clip_id in candidates:
            score = self._similarity(query_arr, self.docs_np[clip_id])
            scored.append((score, clip_id))
        scored.sort(key=lambda x: (-x[0], x[1]))
        ordered = [clip_id for _, clip_id in scored]
        if exact_ids:
            ordered = exact_ids + [clip_id for clip_id in ordered if clip_id not in exact_ids]
        result_ids = ordered[:top_k]
        elapsed_ms = (time.perf_counter() - start) * 1000.0
        return result_ids, elapsed_ms


def flatten_tokens(xy_tokens: np.ndarray, xz_tokens: np.ndarray) -> list[int]:
    """Interleave XY and XZ tokens to a single stream."""
    if xy_tokens.shape != xz_tokens.shape:
        raise ValueError("xy/xz token shape mismatch")
    interleaved = np.stack([xy_tokens, xz_tokens], axis=-1).reshape(-1)
    return [int(v) for v in interleaved.tolist()]
