# RUNBOOK_GATE_M4

## Objective
Replay all core mocap claims on maximalization corpus and confirm no regressions.

## Commands
1. `set -a; [ -f .env ] && source .env; set +a; .venv/bin/python scripts/gate_m4_replay_core_claims.py`

## Expected Outputs
- updated claim replay summary in `claim_status_delta.md`
- checkpoint: `artifacts/2026-02-20_zpe_mocap_wave1/checkpoints/gate_m4.json`

## Fail Signatures
- Any MOC-C001..MOC-C007 regresses under max-wave replay
- Claim remains PASS without max-wave evidence path

## Rollback
- Patch benchmark path and rerun Gate M4 + E gates

## Falsification Before Promotion
- Attempt targeted regressions against each claim threshold before preserving PASS.
