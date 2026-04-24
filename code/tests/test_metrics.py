from __future__ import annotations

import unittest

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from zpe_mocap.metrics import mean_reciprocal_rank, median_rank, recall_at_k


class MetricsTests(unittest.TestCase):
    def test_recall_at_k_ignores_misses(self) -> None:
        ranks = [1, 3, None, 12]
        self.assertAlmostEqual(recall_at_k(ranks, 1), 0.25)
        self.assertAlmostEqual(recall_at_k(ranks, 3), 0.5)
        self.assertAlmostEqual(recall_at_k(ranks, 10), 0.5)

    def test_mean_reciprocal_rank_treats_miss_as_zero(self) -> None:
        ranks = [1, 4, None]
        expected = (1.0 + 0.25 + 0.0) / 3.0
        self.assertAlmostEqual(mean_reciprocal_rank(ranks), expected)

    def test_median_rank_uses_only_hits(self) -> None:
        ranks = [5, None, 1, 3]
        self.assertEqual(median_rank(ranks), 3.0)
        self.assertIsNone(median_rank([None, None]))


if __name__ == "__main__":
    unittest.main()
