# Validation and Cross-Checks

**Analysis Date:** 2026-03-19

## Analytic Cross-Checks

**Limiting Cases Verified:**

- Encode/decode on deterministic synthetic clips: compression ratio, joint-angle RMSE, and MPJPE stay within gate thresholds -> Match: Yes
  - Files: `tests/test_codec.py`, `src/zpe_mocap/benchmark.py`
- Exact retrieval on identical token streams -> Match: Yes
  - File: `tests/test_search.py`
- Determinism replay under fixed seeds -> Match: Yes
  - Files: `src/zpe_mocap/benchmark.py`, `artifacts/2026-02-20_zpe_mocap_wave1/determinism_replay_results.json`

**Limiting Cases NOT Verified:**

- Same thresholds on real BVH/FBX corpora instead of the locked synthetic corpus.
- Same search latency/precision on non-synthetic libraries.
- Live Blender runtime parity when the Blender binary is available from a clean clone.
- Direct ACL same-corpus comparator parity without proxy caveats.

**Symmetry Checks:**

- Mirror-pair similarity is computed and recorded as codec metadata.
  - File: `src/zpe_mocap/codec.py`

**Consistency Relations:**

- Claim promotion must match artifact existence and gate status.
  - Files: `runbooks/RUNBOOK_ZPE_MOCAP_MASTER.md`, `scripts/gate_e_package.py`

## Numerical Validation

**Convergence Tests:**

- No grid, timestep, or tolerance sweep is detected. Validation is threshold-based over deterministic benchmark bundles rather than convergence-analysis-based.
  - Scripts: `scripts/gate_c_benchmarks.py`, `scripts/gate_m3_corpus_stress.py`
  - Parameter study: not detected

**Stability Analysis:**

- Adversarial and malformed-input stability is covered in the falsification gate.
  - Script: `scripts/gate_d_falsification.py`
- Large-corpus stress and replay stability are covered in max-wave replay.
  - Script: `scripts/gate_m3_corpus_stress.py`

**Precision and Error Control:**

- NumPy float operations and explicit unit conversions underpin RMSE, MPJPE, percentiles, and similarity scores.
  - Files: `src/zpe_mocap/metrics.py`, `src/zpe_mocap/benchmark.py`
- Query latency uses wall-clock timing with percentile summaries.
  - File: `src/zpe_mocap/search.py`

## Comparison with Literature

**Reproduced Results:**

- ACL literature compression ratio is carried as a baseline reference value (`2.9x`) for contextual comparison.
  - Comparison in: `src/zpe_mocap/benchmark.py`, `artifacts/2026-02-20_zpe_mocap_wave1/mocap_compression_benchmark.json`

**Discrepancies:**

- Direct ACL same-corpus parity is not fully established in the authoritative root evidence surface.
  - Files: `artifacts/2026-02-20_zpe_mocap_wave1/acl_direct_comparator_table.json`, `concept_resource_traceability.json`
- Blender runtime proof remains bounded by simulated adapters or missing binaries.
  - Files: `src/zpe_mocap/adapters.py`, `scripts/gate_m2_live_runtime.py`, `artifacts/2026-02-20_zpe_mocap_wave1/mocap_blender_roundtrip.json`

## Internal Consistency

**Cross-Method Verification:**

- Synthetic generator output is validated through encode/decode metrics and retarget replay.
  - Method A: `src/zpe_mocap/synthetic.py` -> `src/zpe_mocap/codec.py`
  - Method B: `src/zpe_mocap/benchmark.py` -> artifact JSON in `artifacts/2026-02-20_zpe_mocap_wave1/`

**Self-Consistency:**

- The packaged mirror under `ZPE-Mocap/` reflects the same code and proof surfaces as the root tree.
  - Files: `src/zpe_mocap/`, `ZPE-Mocap/code/src/zpe_mocap/`, `artifacts/`, `ZPE-Mocap/proofs/artifacts/`

## Domain-Specific Notes

**Physical/Scientific Validation:**

- This is not a physics derivation project, so Ward identities, thermodynamic relations, and anomaly matching are not applicable.
- The closest scientific-equivalent checks are determinism, threshold fidelity, search precision, crash-rate, and evidence traceability.

## Test Suite

**Existing Tests:**

- `tests/test_codec.py`: encode/decode threshold sanity for CR, RMSE, and MPJPE.
  - Coverage: codec correctness on a deterministic synthetic clip
- `tests/test_search.py`: exact retrieval sanity for the motion index.
  - Coverage: exact-match search behavior

**Run Commands:**

```bash
python -m unittest discover -s tests -v
python -m unittest discover -s code/tests -v
python3 scripts/gate_c_benchmarks.py
```

**Test Patterns:**

```python
enc = encode_clip(clip, seed=20260220)
dec = decode_zpmoc(enc.payload)
self.assertGreaterEqual(enc.compression_ratio, 10.0)
self.assertLessEqual(joint_rmse_deg(clip.angles_deg, dec.angles_deg), 1.0)
```

**Missing Tests:**

- Clean-clone end-to-end replay from the repo boundary.
- Live Blender runtime regression.
- Same-corpus external comparator regression.
- Drift checks that ensure root and packaged mirrors remain identical after future edits.

## Reproducibility

**Random Seeds:**

- Fixed.
  - Files: `src/zpe_mocap/constants.py`, `runbooks/RUNBOOK_ZPE_MOCAP_MASTER.md`

**Platform Dependence:**

- Blender and USD runtime evidence depends on host availability and interpreter environment.
- Search latency percentiles may vary across hardware even if ordering remains stable.

**Version Pinning:**

- Minimal dependency surface is implied (`numpy`), but a full lockfile is not detected in the root.
  - Files: `ZPE-Mocap/code/README.md`, `.venv/` presence at the repo root

---

_Validation analysis: 2026-03-19_
