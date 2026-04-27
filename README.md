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

ZPE-Mocap is a motion fingerprint index for archive search and deduplication, not a playback codec. It produces compact, indexable fingerprints from skeletal BVH motion data so operators of large mocap archives can locate, dedupe, and retrieve clips by content. Encoding is lossy by design; retrieval fidelity and index latency are the primary proof surfaces. The lane is one of 17 in Zer0pa's ZPE portfolio.

**Honest top-line (CI-anchored, real data):** mean 18.77× compression vs raw BVH float32 on 10 real CMU corpus clips, with retrieval Recall@1 0.125, Recall@10 0.583, and p50 query latency 0.826 ms — the actual product story for an archive-search index. A separate ACL synthetic comparator is documented in the Competitive Benchmarks section with its scope boundaries explicitly drawn (non-CI-gated, non-commensurable: fingerprint extraction vs playback codec); it is orientation material, not the aggregate claim.

The committed front door covers: canonical walk fixture integrity, suffix-index retrieval stability, edge-case decode coverage, and the 10-clip CMU fixture manifest.

## Key Metrics

| Metric | Value | Proof |
|--------|-------|-------|
| Mean compression ratio vs raw BVH float32 (CMU, 10 clips) | **18.77×** | [`results.json`](proofs/artifacts/2026-04-14_cmu_corpus_benchmark/results.json) |
| Retrieval Recall@1 vs random baseline (0.042) | **0.125** (3.0× above random) | [`results.json`](proofs/artifacts/2026-04-24_cmu_retrieval_benchmark/results.json) |
| Query latency p50 | **0.826 ms** | [`results.json`](proofs/artifacts/2026-04-24_cmu_retrieval_benchmark/results.json) |
| Query latency p99 | **1.191 ms** | [`results.json`](proofs/artifacts/2026-04-24_cmu_retrieval_benchmark/results.json) |

> Source: CI-anchored CMU fixture benchmarks. Compression ratio is measured against raw BVH float32 bytes. Retrieval metrics are scoped to same-source clip retrieval across held-out non-overlapping windows on 24 scanned BVH files.

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

## What We Prove

The following surfaces are CI-gated against committed fixtures. Every item below has a named test and a locked artifact.

- **Canonical walk payload is byte-stable.** Artifact: `code/tests/fixtures/canonical_walk.json`, `code/tests/fixtures/canonical_walk_compressed.bin`. Test: `code/tests/test_roundtrip.py::test_canonical_walk_payload_matches_committed_binary`.
- **Canonical walk roundtrip remains numerically stable against the committed fixture.** Artifact: `code/tests/fixtures/canonical_walk_roundtrip.json`. Test: `code/tests/test_roundtrip.py::test_canonical_walk_roundtrip_matches_committed_json`.
- **Exact retrieval over the committed compressed walk fixture remains stable.** Artifacts: `code/tests/fixtures/canonical_walk.json`, `code/tests/fixtures/canonical_walk_compressed.bin`. Tests: `code/tests/test_search.py::test_retrieves_exact`, `code/tests/test_search.py::test_queries_compressed_library`.
- **Search ranking and retrieval metric primitives used by the CMU benchmark remain covered.** Artifacts: `code/zpe_mocap/search.py`, `code/zpe_mocap/metrics.py`, `code/scripts/benchmark_cmu_retrieval.py`. Tests: `code/tests/test_search.py`, `code/tests/test_metrics.py`.
- **The committed CMU fixture manifest remains fixed to the 10 checked-in BVH clips.** Artifacts: `code/fixtures/cmu/manifest.json`, `code/fixtures/cmu/bvh/*.bvh`. Test: `code/tests/test_cmu_offline.py::test_manifest_matches_committed_fixture_set`.

## What We Don't Claim

- **Not a playback codec.** ZPE-Mocap produces lossy fingerprints sized for retrieval and indexing, not playback-grade reconstruction. MPJPE (reconstruction fidelity) is not a design target and is not measured.
- **Lossy by design.** The encoding is intentionally lossy. A decoded fingerprint is not a faithful reconstruction of the source motion.
- **ACL comparator is synthetic only.** The 57.03× figure from the ACL Direct Compression Comparator runs on 10 synthetic clips (wave 1 fixture), not CMU real data. It is not CI-gated and is not the lane's compression claim. The aggregate CI-gated claim is the 18.77× CMU figure.
- **Fingerprint-vs-playback non-commensurability.** ZPE-Mocap and ACL do different jobs; a single ratio number cannot compare them. The ACL comparator is orientation material, not a ranking benchmark.
- **Semantic action retrieval is not claimed.** The retrieval scope is same-source clip retrieval across held-out non-overlapping windows. Cross-action semantic retrieval has not been evaluated.
- **CMU corpus is 10 clips (fixture scale).** The 18.77× compression figure is bounded to 10 checked-in CMU fixture clips. Scale-up to 100+ clips is an upcoming workstream, not a current claim.

## Commercial Readiness

| Field | Value |
|-------|-------|
| Verdict | ACTIVE |
| Stage | Fixture-scale proof. CI surface covers retrieval stability and compression ratio on 10 CMU clips. |
| What a buyer gets today | A working Python reference implementation with CI-anchored fixture benchmarks, proof artifacts, and a defined retrieval scope. |
| What is NOT ready | Production-scale corpus (100+ clips), Recall@1 lift to buyer-evaluable threshold (current 0.125 vs target 0.25+), playback reconstruction (not a lane goal). |

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

### CMU Corpus Compression Detail

