# RUNBOOK_ZPE_MOCAP_MASTER

## Scope Lock
- Canonical repo root: repo root of `ZPE-Mocap`
- Workspace-only material lives outside the repo root
- Execution order: Gate A -> Gate B -> Gate C -> Gate D -> Gate E -> Gate M1 -> Gate M2 -> Gate M3 -> Gate M4 -> Gate E-G1 -> Gate E-G2 -> Gate E-G3 -> Gate E-G4 -> Gate E-G5 -> Gate F-G1 -> Gate F-G2

## Repo Translation Note
- Historical command strings in this imported runbook used the old shell layout.
- Read `scripts/` as `code/scripts/`.
- Read `artifacts/2026-02-20_zpe_mocap_wave1/` as `proofs/artifacts/2026-02-20_zpe_mocap_wave1/`.
- Read `fixtures/` as `code/fixtures/`.
- Read `format/` as `code/format/`.
- Read `external/` as `../external/` from the repo root, or set `ZPE_MOCAP_EXTERNAL_ROOT`.

## Environment Bootstrap Lock
- Mandatory pre-command prologue: `set -a; [ -f .env ] && source .env; set +a`
- `.env` must exist before external resource attempts
- Secret policy: never print token values in logs or artifacts

## Mission and Claims
- MOC-C001: compression ratio >= 10x vs raw BVH float32
- MOC-C002: joint-angle RMSE <= 1 degree
- MOC-C003: MPJPE <= 5 mm
- MOC-C004: search P@10 >= 0.85
- MOC-C005: search latency < 100 ms on 10K clips
- MOC-C006: retargeting MPJPE <= 10 mm
- MOC-C007: Blender roundtrip integrity pass

## Deterministic Seed Policy
- Global seed: `20260220`
- Secondary seeds for adversarial campaigns: `20260221`, `20260222`, `20260223`, `20260224`
- NumPy RNG only (PCG64)
- File ordering for library generation is lexicographic and frozen via manifest
- Determinism verdict: PASS only if 5/5 run hashes match exactly

## Dataset and Resource Provenance Lock
- Synthetic core corpus: `fixtures/locked_corpus_v1.json` (generated deterministically)
- ACL comparator: external value baseline from concept (2.9x) plus in-lane gzip/zstd comparator if ACL binary unavailable
- LAFAN1/LAFAN1-resolved/Mixamo/CMU/usdBVHAnim/bvhio sources are declared in `concept_resource_traceability.json`
- If external resources are inaccessible: nearest viable substitute must be documented with comparability impact and dependent claims set `INCONCLUSIVE` unless equivalence is proven
- NET-NEW resources required by Appendix E: Kaiwu multimodal mocap+bio, BABEL (AMASS), RELI11D, LAFAN1/CMU incumbent baselines
- Impracticality codes allowed: `IMP-LICENSE`, `IMP-ACCESS`, `IMP-COMPUTE`, `IMP-STORAGE`, `IMP-NOCODE`

## Commercialization Closure Lock (Appendix F)
- Claims cannot remain `INCONCLUSIVE` at final handoff.
- Allowed final claim statuses: `PASS`, `FAIL`, `PAUSED_EXTERNAL`.
- If only restricted/non-commercial resources exist and no commercial-safe open alternative exists, claim must be `PAUSED_EXTERNAL` with evidence in `impracticality_decisions.json`.
- If a commercial-safe alternative exists but was not executed successfully, claim must be explicit `FAIL` with evidence.
- Commercial-safe baseline target for mocap closure: CMU MoCap corpus path plus in-lane deterministic replay artifacts.

## Popper-First Falsification Matrix
- DT-MOC-1 malformed hierarchy/cycle/missing joints -> target MOC-C002/C003/C007 stability and crash-rate
- DT-MOC-2 discontinuous high-velocity clips -> target MOC-C002/C003 robustness
- DT-MOC-3 mirrored-limb corruption and retarget mismatch -> target MOC-C006
- DT-MOC-4 deterministic replay mixed corpus -> target all metric-producing claims
- DT-MOC-5 suffix-index false-positive stress -> target MOC-C004/C005

