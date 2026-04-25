from __future__ import annotations

import unittest

from pathlib import Path
import sys

import numpy as np

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
    def assert_optional_array_equal(self, actual: list | None, expected: list | None) -> None:
        if actual is None or expected is None:
            self.assertIs(actual, expected)
            return
        np.testing.assert_array_equal(np.asarray(actual), np.asarray(expected))

    def assert_optional_array_close(
        self,
        actual: list | None,
        expected: list | None,
        *,
        atol: float,
    ) -> None:
        if actual is None or expected is None:
            self.assertIs(actual, expected)
            return
        np.testing.assert_allclose(
            np.asarray(actual, dtype=np.float64),
            np.asarray(expected, dtype=np.float64),
            rtol=0.0,
            atol=atol,
        )

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
        actual = motion_clip_to_payload(decoded)

        for key in ("clip_id", "label", "fps", "joint_names", "parents"):
            self.assertEqual(actual[key], expected[key])

        self.assert_optional_array_close(actual["positions_m"], expected["positions_m"], atol=1e-6)
        self.assert_optional_array_close(actual["angles_deg"], expected["angles_deg"], atol=1e-6)
        self.assert_optional_array_close(actual["rest_pose_m"], expected["rest_pose_m"], atol=1e-9)
        self.assert_optional_array_equal(actual["xy_tokens"], expected["xy_tokens"])
        self.assert_optional_array_equal(actual["xz_tokens"], expected["xz_tokens"])
        self.assert_optional_array_equal(actual["magnitudes_mm"], expected["magnitudes_mm"])


if __name__ == "__main__":
    unittest.main()
