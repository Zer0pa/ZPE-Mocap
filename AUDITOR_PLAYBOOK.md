<img src=".github/assets/readme/zpe-masthead.gif" alt="ZPE-Mocap Masthead" width="100%">

# Auditor Playbook

Shortest honest verification path for the current ZPE-Mocap staging repo. Current authority is the imported `2026-02-20` synthetic-corpus wave only. No CMU commercialization-safe closure, no Blender runtime proof, and no clean-clone verification are promoted. If your clone is a fork, use its URL and keep evidence references identical.

## Audit Scope (Table-Driven)

| Area | Current truth | Evidence anchor | Boundary |
| --- | --- | --- | --- |
| Install + unit tests | Editable install and minimal tests should pass | `code/tests` | Only the minimal sanity surface is covered |
| Proof bundle presence | Historical wave1 bundle is present in-repo | `proofs/artifacts/2026-02-20_zpe_mocap_wave1/` | Imported lineage may include machine-absolute paths |
| Synthetic-only authority | All promoted results are synthetic-corpus only | `README.md` | No external or commercial dataset proofs are promoted |
| Blender/USD runtime | Blender path remains simulated | `proofs/artifacts/.../mocap_blender_roundtrip.json` | No live Blender binary run in this repo |
| CMU commercialization | CMU-backed closure is not promoted | `docs/ARCHITECTURE.md` | CMU-related claims remain non-authoritative |
| Clean-clone replay | Not established by this path | `PUBLIC_AUDIT_LIMITS.md` | Requires cold-clone verification outside this lane |

## Shortest Repo Audit Path (Table-Driven)

| Step | Command | Expected signal |
| --- | --- | --- |
| 1. Clone + install | `git clone https://github.com/Zer0pa/ZPE-Mocap.git`<br>`cd ZPE-Mocap`<br>`python -m venv .venv`<br>`source .venv/bin/activate`<br>`python -m pip install -e ./code` | Editable install completes without errors |
| 2. Run minimal tests | `python -m unittest discover -s code/tests -v` | `2/2` tests pass |
| 3. Smoke codec path | `python - <<'PY'`<br>`from zpe_mocap.codec import decode_zpmoc, encode_clip`<br>`from zpe_mocap.synthetic import generate_clip`<br>`clip = generate_clip(clip_id="audit_smoke", label="walk", frames=120, fps=60, seed=20260220, noise_scale=0.0002)`<br>`enc = encode_clip(clip, seed=20260220)`<br>`dec = decode_zpmoc(enc.payload)`<br>`print({"compression_ratio": enc.compression_ratio, "decoded_clip_id": dec.clip_id, "encoded_size_bytes": enc.encoded_size_bytes})`<br>`PY` | Prints a dict with a non-empty `decoded_clip_id` |
| 4. Verify proof anchors | Inspect the wave1 artifacts below | Files exist and are readable |

## Proof Anchors (Wave1 Synthetic Bundle)

| Anchor | What it supports | Status boundary |
| --- | --- | --- |
| `proofs/artifacts/2026-02-20_zpe_mocap_wave1/mocap_compression_benchmark.json` | Synthetic compression/fidelity benchmarks | Synthetic-only authority |
| `proofs/artifacts/2026-02-20_zpe_mocap_wave1/mocap_search_eval.json` | Synthetic search quality metrics | Synthetic-only authority |
| `proofs/artifacts/2026-02-20_zpe_mocap_wave1/acl_direct_comparator_table.json` | ACL comparator notes | Comparator is historical, not a current in-repo rerun |
| `proofs/artifacts/2026-02-20_zpe_mocap_wave1/integration_readiness_contract.json` | Integration readiness status | External runtime not proven |
| `proofs/artifacts/2026-02-20_zpe_mocap_wave1/mocap_blender_roundtrip.json` | Blender adapter roundtrip note | Simulated adapter path only |

## If Your Replay Disagrees

| Capture | Why |
| --- | --- |
| Commit SHA | Pinpoint repo snapshot |
| Exact commands | Reproduce your path |
| Python version | Verify runtime alignment |
| Stdout/stderr | Diagnose deltas quickly |

Then compare against `README.md`, `PUBLIC_AUDIT_LIMITS.md`, and `proofs/README.md`.

<img src=".github/assets/readme/zpe-masthead.gif" alt="ZPE-Mocap Masthead" width="100%">
