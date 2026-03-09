# RUNBOOK_GATE_C

## Objective
Run benchmark matrix for compression, fidelity, search quality, latency, retargeting, and Blender roundtrip integrity.

## Commands
1. `python3 scripts/gate_c_benchmarks.py`

## Expected Outputs
- `mocap_compression_benchmark.json`
- `mocap_joint_fidelity.json`
- `mocap_position_fidelity.json`
- `mocap_search_eval.json`
- `mocap_query_latency.json`
- `mocap_retarget_eval.json`
- `mocap_blender_roundtrip.json`
- checkpoint: `.../checkpoints/gate_c.json`

## Fail Signatures
- Any threshold breach for C001-C007
- Empty candidate sets for search benchmark
- Latency distribution p95 >= 100ms

## Rollback
- Keep benchmark inputs locked; patch implementation, rerun Gate C onward

## Falsification Before Promotion
- Stress false-positive query sets before confirming P@10