**Primary compression authority — honest headline.** Ratios measured against real CMU mocap data (10 fixture clips, cgspeed MotionBuilder-friendly BVH conversion, 2010). Basis: raw BVH float32 bytes. Reconstruction fidelity (MPJPE) is not a design target for a fingerprint index and is not claimed here. The 18.77× mean is the figure that travels with this lane.

| Field | Value | Proof |
|-------|-------|-------|
| Mean compression ratio vs raw BVH float32 | **18.77×** | [`results.json`](proofs/artifacts/2026-04-14_cmu_corpus_benchmark/results.json) |
| Compression ratio range | 15.22×–22.98× | [`results.json`](proofs/artifacts/2026-04-14_cmu_corpus_benchmark/results.json) |
| Clip count | 10 (walk, run, hop, combat, swim, calisthenics) | [`summary.md`](proofs/artifacts/2026-04-14_cmu_corpus_benchmark/summary.md) |
| Corpus | CMU MoCap database via cgspeed BVH conversion (2010) | [`results.json`](proofs/artifacts/2026-04-14_cmu_corpus_benchmark/results.json) |

### CMU Retrieval Benchmark Detail

The current retrieval authority is the 2026-04-24 CMU held-out-window benchmark. Scope: same-source clip retrieval across non-overlapping windows, not playback-grade reconstruction and not semantic action retrieval.

| Field | Value | Proof |
|-------|-------|-------|
| Verdict | PASS for retrieval/indexing scope | [`summary.md`](proofs/artifacts/2026-04-24_cmu_retrieval_benchmark/summary.md) |
| Corpus | 24 scanned BVH files, 24 clips used | [`results.json`](proofs/artifacts/2026-04-24_cmu_retrieval_benchmark/results.json) |
| Relevance target | Same source clip across held-out non-overlapping windows | [`summary.md`](proofs/artifacts/2026-04-24_cmu_retrieval_benchmark/summary.md) |
| Recall@1 | 0.125000 (3.0× random baseline of 0.042) | [`results.json`](proofs/artifacts/2026-04-24_cmu_retrieval_benchmark/results.json) |
| Recall@5 | 0.416667 | [`summary.md`](proofs/artifacts/2026-04-24_cmu_retrieval_benchmark/summary.md) |
| Recall@10 | 0.583333 | [`summary.md`](proofs/artifacts/2026-04-24_cmu_retrieval_benchmark/summary.md) |
| Mean reciprocal rank | 0.277189 | [`summary.md`](proofs/artifacts/2026-04-24_cmu_retrieval_benchmark/summary.md) |
| Median rank | 6.0 | [`summary.md`](proofs/artifacts/2026-04-24_cmu_retrieval_benchmark/summary.md) |
| Latency p50 | 0.826 ms | [`results.json`](proofs/artifacts/2026-04-24_cmu_retrieval_benchmark/results.json) |
| Latency p95 | 0.869 ms | [`summary.md`](proofs/artifacts/2026-04-24_cmu_retrieval_benchmark/summary.md) |
| Latency p99 | 1.191 ms | [`results.json`](proofs/artifacts/2026-04-24_cmu_retrieval_benchmark/results.json) |

## Competitive Benchmarks

**Synthetic comparison (non-CI-gated, non-commensurable: fingerprint extraction vs playback codec).** This comparator runs on 10 synthetic clips (wave 1 fixture), not CMU real data. ZPE-Mocap extracts a lossy fingerprint sized for retrieval; ACL targets playback-grade reconstruction. The two systems are not commensurable on a single ratio number — a fingerprint index and a playback codec are doing different jobs — and this benchmark is not gated by CI. Reported here for orientation only; do not treat the 57.03× figure as the lane's compression claim. The aggregate, CI-gated claim is the 18.77× CMU figure above.

| Codec | Mean ratio vs raw BVH float32 | ACL level | Corpus | Proof |
|-------|-------------------------------|-----------|--------|-------|
| ZPE-Mocap | 57.03× | n/a (fingerprinting) | 10 synthetic clips | [`acl_direct_comparator_table.json`](proofs/artifacts/2026-02-20_zpe_mocap_wave1/acl_direct_comparator_table.json) |
| ACL (Animation Compression Library) | 19.15× | medium | same 10 synthetic clips | [`acl_direct_comparator_table.json`](proofs/artifacts/2026-02-20_zpe_mocap_wave1/acl_direct_comparator_table.json) |

ACL reference: [github.com/nfrechette/acl](https://github.com/nfrechette/acl). ACL binary was built locally from source and run directly; the ratio is measured against the same raw BVH float32 baseline. This result is not CI-gated and is bounded to the wave 1 synthetic fixture.

## Proof Anchors

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
| `proofs/artifacts/2026-02-20_zpe_mocap_wave1/acl_direct_comparator_table.json` | PRESENT |

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

The checked-in benchmark bundles under `proofs/artifacts/` remain available for manual inspection. Promoted metrics above are bounded to retrieval/indexing scope. Read [docs/LEGAL_BOUNDARIES.md](docs/LEGAL_BOUNDARIES.md) before turning any artifact in this repo into a broader playback or commercial claim.

## Upcoming Workstreams

This section captures the active lane priorities — what the next agent or contributor picks up, and what investors should expect. Cadence is continuous, not milestoned.

- **CMU benchmark scale-up (10 → 100+ clips)** — Active Engineering. Pure data-ingestion work; closes proof-surface gap to a buyer-evaluable corpus.
- **Recall@1 lift via fingerprint primitives** — Research-Deferred — Investigation Underway. Current 0.125 needs lift to 0.25+ for archive-search buyers; learned-embedding head, metric-learning fine-tune, or alternative distance function under investigation.
