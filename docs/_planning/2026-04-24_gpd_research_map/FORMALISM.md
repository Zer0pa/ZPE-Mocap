# Theoretical Frameworks

**Analysis Date:** 2026-03-19

## Physical System

**Subject:** Deterministic motion-compression, retrieval, and retargeting system for synthetic human-motion clips. No genuine physics formalism is detected in this repo; the governing formalism is an implementation-level motion-codec and benchmark framework documented in `PRD_ZPE_MOCAP_SECTOR_EXPANSION_WAVE1_2026-02-20.md`, `runbooks/RUNBOOK_ZPE_MOCAP_MASTER.md`, and `src/zpe_mocap/`.

**Scales:**

- Compression: target `>= 10x` vs raw BVH float32, stretch target `>= 12x`; implemented in `src/zpe_mocap/benchmark.py`.
- Fidelity: joint-angle RMSE threshold `<= 1 deg`, MPJPE threshold `<= 5 mm`, retarget MPJPE threshold `<= 10 mm`; enforced in `tests/test_codec.py`, `scripts/gate_c_benchmarks.py`, and artifact JSON under `artifacts/2026-02-20_zpe_mocap_wave1/`.
- Time: clip frame rates are typically `60 fps`; query latency target is `< 100 ms` on a 10K-clip synthetic library; defined in `PRD_ZPE_MOCAP_SECTOR_EXPANSION_WAVE1_2026-02-20.md` and `src/zpe_mocap/benchmark.py`.
- Dimensionless parameters: `p_at_10`, mirror similarity, periodicity confidence, and compression ratio.

**Degrees of Freedom:**

- `MotionClip.positions_m`: frame-by-joint Cartesian trajectories in meters, defined in `src/zpe_mocap/synthetic.py`.
- `MotionClip.angles_deg`: frame-by-joint Euler-like angular representation in degrees, defined in `src/zpe_mocap/synthetic.py`.
- `xy_tokens` / `xz_tokens`: 8-way directional token streams per joint, generated in `src/zpe_mocap/synthetic.py` and reconstructed in `src/zpe_mocap/codec.py`.
- `magnitudes_mm`: per-joint motion magnitudes in millimeters, defined in `src/zpe_mocap/synthetic.py` and serialized in `src/zpe_mocap/codec.py`.

## Theoretical Framework

**Primary Framework:**

- Deterministic parent-relative token codec over synthetic skeleton motion.
- Formulation: tokenized local-delta quantization plus zlib-packed binary container.
- File: `src/zpe_mocap/codec.py`

**Secondary/Supporting Frameworks:**

- Synthetic corpus generator with fixed skeletal topology, label-conditioned motion templates, and seeded Gaussian perturbations.
  - File: `src/zpe_mocap/synthetic.py`
- Suffix-like k-gram retrieval index for action search.
  - File: `src/zpe_mocap/search.py`
- Scale-space retarget baseline.
  - File: `src/zpe_mocap/retarget.py`
- Gate-oriented evidence packaging and claim adjudication.
  - Files: `scripts/gate_*.py`, `runbooks/RUNBOOK_ZPE_MOCAP_MASTER.md`

## Fundamental Equations

**Governing Equations:**

| Equation / Rule | Type | Location | Status |
| --- | --- | --- | --- |
| 8-way directional quantization from local deltas to XY/XZ tokens | Constitutive encoding rule | `src/zpe_mocap/codec.py` | Implemented |
| Token-to-delta reconstruction with magnitude scaling | Decoder reconstruction rule | `src/zpe_mocap/codec.py` | Implemented |
| Parent-relative modulo-8 token transform | Hierarchy constraint encoding | `src/zpe_mocap/codec.py` | Implemented |
| Local-state accumulation to reconstruct positions | Motion update rule | `src/zpe_mocap/synthetic.py`, `src/zpe_mocap/codec.py` | Implemented |
| Benchmark threshold rules for CR, RMSE, MPJPE, P@10, latency | Acceptance contract | `PRD_ZPE_MOCAP_SECTOR_EXPANSION_WAVE1_2026-02-20.md`, `src/zpe_mocap/benchmark.py` | Defined and executed |

**Equation of Motion / Field Equations:**

- Form: no physical equation of motion is present; the repo uses deterministic procedural motion generation via token templates, rest-pose offsets, and accumulated local deltas.
- File: `src/zpe_mocap/synthetic.py`
- Derived from: code-defined synthetic motion model, not from a Lagrangian or Hamiltonian.

**Constraints:**

- Valid skeleton hierarchy with a single rooted parent graph and required payload fields.
  - Files: `src/zpe_mocap/validation.py`, `src/zpe_mocap/codec.py`
- Codec payload must carry `magic`, version, joint names, parent list, and segment payloads.
  - File: `src/zpe_mocap/codec.py`

## Symmetries and Conservation Laws

**Exact Symmetries:**

- Left/right mirror-pair symmetry is explicitly modeled through `MIRROR_PAIRS` and `TOKEN_MIRROR`.
  - Files: `src/zpe_mocap/constants.py`, `src/zpe_mocap/codec.py`
