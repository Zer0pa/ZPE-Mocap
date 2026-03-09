# RunPod Execution Plan

- required: `False`
- reason: No IMP-COMPUTE items recorded
- container_image: runpod/pytorch:2.3.1-cuda12.1-cudnn8-devel
- execution_steps:
  1. checkout lane repo snapshot
  2. install Python deps from `.venv` parity list
  3. install pinned dependencies from `runpod_requirements_lock.txt`
  4. run exact command chain listed in runpod_readiness_manifest.json
  5. upload expected artifact manifest to lane output root
- lock_file: artifacts/2026-02-20_zpe_mocap_wave1/runpod_requirements_lock.txt
- exact_command_chain:
  - `python3 scripts/gate_a_setup.py`
  - `python3 scripts/gate_b_build.py`
  - `python3 scripts/gate_c_benchmarks.py`
  - `python3 scripts/gate_d_falsification.py`
  - `python3 scripts/gate_m3_corpus_stress.py`
  - `python3 scripts/gate_m4_replay_core_claims.py`
  - `python3 scripts/gate_f_commercial_closure.py`
  - `python3 scripts/gate_e_package.py`
- expected_artifact_manifest:
  - `handoff_manifest.json`
  - `before_after_metrics.json`
  - `falsification_results.md`
  - `claim_status_delta.md`
  - `command_log.txt`
  - `quality_gate_scorecard.json`
  - `net_new_gap_closure_matrix.json`
  - `impracticality_decisions.json`
  - `runpod_readiness_manifest.json`
  - `runpod_exec_plan.md`
  - `runpod_requirements_lock.txt`
