# Computational Architecture

**Analysis Date:** 2026-03-19

## Mathematical Setting

**Spaces:**

- Motion-clip tensor space: arrays with shape `[frames, joints, 3]` for positions and angles.
  - File: `src/zpe_mocap/synthetic.py`
- Token-stream space: flattened integer k-gram retrieval streams derived from interleaved XY/XZ token channels.
  - Files: `src/zpe_mocap/search.py`, `src/zpe_mocap/benchmark.py`
- Artifact space: JSON/Markdown proof outputs rooted at `artifacts/2026-02-20_zpe_mocap_wave1/`.
  - Files: `src/zpe_mocap/constants.py`, `scripts/_common.py`

**Key Computational Objects:**

| Object | Type | Symbol / Name | Defined In |
| --- | --- | --- | --- |
| Encoded motion payload | Binary container | `EncodedMotion` | `src/zpe_mocap/codec.py` |
| Synthetic motion clip | Data record | `MotionClip` | `src/zpe_mocap/synthetic.py` |
| Search index | Retrieval structure | `MotionSuffixIndex` | `src/zpe_mocap/search.py` |
| Benchmark bundle | Result bundle | `BenchmarkBundle` | `src/zpe_mocap/benchmark.py` |
| Adapter roundtrip record | Compatibility result | `AdapterRoundtripResult` | `src/zpe_mocap/adapters.py` |

## Notation and Conventions

**Index Conventions:**

- `frames, joints, 3` axis order is consistent across motion arrays.
- Parent hierarchy is encoded by integer indices in `PARENTS`.
- Claim IDs use `MOC-C001` through `MOC-C007`.

**Custom Macros / Naming:**

- `_quantize_*`, `_detect_*`, `_apply_*`, `_restore_*` prefixes denote codec-internal helpers.
- `gate_*` scripts align one file per execution gate.
- `positions_m`, `angles_deg`, `magnitudes_mm`, `p95_ms`, and `p_at_10` embed units directly in names.

**Operator Ordering:**

- No symbolic operator algebra is used. Ordering is procedural and gate-driven.

## Algebraic Structure

**Discrete Structures:**

- 8-way directional token alphabet with mirror mapping.
  - Files: `src/zpe_mocap/constants.py`, `src/zpe_mocap/codec.py`
- Parent-relative modulo-8 encoding and restoration.
  - File: `src/zpe_mocap/codec.py`

**Representations:**

- Skeleton joint tree with fixed `JOINT_NAMES`, `PARENTS`, and `REST_OFFSETS`.
  - Files: `src/zpe_mocap/constants.py`, `src/zpe_mocap/synthetic.py`

## Functional Structure

**Core Functional Pipeline:**

- Synthetic generation -> encode -> decode -> metric evaluation -> artifact write.
  - Files: `src/zpe_mocap/synthetic.py`, `src/zpe_mocap/codec.py`, `src/zpe_mocap/benchmark.py`, `scripts/gate_c_benchmarks.py`
- Artifact bundle -> claim adjudication -> packaging -> readiness reporting.
  - Files: `scripts/gate_e_package.py`, `scripts/gate_f_commercial_closure.py`

**Variational Principles:**

- Not applicable. This repo uses algorithmic transforms and threshold checks rather than optimization-based solvers.

## Computational Architecture

**Directory Layout:**

```text
[project-root]/
+-- src/zpe_mocap/                 # authoritative Python reference implementation
+-- scripts/                       # gate executors and artifact packagers
+-- tests/                         # lightweight sanity tests
+-- fixtures/                      # deterministic locked corpus inputs
+-- format/                        # schema definition
+-- artifacts/2026-02-20_zpe_mocap_wave1/  # proof outputs and checkpoints
+-- runbooks/                      # gate protocol and failure signatures
+-- ZPE-Mocap/                     # packaged repo-facing mirror with docs/proofs/code
+-- external/acl/                  # dependency/baseline source, not core truth surface
```

**Computational Pipeline:**

1. Gate A: fixture and schema lock.
   - Script: `scripts/gate_a_setup.py`
2. Gate B: codec, search, retarget smoke surface.
   - Script: `scripts/gate_b_build.py`
3. Gate C: quantitative benchmark generation.
   - Script: `scripts/gate_c_benchmarks.py`
4. Gate D: falsification and determinism stress.
   - Script: `scripts/gate_d_falsification.py`
5. Gate E/F and M1-M4: package, comparator, live-runtime, stress replay, and commercialization closure.
   - Scripts: `scripts/gate_e_package.py`, `scripts/gate_m1_acl_comparator.py`, `scripts/gate_m2_live_runtime.py`, `scripts/gate_m3_corpus_stress.py`, `scripts/gate_m4_replay_core_claims.py`, `scripts/gate_f_commercial_closure.py`

**Key Algorithms:**

- Parent-relative token codec with periodicity and mirror-group metadata extraction.
  - Implementation: `src/zpe_mocap/codec.py`
- Label-conditioned synthetic corpus generation with deterministic seeds.
  - Implementation: `src/zpe_mocap/synthetic.py`
- Suffix-like k-gram retrieval with exact-match priority.
  - Implementation: `src/zpe_mocap/search.py`
- Scale-space retarget benchmark.
  - Implementation: `src/zpe_mocap/retarget.py`

**Symbolic Computation:**

- Not detected.

**Numerical Methods:**

- NumPy-based array transforms, percentile summaries, and mean-based threshold checks.
  - Implementation: `src/zpe_mocap/benchmark.py`, `src/zpe_mocap/metrics.py`
  - Parameters: search library size `10_000`, query count `120`, retarget sample count `40`, adapter sample count `16`

## Transformation Properties

**How Objects Transform:**

- Absolute tokens become parent-relative modulo-8 streams before serialization.
  - File: `src/zpe_mocap/codec.py`
- Left/right joint token streams are mirrored through `TOKEN_MIRROR` for structure diagnostics.
  - File: `src/zpe_mocap/codec.py`
- Retargeting rescales motion to a `target_scale`.
  - File: `src/zpe_mocap/retarget.py`

**Covariance / Invariance:**

- Determinism under fixed seeds is an explicit invariant checked by `determinism_hash`.
  - Verified in: `src/zpe_mocap/benchmark.py`, `artifacts/2026-02-20_zpe_mocap_wave1/determinism_replay_results.json`

## Boundary and Initial Conditions

**Boundary Conditions:**

- First frame uses the rest pose; reconstruction starts from `rest_frame`.
  - Files: `src/zpe_mocap/synthetic.py`, `src/zpe_mocap/codec.py`
- External resource boundaries are staged through `.env`, `../external/`, and explicit IMP-* adjudication.
  - Files: `runbooks/RUNBOOK_ZPE_MOCAP_MASTER.md`, `scripts/gate_m2_live_runtime.py`

**Initial Conditions:**

- Global seed `20260220` and fixed action label inventory initialize deterministic replay.
  - Files: `src/zpe_mocap/constants.py`, `runbooks/RUNBOOK_ZPE_MOCAP_MASTER.md`

---

_Architecture analysis: 2026-03-19_