- Deterministic seed reproducibility is enforced as an invariant for replay runs.
  - Files: `src/zpe_mocap/constants.py`, `src/zpe_mocap/benchmark.py`, `runbooks/RUNBOOK_ZPE_MOCAP_MASTER.md`

**Approximate Symmetries:**

- Periodic motion structure is treated as a detectable pattern, not a guaranteed invariant; confidence below `0.72` suppresses periodicity claims.
  - File: `src/zpe_mocap/codec.py`

**Gauge Symmetries:**

- Not detected. This is not a gauge-theory project.

**Ward Identities / Selection Rules:**

- Not detected in physics form. The closest analogue is the gate rule that claims may be promoted only with matching evidence artifacts.
  - Files: `runbooks/RUNBOOK_ZPE_MOCAP_MASTER.md`, `scripts/gate_e_package.py`

**Anomalies:**

- No quantum or field-theoretic anomalies are relevant.

**Topological Properties:**

- Not detected.

**Dualities and Correspondences:**

- No formal dualities are documented. The nearest correspondence is between synthetic proxy evidence and claimed external/runtime comparators, and that correspondence is repeatedly marked partial or simulated.
  - Files: `artifacts/2026-02-20_zpe_mocap_wave1/concept_resource_traceability.json`, `ZPE-Mocap/README.md`

## Parameters and Couplings

**Fundamental Parameters:**

- `GLOBAL_SEED = 20260220`: master reproducibility seed.
  - Defined in: `src/zpe_mocap/constants.py`
- `k` for `MotionSuffixIndex`: k-gram length for retrieval.
  - Defined in: `src/zpe_mocap/search.py`
- `noise_scale`, `frames`, `fps`, `skeleton_scale`: motion generation controls.
  - Defined in: `src/zpe_mocap/synthetic.py`
- Acceptance thresholds for CR, RMSE, MPJPE, P@10, and latency.
  - Defined in: `PRD_ZPE_MOCAP_SECTOR_EXPANSION_WAVE1_2026-02-20.md`, `src/zpe_mocap/benchmark.py`

**Derived Quantities:**

- `compression_ratio = raw_bvh_float32_bytes / encoded_size_bytes`
  - Computed in: `src/zpe_mocap/codec.py`
- `p_at_10`, `p50_ms`, `p95_ms`, `p99_ms`
  - Computed in: `src/zpe_mocap/benchmark.py`
- `payload_hash` and determinism hash
  - Computed in: `src/zpe_mocap/codec.py`, `src/zpe_mocap/benchmark.py`

**Dimensionless Ratios:**

- `compression_ratio`: core authority metric for storage efficiency.
- `precision_at_10`: retrieval quality metric.
- `mirror_similarity` and periodicity confidence: structural diagnostics inside codec metadata.

## Phase Structure / Regimes

**Regimes Studied:**

- Wave-1 core synthetic benchmark regime.
  - Applicable files: `scripts/gate_a_setup.py`, `scripts/gate_b_build.py`, `scripts/gate_c_benchmarks.py`, `scripts/gate_d_falsification.py`, `scripts/gate_e_package.py`
- Max-wave closure regime with ACL comparator, live-runtime attempt, larger-corpus stress, and commercialization adjudication.
  - Applicable files: `scripts/gate_m1_acl_comparator.py`, `scripts/gate_m2_live_runtime.py`, `scripts/gate_m3_corpus_stress.py`, `scripts/gate_m4_replay_core_claims.py`, `scripts/gate_f_commercial_closure.py`

**Phase Transitions / Crossovers:**

- Claim state transitions are `UNTESTED -> PASS/FAIL/INCONCLUSIVE/PAUSED_EXTERNAL` depending on evidence, resource availability, and commercialization rules.
  - Files: `runbooks/RUNBOOK_ZPE_MOCAP_MASTER.md`, `scripts/gate_e_package.py`, `artifacts/2026-02-20_zpe_mocap_wave1/commercialization_claim_adjudication.json`

**Known Limiting Cases:**

- Exact encode/decode smoke validation on deterministic synthetic clips.
  - Files: `tests/test_codec.py`, `src/zpe_mocap/benchmark.py`
- Simulated Blender/USD adapter path instead of live DCC runtime.
  - Files: `src/zpe_mocap/adapters.py`, `scripts/gate_m2_live_runtime.py`

## Units and Conventions

**Unit System:**

- Lengths: meters for `positions_m`, millimeters for MPJPE reporting and `magnitudes_mm`.
- Angles: degrees for `angles_deg` and RMSE thresholds.
- Time: frame counts and milliseconds.
- Metric signature: not applicable.
- Files: `src/zpe_mocap/synthetic.py`, `src/zpe_mocap/metrics.py`, `src/zpe_mocap/benchmark.py`

**Key Conventions:**

- `PASS` is evidence-bound and should not be promoted when only simulated or proxy support exists.
- Parent-relative token transforms are modulo 8.
- Motion labels come from the fixed `ACTION_LABELS` set.
- File and artifact naming centers on `MOC-C00N` claim IDs and `gate_*` execution stages.

---

_Framework analysis: 2026-03-19_
