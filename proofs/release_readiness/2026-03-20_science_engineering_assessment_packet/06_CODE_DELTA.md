# Code Delta

## Source Changes Required To Close The Local Run

Two source changes were needed during the final closure run.

### 1. Regression rerun path fix

File: [gate_e_package.py](/Users/Zer0pa/ZPE/ZPE%20Mocap/ZPE-Mocap/code/scripts/gate_e_package.py#L298)

Change:
- the regression unittest discovery now runs from `ROOT / "code"` instead of the repo root

Reason:
- the old call looked for `tests/` at the wrong level and could not re-run the packaged regression surface honestly from the inner repo boundary

Diff summary:
- `cwd=str(ROOT)` -> `cwd=str(ROOT / "code")`

### 2. ACL comparator build narrowing

File: [gate_m1_acl_comparator.py](/Users/Zer0pa/ZPE/ZPE%20Mocap/ZPE-Mocap/code/scripts/gate_m1_acl_comparator.py#L163)

Changes:
- if `acl_compressor` already exists, skip the full rebuild
- otherwise build only the `acl_compressor` target instead of the whole tree

Reason:
- the earlier path could waste time on a full ACL build even when the required comparator binary was already present
- narrowing the build made Gate M1 converge on the actual comparator requirement instead of the larger upstream build graph

## Non-Source Changes

The rest of the diff is the refreshed artifact surface:
- gate checkpoints
- metric JSON outputs
- commercialization and resource adjudication outputs
- receipts and `.gpd` state records

## Reviewer Guidance

There is no large product refactor hidden in the closeout. The meaningful engineering delta is small and local; the main outcome is refreshed evidence, not a rewritten implementation.
