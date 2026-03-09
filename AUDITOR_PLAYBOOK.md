# Auditor Playbook

This is the shortest honest verification path for the current private staging repo.

## What This Path Establishes

- the package installs from `./code`
- the minimal unit-test surface passes
- the repo contains the imported February 20, 2026 proof bundle
- current docs correctly distinguish proved synthetic-corpus results from simulated or absent external/runtime claims

## Shortest Repo Audit Path

1. Clone the private repo and create an environment:

```bash
git clone https://github.com/Zer0pa/ZPE-Mocap.git
cd ZPE-Mocap
python -m venv .venv
source .venv/bin/activate
python -m pip install -e ./code
```

2. Run the current lightweight sanity surface:

```bash
python -m unittest discover -s code/tests -v
```

3. Run one direct package smoke:

```bash
python - <<'PY'
from zpe_mocap.codec import decode_zpmoc, encode_clip
from zpe_mocap.synthetic import generate_clip

clip = generate_clip(
    clip_id="audit_smoke",
    label="walk",
    frames=120,
    fps=60,
    seed=20260220,
    noise_scale=0.0002,
)
enc = encode_clip(clip, seed=20260220)
dec = decode_zpmoc(enc.payload)
print(
    {
        "compression_ratio": enc.compression_ratio,
        "decoded_clip_id": dec.clip_id,
        "encoded_size_bytes": enc.encoded_size_bytes,
    }
)
PY
```

4. Inspect the historical proof anchors:

- `proofs/artifacts/2026-02-20_zpe_mocap_wave1/mocap_compression_benchmark.json`
- `proofs/artifacts/2026-02-20_zpe_mocap_wave1/mocap_search_eval.json`
- `proofs/artifacts/2026-02-20_zpe_mocap_wave1/acl_direct_comparator_table.json`
- `proofs/artifacts/2026-02-20_zpe_mocap_wave1/integration_readiness_contract.json`
- `proofs/artifacts/2026-02-20_zpe_mocap_wave1/mocap_blender_roundtrip.json`

## Expected Current Truth

- the editable install succeeds
- `code/tests` passes `2/2`
- the imported proof bundle exists and is readable
- Blender/USD compatibility remains documented as simulated
- CMU-backed commercialization closure remains unpromoted

## If Your Replay Disagrees

Capture:
- commit SHA
- exact commands
- Python version
- stdout/stderr

Then compare against:
- `README.md`
- `PUBLIC_AUDIT_LIMITS.md`
- `proofs/README.md`
