"""zpe-mocap Wave-1 deterministic reference implementation."""

from .codec import decode_zpmoc, encode_clip
from .constants import GLOBAL_SEED
from .retarget import retarget_clip
from .search import MotionSuffixIndex
from .synthetic import MotionClip, generate_clip

__version__ = "0.1.0"

__all__ = [
    "GLOBAL_SEED",
    "MotionClip",
    "MotionSuffixIndex",
    "__version__",
    "decode_zpmoc",
    "encode_clip",
    "generate_clip",
    "retarget_clip",
]
