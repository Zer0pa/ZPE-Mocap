# ZPE-Mocap CMU Retrieval Benchmark Summary

## Scope

- corpus root: `/Users/Zer0pa/ZPE/ZPE Mocap/external/cmu_github_mirror`
- scanned BVH files: `24`
- clips used: `24`
- clips skipped for short duration: `0`
- window frames: `48`
- library windows per clip: `2`
- query windows per clip: `1`

## Retrieval Metrics

- recall@1: `0.125000`
- recall@5: `0.416667`
- recall@10: `0.583333`
- mean reciprocal rank: `0.277189`
- median rank: `6.0`
- latency p50: `0.825833 ms`
- latency p95: `0.869380 ms`

## Interpretation

- This benchmark is real-data retrieval over non-overlapping held-out windows from committed BVH corpus files.
- The relevance target is source-clip identity, not action-level semantic labeling.
- This strengthens the retrieval/indexing wedge without promoting playback-grade reconstruction.
