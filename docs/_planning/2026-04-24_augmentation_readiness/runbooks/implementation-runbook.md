# ZPE-Mocap Implementation Runbook

## Purpose

Implement only the minimum code and doc changes required to support the next real-corpus retrieval authority upgrade. This runbook is not for broad product expansion.

## Owner / Agent Type

Implementation agent with repo-local write authority and GitHub read-only posture until separately authorized.

## Input Artifacts

- `/Users/Zer0pa/ZPE/ZPE Mocap/ZPE-Mocap/code/zpe_mocap/benchmark.py`
- `/Users/Zer0pa/ZPE/ZPE Mocap/ZPE-Mocap/code/zpe_mocap/cmu.py`
- `/Users/Zer0pa/ZPE/ZPE Mocap/ZPE-Mocap/code/scripts/benchmark_cmu.py`
- `/Users/Zer0pa/ZPE/ZPE Mocap/ZPE-Mocap/code/scripts/cmu_ingest.py`
- `/Users/Zer0pa/ZPE/ZPE Mocap/ZPE-Mocap/README.md`
- `/Users/Zer0pa/ZPE/ZPE Mocap/ZPE-Mocap/docs/ARCHITECTURE.md`
- `/Users/Zer0pa/ZPE/ZPE Mocap/ZPE-Mocap/docs/LEGAL_BOUNDARIES.md`
- `/Users/Zer0pa/Status_Packets/2026-04-24_Augmentation_PRD_Readiness/lane_outputs/ZPE-Mocap/AUGMENTED_PRD.md`

## Output Artifacts

- Scoped code changes enabling honest real-corpus retrieval benchmarking
- Reconciled repo-facing docs only where justified by proof
- No branch mutation, commit, push, or PR in this runbook

## Acceptance Gate

Pass only if:

- the benchmark path can run on real corpus data without stale ingest dependence;
- the retrieval evaluation no longer leaks exact-duplicate query/library identity;
- repo-facing docs stay within the proof surface;
- implementation remains narrow and understandable.

## Failure Mode

Fail the run if:

- implementation drifts toward playback/reconstruction objectives;
- code changes require speculative architecture not needed for the benchmark;
- docs get updated before proof exists;
- local dirty-state conflicts make file ownership ambiguous.

## Mac / RunPod / HF Requirement

- Mac: required and expected to be enough.
- HF: required only for large corpus/proof custody awareness.
- RunPod: optional CPU only if local runtime or disk becomes the bottleneck.
- GPU: not required.

## Procedure

1. Resolve stale local-state ownership before editing.

   Current hazards are:

   - modified `README.md`
   - untracked `docs/_planning/`
   - branch upstream gone

   Do not overwrite these blindly.

2. Narrow the code changes.

   Target only the paths needed for:

   - real-corpus benchmark input selection;
   - split handling for non-duplicate retrieval evaluation;
   - proof artifact emission;
   - doc truth reconciliation after proof exists.

3. Prefer existing local patterns.

   Keep the retrieval surface centered on `MotionSuffixIndex` and the current token pipeline unless proof work demands a scoped extension. Do not introduce a new retrieval architecture in this execution wave.

4. Keep docs frozen until proof lands.

   `docs/ARCHITECTURE.md` and `docs/LEGAL_BOUNDARIES.md` can be reconciled to current truth early because that corrects overclaim drift. Stronger repo-front-door promotion waits until the new benchmark is complete.

5. Leave future-wave work out.

   Cross-corpus embedding models, RVQ research stacks, retarget heads, and robotics-specific extensions remain planned future work unless the current benchmark closes cleanly first.
