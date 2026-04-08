from __future__ import annotations

import os
import unittest

import numpy as np

from pathlib import Path

from zpe_mocap.bvh_loader import load_bvh_motion_clip
from zpe_mocap.codec import decode_zpmoc, encode_clip
from zpe_mocap.metrics import joint_rmse_deg, mpjpe_mm


class CmuRealBvhTests(unittest.TestCase):
    def test_roundtrip_on_actual_cmu_bvh(self) -> None:
        sample_path = os.environ.get("ZPE_MOCAP_CMU_REAL_BVH")
        if not sample_path:
            self.skipTest("Set ZPE_MOCAP_CMU_REAL_BVH to run the real CMU BVH roundtrip test.")

        bvh_path = Path(sample_path)
        clip = load_bvh_motion_clip(bvh_path, clip_id=bvh_path.stem, label="walk")
        encoded = encode_clip(clip, seed=20260220)
        decoded = decode_zpmoc(encoded.payload)

        joint_error = joint_rmse_deg(clip.angles_deg, decoded.angles_deg)
        position_error = mpjpe_mm(clip.positions_m, decoded.positions_m)

        self.assertGreater(encoded.compression_ratio, 1.0)
        self.assertEqual(decoded.positions_m.shape, clip.positions_m.shape)
        self.assertEqual(decoded.angles_deg.shape, clip.angles_deg.shape)
        self.assertTrue(np.isfinite(joint_error))
        self.assertTrue(np.isfinite(position_error))


if __name__ == "__main__":
    unittest.main()
