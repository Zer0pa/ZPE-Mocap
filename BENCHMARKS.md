# Benchmarks

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

1. Set `ZPE_MOCAP_CMU_ROOT` to a writable cache with downloaded BVH files.
2. Run `python code/scripts/cmu_ingest.py`.
3. Run `python code/scripts/gate_c_benchmarks.py`.
4. Publish only the rows generated from that run of record.

## Current Published Metrics

| dataset | metric | value | source |
|---------|--------|-------|--------|
| Synthetic wave1 (80 clips) | compression ratio vs raw BVH float32 | `zpmoc_mean_cr=85.1893` | `proofs/artifacts/2026-02-20_zpe_mocap_wave1/mocap_compression_benchmark.json` |
| Synthetic wave1 (80 clips) | gzip ratio vs raw BVH float32 | `gzip_mean_cr=69.7018` | `proofs/artifacts/2026-02-20_zpe_mocap_wave1/mocap_compression_benchmark.json` |
| Synthetic wave1 (80 clips) | position fidelity | `mpjpe_mean_mm=1.1901` | `proofs/artifacts/2026-02-20_zpe_mocap_wave1/mocap_position_fidelity.json` |
| Synthetic wave1 (80 clips) | query latency p95 | `p95_ms=26.1375` | `proofs/artifacts/2026-02-20_zpe_mocap_wave1/mocap_query_latency.json` |

## Baseline Comparison Skeleton

| dataset | baseline | ZPE | ratio | improvement |
|---------|----------|-----|-------|-------------|
| CMU MoCap corpus | pending phase 3 | pending phase 3 | pending phase 3 | pending phase 3 |
