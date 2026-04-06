from __future__ import annotations

import unittest

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
TEST_ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(TEST_ROOT))
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "src"))

from fixture_utils import load_binary_fixture, load_motion_fixture
from zpe_mocap.codec import decode_zpmoc, encode_clip
from zpe_mocap.constants import GLOBAL_SEED
from zpe_mocap.search import MotionSuffixIndex
from zpe_mocap.search import flatten_tokens
from zpe_mocap.synthetic import generate_clip


class SearchTests(unittest.TestCase):
    def test_retrieves_exact(self) -> None:
        idx = MotionSuffixIndex(k=4)
        seq = [0, 1, 2, 3, 4, 5, 6, 7] * 5
        idx.add("clip_a", seq, "walk")
        idx.add("clip_b", list(reversed(seq)), "turn")
        ids, _ = idx.query(seq, top_k=1)
        self.assertEqual(ids[0], "clip_a")

    def test_queries_compressed_library(self) -> None:
        walk_clip = load_motion_fixture("canonical_walk.json")
        run_clip = generate_clip("search_run", "run", frames=100, fps=60, seed=GLOBAL_SEED + 1)
        jump_clip = generate_clip("search_jump", "jump", frames=100, fps=60, seed=GLOBAL_SEED + 2)

        index = MotionSuffixIndex(k=6)
        library = [
            ("walk_fixture", walk_clip, load_binary_fixture("canonical_walk_compressed.bin")),
            ("run_fixture", run_clip, encode_clip(run_clip, seed=GLOBAL_SEED + 1).payload),
            ("jump_fixture", jump_clip, encode_clip(jump_clip, seed=GLOBAL_SEED + 2).payload),
        ]

        for clip_id, source_clip, payload in library:
            decoded = decode_zpmoc(payload)
            tokens = flatten_tokens(decoded.xy_tokens, decoded.xz_tokens)
            index.add(clip_id, tokens, source_clip.label)

        walk_query = decode_zpmoc(load_binary_fixture("canonical_walk_compressed.bin"))
        query_tokens = flatten_tokens(walk_query.xy_tokens, walk_query.xz_tokens)
        ids, elapsed_ms = index.query(query_tokens, top_k=3)

        self.assertEqual(ids[0], "walk_fixture")
        self.assertGreaterEqual(elapsed_ms, 0.0)


if __name__ == "__main__":
    unittest.main()
