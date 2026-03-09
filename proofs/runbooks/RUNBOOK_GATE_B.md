# RUNBOOK_GATE_B

## Objective
Implement deterministic codec, decode path, search index, retarget mapping, and adapter stubs with transparent failure behavior.

## Commands
1. `python3 scripts/gate_b_build.py`

## Expected Outputs
- `src/zpe_mocap/*.py` core modules
- core smoke tests pass
- checkpoint: `artifacts/2026-02-20_zpe_mocap_wave1/checkpoints/gate_b.json`

## Fail Signatures
- Decode drift above tolerance in smoke clips
- Nondeterministic output bytes on repeated encode
- Silent fallback instead of explicit error states

## Rollback
- Revert to prior gate checkpoint artifacts and patch minimal module(s)

## Falsification Before Promotion
- High-velocity discontinuity clip should not crash and should report fidelity degradation explicitly
