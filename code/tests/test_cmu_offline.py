from __future__ import annotations

import unittest

from pathlib import Path
import sys

import numpy as np

TEST_ROOT = Path(__file__).resolve().parent
ROOT = TEST_ROOT.parent
sys.path.insert(0, str(ROOT))

from zpe_mocap.bvh_loader import bvhio, load_bvh_metadata
from zpe_mocap.codec import decode_zpmoc, encode_clip
from zpe_mocap.cmu import CMU_FIXTURE_ROOT, load_cmu_clips, load_manifest
from zpe_mocap.metrics import mpjpe_mm

EXPECTED_SUBJECT_TRIALS = [
    "02_01",
    "02_03",
    "05_01",
    "13_29",
    "16_15",
    "35_01",
    "49_02",
    "69_04",
    "86_01",
    "126_07",
]


class CmuOfflineTests(unittest.TestCase):
    def test_manifest_matches_committed_fixture_set(self) -> None:
        entries = load_manifest(mode="fixture")
        subject_trials = [entry["subject_trial"] for entry in entries]

        self.assertEqual(subject_trials, EXPECTED_SUBJECT_TRIALS)

    @unittest.skipUnless(bvhio is not None, "bvhio is required for CMU BVH loader tests")
    def test_manifest_metadata_matches_bvh_files(self) -> None:
        for entry in load_manifest(mode="fixture"):
            path = Path(CMU_FIXTURE_ROOT) / entry["relative_path"]
            metadata = load_bvh_metadata(path)
            self.assertEqual(metadata.frames, entry["frames"])
            self.assertEqual(metadata.joints, entry["joints"])
            self.assertEqual(metadata.fps, entry["fps"])

    @unittest.skipUnless(bvhio is not None, "bvhio is required for CMU BVH loader tests")
    def test_first_fixture_roundtrip_metrics_are_finite(self) -> None:
        clip = load_cmu_clips(mode="fixture", subject_trials=[EXPECTED_SUBJECT_TRIALS[0]])[0]

        encoded = encode_clip(clip, seed=20260220)
        decoded = decode_zpmoc(encoded.payload)

        self.assertEqual(decoded.positions_m.shape, clip.positions_m.shape)
        self.assertEqual(decoded.angles_deg.shape, clip.angles_deg.shape)
        self.assertTrue(np.isfinite(decoded.positions_m).all())
        self.assertTrue(np.isfinite(decoded.angles_deg).all())
        self.assertGreaterEqual(mpjpe_mm(clip.positions_m, decoded.positions_m), 0.0)


if __name__ == "__main__":
    unittest.main()
