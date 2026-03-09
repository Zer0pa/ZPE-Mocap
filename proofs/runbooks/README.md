# Runbooks

These runbooks were imported from the outer workspace and preserved for execution lineage.

## Translation Rule

Where a historical runbook says:
- `scripts/` read `code/scripts/`
- `artifacts/` read `proofs/artifacts/`
- `fixtures/` read `code/fixtures/`
- `format/` read `code/format/`
- `external/` read `../external/` from the repo root, or use `ZPE_MOCAP_EXTERNAL_ROOT`

## Historical Caveat

Some imported runbooks still contain stale absolute paths in their body text. Those are historical references, not current repo-root instructions.
