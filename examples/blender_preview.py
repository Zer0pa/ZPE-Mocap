#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

from _common import DEFAULT_SEED, ensure_output_dir, write_json, write_minimal_bvh
from zpe_mocap.bvh_loader import load_bvh_motion_clip
from zpe_mocap.codec import decode_zpmoc, encode_clip


def _generated_blender_script(original_bvh: Path, decoded_json: Path) -> str:
    original_literal = repr(str(original_bvh))
    decoded_literal = repr(str(decoded_json))
    return f"""import bpy
import json
from pathlib import Path

ORIGINAL_BVH = Path({original_literal})
DECODED_JSON = Path({decoded_literal})

bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)

if ORIGINAL_BVH.exists():
    bpy.ops.import_anim.bvh(filepath=str(ORIGINAL_BVH))

with DECODED_JSON.open('r', encoding='utf-8') as handle:
    payload = json.load(handle)

scene = bpy.context.scene
scene.render.fps = int(payload['fps'])
collection = bpy.data.collections.new('ZPE Decoded Preview')
bpy.context.scene.collection.children.link(collection)

joint_objects = {{}}
for joint_name in payload['joint_names']:
    obj = bpy.data.objects.new(joint_name, None)
    obj.empty_display_type = 'SPHERE'
    obj.empty_display_size = 0.04
    collection.objects.link(obj)
    joint_objects[joint_name] = obj

for frame_index, frame_positions in enumerate(payload['positions_m'], start=1):
    scene.frame_set(frame_index)
    for joint_name, position in zip(payload['joint_names'], frame_positions):
        obj = joint_objects[joint_name]
        obj.location = position
        obj.keyframe_insert(data_path='location', frame=frame_index)

print('Imported original BVH and keyed decoded positions for preview.')
"""


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate a Blender preview script for original vs decoded motion.")
    parser.add_argument("--input", type=Path, help="Path to a BVH file. Defaults to a minimal local fixture.")
    parser.add_argument("--output-dir", help="Directory for emitted preview artifacts.")
    parser.add_argument("--clip-id", default="blender_preview")
    parser.add_argument("--label", default="walk")
    parser.add_argument("--seed", type=int, default=DEFAULT_SEED)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    output_dir = ensure_output_dir(args.output_dir, prefix="zpe_mocap_blender_")
    source_path = args.input or (output_dir / "minimal_walk.bvh")
    if args.input is None:
        write_minimal_bvh(source_path)

    clip = load_bvh_motion_clip(source_path, clip_id=args.clip_id, label=args.label)
    encoded = encode_clip(clip, seed=args.seed)
    decoded = decode_zpmoc(encoded.payload)

    decoded_json = output_dir / "decoded_positions.json"
    decoded_payload = {
        "clip_id": decoded.clip_id,
        "fps": int(decoded.fps),
        "joint_names": decoded.joint_names,
        "positions_m": decoded.positions_m.tolist(),
    }
    write_json(decoded_json, decoded_payload)

    blender_script = output_dir / "blender_preview_generated.py"
    blender_script.write_text(_generated_blender_script(source_path, decoded_json), encoding="utf-8")

    summary = {
        "source_bvh": str(source_path),
        "decoded_json": str(decoded_json),
        "blender_script": str(blender_script),
        "compression_ratio": float(encoded.compression_ratio),
        "payload_hash": encoded.payload_hash,
    }
    write_json(output_dir / "blender_preview_summary.json", summary)
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
