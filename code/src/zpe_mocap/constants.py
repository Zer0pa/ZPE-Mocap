from __future__ import annotations

from pathlib import Path

GLOBAL_SEED = 20260220
PACKAGE_ROOT = Path(__file__).resolve().parent
SRC_ROOT = PACKAGE_ROOT.parent
CODE_ROOT = SRC_ROOT.parent
REPO_ROOT = CODE_ROOT.parent

OUTPUT_ROOT = REPO_ROOT / "proofs" / "artifacts" / "2026-02-20_zpe_mocap_wave1"
CHECKPOINT_DIR = OUTPUT_ROOT / "checkpoints"

TOKEN_NAMES = ("E", "NE", "N", "NW", "W", "SW", "S", "SE")

# Unit vectors for 8-way direction quantization.
TOKEN_VECTORS_2D = {
    0: (1.0, 0.0),
    1: (0.7071067812, 0.7071067812),
    2: (0.0, 1.0),
    3: (-0.7071067812, 0.7071067812),
    4: (-1.0, 0.0),
    5: (-0.7071067812, -0.7071067812),
    6: (0.0, -1.0),
    7: (0.7071067812, -0.7071067812),
}

TOKEN_MIRROR = {
    0: 4,
    1: 3,
    2: 2,
    3: 1,
    4: 0,
    5: 7,
    6: 6,
    7: 5,
}

JOINT_NAMES = [
    "Hips",
    "Spine",
    "Chest",
    "Neck",
    "Head",
    "LeftShoulder",
    "LeftArm",
    "LeftForeArm",
    "LeftHand",
    "RightShoulder",
    "RightArm",
    "RightForeArm",
    "RightHand",
    "LeftUpLeg",
    "LeftLeg",
    "LeftFoot",
    "LeftToe",
    "RightUpLeg",
    "RightLeg",
    "RightFoot",
    "RightToe",
    "RootNub",
]

PARENTS = [
    -1,
    0,
    1,
    2,
    3,
    2,
    5,
    6,
    7,
    2,
    9,
    10,
    11,
    0,
    13,
    14,
    15,
    0,
    17,
    18,
    19,
    4,
]

# Local bind-pose offsets in meters.
REST_OFFSETS = [
    (0.0, 0.0, 0.0),
    (0.0, 0.12, 0.0),
    (0.0, 0.14, 0.0),
    (0.0, 0.14, 0.0),
    (0.0, 0.12, 0.02),
    (0.09, 0.10, 0.0),
    (0.13, 0.00, 0.0),
    (0.12, 0.00, 0.0),
    (0.10, 0.00, 0.0),
    (-0.09, 0.10, 0.0),
    (-0.13, 0.00, 0.0),
    (-0.12, 0.00, 0.0),
    (-0.10, 0.00, 0.0),
    (0.08, -0.13, 0.0),
    (0.00, -0.22, 0.0),
    (0.00, -0.22, 0.03),
    (0.00, -0.05, 0.08),
    (-0.08, -0.13, 0.0),
    (0.00, -0.22, 0.0),
    (0.00, -0.22, 0.03),
    (0.00, -0.05, 0.08),
    (0.00, 0.02, 0.04),
]

MIRROR_PAIRS = [
    ("LeftShoulder", "RightShoulder"),
    ("LeftArm", "RightArm"),
    ("LeftForeArm", "RightForeArm"),
    ("LeftHand", "RightHand"),
    ("LeftUpLeg", "RightUpLeg"),
    ("LeftLeg", "RightLeg"),
    ("LeftFoot", "RightFoot"),
    ("LeftToe", "RightToe"),
]

ACTION_LABELS = (
    "walk",
    "turn_left",
    "turn_right",
    "run",
    "jump",
    "punch",
    "crouch",
    "sidestep",
    "idle",
    "fall_recover",
)
