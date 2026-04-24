# Conventions and Methodology

**Analysis Date:** 2026-03-19

## Convention Inventory

**Implementation Naming:**
- Result: units and semantics are embedded directly in variable names.
- Files: `src/zpe_mocap/synthetic.py`, `src/zpe_mocap/metrics.py`, `src/zpe_mocap/benchmark.py`
- Method: code-level naming convention rather than symbolic notation.
- Key examples: `positions_m`, `angles_deg`, `magnitudes_mm`, `payload_hash`, `p95_ms`
- Status: consistent across the root package and the packaged mirror under `ZPE-Mocap/code/src/zpe_mocap/`

**Status Vocabulary:**
- Result: claim surfaces use `PASS`, `FAIL`, `UNTESTED`, `INCONCLUSIVE`, and `PAUSED_EXTERNAL`.
- Files: `runbooks/RUNBOOK_ZPE_MOCAP_MASTER.md`, `scripts/gate_e_package.py`, `scripts/gate_f_commercial_closure.py`
- Method: gate-controlled status promotion.
- Status: consistent in contract prose; some imported historical artifacts still overstate `PASS` when runtime proof is only simulated

## Approximations Made

**Synthetic Proxy Corpus:**
- What is neglected: real BVH/FBX corpora, real DCC runtime behavior, and diverse external-motion distributions.
- Justification given: deterministic, reproducible in-lane benchmark surface.
- Justification quality: Adequate for internal synthetic benchmarking, weak for commercialization/runtime closure.
- Parameter controlling approximation: locked synthetic corpus plus fixed seeds.
- Estimated error: not quantified relative to real-world motion distributions.
- Files: `fixtures/locked_corpus_v1.json`, `src/zpe_mocap/synthetic.py`, `artifacts/2026-02-20_zpe_mocap_wave1/concept_resource_traceability.json`

**Simulated Adapter Path:**
- What is neglected: actual Blender runtime and full USD bridge execution.
- Justification given: runtime availability may be absent; surrogate encode/decode path retained for bounded evidence.
- Justification quality: Adequate for smoke simulation, missing for live-runtime truth.
- Parameter controlling approximation: runtime availability in `scripts/gate_m2_live_runtime.py`
- Estimated error: interoperability risk remains open.
- Files: `src/zpe_mocap/adapters.py`, `scripts/gate_m2_live_runtime.py`

**ACL Literature Baseline:**
- What is neglected: exact same-corpus binary comparator parity.
- Justification given: direct ACL binary may be unavailable in-lane.
- Justification quality: Partial only.
- Parameter controlling approximation: comparator availability and external build success.
- Estimated error: direct parity claim cannot be made from the literature number alone.
- Files: `src/zpe_mocap/benchmark.py`, `artifacts/2026-02-20_zpe_mocap_wave1/acl_direct_comparator_table.json`

## Assumptions Catalog

**Explicit Assumptions:**
- Fixed seed reproducibility is sufficient to define deterministic truth for this lane.
  - Files: `src/zpe_mocap/constants.py`, `runbooks/RUNBOOK_ZPE_MOCAP_MASTER.md`
- Package surface and proof bundle under `ZPE-Mocap/` mirror root truth but do not outrank it.
  - Files: `ZPE-Mocap/README.md`, `ZPE-Mocap/docs/README.md`
- External resource failures must be recorded via IMP-* codes rather than silently substituted.
  - File: `runbooks/RUNBOOK_ZPE_MOCAP_MASTER.md`

**Implicit Assumptions:**
- The synthetic action label set is representative enough to benchmark codec, search, and retarget behavior.
  - Files: `src/zpe_mocap/constants.py`, `src/zpe_mocap/synthetic.py`
  - Risk: out-of-distribution real clips may violate current thresholds.
- Exact-match retrieval on synthetic token streams meaningfully proxies real motion retrieval.
  - Files: `src/zpe_mocap/search.py`, `tests/test_search.py`
  - Risk: search precision and latency may shift materially on true corpus diversity.

## Rigor Assessment

**Metric and Claim Discipline:**
- Rigor level: Physicist-standard equivalent in software terms; thresholds and gates are explicit, but not all external closures are re-proven in the current repo boundary.
- Issues:
  - simulated adapter results coexist with `PASS` fields in imported artifacts
  - root and packaged mirrors duplicate truth surfaces and can drift
- Files: `scripts/gate_e_package.py`, `artifacts/2026-02-20_zpe_mocap_wave1/mocap_blender_roundtrip.json`, `PHASE_4_5_HANDOFF_2026-03-09.md`

## Dimensional Analysis

**Consistency Checks:**
- `positions_m` and `mpjpe_mm` convert meters to millimeters consistently in metric reporting.
  - Files: `src/zpe_mocap/synthetic.py`, `src/zpe_mocap/metrics.py`
- `angles_deg` and the `<= 1 deg` threshold align consistently.
  - Files: `src/zpe_mocap/synthetic.py`, `tests/test_codec.py`
- `latency_ms` metrics are stored and compared in milliseconds.
  - Files: `src/zpe_mocap/metrics.py`, `src/zpe_mocap/benchmark.py`

**Dimensional Anomalies:**
- No hard unit mismatch is detected in the core package. The main issue is semantic, not dimensional: simulated runtime evidence is sometimes packaged beside stronger status labels than the runtime facts warrant.
  - Files: `src/zpe_mocap/adapters.py`, `scripts/gate_m2_live_runtime.py`, `artifacts/2026-02-20_zpe_mocap_wave1/integration_readiness_contract.json`

## Sign and Factor Conventions

**Sign Choices:**
- 8-way token directions follow a clockwise/counterclockwise mapping encoded in `TOKEN_VECTORS_2D`.
  - Consistent throughout: Yes
- Left/right mirroring uses a fixed token involution in `TOKEN_MIRROR`.
  - Consistent throughout: Yes

**Factor Tracking:**
- Root-joint and child-joint reconstructions use different scale factors (`0.25` and `0.08`) in both generation and reconstruction paths.
  - Known issues: none detected inside the current synthetic framework
  - Files: `src/zpe_mocap/synthetic.py`, `src/zpe_mocap/codec.py`

## Notation Consistency

**Consistent Usage:**
- Claim IDs, gate IDs, and artifact names are stable across the repo.
- Units remain embedded in identifier names.

**Conflicts:**
- The same codebase and proof bundle exist both at the root and under `ZPE-Mocap/`, which is a structural duplication rather than a naming conflict.
  - Files: `src/zpe_mocap/codec.py`, `ZPE-Mocap/code/src/zpe_mocap/codec.py`

---

_Convention analysis: 2026-03-19_
