from __future__ import annotations

import numpy as np


def joint_rmse_deg(reference_deg: np.ndarray, candidate_deg: np.ndarray) -> float:
    diff = reference_deg - candidate_deg
    return float(np.sqrt(np.mean(diff * diff)))


def mpjpe_mm(reference_m: np.ndarray, candidate_m: np.ndarray) -> float:
    diff = reference_m - candidate_m
    dist = np.sqrt(np.sum(diff * diff, axis=-1))
    return float(np.mean(dist) * 1000.0)


def precision_at_k(labels: list[str], predictions: list[list[str]], k: int = 10) -> float:
    if not labels:
        return 0.0
    scores = []
    for expected, pred in zip(labels, predictions):
        top = pred[:k]
        hits = sum(1 for candidate in top if candidate == expected)
        scores.append(hits / float(k))
    return float(np.mean(scores))


def percentile_ms(samples_ms: list[float], p: float) -> float:
    if not samples_ms:
        return 0.0
    return float(np.percentile(np.asarray(samples_ms, dtype=np.float64), p))
