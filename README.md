<h1 align="center">ZPE-Mocap</h1>

<p align="center">
  <img src=".github/assets/readme/zpe-masthead.gif" alt="ZPE-Mocap Masthead" width="100%">
</p>

<p align="center">
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-SAL%20v7.0-e5e7eb?labelColor=111111" alt="License: SAL v7.1"></a>
  <a href="code/README.md"><img src="https://img.shields.io/badge/python-reference%20implementation-e5e7eb?labelColor=111111" alt="Python reference implementation"></a>
  <a href="proofs/artifacts/2026-04-24_cmu_retrieval_benchmark/summary.md"><img src="https://img.shields.io/badge/current%20authority-CMU%20retrieval-e5e7eb?labelColor=111111" alt="Current authority: CMU retrieval"></a>
  <a href="docs/LEGAL_BOUNDARIES.md"><img src="https://img.shields.io/badge/lane%20boundaries-retrieval%20not%20playback-e5e7eb?labelColor=111111" alt="Lane boundaries: retrieval, not playback"></a>
</p>

---

## What This Is

Motion fingerprint index for archive search. Lossy skeletal BVH fingerprints support dedupe and retrieval, not playback. Install from PyPI: `pip install zpe-mocap`

**Honest top-line (CI-anchored, real data):** mean 18.77× compression vs raw BVH float32 on 10 real CMU corpus clips, with retrieval Recall@1 0.125, Recall@10 0.583, and p50 query latency 0.826 ms — the actual product story for an archive-search index. A separate ACL synthetic comparator is documented in the Competitive Benchmarks section with its scope boundaries explicitly drawn (non-CI-gated, non-commensurable: fingerprint extraction vs playback codec); it is orientation material, not the aggregate claim.

The committed front door covers: canonical walk fixture integrity, suffix-index retrieval stability, edge-case decode coverage, and the 10-clip CMU fixture manifest.

## Codec Mechanics

<p>
  <img src=".github/assets/readme/lane-mechanics/MOCAP.gif" alt="ZPE-Mocap Codec Mechanics animation" width="100%">
</p>

| Field | Value |
| ------- | ------- |
| Architecture | SKELETON_MANIFOLD |
| Encoding | JOINT_ANGLE_V2 |
| Mechanics Asset | `.github/assets/readme/lane-mechanics/MOCAP.gif` |

## Key Metrics

| Metric | Value | Baseline |
| -------- | ------- | ---------- |
| Mean compression ratio vs raw BVH float32 (CMU, 10 clips) | 18.77× |  |
| Retrieval Recall@1 vs random baseline (0.042) | 0.125 | 3.0× above random |
| Query latency p50 | 0.826 ms |  |
| Query latency p99 | 1.191 ms |  |

> Source: CI-anchored CMU fixture benchmarks. Compression ratio is measured against raw BVH float32 bytes. Retrieval metrics are scoped to same-source clip retrieval across held-out non-overlapping windows on 24 scanned BVH files.

## Repo Identity

| Field | Value |
| ------- | ------- |
| Identifier | ZPE-Mocap |
| Repository | https://github.com/Zer0pa/ZPE-Mocap |
| Section | encoding |
| Visibility | PUBLIC |
| Architecture | SKELETON_MANIFOLD |
| Encoding | JOINT_ANGLE_V2 |
| Commit SHA | 6cef1728ef56 |
| License | SAL-7.0 |
| Authority Source | proofs/artifacts/2026-04-24_cmu_retrieval_benchmark/results.json |

## Readiness

| Field | Value |
| ------- | ------- |
| Verdict | STAGED |
| Checks | 7/7 |
| Anchors | 6 display anchors |
| Commit | 6cef1728ef56 |
| Authority | proofs/artifacts/2026-04-24_cmu_retrieval_benchmark/results.json |

### Honest Blocker

No claim of playback-quality pose reconstruction.; No claim of real-data parity with the synthetic benchmark bundle.; No claim that the synthetic ACL comparison is a fair commercial benchmark.

## What We Prove

