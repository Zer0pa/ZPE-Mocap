# 2026-04-14 CMU corpus benchmark

## Scope

- Corpus mode: `fixture`
- Corpus root: `code/fixtures/cmu`
- Selected clips: `10`
- External ingest status: failed
- External ingest evidence: `proofs/artifacts/2026-04-14_cmu_corpus_benchmark/cmu_ingest_attempt.log`

## Result

- Mean compression ratio vs raw BVH float32: `18.77232014335372x`
- Compression ratio range vs raw BVH float32: `15.222953904045156x` to `22.98069498069498x`
- Mean compression ratio vs source BVH file: `19.19186883976752x`
- Mean MPJPE: `32.45230144481235 mm`
- Mean joint-angle RMSE: `82.51017542212895 deg`
- Mean encode latency: `45.9550126 ms`
- Mean decode latency: `63.3215582 ms`

## Limitation

- `scripts/cmu_ingest.py` failed with `HTTP Error 404: Not Found`
- Authority corpus for this run is the committed 10-clip CMU fixture set, not a freshly downloaded full CMU mirror
