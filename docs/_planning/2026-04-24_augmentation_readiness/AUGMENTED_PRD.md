# ZPE-Mocap Augmented PRD

## Lane Objective

Advance ZPE-Mocap as a deterministic motion retrieval and indexing product for skeletal motion corpora. The lane objective is not playback-grade reconstruction. The near-term execution goal is to replace synthetic retrieval authority with real-corpus retrieval authority while keeping repo claims aligned to the current proof surface.

## Current Authority Surface

- Real-data authority bundle: `/Users/Zer0pa/ZPE/ZPE Mocap/ZPE-Mocap/proofs/artifacts/2026-04-14_cmu_corpus_benchmark/`
- Proven real-data metrics on the committed 10-clip CMU fixture corpus:
  - mean compression ratio: `18.77232014335372x`
  - mean MPJPE: `32.45230144481235 mm`
  - mean joint-angle RMSE: `82.51017542212895 deg`
- Proven synthetic retrieval lineage:
  - `P@10 = 1.0`
  - latency `p95 = 26.137510099943025 ms`
- Current honest interpretation:
  - retrieval/indexing wedge is supported
  - playback/reconstruction-grade authority is not supported

## Sovereign Acceptance Gate

The sovereign acceptance gate for the next augmentation wave is real-data retrieval authority closure. A pass requires a real-corpus retrieval benchmark with explicit retrieval metrics, latency, and corpus lineage that can support ZPE-Mocap as a searchable motion index. Compression improvements, README polish, synthetic wins, or demo quality do not substitute for this gate.

## Blockers And Kill Conditions

### Current blockers

- Repo truth drifts across `README.md`, `docs/ARCHITECTURE.md`, and `docs/LEGAL_BOUNDARIES.md`.
- The current real-data benchmark is a 10-clip fixture corpus, not a broad real-corpus retrieval benchmark.
- `code/scripts/cmu_ingest.py` points at a stale CMU ingest path and cannot currently support fresh external ingestion.
- Local Git state is not execution-clean: `README.md` is modified, `docs/_planning/` is untracked, and the current branch upstream is gone.
- The repo has `.gpd/` but no active `.gpd/ROADMAP.md`, `.gpd/STATE.md`, or installed phases.

### Kill conditions

- If the retrieval benchmark still depends on exact-duplicate query/library matching, do not promote it as authority.
- If a larger real-corpus benchmark cannot materially improve beyond the fixture-bound proof, hold front-door promotion and keep the lane `PARTIAL`.
- If execution pressure shifts the lane back toward playback/reconstruction messaging, stop and re-scope.
- If the only way to produce authority is an unlicensed or unverifiable corpus path, stop and replace the corpus plan.

## Augmentation Research Synthesis

The original lane brief and shared augmentation research agree on the same strategic direction:

- Double down on retrieval/indexing, not playback.
- Move from synthetic retrieval evidence to real-corpus retrieval evidence.
- Treat compressed tokenization and embedding search as the product core.
- Keep retargeting or reconstruction as downstream optional work, not the front door.

The shared research suggests a longer-range upside in cross-corpus motion retrieval across sources such as HumanML3D, Motion-X++, and AMASS, possibly with RVQ tokenization and a TMR/SGAR-style dual encoder. That is directionally useful, but it is not the immediate proof move. The immediate proof move should stay closer to current repo reality: repair the corpus path, benchmark retrieval on real BVH data, and prove retrieval authority without inventing a new research stack first.

## Chosen Wedge / Rejected Wedges

### Chosen wedge

Deterministic motion retrieval and indexing over real skeletal motion corpora, with compression as an enabling property and latency as a retrieval utility metric.

### Rejected wedges

- Playback-grade codec claims
- Reconstruction-grade fidelity claims
- Synthetic retrieval as headline authority
- Compression-SOTA or commercial superiority claims from the current evidence
- Repo-front-door repositioning beyond the current proof surface

## Commercial / Grant / Research Upside

### Commercial upside

The strongest commercial story is searchable motion infrastructure for robotics, simulation, animation, and motion-library operations. The wedge is a fast compressed motion index upstream of downstream retargeting or control systems, not a finished animation runtime.

### Grant upside

The shared research points toward physical-AI, robotics, and embodied-data infrastructure calls as the best thematic fit. Those references are useful for direction, but they should be treated as sourced from the provided research packet rather than re-verified live funding guidance in this readiness pass.

### Research upside

The research upside is a defensible retrieval benchmark over real motion corpora, followed by optional cross-corpus embedding work only after the repo has a real-data retrieval authority surface.

