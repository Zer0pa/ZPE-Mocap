# RUNBOOK_GATE_M2

## Objective
Attempt live Blender and USD runtime roundtrip validation (not simulation-only).

## Commands
1. `set -a; [ -f .env ] && source .env; set +a; .venv/bin/python scripts/gate_m2_live_runtime.py`
2. Local fix path:
   - `python3.11 -m pip install --user usd-core`
   - `python3.11 -c "from pxr import Usd; print('usd_import_ok')"`
3. Container fallback (if local runtime fails):
   - `docker run --rm -v "$PWD:/work" -w /work python:3.11 bash -lc 'pip install usd-core && python -c \"from pxr import Usd; print(Usd.GetVersion())\"'`

## Expected Outputs
- live runtime section in `max_resource_validation_log.md`
- `mocap_blender_roundtrip.json`/runtime annotations updated
- checkpoint: `artifacts/2026-02-20_zpe_mocap_wave1/checkpoints/gate_m2.json`

## Fail Signatures
- Only simulated checks presented as live pass
- No command evidence for blender/usd runtime attempts
- Missing IMP-* adjudication for blocked runtime
- `blender` and USD runtime both unavailable after local + container attempts

## Rollback
- Patch runtime scripts/environment setup and rerun Gate M2 onward

## Falsification Before Promotion
- Use malformed/unsupported clip in live runtime path to confirm failure transparency.
