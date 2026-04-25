<h1 align="center">ZPE-Mocap</h1>

<p align="center">
  <img src=".github/assets/readme/zpe-masthead.gif" alt="ZPE-Mocap Masthead" width="100%">
</p>

<p align="center">
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-SAL%20v7.0-e5e7eb?labelColor=111111" alt="License: SAL v7.0"></a>
  <a href="code/README.md"><img src="https://img.shields.io/badge/python-reference%20implementation-e5e7eb?labelColor=111111" alt="Python reference implementation"></a>
  <a href="proofs/artifacts/2026-04-24_cmu_retrieval_benchmark/summary.md"><img src="https://img.shields.io/badge/current%20authority-CMU%20retrieval-e5e7eb?labelColor=111111" alt="Current authority: CMU retrieval"></a>
  <a href="docs/LEGAL_BOUNDARIES.md"><img src="https://img.shields.io/badge/lane%20boundaries-retrieval%20not%20playback-e5e7eb?labelColor=111111" alt="Lane boundaries: retrieval, not playback"></a>
</p>

---

## What This Is

ZPE-Mocap is a deterministic motion fingerprinting and retrieval codec for skeletal motion data. The CI-backed repo surface is the canonical walk fixture, suffix-index retrieval behavior, edge-case decode coverage, and the committed 10-clip CMU fixture manifest. This front door does not promote playback-grade reconstruction or commercial-closure claims.

## CI-Verified Surface

| Surface | Backing artifact | CI path |
|--------|------------------|---------|
| Canonical walk payload is byte-stable. | `code/tests/fixtures/canonical_walk.json`, `code/tests/fixtures/canonical_walk_compressed.bin` | `code/tests/test_roundtrip.py::test_canonical_walk_payload_matches_committed_binary` |
| Canonical walk roundtrip remains numerically stable against the committed fixture. | `code/tests/fixtures/canonical_walk_roundtrip.json` | `code/tests/test_roundtrip.py::test_canonical_walk_roundtrip_matches_committed_json` |
| Exact retrieval over the committed compressed walk fixture remains stable. | `code/tests/fixtures/canonical_walk.json`, `code/tests/fixtures/canonical_walk_compressed.bin` | `code/tests/test_search.py::test_retrieves_exact`, `code/tests/test_search.py::test_queries_compressed_library` |
| Search ranking and retrieval metric primitives used by the CMU benchmark remain covered. | `code/zpe_mocap/search.py`, `code/zpe_mocap/metrics.py`, `code/scripts/benchmark_cmu_retrieval.py` | `code/tests/test_search.py`, `code/tests/test_metrics.py` |
| The committed CMU fixture manifest remains fixed to the 10 checked-in BVH clips. | `code/fixtures/cmu/manifest.json`, `code/fixtures/cmu/bvh/*.bvh` | `code/tests/test_cmu_offline.py::test_manifest_matches_committed_fixture_set` |

## CMU Retrieval Benchmark

The current retrieval authority is the 2026-04-24 CMU held-out-window benchmark. It supports the retrieval/indexing wedge only: same-source clip retrieval across non-overlapping windows, not playback-grade reconstruction and not semantic action retrieval.

| Field | Value | Proof |
|-------|-------|-------|
| Verdict | PASS for retrieval/indexing scope | [`summary.md`](proofs/artifacts/2026-04-24_cmu_retrieval_benchmark/summary.md) |
| Corpus | 24 scanned BVH files, 24 clips used | [`results.json`](proofs/artifacts/2026-04-24_cmu_retrieval_benchmark/results.json) |
| Relevance target | Same source clip across held-out non-overlapping windows | [`summary.md`](proofs/artifacts/2026-04-24_cmu_retrieval_benchmark/summary.md) |
| Recall@1 | 0.125000 | [`summary.md`](proofs/artifacts/2026-04-24_cmu_retrieval_benchmark/summary.md) |
| Recall@5 | 0.416667 | [`summary.md`](proofs/artifacts/2026-04-24_cmu_retrieval_benchmark/summary.md) |
| Recall@10 | 0.583333 | [`summary.md`](proofs/artifacts/2026-04-24_cmu_retrieval_benchmark/summary.md) |
| Mean reciprocal rank | 0.277189 | [`summary.md`](proofs/artifacts/2026-04-24_cmu_retrieval_benchmark/summary.md) |
| Median rank | 6.0 | [`summary.md`](proofs/artifacts/2026-04-24_cmu_retrieval_benchmark/summary.md) |
| Latency p95 | 0.869380 ms | [`summary.md`](proofs/artifacts/2026-04-24_cmu_retrieval_benchmark/summary.md) |

