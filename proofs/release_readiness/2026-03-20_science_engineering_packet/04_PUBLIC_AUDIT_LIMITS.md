# Audit Limits

This repo is a private staging repo, not a public release surface.

## What The Current Audit Path Can Establish

- the package installs from `./code`
- the current minimal unit-test surface passes
- the historical February 20, 2026 proof bundle is present in-repo
- repo-facing docs do not promote CMU-backed commercialization closure or direct Blender runtime proof

## What The Current Audit Path Does Not Establish

- public release readiness
- blind-clone reproducibility from an external machine
- current direct Blender runtime proof
- current CMU corpus presence
- commercial-safe launch posture

## Limits Matrix

| Limit | Current state | Why it matters |
| --- | --- | --- |
| Historical proof bundle | Imported verbatim from the outer workspace | Some artifacts retain stale absolute paths as lineage |
| Runtime compatibility | Blender/USD remains simulation-heavy in current docs and imported artifacts | A historical PASS sentence is not enough for launch promotion |
| External data | ACL and dataset clones remain outside the repo | This repo is intentionally not vendoring nested repos or datasets |
| Commercial-safe posture | CMU-backed closure is contradicted by current local data presence | Commercialization-safe prose remains downgraded |
| Verification depth | Only lightweight install/import/test sanity has been run in this phase | Phase 5 must perform the real cold-clone verification |

## Use These Files Together

- `README.md`
- `AUDITOR_PLAYBOOK.md`
- `docs/README.md`
- `proofs/README.md`