- Canonical walk payload is byte-stable. Artifact: code/tests/fixtures/canonical_walk.json, code/tests/fixtures/canonical_walk_compressed.bin. Test: code/tests/test_roundtrip.py::test_canonical_walk_payload_matches_committed_binary.
- Canonical walk roundtrip remains numerically stable against the committed fixture. Artifact: code/tests/fixtures/canonical_walk_roundtrip.json. Test: code/tests/test_roundtrip.py::test_canonical_walk_roundtrip_matches_committed_json.
- Exact retrieval over the committed compressed walk fixture remains stable. Artifacts: code/tests/fixtures/canonical_walk.json, code/tests/fixtures/canonical_walk_compressed.bin. Tests: code/tests/test_search.py::test_retrieves_exact, code/tests/test_search.py::test_queries_compressed_library.
- Search ranking and retrieval metric primitives used by the CMU benchmark remain covered. Artifacts: code/zpe_mocap/search.py, code/zpe_mocap/metrics.py, code/scripts/benchmark_cmu_retrieval.py. Tests: code/tests/test_search.py, code/tests/test_metrics.py.
- The committed CMU fixture manifest remains fixed to the 10 checked-in BVH clips. Artifacts: code/fixtures/cmu/manifest.json, code/fixtures/cmu/bvh/*.bvh. Test: code/tests/test_cmu_offline.py::test_manifest_matches_committed_fixture_set.

## What We Don't Claim

- Not a playback codec. ZPE-Mocap produces lossy fingerprints sized for retrieval and indexing, not playback-grade reconstruction. MPJPE (reconstruction fidelity) is not a design target and is not measured.
- Lossy by design. The encoding is intentionally lossy. A decoded fingerprint is not a faithful reconstruction of the source motion.
- ACL comparator is synthetic only. The 57.03× figure from the ACL Direct Compression Comparator runs on 10 synthetic clips (wave 1 fixture), not CMU real data. It is not CI-gated and is not the lane's compression claim. The aggregate CI-gated claim is the 18.77× CMU figure.
- Fingerprint-vs-playback non-commensurability. ZPE-Mocap and ACL do different jobs; a single ratio number cannot compare them. The ACL comparator is orientation material, not a ranking benchmark.
- Semantic action retrieval is not claimed. The retrieval scope is same-source clip retrieval across held-out non-overlapping windows. Cross-action semantic retrieval has not been evaluated.
- CMU corpus is 10 clips (fixture scale). The 18.77× compression figure is bounded to 10 checked-in CMU fixture clips. Scale-up to 100+ clips is an upcoming workstream, not a current claim.

## Verification Status

| Code | Check | Verdict |
| ------ | ------- | --------- |
| T_01 | Canonical walk payload matches committed binary fixture | PASS |
| T_02 | Canonical walk roundtrip matches committed JSON fixture within numerical tolerance | PASS |
| T_03 | Synthetic encode/decode threshold smoke path | PASS |
| T_04 | Suffix-index exact retrieval remains stable | PASS |
| T_05 | Retrieval metric helpers used by the CMU benchmark remain stable | PASS |
| T_06 | CMU fixture manifest remains fixed to the committed 10-clip set | PASS |
| T_07 | Decode edge cases preserve expected shapes and fps | PASS |

## Proof Anchors

| Path | State |
| ------ | ------- |
| `proofs/artifacts/2026-04-14_cmu_corpus_benchmark/results.json` | VERIFIED |
| `proofs/artifacts/2026-04-14_cmu_corpus_benchmark/summary.md` | VERIFIED |
| `proofs/artifacts/2026-04-24_cmu_retrieval_benchmark/results.json` | VERIFIED |
| `proofs/artifacts/2026-04-24_cmu_retrieval_benchmark/summary.md` | VERIFIED |
| `proofs/artifacts/2026-02-20_zpe_mocap_wave1/mocap_compression_benchmark.json` | VERIFIED |
| `proofs/artifacts/2026-02-20_zpe_mocap_wave1/mocap_joint_fidelity.json` | VERIFIED |

## Repo Shape

| Field | Value |
| ------- | ------- |
| Proof Anchors | 6 display anchors |
| Modality Lanes | 1 |
| Architecture | SKELETON_MANIFOLD |
| Encoding | JOINT_ANGLE_V2 |
| Verification | 7/7 checks |
| Authority Source | proofs/artifacts/2026-04-24_cmu_retrieval_benchmark/results.json |

- `code/`: Python reference implementation and repo-local tests.
- `proofs/artifacts/2026-02-20_zpe_mocap_wave1/`: historical synthetic ceiling bundle.
- `proofs/artifacts/2026-04-14_cmu_corpus_benchmark/`: checked-in CMU fixture benchmark bundle.
- `proofs/artifacts/2026-04-24_cmu_retrieval_benchmark/`: current CMU retrieval authority bundle.
- `docs/`: architecture and legal-boundary notes.
- `proofs/logs/`, `proofs/source_refs/`: lineage and source-reference material.

## Competitive Benchmarks

**Synthetic comparison (non-CI-gated, non-commensurable: fingerprint extraction vs playback codec).** This comparator runs on 10 synthetic clips (wave 1 fixture), not CMU real data. ZPE-Mocap extracts a lossy fingerprint sized for retrieval; ACL targets playback-grade reconstruction. The two systems are not commensurable on a single ratio number — a fingerprint index and a playback codec are doing different jobs — and this benchmark is not gated by CI. Reported here for orientation only; do not treat the 57.03× figure as the lane's compression claim. The aggregate, CI-gated claim is the 18.77× CMU figure above.

| Codec | Mean ratio vs raw BVH float32 | ACL level | Corpus | Proof |
|-------|-------------------------------|-----------|--------|-------|
| ZPE-Mocap | 57.03× | n/a (fingerprinting) | 10 synthetic clips | [`acl_direct_comparator_table.json`](proofs/artifacts/2026-02-20_zpe_mocap_wave1/acl_direct_comparator_table.json) |
| ACL (Animation Compression Library) | 19.15× | medium | same 10 synthetic clips | [`acl_direct_comparator_table.json`](proofs/artifacts/2026-02-20_zpe_mocap_wave1/acl_direct_comparator_table.json) |

ACL reference: [github.com/nfrechette/acl](https://github.com/nfrechette/acl). ACL binary was built locally from source and run directly; the ratio is measured against the same raw BVH float32 baseline. This result is not CI-gated and is bounded to the wave 1 synthetic fixture.

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
