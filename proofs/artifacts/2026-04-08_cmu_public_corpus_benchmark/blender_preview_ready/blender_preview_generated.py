import bpy
import json
from pathlib import Path

ORIGINAL_BVH = Path('/tmp/zpe_mocap_cmu_full_cache/data/001/01_01.bvh')
DECODED_JSON = Path('proofs/artifacts/2026-04-08_cmu_public_corpus_benchmark/blender_preview_ready/decoded_positions.json')

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

joint_objects = {}
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
