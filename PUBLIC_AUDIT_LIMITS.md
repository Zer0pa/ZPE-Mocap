# Public Audit Limits

This repo is a private staging surface. The only promoted authority is the imported `2026-02-20` synthetic-corpus wave. No CMU commercialization-safe closure, no Blender runtime proof, and no clean-clone verification are promoted.

## What A Public Audit Can Establish (Table-Driven)

| Claim | Current status | Evidence anchor | Boundary |
| --- | --- | --- | --- |
| Editable install | Verifiable | `AUDITOR_PLAYBOOK.md` | Confined to the minimal install path |
| Minimal unit tests | Verifiable | `code/tests` | Only the current sanity surface |
| Proof bundle presence | Verifiable | `proofs/artifacts/2026-02-20_zpe_mocap_wave1/` | Historical import, not a new run-of-record |
| Synthetic-only authority | Verifiable | `README.md` | No external or commercial dataset claims |
| CMU/Blender/clean-clone disclaimers | Verifiable | `README.md` | Disclaimers are explicit and current |

## What A Public Audit Cannot Establish (Table-Driven)

| Limit | Current status | Why it matters |
| --- | --- | --- |
| Public release readiness | Not established | This repo is a staging snapshot, not a release surface |
| Clean-clone reproducibility | Not established | No cold-clone verification has been accepted in-repo |
| Direct Blender runtime proof | Not established | Blender adapter evidence is simulation-only |
| CMU corpus presence | Not established | CMU data is not vendored into this repo |
| Commercial-safe launch posture | Not established | CMU-backed closure is not promoted here |

## Limits Matrix (Table-Driven)

| Boundary | Current truth | Evidence anchor | Audit impact |
| --- | --- | --- | --- |
| Historical proof bundle | Imported wave1 artifacts | `proofs/artifacts/2026-02-20_zpe_mocap_wave1/` | Some artifacts retain machine-absolute paths |
| Runtime compatibility | Blender/USD remains simulation-heavy | `proofs/artifacts/.../mocap_blender_roundtrip.json` | A historical `PASS` is not launch proof |
| External data | ACL/CMU/dataset clones are outside the repo | `docs/ARCHITECTURE.md` | No external dataset parity is proven here |
| Commercial-safe posture | CMU-backed closure not promoted | `README.md` | Commercial claims remain downgraded |
| Verification depth | Only lightweight sanity runs are documented | `AUDITOR_PLAYBOOK.md` | Clean-clone and max-wave gates remain pending |

## Use These Files Together

`README.md`, `AUDITOR_PLAYBOOK.md`, `docs/README.md`, `proofs/README.md`.