## Command Ledger (Predeclared)
1. `python3 scripts/gate_a_setup.py`
   - Expected: fixture lock, schema hash, gate A status file
   - Fail signature: missing schema/fixture manifest, nondeterministic manifest hash
2. `python3 scripts/gate_b_build.py`
   - Expected: codec/search/retarget modules compile, smoke checks pass
   - Fail signature: import errors, decode mismatch, schema mismatch
3. `python3 scripts/gate_c_benchmarks.py`
   - Expected: benchmark JSON artifacts for C001-C007 precursors
   - Fail signature: thresholds miss, benchmark crash, empty result sets
4. `python3 scripts/gate_d_falsification.py`
   - Expected: falsification markdown, determinism replay JSON, crash-rate summary
   - Fail signature: uncaught exceptions, hash drift, adversarial harness failure
5. `python3 scripts/gate_e_package.py`
   - Expected: full artifact contract and handoff manifest
   - Fail signature: missing required file, malformed JSON schema, incomplete claim map
6. `python3 scripts/gate_m1_acl_comparator.py`
   - Expected: direct ACL comparator attempt outputs and reproducibility table
   - Fail signature: ACL build/runtime unavailable without IMP-* adjudication log
7. `python3 scripts/gate_m2_live_runtime.py`
   - Expected: Blender/USD live runtime attempt artifacts (or IMP-* with evidence)
   - Fail signature: simulated-only result presented as live pass
8. `python3 scripts/gate_m3_corpus_stress.py`
   - Expected: large-corpus stress determinism/crash evidence
   - Fail signature: determinism drift or crash-rate > 0%
9. `python3 scripts/gate_m4_replay_core_claims.py`
   - Expected: core claim replay under max-wave corpus
   - Fail signature: any core claim regresses without downgrade
10. `python3 scripts/gate_e_appendix_ingestion.py`
   - Expected: Appendix E artifacts (`max_resource_lock.json`, `max_resource_validation_log.md`, `max_claim_resource_map.json`, `impracticality_decisions.json`, `multisensor_alignment_report.json`, `joint_class_error_breakdown.json`, `net_new_gap_closure_matrix.json`)
   - Fail signature: missing E artifacts, missing command evidence, missing IMP-* reasoning where needed
11. `python3 scripts/gate_e_runpod_readiness.py`
   - Expected: `runpod_readiness_manifest.json` and `runpod_exec_plan.md` when any `IMP-COMPUTE`
   - Fail signature: IMP-COMPUTE present but RunPod artifacts missing
12. `python3 scripts/gate_f_commercial_closure.py`
   - Expected: `commercialization_claim_adjudication.json` and updated `max_claim_resource_map.json` with PASS/FAIL/PAUSED_EXTERNAL only
   - Fail signature: any final claim left `INCONCLUSIVE` or missing commercialization evidence

## Expected Output Root
- `artifacts/2026-02-20_zpe_mocap_wave1/`

## Rollback Strategy
- Gate checkpoint file at each gate: `artifacts/2026-02-20_zpe_mocap_wave1/checkpoints/gate_*.json`
- On gate failure: patch minimally, rerun failed gate and all downstream gates
- Rollback trigger: deterministic drift, uncaught crash, fidelity regression, schema drift
- Max-wave rollback trigger: failed direct-comparator attempt without evidence trail, live-runtime gate unverifiable, or missing E-G artifacts
- Final-phase rollback trigger: any claim remains `INCONCLUSIVE`, or Appendix F commercialization rules are violated

