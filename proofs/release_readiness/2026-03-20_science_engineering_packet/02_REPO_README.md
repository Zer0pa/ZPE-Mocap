# ZPE-Mocap

Private staging repo for the ZPE Mocap sector.

This repo contains:
- a deterministic Python reference implementation under `code/`
- a curated historical proof bundle under `proofs/`
- repo-facing docs that separate current repo reality from stale handoff prose

## Current Reality

- Package surface now lives at `./code`; editable install is `python -m pip install -e ./code`.
- The current lightweight sanity surface is `python -m unittest discover -s code/tests -v`.
- The imported February 20, 2026 proof bundle reports strong synthetic-corpus results:
  - `zpmoc_mean_cr=85.1893`
  - `joint_angle_rmse_deg≈1.16e-07`
  - `mpjpe_mean_mm=1.1901`
  - `p_at_10=1.0`
  - `query_latency_p95_ms=43.4239`
- The same historical bundle also contains a direct ACL comparator on the same synthetic raw-BVH32 baseline:
  - `zpmoc_mean_ratio=57.0328`
  - `acl_mean_ratio_same_raw_bvh32=19.1487`

## Not Promoted Here

- No blind-clone verification has been run from this repo boundary yet.
- No current direct Blender runtime pass is promoted; the imported compatibility record remains `simulated roundtrip` / `simulated smoke`.
- No CMU-backed commercialization-safe closure is promoted; the workspace CMU clone is absent of usable corpus files.
- Imported historical artifacts are preserved as evidence lineage and may retain stale machine-absolute paths.

## Quick Verify

```bash
git clone https://github.com/Zer0pa/ZPE-Mocap.git
cd ZPE-Mocap
python -m venv .venv
source .venv/bin/activate
python -m pip install -e ./code
python -m unittest discover -s code/tests -v
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

## Proof Anchors

- `proofs/artifacts/2026-02-20_zpe_mocap_wave1/mocap_compression_benchmark.json`
- `proofs/artifacts/2026-02-20_zpe_mocap_wave1/mocap_joint_fidelity.json`
- `proofs/artifacts/2026-02-20_zpe_mocap_wave1/mocap_position_fidelity.json`
- `proofs/artifacts/2026-02-20_zpe_mocap_wave1/mocap_search_eval.json`
- `proofs/artifacts/2026-02-20_zpe_mocap_wave1/mocap_query_latency.json`
- `proofs/artifacts/2026-02-20_zpe_mocap_wave1/acl_direct_comparator_table.json`
- `proofs/artifacts/2026-02-20_zpe_mocap_wave1/integration_readiness_contract.json`
- `proofs/artifacts/2026-02-20_zpe_mocap_wave1/falsification_results.md`

## Repo Map

- `code/`: installable package, tests, scripts, fixtures, schema
- `docs/`: architecture, legal boundaries, support, docs index
- `proofs/`: imported evidence bundle plus runbooks and future verification surfaces

## Read Next

- `AUDITOR_PLAYBOOK.md`
- `PUBLIC_AUDIT_LIMITS.md`
- `docs/README.md`
- `proofs/README.md`
