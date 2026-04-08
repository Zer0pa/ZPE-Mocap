# Benchmarks

This file is an evidence ledger, not a replacement for the README authority block. The imported `2026-02-20_zpe_mocap_wave1` synthetic bundle remains the only promoted front-door authority surface. The public CMU subset run below is phase-3 evidence only and does not support a sub-degree-fidelity claim.

## Methodology

### Synthetic wave1 readback

1. Use the imported authority bundle in `proofs/artifacts/2026-02-20_zpe_mocap_wave1/`.
2. Read `mocap_compression_benchmark.json`, `mocap_position_fidelity.json`, and `mocap_query_latency.json`.
3. Copy only artifact-backed values into the published tables below.

### Single-file BVH smoke

1. Install extras: `python -m pip install -e "./code[cmu,test,docs]"`.
2. Run `python examples/bvh_compress.py`.
3. Run `python examples/cmu_offline_demo.py` for one real CMU BVH file.
4. Inspect the emitted JSON summaries for compression ratio, joint RMSE, and MPJPE.

### Corpus benchmark path

1. Run `./.venv/bin/python code/scripts/benchmark_cmu_public_corpus.py --target-sequences 100 --extra-candidates 0 --workers 6 --timeout-sec 180 --retry-count 3 --cache-root /tmp/zpe_mocap_cmu_full_cache --artifact-root proofs/artifacts/2026-04-08_cmu_public_corpus_benchmark`.
2. The script lists the public CMU GitHub mirror tree at `https://api.github.com/repos/una-dinosauria/cmu-mocap/git/trees/master?recursive=1`.
3. It selects a deterministic round-robin subset across subject directories, downloads the exact BVH files into `/tmp/zpe_mocap_cmu_full_cache`, then computes per-clip ratio, RMSE, and MPJPE.
4. Publish only the rows generated from `proofs/artifacts/2026-04-08_cmu_public_corpus_benchmark/cmu_public_corpus_benchmark.json`.

### Blocked surfaces

- AMASS remains blocked in this phase. Registration is required at `https://amass.is.tue.mpg.de/`.
- Mixamo remains blocked in this phase. Adobe login is required at `https://www.mixamo.com/`.
- Blender viewport GIF remains blocked in this phase. See `proofs/artifacts/2026-04-08_cmu_public_corpus_benchmark/phase3_blockers.md`.
- Blender preview scaffold is available at `proofs/artifacts/2026-04-08_cmu_public_corpus_benchmark/blender_preview_ready/`.

## Current Published Metrics

| dataset | metric | value | source |
|---------|--------|-------|--------|
| Synthetic wave1 (80 clips) | compression ratio vs raw BVH float32 | `zpmoc_mean_cr=85.1893` | `proofs/artifacts/2026-02-20_zpe_mocap_wave1/mocap_compression_benchmark.json` |
| Synthetic wave1 (80 clips) | gzip ratio vs raw BVH float32 | `gzip_mean_cr=69.7018` | `proofs/artifacts/2026-02-20_zpe_mocap_wave1/mocap_compression_benchmark.json` |
| Synthetic wave1 (80 clips) | position fidelity | `mpjpe_mean_mm=1.1901` | `proofs/artifacts/2026-02-20_zpe_mocap_wave1/mocap_position_fidelity.json` |
| Synthetic wave1 (80 clips) | query latency p95 | `p95_ms=26.1375` | `proofs/artifacts/2026-02-20_zpe_mocap_wave1/mocap_query_latency.json` |
| CMU MoCap public subset (100 sequences) | total duration | `0.2991 hours` | `proofs/artifacts/2026-04-08_cmu_public_corpus_benchmark/cmu_public_corpus_benchmark.json` |
| CMU MoCap public subset (100 sequences) | compression ratio vs raw BVH float32 | `zpe_ratio_mean=20.3016x` | `proofs/artifacts/2026-04-08_cmu_public_corpus_benchmark/cmu_public_corpus_benchmark.json` |
| CMU MoCap public subset (100 sequences) | gzip ratio vs raw BVH float32 | `gzip_ratio_mean=1.4432x` | `proofs/artifacts/2026-04-08_cmu_public_corpus_benchmark/cmu_public_corpus_benchmark.json` |
| CMU MoCap public subset (100 sequences) | joint-angle RMSE | `joint_angle_rmse_deg_mean=80.3369` | `proofs/artifacts/2026-04-08_cmu_public_corpus_benchmark/cmu_public_corpus_benchmark.json` |
| CMU MoCap public subset (100 sequences) | position fidelity | `mpjpe_mm_mean=44.3691` | `proofs/artifacts/2026-04-08_cmu_public_corpus_benchmark/cmu_public_corpus_benchmark.json` |

## CMU Public Subset

Result: the 100-sequence public CMU subset beats gzip on ratio, but it does not support the brief's requested phrase `sub-degree joint fidelity`. Mean joint-angle RMSE is `80.3369 deg`, mean MPJPE is `44.3691 mm`, and Blender viewport evidence is still absent.

| dataset | sequences | joints | frames | ratio | RMSE (deg) | MPJPE (mm) |
|---------|-----------|--------|--------|-------|------------|------------|
| CMU MoCap public subset | `100` | `31.00 mean` | `129230` | `20.3016x` | `80.3369` | `44.3691` |

Artifact source: `proofs/artifacts/2026-04-08_cmu_public_corpus_benchmark/cmu_public_corpus_benchmark.json`
Preview scaffold: `proofs/artifacts/2026-04-08_cmu_public_corpus_benchmark/blender_preview_ready/blender_preview_generated.py`

## Baseline Comparison

| dataset | baseline | ZPE | ratio | improvement |
|---------|----------|-----|-------|-------------|
| CMU MoCap public subset | `gzip -9 vs raw BVH float32` | `20.3016x` | `1.4432x` | `14.0672x` |
