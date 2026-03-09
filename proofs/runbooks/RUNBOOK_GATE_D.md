# RUNBOOK_GATE_D

## Objective
Run Popper-first adversarial and malformed campaigns plus deterministic replay and crash-rate accounting.

## Commands
1. `python3 scripts/gate_d_falsification.py`

## Expected Outputs
- `falsification_results.md`
- `determinism_replay_results.json`
- checkpoint: `.../checkpoints/gate_d.json`

## Fail Signatures
- Uncaught exception in malformed tests
- Determinism hash mismatch across 5 runs
- Any crash-rate above 0%

## Rollback
- Patch failing harness/module, rerun Gate D and Gate E

## Falsification Before Promotion
- Claims can be downgraded to `INCONCLUSIVE` if adversarial failure unresolved
