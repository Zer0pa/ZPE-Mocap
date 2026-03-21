# RUNBOOK_GATE_F

## Objective
Close Appendix F commercialization gates with explicit final claim statuses (PASS/FAIL/PAUSED_EXTERNAL), no INCONCLUSIVE residue.

## Commands
1. `set -a; [ -f .env ] && source .env; set +a; .venv/bin/python scripts/gate_f_commercial_closure.py`
2. `.venv/bin/python scripts/gate_e_package.py`

## Expected Outputs
- `commercialization_claim_adjudication.json`
- updated `max_claim_resource_map.json` (PASS/FAIL/PAUSED_EXTERNAL only)
- updated `claim_status_delta.md` with explicit statuses
- checkpoint: `artifacts/2026-02-20_zpe_mocap_wave1/checkpoints/gate_f.json`

## Fail Signatures
- Any claim remains `INCONCLUSIVE`
- `PAUSED_EXTERNAL` without `IMP-*` evidence and fallback note
- Claim marked `PASS` without commercial-safe evidence path

## Rollback
- Patch resource/claim adjudication rules and rerun Gate F + Gate E packaging

## Falsification Before Promotion
- Try to disprove each PASS claim by checking missing commercial-safe corpus/runtime evidence.
- If disproof succeeds, downgrade to FAIL or PAUSED_EXTERNAL.
