# ZPE-Mocap GPD Execution Plan

## Phase Name / Number Or Proposed Phase Name

Proposed phase: `AUG-MOCAP-01 Real-Corpus Retrieval Authority Upgrade`

This repo is not currently an active `.gpd` project. `.gpd/` exists, but there is no installed `ROADMAP.md`, `STATE.md`, or active phase tree. This file is therefore GPD-ready rather than an installed phase artifact.

## Phase Objective

Upgrade ZPE-Mocap from fixture-bound real-data compression evidence plus synthetic retrieval lineage to a real-corpus retrieval authority surface that supports the retrieval/indexing wedge without broadening into playback claims.

## Dependency Chain

1. Confirm repo truth and stale local-state ownership.
2. Confirm HF custody and accessible corpus paths.
3. Reconcile current docs to existing truth where they overclaim or drift.
4. Repair benchmark path for non-duplicate real-corpus retrieval evaluation.
5. Run the benchmark and emit proof artifacts.
6. Re-verify repo-facing claims against the new proof.

## Wave Plan

### Wave 0: Entry checks

- Confirm current branch, dirty files, and gone-upstream hazard.
- Confirm `Zer0pa/ZPE-Mocap-artifacts` is visible and remains the authority target.
- Confirm local CMU mirror/cache paths are present.

### Wave 1: Truth reconciliation

- Align `docs/ARCHITECTURE.md` and `docs/LEGAL_BOUNDARIES.md` to current README/proof truth.
- Record any unresolved front-door wording that must wait for new proof.

### Wave 2: Benchmark repair

- Remove exact-duplicate retrieval leakage from the current benchmark design.
- Replace stale ingest dependence with the already available CMU mirror/cache path where possible.
- Define the real-corpus split and benchmark manifest.

### Wave 3: Proof execution

- Run the benchmark on Mac CPU first.
- Emit JSON/markdown proof artifacts under `proofs/artifacts/<date>_...`.
- Store any large benchmark bundles in HF if needed.

### Wave 4: Verification and release-readiness

- Re-check repo truth against the new proof.
- Produce final release-readiness verdict and remaining blockers.

## Subagent Plan

- Repo-truth explorer: inspect doc drift and claim boundaries.
- Custody explorer: verify HF authority target and large-artifact coverage.
- Benchmark worker: own retrieval benchmark repair and proof artifact generation.
- Verification worker: own post-proof validation and final authority check.

The coordinating agent retains the final lane decision and release-readiness verdict.

## Verification Loop

1. Read current proof and current docs.
2. Implement one scoped benchmark or truth-alignment change.
3. Run targeted validation.
4. Check whether the change strengthens the sovereign gate.
5. If yes, keep it and move to the next dependency.
6. If no, revert the interpretation, not by force-resetting the repo, but by refusing to promote the failed result.

## Checkpoint Policy

- Checkpoint after Wave 0 with explicit note on dirty local-state hazards.
- Checkpoint after Wave 1 with the reconciled truth boundary.
- Checkpoint after Wave 2 when the benchmark methodology is fixed and non-duplicate.
- Checkpoint after Wave 3 only when proof artifacts exist and are readable.
- Final checkpoint after Wave 4 with a strict readiness verdict.

No checkpoint may claim pass status unless the corresponding artifact exists and supports it.

## What Must Be True Before `gpd-execute-phase` Starts

- The user explicitly authorizes execution, not just readiness planning.
- File ownership around the current dirty `README.md` and untracked `docs/_planning/` is resolved.
- The gone-upstream branch hazard has a clear local execution policy.
- The coordinator accepts `AUG-MOCAP-01` as the next inserted/proposed phase or initializes `.gpd` properly.
- The benchmark methodology is defined as non-duplicate real-corpus retrieval, not synthetic retrieval replay.
- HF authority target remains `Zer0pa/ZPE-Mocap-artifacts`.
- Execution scope stays retrieval/indexing only; playback/reconstruction remains out of scope.
