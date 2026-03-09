from __future__ import annotations

import unittest

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from zpe_mocap.search import MotionSuffixIndex


class SearchTests(unittest.TestCase):
    def test_retrieves_exact(self) -> None:
        idx = MotionSuffixIndex(k=4)
        seq = [0, 1, 2, 3, 4, 5, 6, 7] * 5
        idx.add("clip_a", seq, "walk")
        idx.add("clip_b", list(reversed(seq)), "turn")
        ids, _ = idx.query(seq, top_k=1)
        self.assertEqual(ids[0], "clip_a")


if __name__ == "__main__":
    unittest.main()
