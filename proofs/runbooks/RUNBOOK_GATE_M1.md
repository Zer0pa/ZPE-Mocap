# RUNBOOK_GATE_M1

## Objective
Execute gzip/zstd comparator on the lane corpus and emit an auditable ACL comparison table.

## Commands
1. `python -m pip install -e "./code[gates]"`
2. `set -a; [ -f .env ] && source .env; set +a; .venv/bin/python scripts/gate_m1_acl_comparator.py`

## Expected Outputs
- `acl_direct_comparator_table.json`
- checkpoint: `artifacts/2026-02-20_zpe_mocap_wave1/checkpoints/gate_m1.json`

## Fail Signatures
- Comparator JSON missing or lacks gzip/zstd/ZPE values
- Gate M1 checkpoint not written
- Zstandard import failure (missing `gates` extra)

## Rollback
- Install `gates` extra, rerun Gate M1 and downstream max-wave gates

## Falsification Before Promotion
- Attempt to reproduce comparator with deterministic fixture replay and verify identical table rows across reruns.
