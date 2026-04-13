# V6 Authority Surface — Completion Report

**Repo:** ZPE-Mocap
**Agent:** Codex
**Date:** 2026-04-14
**Branch:** campaign/v6-authority-surface

## Dimensions Executed

- [x] **A: Key Metrics** — rewritten
- [x] **B: Competitive Benchmarks** — added
- [x] **C: pip Install Fix** — fixed with root-level `pyproject.toml`
- [x] **D: Publish Workflow** — added
- [ ] **E: Proof Sync** — N/A

## Verification

- pip install from root: PASS
- import test: PASS
- Proof anchors verified: 5/5 exist
- Competitive claims honest: YES

## Key Metrics Written

| Metric | Value | Baseline | Proof File |
|--------|-------|----------|------------|
| COMPRESSION | 85.189× | vs ACL ~19× (industry std) | `proofs/artifacts/2026-02-20_zpe_mocap_wave1/mocap_compression_benchmark.json`, `proofs/artifacts/2026-02-20_zpe_mocap_wave1/acl_direct_comparator_table.json` |
| MPJPE | 1.190072 mm | position fidelity | `proofs/artifacts/2026-02-20_zpe_mocap_wave1/mocap_position_fidelity.json` |
| SEARCH | p@10 = 1.0 | 120 queries | `proofs/artifacts/2026-02-20_zpe_mocap_wave1/mocap_search_eval.json` |
| LATENCY | 26.1375 ms p95 | — | `proofs/artifacts/2026-02-20_zpe_mocap_wave1/mocap_query_latency.json` |

## Issues / Blockers

- Root package metadata now exposes `LicenseRef-Zer0pa-SAL-6.2` per the V6 campaign brief, but the repo `LICENSE` files remain SAL v6.0 and were left untouched because license-file edits are outside this campaign scope.
