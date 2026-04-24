<h1 align="center">ZPE-Mocap</h1>

<p align="center">
  <img src=".github/assets/readme/zpe-masthead.gif" alt="ZPE-Mocap Masthead" width="100%">
</p>

<p align="center">
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-SAL%20v7.0-e5e7eb?labelColor=111111" alt="License: SAL v7.0"></a>
  <a href="code/README.md"><img src="https://img.shields.io/badge/python-reference%20implementation-e5e7eb?labelColor=111111" alt="Python reference implementation"></a>
  <a href="proofs/artifacts/2026-04-24_cmu_retrieval_benchmark/summary.md"><img src="https://img.shields.io/badge/current%20authority-real%20CMU%20retrieval-e5e7eb?labelColor=111111" alt="Current authority: real CMU retrieval"></a>
  <a href="docs/LEGAL_BOUNDARIES.md"><img src="https://img.shields.io/badge/lane%20boundaries-retrieval%20not%20playback-e5e7eb?labelColor=111111" alt="Lane boundaries: retrieval, not playback"></a>
</p>

---

## What This Is

ZPE-Mocap is a deterministic skeletal-motion fingerprinting codec for BVH joint streams. It operates on ordered joint-angle motion and emits compact fingerprints for search, indexing, and retrieval rather than playback-grade pose reconstruction.

The real-data authority surface is now two-part: the committed CMU fixture benchmark for compression/fidelity and the 2026-04-24 held-out CMU retrieval benchmark for search/indexing. The fixture benchmark remains `18.77×` mean bandwidth reduction, `32.45 mm` mean MPJPE, and `82.51°` mean joint-angle RMSE across 10 BVH clips. The retrieval benchmark adds real-data held-out-window retrieval on 24 BVH files at `recall@10 = 0.5833` with `0.87 ms` p95 query latency. That closes the front door around retrieval/indexing only, not playback-grade reconstruction.

| Field | Value |
|-------|-------|
| Architecture | SKELETON_MANIFOLD |
| Encoding | JOINT_ANGLE_V2 |

## Key Metrics

| Metric | Value | Baseline |
|--------|-------|----------|
| CMU_BANDWIDTH | 18.77× | — |
| CMU_MPJPE | 32.45 mm | — |
| CMU_ANGLE_RMSE | 82.51° | — |
| CMU_RETRIEVAL_R10 | 0.5833 | 24 clips |

Source: [results.json](proofs/artifacts/2026-04-14_cmu_corpus_benchmark/results.json), [summary.md](proofs/artifacts/2026-04-14_cmu_corpus_benchmark/summary.md), [results.json](proofs/artifacts/2026-04-24_cmu_retrieval_benchmark/results.json), [summary.md](proofs/artifacts/2026-04-24_cmu_retrieval_benchmark/summary.md)

## Competitive Benchmarks

The only committed comparator tables are synthetic. They are useful for lineage, but they are not the commercial wedge because the synthetic corpus is generated from the ZPE token vocabulary itself. Real evaluation should be judged from the CMU fixture results above.

| Tool | Corpus | Result | Notes |
|------|--------|--------|-------|
| **ZPE-Mocap** | synthetic comparator set | **57.0× mean** | Same synthetic clips used for the ACL table |
| ACL | synthetic comparator set | 19.1× mean | Circular methodology; not a fair real-world comparator |
| gzip | synthetic corpus | 69.70× | General-purpose baseline on the same synthetic surface |

Source: [acl_direct_comparator_table.json](proofs/artifacts/2026-02-20_zpe_mocap_wave1/acl_direct_comparator_table.json), [mocap_compression_benchmark.json](proofs/artifacts/2026-02-20_zpe_mocap_wave1/mocap_compression_benchmark.json)

## What We Prove

- `18.77×` mean bandwidth reduction on the committed 10-clip CMU fixture corpus.
- `32.45 mm` MPJPE and `82.51°` joint-angle RMSE on real BVH data, which is sufficient for retrieval/indexing judgment but not playback.
- Real held-out CMU window retrieval on 24 BVH files at `recall@10 = 0.5833`, `median rank = 6`, and `0.87 ms` p95 query latency.
- A committed Wave-1 evidence bundle with explicit commercialization and integration boundaries.

## What We Don't Claim

- No claim of playback-quality pose reconstruction.
- No claim of semantic action retrieval beyond held-out same-source clip windows on the current real benchmark.
- No claim that the synthetic ACL comparison is a fair commercial benchmark.
- No claim of Blender runtime closure, clean-clone verification, or commercialization-safe closure.
- No claim that this repo is a released animation-runtime product.

## Commercial Readiness

| Field | Value |
|-------|-------|
| Verdict | PARTIAL |
| Commit SHA | 3492b9b1d1c3 |
| Confidence | 89% |
| Source | proofs/artifacts/2026-04-24_cmu_retrieval_benchmark/summary.md |

## Tests and Verification

| Code | Check | Verdict |
|------|-------|---------|
| V_01 | CMU fixture benchmark | PASS |
| V_02 | Real CMU held-out retrieval benchmark | PASS |
| V_03 | Synthetic compression benchmark | PASS |
| V_04 | Synthetic joint fidelity | PASS |
| V_05 | Synthetic search ranking | PASS |
| V_06 | Synthetic query latency | PASS |
| V_07 | Commercialization claim adjudication | INC |

## Proof Anchors

| Path | State |
|------|-------|
| `proofs/artifacts/2026-04-14_cmu_corpus_benchmark/results.json` | VERIFIED |
| `proofs/artifacts/2026-04-14_cmu_corpus_benchmark/summary.md` | VERIFIED |
| `proofs/artifacts/2026-04-24_cmu_retrieval_benchmark/results.json` | VERIFIED |
| `proofs/artifacts/2026-04-24_cmu_retrieval_benchmark/summary.md` | VERIFIED |
| `proofs/artifacts/2026-02-20_zpe_mocap_wave1/mocap_compression_benchmark.json` | VERIFIED |
| `proofs/artifacts/2026-02-20_zpe_mocap_wave1/mocap_joint_fidelity.json` | VERIFIED |
| `proofs/artifacts/2026-02-20_zpe_mocap_wave1/mocap_search_eval.json` | VERIFIED |
| `proofs/artifacts/2026-02-20_zpe_mocap_wave1/mocap_query_latency.json` | VERIFIED |
| `proofs/artifacts/2026-02-20_zpe_mocap_wave1/quality_gate_scorecard.json` | VERIFIED |
| `proofs/artifacts/2026-02-20_zpe_mocap_wave1/commercialization_claim_adjudication.json` | VERIFIED |

## Repo Shape

| Field | Value |
|-------|-------|
| Proof Anchors | 10 |
| Modality Lanes | 1 |
| Authority Source | `proofs/artifacts/2026-04-24_cmu_retrieval_benchmark/summary.md` |

- `code/`: Python reference implementation and repo-local tests.
- `proofs/artifacts/2026-02-20_zpe_mocap_wave1/`: historical synthetic ceiling bundle.
- `proofs/artifacts/2026-04-14_cmu_corpus_benchmark/`: current real-data benchmark authority.
- `proofs/artifacts/2026-04-24_cmu_retrieval_benchmark/`: current real-data retrieval authority.
- `docs/`: architecture and legal-boundary notes.
- `proofs/logs/`, `proofs/source_refs/`: lineage and source-reference material.

## Quick Start

```bash
# Install from PyPI
pip install zpe-mocap
```

Or use the repository verification path:

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

Read [docs/LEGAL_BOUNDARIES.md](docs/LEGAL_BOUNDARIES.md) before turning any synthetic result into a broader commercial claim.
