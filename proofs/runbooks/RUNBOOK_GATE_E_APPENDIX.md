# RUNBOOK_GATE_E_APPENDIX

## Objective
Close Appendix E NET-NEW ingestion gates E-G1..E-G5 with evidence and IMP-* adjudication.

## Commands
1. `set -a; [ -f .env ] && source .env; set +a; .venv/bin/python scripts/gate_e_appendix_ingestion.py`
2. `set -a; [ -f .env ] && source .env; set +a; .venv/bin/python scripts/gate_e_runpod_readiness.py`

## Expected Outputs
- `max_resource_lock.json`
- `max_resource_validation_log.md`
- `max_claim_resource_map.json`
- `impracticality_decisions.json`
- `multisensor_alignment_report.json`
- `joint_class_error_breakdown.json`
- `net_new_gap_closure_matrix.json`
- `runpod_readiness_manifest.json` and `runpod_exec_plan.md` when any `IMP-COMPUTE`
- checkpoint: `artifacts/2026-02-20_zpe_mocap_wave1/checkpoints/gate_e_appendix.json`

## Fail Signatures
- Any E3 resource missing command attempt evidence
- Missing IMP-* code for blocked resources
- MOC claims closed on locomotion-only evidence
- IMP-COMPUTE present without RunPod artifacts

## Rollback
- Patch ingestion and evidence synthesis scripts; rerun Appendix E gates

## Falsification Before Promotion
- Re-check every closed claim has non-locomotion and stratified evidence, otherwise downgrade.
