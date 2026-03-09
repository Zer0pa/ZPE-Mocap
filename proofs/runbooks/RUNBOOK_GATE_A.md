# RUNBOOK_GATE_A

## Objective
Establish reproducibility contract before implementation: runbooks, fixture lock, and schema freeze.

## Inputs
- `STARTUP_PROMPT_ZPE_MOCAP_SECTOR_AGENT_2026-02-20.md`
- `PRD_ZPE_MOCAP_SECTOR_EXPANSION_WAVE1_2026-02-20.md`
- concept anchor + quality rubric references

## Commands
1. `python3 scripts/gate_a_setup.py`

## Expected Outputs
- `runbooks/` complete with master + gate runbooks
- `fixtures/locked_corpus_v1.json`
- `format/ZPMOC_SCHEMA_V1.json`
- checkpoint: `artifacts/2026-02-20_zpe_mocap_wave1/checkpoints/gate_a.json`

## Fail Signatures
- Missing required runbook sections
- Non-deterministic fixture manifest hash
- Schema missing version/endianness/token dictionary fields

## Rollback
- Restore previous checkpoint files and rerun Gate A with fixed seed

## Falsification Before Promotion
- Attempt to violate schema with malformed payload and verify parser rejection
