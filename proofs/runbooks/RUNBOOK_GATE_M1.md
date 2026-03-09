# RUNBOOK_GATE_M1

## Objective
Execute direct ACL comparator attempt on lane corpus with reproducible command evidence.

## Commands
1. `set -a; [ -f .env ] && source .env; set +a; .venv/bin/python scripts/gate_m1_acl_comparator.py`
2. Local fix path:
   - `.venv/bin/python -m pip install cmake ninja`
   - `git -C external/acl submodule update --init --recursive`
3. Container fallback (if local toolchain fails):
   - `docker run --rm -v "$PWD:/work" -w /work ubuntu:22.04 bash -lc 'apt-get update && apt-get install -y cmake ninja-build clang git python3 && ...'`

## Expected Outputs
- `max_resource_validation_log.md` ACL attempt section
- `impracticality_decisions.json` entry if ACL cannot run directly
- checkpoint: `artifacts/2026-02-20_zpe_mocap_wave1/checkpoints/gate_m1.json`

## Fail Signatures
- No direct ACL attempt commands recorded
- Comparator represented as PASS without executable evidence
- IMP-* missing when comparator run is blocked
- `acl_compressor` binary missing after local + container attempts
- No deterministic same-corpus ACL-vs-ZPMOC table emitted

## Rollback
- Patch harness or dependency path; rerun Gate M1 and downstream max-wave gates

## Falsification Before Promotion
- Attempt to reproduce comparator with deterministic fixture replay and verify identical table rows across reruns.
