<h1 align="center">ZPE-Mocap</h1>

<p align="center">
  <img src=".github/assets/readme/zpe-masthead.gif" alt="ZPE-Mocap Masthead" width="100%">
</p>

<p align="center">
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-SAL%20v6.2-e5e7eb?labelColor=111111" alt="License: SAL v6.2"></a>
  <a href="code/README.md"><img src="https://img.shields.io/badge/python-reference%20implementation-e5e7eb?labelColor=111111" alt="Python reference implementation"></a>
  <a href="proofs/artifacts/2026-04-14_cmu_corpus_benchmark/summary.md"><img src="https://img.shields.io/badge/current%20authority-CMU%20fixture%20benchmark-e5e7eb?labelColor=111111" alt="Current authority: CMU fixture benchmark"></a>
  <a href="docs/LEGAL_BOUNDARIES.md"><img src="https://img.shields.io/badge/lane%20boundaries-retrieval%20not%20playback-e5e7eb?labelColor=111111" alt="Lane boundaries: retrieval, not playback"></a>
</p>

---

## What This Is

ZPE-Mocap is a deterministic motion fingerprinting and retrieval codec for skeletal motion data. The commercial wedge is not faithful pose reconstruction. It is compact motion fingerprints for search, indexing, and retrieval where raw BVH archives are expensive to store and slow to query.

The real-data authority surface is the committed CMU fixture benchmark: `18.77×` mean bandwidth reduction, `32.45 mm` mean MPJPE, and `82.51°` mean joint-angle RMSE across 10 BVH clips. That angle error is too high for playback-grade reconstruction, so the lane must be read as retrieval/indexing only. The older synthetic bundle remains useful for ceiling behavior and search latency, but it is not the commercial front door.

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
| SYNTHETIC_BANDWIDTH | 85.19× | gzip 69.70× |

Source: [results.json](proofs/artifacts/2026-04-14_cmu_corpus_benchmark/results.json), [summary.md](proofs/artifacts/2026-04-14_cmu_corpus_benchmark/summary.md), [mocap_search_eval.json](proofs/artifacts/2026-02-20_zpe_mocap_wave1/mocap_search_eval.json)

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
- Synthetic search ranking at `p@10 = 1.0` and synthetic query latency at `26.14 ms` p95.
- A committed Wave-1 evidence bundle with explicit commercialization and integration boundaries.

## What We Don't Claim

- No claim of playback-quality pose reconstruction.
- No claim of real-data parity with the synthetic benchmark bundle.
- No claim that the synthetic ACL comparison is a fair commercial benchmark.
- No claim of Blender runtime closure, clean-clone verification, or commercialization-safe closure.
- No claim that this repo is a released animation-runtime product.

## Commercial Readiness

| Field | Value |
|-------|-------|
| Verdict | CONDITIONAL — retrieval/indexing mode only |
| Commit SHA | c3f8ac9dd082 |
| Primary Boundary | `82.51°` CMU joint-angle RMSE blocks playback claims |
| Source | `proofs/artifacts/2026-04-14_cmu_corpus_benchmark/summary.md`, `proofs/artifacts/2026-02-20_zpe_mocap_wave1/commercialization_claim_adjudication.json` |

The live commercial wedge is motion fingerprinting and similarity retrieval. Anything broader than that is overstating what the current evidence supports.

## Tests and Verification

| Code | Check | Verdict |
|------|-------|---------|
| V_01 | CMU fixture benchmark | PASS |
| V_02 | Synthetic compression benchmark | PASS |
| V_03 | Synthetic joint fidelity | PASS |
| V_04 | Synthetic search ranking | PASS |
| V_05 | Synthetic query latency | PASS |
| V_06 | Commercialization claim adjudication | CONDITIONAL |

## Proof Anchors

| Path | State |
|------|-------|
| `proofs/artifacts/2026-04-14_cmu_corpus_benchmark/results.json` | VERIFIED |
| `proofs/artifacts/2026-04-14_cmu_corpus_benchmark/summary.md` | VERIFIED |
| `proofs/artifacts/2026-02-20_zpe_mocap_wave1/mocap_compression_benchmark.json` | VERIFIED |
| `proofs/artifacts/2026-02-20_zpe_mocap_wave1/mocap_joint_fidelity.json` | VERIFIED |
| `proofs/artifacts/2026-02-20_zpe_mocap_wave1/mocap_search_eval.json` | VERIFIED |
| `proofs/artifacts/2026-02-20_zpe_mocap_wave1/mocap_query_latency.json` | VERIFIED |
| `proofs/artifacts/2026-02-20_zpe_mocap_wave1/quality_gate_scorecard.json` | VERIFIED |
| `proofs/artifacts/2026-02-20_zpe_mocap_wave1/commercialization_claim_adjudication.json` | VERIFIED |

## Repo Shape

| Field | Value |
|-------|-------|
| Proof Anchors | 8 |
| Modality Lanes | 1 |
| Authority Source | `proofs/artifacts/2026-04-14_cmu_corpus_benchmark/summary.md` |

- `code/`: Python reference implementation and repo-local tests.
- `proofs/artifacts/2026-02-20_zpe_mocap_wave1/`: historical synthetic ceiling bundle.
- `proofs/artifacts/2026-04-14_cmu_corpus_benchmark/`: current real-data benchmark authority.
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