## Fallback Strategy
- Resource unavailable: substitute deterministic synthetic corpus extension with explicit comparability note
- External comparator unavailable: use gzip/zstd and ACL literature baseline; mark ACL direct comparator `INCONCLUSIVE`
- Blender/USD integration unavailable in runtime: run adapter integrity simulation and mark real DCC runtime evidence `INCONCLUSIVE`
- NET-NEW resource fallback must include IMP-* code, command transcript, substitution, and claim-impact annotation in `impracticality_decisions.json`

## Final Closure Loop (2026-02-21)
### Blockers Before
- B1 (P0): `gate_m1` FAIL (ACL direct comparator missing executable/comparator evidence path)
- B2 (P0): `gate_m2` FAIL (no live Blender/USD runtime proof)
- B3 (P1): `MOC-C006` `PAUSED_EXTERNAL` (commercial-safe retarget substitute unresolved)

### Per-Blocker Execution Order
1. Local dependency/install fix.
2. Reproducible containerized path.
3. Commercial-safe open substitute.
4. GPU/RunPod readiness fallback package.

### Predeclared Closure Commands
1. `.venv/bin/python -m pip install cmake ninja`
2. `git -C external/acl submodule update --init --recursive`
3. `./external/acl/build_make/tools/acl_compressor/main_generic/acl_compressor ...`
4. `python3.11 -m pip install --user usd-core`
5. `.venv/bin/python scripts/gate_m1_acl_comparator.py`
6. `.venv/bin/python scripts/gate_m2_live_runtime.py`
7. `.venv/bin/python scripts/gate_e_appendix_ingestion.py`
8. `.venv/bin/python scripts/gate_e_runpod_readiness.py`
9. `.venv/bin/python scripts/gate_f_commercial_closure.py`
10. `.venv/bin/python scripts/gate_e_package.py`

### Final Closure Artifacts
- `blockers_before_after.json`
- refreshed `claim_status_delta.md`
- refreshed `quality_gate_scorecard.json`
- refreshed `falsification_results.md`
- refreshed `command_log.txt`
- refreshed `runpod_readiness_manifest.json`
- refreshed `runpod_exec_plan.md`

## Claim Promotion Policy
- Claims remain `UNTESTED` until evidence file exists in output root
- Claims move to `PASS` only if threshold is met and falsification gate did not invalidate
- Claims with substitution and unproven equivalence remain `INCONCLUSIVE`
- Final closure override: before handoff, every `INCONCLUSIVE` must be resolved to `FAIL` or `PAUSED_EXTERNAL` with evidence-backed adjudication

## Appendix B Traceability Plan
1. ACL comparator benchmark -> compression benchmark + traceability mapping
2. LAFAN1 and LAFAN1-resolved -> core benchmark dataset mapping
3. bvhio BVH roundtrip -> IO adapter test evidence
4. usdBVHAnim integration -> adapter evidence and fallback status
5. Mixamo retargeting -> retarget benchmark mapping
6. CMU diversity set -> stress matrix mapping
7. MoMa retarget study -> explicit design decision note with citation mapping

## Appendix D/E Traceability Plan
1. M1 ACL direct comparator -> `max_resource_validation_log.md`, `impracticality_decisions.json`, `net_new_gap_closure_matrix.json`
2. M2 Blender/USD live runtime -> `max_resource_validation_log.md`, `multisensor_alignment_report.json`
3. M3 large-corpus stress replay -> `determinism_replay_results.json`, `falsification_results.md`, `joint_class_error_breakdown.json`
4. M4 core claim replay -> updated `claim_status_delta.md` and gate checkpoint
5. E-G1..E-G5 closure -> `max_resource_lock.json`, `max_claim_resource_map.json`, `impracticality_decisions.json`, `runpod_readiness_manifest.json` (if IMP-COMPUTE), `net_new_gap_closure_matrix.json`
6. F-G1/F-G2 commercialization closure -> `commercialization_claim_adjudication.json`, updated `claim_status_delta.md`, updated `handoff_manifest.json`
