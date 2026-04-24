# ZPE-Mocap Workstream Plan — 2026-04-23

## Status Snapshot

- Local repo is on branch `chore/novelty-card-backfill-2026-04-22` at commit `58edcd5`.
- Relative to `main`, this branch is ahead by 1 commit only, and that delta is `CITATION.cff`.
- The working tree is not clean: `README.md` has an unstaged wording edit.
- GitHub repo is live at `https://github.com/Zer0pa/ZPE-Mocap`, default branch `main`, viewer permission `ADMIN`.
- Open PRs visible from this machine:
  - `#11` `reorientation: align repo docs to ethos`
  - `#12` `chore: instantiate SAL v7.0 portfolio-wide`
- The repo is not currently a GPD-initialized project: no `.gpd/ROADMAP.md`, `.gpd/STATE.md`, or phase directories exist.

## Current Proof Position

- Real-data authority surface: `proofs/artifacts/2026-04-14_cmu_corpus_benchmark/`
- Real-data result:
  - mean compression ratio vs raw BVH float32: `18.7723x`
  - mean MPJPE: `32.4523 mm`
  - mean joint-angle RMSE: `82.5102 deg`
- Synthetic retained evidence:
  - search precision at 10: `1.0`
  - query latency p95: `26.1375 ms`
  - quality gate scorecard: `PASS`, total score `46`
- Local package/test health:
  - `12 passed, 2 skipped` in a fresh temporary venv

## Highest-Value Observations

1. The commercial wedge is retrieval/indexing, not playback.
2. The real-data authority surface exists, but it is still only a 10-clip CMU fixture set.
3. `README.md` is materially more current than `docs/ARCHITECTURE.md` and `docs/LEGAL_BOUNDARIES.md`, which still describe an older synthetic-authority story.
4. There is no GPD planning scaffold in this repo, so any phase work needs either:
   - manual planning docs inside the repo, or
   - a deliberate `.gpd` initialization pass before using GPD commands.

## Recommended Work Phases

### Phase A — Authority Surface Reconciliation

**Objective:** Make all repo-facing docs tell the same truth as the current README and proof artifacts.

**Tasks**
- Reconcile `docs/ARCHITECTURE.md` with the CMU fixture authority surface.
- Reconcile `docs/LEGAL_BOUNDARIES.md` with the retrieval-only public posture.
- Confirm `README.md`, docs, and proof-commentary files all point to the same current authority artifact set.

**Verification**
- `git diff --check`
- repo-wide grep for stale synthetic-front-door phrasing
- fresh read-through of README + docs side by side

**Compute**
- Mac CPU only
- RunPod not needed
- GPU not needed

**Wall clock**
- `1-2 hours`

**Grant / commercial advantage**
- `Medium-High`
- This removes diligence friction immediately because it collapses contradictory public surfaces.

### Phase B — Real Retrieval Authority Upgrade

**Objective:** Expand from the committed CMU fixture set to a larger real-data retrieval benchmark and make retrieval the unambiguous front-door proof.

**Tasks**
- Repair or replace the stale CMU ingest path in `code/scripts/cmu_ingest.py`.
- Acquire a larger commercial-safe BVH corpus or a refreshed CMU pull path.
- Re-run benchmarking on a broader real corpus.
- Emit a clean proof bundle with:
  - retrieval precision
  - retrieval latency
  - compression ratio
  - explicit non-playback boundary

**Verification**
- benchmark run completes from code/scripts
- artifact bundle lands under `proofs/artifacts/...`
- README and docs cite the new bundle consistently
- tests still pass

**Compute**
- CPU only
- RunPod CPU is useful if:
  - the corpus is materially larger than the 10-clip fixture set, or
  - Mac disk pressure remains tight during ingestion and benchmarking
- GPU not needed

**Wall clock**
- `4-8 hours` total, with `1-3 hours` of active operator time

**Grant / commercial advantage**
- `High`
- This is the single most disproportionate next move because it upgrades the buyer-facing proof without requiring a new codec invention.

### Phase C — Clean-Clone / Install Confidence Pass

**Objective:** Prove the repo and package work cleanly from scratch for an outsider.

**Tasks**
- Fresh clone verification
- `pip install zpe-mocap` smoke test
- repo editable-install smoke test
- ensure the install path and proof path agree

**Verification**
- fresh venv install
- smoke command succeeds
- tests pass in the fresh environment

**Compute**
- Mac CPU only
- RunPod not needed
- GPU not needed

**Wall clock**
- `1-2 hours`

**Grant / commercial advantage**
- `Medium`
- It improves diligence confidence, but it is less leverage than expanding real-data authority.

### Phase D — Runtime / Playback Expansion (Only If Strategy Changes)

**Objective:** Only pursue Blender/runtime closure if the commercial story expands beyond retrieval/indexing.

**Tasks**
- Define whether playback/runtime is actually part of the near-term product wedge.
- If yes, plan a dedicated runtime validation phase.
- If no, keep this explicitly deferred.

**Verification**
- explicit go / no-go decision in docs and planning notes

**Compute**
- CPU likely enough for validation orchestration
- GPU not needed for the current evidence path

**Wall clock**
- `0.5-1 day` if activated

**Grant / commercial advantage**
- `Low` right now
- This is not the sharpest next move unless strategy changes.

## Pod Recommendation

- **Immediate next work:** no pod required.
- **Best-use pod case:** Phase B on a larger real corpus, CPU-only.
- **GPU pod:** not justified for the current lane objective.

## Recommended Order

1. Phase A
2. Phase B
3. Phase C
4. Phase D only if product strategy broadens

## Practical Next Move

If choosing one next action only, do **Phase B** after a short Phase A cleanup. That combination gives the strongest disproportionate commercial and grant narrative: the repo becomes internally consistent, then the retrieval wedge is backed by a broader real-data authority surface instead of a small fixture-bound one.