## Mechanics-Layer Implications

ZPE-Mocap remains a `partial` mechanics-layer lane.

- Object basis: skeletal motion sequences from BVH now, with later SMPL/SMPL-X only when artifact-backed.
- Object currency: frames, joints, temporal pose deltas, retrieval tokens, and corpus IDs.
- Transform: deterministic tokenization/compression plus retrieval index construction and querying.
- Preserved surface: retrieval relevance and query latency when supported by real-data proofs.
- Failure surface: playback/reconstruction fidelity remains weak and must stay explicit.
- Authority anchors: proof JSON/markdown artifacts, benchmark code, and custody-backed corpora.

No mechanics-layer promotion should outrun the artifact set.

## Repo-Front-Door Implications

- Keep the repo front door aligned to retrieval/indexing truth.
- Do not promote playback, runtime, Blender, clean-clone closure, or commercialization-safe closure beyond current proof.
- Reconcile `docs/ARCHITECTURE.md` and `docs/LEGAL_BOUNDARIES.md` to the same authority position already reflected in `README.md`.
- Keep the canonical README structure and repo playbook conventions intact.

## GitHub Requirements

- GitHub remains the authority for code, docs, and small proof files.
- No GitHub mutation occurs in this readiness pass.
- Before execution publishes results, the lane needs a human decision on the current branch because `origin/chore/novelty-card-backfill-2026-04-22` is gone.
- Any future doc or proof updates must land only after the relevant authority artifact exists.

## Hugging Face Requirements

- Hugging Face is the authority for large corpora, benchmark caches, and large proof bundles.
- Verified authoritative dataset repo: `Zer0pa/ZPE-Mocap-artifacts`
- Verified duplicate legacy repo also exists: `Architect-Prime/ZPE-Mocap-artifacts`
- Execution should treat `Zer0pa/ZPE-Mocap-artifacts` as the authoritative custody target and avoid further namespace drift.
- Current HF-class material already in scope:
  - `external/cmu_github_mirror/**`
  - `external/cmu_phase3_benchmark_cache/**`
  - custody copies of `README.md` and `docs/_planning/2026-04-23_WORKSTREAM_PLAN.md`

## RunPod Requirements

- RunPod is not required for the first execution wave.
- Mac CPU is sufficient for repo truth reconciliation, benchmark repair, and an initial larger real-corpus retrieval pass against the currently available CMU mirror/cache.
- A CPU pod becomes justified only if corpus expansion, repeated full-corpus sweeps, or disk/runtime pressure makes the Mac pass materially slower or less reproducible.
- GPU is not justified by the current execution plan.

## Execution Phases

### Phase 0: Execution entry checks

- Freeze current repo truth and ownership boundaries.
- Confirm dirty local files are not overwritten.
- Confirm HF custody target and corpus paths.

### Phase 1: Authority surface reconciliation

- Align `docs/ARCHITECTURE.md` and `docs/LEGAL_BOUNDARIES.md` to the current README/proof truth.
- Remove stale synthetic-front-door interpretation from current docs.

### Phase 2: Real-corpus retrieval benchmark repair

- Replace the stale CMU ingest path or bypass it with the already-custodied CMU mirror/cache.
- Repair benchmark design so retrieval is not measured on exact duplicate queries.
- Build a real-corpus retrieval benchmark with held-out query clips or windows.
- Emit proof artifacts for retrieval metrics, latency, corpus lineage, and non-playback boundary.

### Phase 3: Proof packaging and front-door update

- Package the new benchmark artifact bundle.
- Update repo-facing docs only to the level supported by the new proof.
- Keep rejected wedges explicitly rejected.

### Phase 4: Optional next-wave expansion

- Evaluate whether broader cross-corpus retrieval work is justified.
- Only then consider HumanML3D, Motion-X++, AMASS, or downstream retargeting work.

## Verification Gates

- Gate 1: all current-doc claims match the active proof surface
- Gate 2: retrieval benchmark uses real data and non-duplicate query methodology
- Gate 3: proof bundle includes retrieval metrics, latency, corpus lineage, and explicit non-playback boundary
- Gate 4: no repo-facing wording outruns the proof
- Gate 5: large artifacts and caches remain covered by HF custody

## End-To-End Readiness Verdict

Execution is now proven end to end for the current wedge. The lane remains deliberately narrow: real-data held-out-window retrieval/indexing is supported, while playback-grade reconstruction and semantic action retrieval are still out of scope. Mac CPU was sufficient for the implemented retrieval proof on a deterministic 24-file CMU mirror slice, and RunPod remains unnecessary for this completed wave.
