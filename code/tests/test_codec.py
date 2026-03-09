from __future__ import annotations

import unittest

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from zpe_mocap.codec import decode_zpmoc, encode_clip
from zpe_mocap.metrics import joint_rmse_deg, mpjpe_mm
from zpe_mocap.synthetic import generate_clip


class CodecTests(unittest.TestCase):
    def test_encode_decode_thresholds(self) -> None:
        clip = generate_clip(
            clip_id="ut_clip",
            label="walk",
            frames=160,
            fps=60,
            seed=20260220,
            noise_scale=0.0002,
        )
        enc = encode_clip(clip, seed=20260220)
        dec = decode_zpmoc(enc.payload)

        self.assertGreaterEqual(enc.compression_ratio, 10.0)
        self.assertLessEqual(joint_rmse_deg(clip.angles_deg, dec.angles_deg), 1.0)
        self.assertLessEqual(mpjpe_mm(clip.positions_m, dec.positions_m), 5.0)


if __name__ == "__main__":
    unittest.main()
