# ZPE-Mocap Verification And Release Readiness Runbook

## Purpose

Verify that the lane's execution outputs actually strengthen the authority surface and that repo-facing claims remain honest. This runbook decides whether the lane can be described as execution-complete for the wave.

## Owner / Agent Type

Verification and release-readiness agent.

## Input Artifacts

- New proof bundle produced by the benchmark run
- Updated benchmark code and scripts
- `/Users/Zer0pa/ZPE/ZPE Mocap/ZPE-Mocap/README.md`
- `/Users/Zer0pa/ZPE/ZPE Mocap/ZPE-Mocap/docs/ARCHITECTURE.md`
- `/Users/Zer0pa/ZPE/ZPE Mocap/ZPE-Mocap/docs/LEGAL_BOUNDARIES.md`
- `/Users/Zer0pa/Status_Packets/2026-04-24_HF_Custody_Central_Report/lane_reports/ZPE-Mocap_HF_CUSTODY_REPORT.md`

## Output Artifacts

- Release-readiness verdict
- Remaining blocker list
- Verification notes pointing at exact proof paths and claim boundaries

## Acceptance Gate

Pass only if:

- repo truth, proof truth, and custody truth align;
- the new benchmark materially improves real retrieval authority;
- synthetic retrieval no longer stands as the headline retrieval proof;
- playback/reconstruction remains explicitly unsupported unless separately proven;
- large artifacts remain recoverable through HF custody.

## Failure Mode

Fail the run if:

- mixed evidence is narrated as a pass;
- new proof is real-data in name only but still exact-match or fixture-bound in practice;
- repo docs outrun the new artifact set;
- custody or branch-state hazards make the release irreproducible.

## Mac / RunPod / HF Requirement

- Mac: required.
- HF: read-only verification required.
- RunPod: not required unless the proof itself was produced there.
- GPU: not required.

## Procedure

1. Re-read the new proof bundle before any verdict.

   Confirm the benchmark scope, split methodology, retrieval metrics, latency metrics, and stated limitations.

2. Compare the repo front door to the proof.

   Check whether `README.md`, `docs/ARCHITECTURE.md`, and `docs/LEGAL_BOUNDARIES.md` all tell the same truth.

3. Re-check custody.

   Confirm the large corpus/proof surfaces are either in GitHub because they are small enough, or in the authoritative HF repo because they are large.

4. Issue a strict verdict.

   Use the smallest truthful verdict. If the lane still only supports retrieval/indexing partially, keep it `PARTIAL`.

5. Record remaining blockers instead of smoothing them over.

   Any unresolved branch-state, corpus-lineage, or claim-boundary issue must remain visible in the final report.
