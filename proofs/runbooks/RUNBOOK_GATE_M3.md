# RUNBOOK_GATE_M3

## Objective
Run large-corpus stress and determinism replay under max-wave conditions.

## Commands
1. `set -a; [ -f .env ] && source .env; set +a; .venv/bin/python scripts/gate_m3_corpus_stress.py`

## Expected Outputs
- stress entries in `falsification_results.md`
- `joint_class_error_breakdown.json`
- checkpoint: `artifacts/2026-02-20_zpe_mocap_wave1/checkpoints/gate_m3.json`

## Fail Signatures
- Determinism replay drifts from 5/5
- Uncaught crash rate above 0%
- Missing joint-class stratified metrics

## Rollback
- Patch failing stress path and rerun Gate M3 onward

## Falsification Before Promotion
- Stress style-confusable action pairs and ballistic segments before maintaining claim PASS.
