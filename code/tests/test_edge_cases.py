from __future__ import annotations

import unittest

from pathlib import Path
import sys

import numpy as np

TEST_ROOT = Path(__file__).resolve().parent
ROOT = TEST_ROOT.parent
sys.path.insert(0, str(ROOT))

from zpe_mocap.codec import decode_zpmoc, encode_clip
from zpe_mocap.synthetic import MotionClip


def make_chain_clip(frames: int, joints: int, *, fps: int = 60, static: bool = False) -> MotionClip:
    joint_names = [f"J{joint}" for joint in range(joints)]
    parents = [-1] + [joint - 1 for joint in range(1, joints)]
    positions = np.zeros((frames, joints, 3), dtype=np.float64)
    angles = np.zeros((frames, joints, 3), dtype=np.float64)
    rest_pose = np.zeros((joints, 3), dtype=np.float64)

    for joint in range(1, joints):
        rest_pose[joint] = rest_pose[joint - 1] + np.array([0.0, 0.1, 0.0], dtype=np.float64)

    if frames:
        positions[0] = rest_pose
        for frame in range(1, frames):
            positions[frame] = positions[frame - 1] if static else positions[frame - 1] + 0.001

    return MotionClip(
        clip_id="edge_case",
        label="edge_case",
        fps=fps,
        joint_names=joint_names,
        parents=parents,
        positions_m=positions,
        angles_deg=angles,
        rest_pose_m=rest_pose,
    )


class EdgeCaseTests(unittest.TestCase):
    def test_empty_motion_raises(self) -> None:
        clip = make_chain_clip(frames=0, joints=1)
        encoded = encode_clip(clip, seed=123)

        with self.assertRaises(IndexError):
            decode_zpmoc(encoded.payload)

    def test_single_frame_roundtrip_is_exact(self) -> None:
        clip = make_chain_clip(frames=1, joints=1)

        decoded = decode_zpmoc(encode_clip(clip, seed=123).payload)

        np.testing.assert_array_equal(decoded.positions_m, clip.positions_m)
        np.testing.assert_array_equal(decoded.angles_deg, clip.angles_deg)

    def test_one_joint_roundtrip_preserves_shape(self) -> None:
        clip = make_chain_clip(frames=10, joints=1)

        decoded = decode_zpmoc(encode_clip(clip, seed=123).payload)

        self.assertEqual(decoded.positions_m.shape, clip.positions_m.shape)
        self.assertEqual(decoded.angles_deg.shape, clip.angles_deg.shape)

    def test_hundred_joint_roundtrip_preserves_shape(self) -> None:
        clip = make_chain_clip(frames=10, joints=100)

        decoded = decode_zpmoc(encode_clip(clip, seed=123).payload)

        self.assertEqual(decoded.positions_m.shape, clip.positions_m.shape)
        self.assertEqual(decoded.angles_deg.shape, clip.angles_deg.shape)
        self.assertTrue(np.isfinite(decoded.positions_m).all())

    def test_static_pose_stays_static(self) -> None:
        clip = make_chain_clip(frames=10, joints=5, static=True)

        decoded = decode_zpmoc(encode_clip(clip, seed=123).payload)

        self.assertTrue(np.all(decoded.positions_m == decoded.positions_m[:1]))
        np.testing.assert_allclose(decoded.positions_m, clip.positions_m, atol=1e-7, rtol=0.0)

    def test_high_framerate_preserves_fps(self) -> None:
        clip = make_chain_clip(frames=10, joints=5, fps=1000)

        decoded = decode_zpmoc(encode_clip(clip, seed=123).payload)

        self.assertEqual(decoded.fps, 1000)
        self.assertEqual(decoded.positions_m.shape, clip.positions_m.shape)


if __name__ == "__main__":
    unittest.main()
