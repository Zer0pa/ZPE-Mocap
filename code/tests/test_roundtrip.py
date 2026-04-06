from __future__ import annotations

import unittest

from pathlib import Path
import sys

TEST_ROOT = Path(__file__).resolve().parent
ROOT = TEST_ROOT.parent
sys.path.insert(0, str(TEST_ROOT))
sys.path.insert(0, str(ROOT))

from fixture_utils import (
    load_binary_fixture,
    load_fixture_json,
    load_motion_fixture,
    motion_clip_to_payload,
)
from zpe_mocap.codec import decode_zpmoc, encode_clip
from zpe_mocap.constants import GLOBAL_SEED


class RoundtripFixtureTests(unittest.TestCase):
    def test_canonical_walk_payload_matches_committed_binary(self) -> None:
        clip = load_motion_fixture("canonical_walk.json")
        expected = load_binary_fixture("canonical_walk_compressed.bin")

        encoded = encode_clip(clip, seed=GLOBAL_SEED)

        self.assertEqual(encoded.payload, expected)

    def test_canonical_walk_roundtrip_matches_committed_json(self) -> None:
        clip = load_motion_fixture("canonical_walk.json")
        expected = load_fixture_json("canonical_walk_roundtrip.json")

        encoded = encode_clip(clip, seed=GLOBAL_SEED)
        decoded = decode_zpmoc(encoded.payload)

        self.assertEqual(motion_clip_to_payload(decoded), expected)


if __name__ == "__main__":
    unittest.main()