## Tests and Verification

| Code | Check | Verdict |
|------|-------|---------|
| T_01 | Canonical walk payload matches committed binary fixture | PASS |
| T_02 | Canonical walk roundtrip matches committed JSON fixture within numerical tolerance | PASS |
| T_03 | Synthetic encode/decode threshold smoke path | PASS |
| T_04 | Suffix-index exact retrieval remains stable | PASS |
| T_05 | Retrieval metric helpers used by the CMU benchmark remain stable | PASS |
| T_06 | CMU fixture manifest remains fixed to the committed 10-clip set | PASS |
| T_07 | Decode edge cases preserve expected shapes and fps | PASS |

## Evidence On Disk

| Path | State |
|------|-------|
| `proofs/artifacts/2026-04-14_cmu_corpus_benchmark/results.json` | PRESENT |
| `proofs/artifacts/2026-04-14_cmu_corpus_benchmark/summary.md` | PRESENT |
| `proofs/artifacts/2026-04-24_cmu_retrieval_benchmark/results.json` | PRESENT |
| `proofs/artifacts/2026-04-24_cmu_retrieval_benchmark/summary.md` | PRESENT |
| `proofs/artifacts/2026-02-20_zpe_mocap_wave1/mocap_compression_benchmark.json` | PRESENT |
| `proofs/artifacts/2026-02-20_zpe_mocap_wave1/mocap_joint_fidelity.json` | PRESENT |
| `proofs/artifacts/2026-02-20_zpe_mocap_wave1/mocap_search_eval.json` | PRESENT |
| `proofs/artifacts/2026-02-20_zpe_mocap_wave1/mocap_query_latency.json` | PRESENT |

## Repo Shape

| Field | Value |
|-------|-------|
| Evidence Bundles | 3 |
| Modality Lanes | 1 |
| CI Front Door | fixture-backed encode/decode, retrieval, and metric-helper checks |

- `code/`: Python reference implementation and repo-local tests.
- `proofs/artifacts/2026-02-20_zpe_mocap_wave1/`: historical synthetic ceiling bundle.
- `proofs/artifacts/2026-04-14_cmu_corpus_benchmark/`: checked-in CMU fixture benchmark bundle.
- `proofs/artifacts/2026-04-24_cmu_retrieval_benchmark/`: current CMU retrieval authority bundle.
- `docs/`: architecture and legal-boundary notes.
- `proofs/logs/`, `proofs/source_refs/`: lineage and source-reference material.

## Quick Start

```bash
git clone https://github.com/Zer0pa/ZPE-Mocap.git
cd ZPE-Mocap
python -m venv .venv
source .venv/bin/activate
python -m pip install -e ./code
python -m unittest discover -s code/tests -v
```

Smoke check:

```bash
python - <<'PY'
from zpe_mocap.codec import decode_zpmoc, encode_clip
from zpe_mocap.synthetic import generate_clip

clip = generate_clip(
    clip_id="readme_smoke",
    label="walk",
    frames=120,
    fps=60,
    seed=20260220,
    noise_scale=0.0002,
)
enc = encode_clip(clip, seed=20260220)
dec = decode_zpmoc(enc.payload)
print(enc.compression_ratio, dec.clip_id)
PY
```

The checked-in benchmark bundles under `proofs/artifacts/` remain available for manual inspection. Only the CMU retrieval metrics surfaced above are promoted here, and they are bounded to retrieval/indexing scope by the proof artifact and CI-covered search primitives.

Read [docs/LEGAL_BOUNDARIES.md](docs/LEGAL_BOUNDARIES.md) before turning any artifact in this repo into a broader playback or commercial claim.
