# ZPE-Mocap Repo Truth And Governance Runbook

## Purpose

Establish the repo-truth procedure for the ZPE-Mocap augmentation PRD readiness pass. This runbook keeps the public lane posture bounded to the current authority metric: deterministic BVH motion fingerprinting for search, indexing, and retrieval. It must not promote playback-quality pose reconstruction, Blender/runtime closure, clean-clone closure, or full commercialization-safe closure unless fresh artifact-backed proof exists.

## Owner / Agent Type

Repo-truth and governance agent with read-only GitHub posture. The agent may inspect the local repo and draft readiness evidence. The agent must not mutate GitHub, push commits, upload artifacts, or overwrite another agent's edits.

## Input Artifacts

- `/Users/Zer0pa/ZPE/ZPE Mocap/ZPE-Mocap/README.md`
- `/Users/Zer0pa/ZPE/ZPE Mocap/ZPE-Mocap/docs/LEGAL_BOUNDARIES.md`
- `/Users/Zer0pa/ZPE/ZPE Mocap/ZPE-Mocap/docs/ARCHITECTURE.md`
- `/Users/Zer0pa/ZPE/ZPE Mocap/ZPE-Mocap/docs/_planning/2026-04-23_WORKSTREAM_PLAN.md`
- `/Users/Zer0pa/ZPE/ZPE Mocap/ZPE-Mocap/code/README.md`
- `/Users/Zer0pa/ZPE/ZPE Mocap/ZPE-Mocap/proofs/artifacts/2026-04-14_cmu_corpus_benchmark/results.json`
- `/Users/Zer0pa/ZPE/ZPE Mocap/ZPE-Mocap/proofs/artifacts/2026-04-14_cmu_corpus_benchmark/summary.md`
- `/Users/Zer0pa/ZPE/ZPE Mocap/ZPE-Mocap/proofs/artifacts/2026-02-20_zpe_mocap_wave1/mocap_search_eval.json`
- `/Users/Zer0pa/ZPE/ZPE Mocap/ZPE-Mocap/proofs/artifacts/2026-02-20_zpe_mocap_wave1/mocap_query_latency.json`
- `/Users/Zer0pa/ZPE/ZPE Mocap/ZPE-Mocap/proofs/artifacts/2026-02-20_zpe_mocap_wave1/quality_gate_scorecard.json`
- `/Users/Zer0pa/Status_Packets/2026-04-24_HF_Custody_Central_Report/lane_reports/ZPE-Mocap_HF_CUSTODY_REPORT.md`

## Output Artifacts

- A repo-truth readiness note or checklist in the PRD readiness packet, if requested by the coordinator.
- A list of exact file paths and line references that need later repo cleanup.
- No GitHub commit, no branch mutation, no upload, and no proof rewrite during this runbook unless separately authorized.

## Acceptance Gate

Pass only if all reviewed repo-facing claims are consistent with the current authority surface:

- Current real-data authority is `/Users/Zer0pa/ZPE/ZPE Mocap/ZPE-Mocap/proofs/artifacts/2026-04-14_cmu_corpus_benchmark/`.
- Promoted metrics remain `18.77x` mean bandwidth reduction, `32.45 mm` mean MPJPE, and `82.51 deg` mean joint-angle RMSE across the committed 10-clip CMU fixture corpus.
- Public interpretation is retrieval/indexing only, no playback-quality reconstruction.
- Synthetic evidence may be retained as historical ceiling/search evidence, not the commercial front door.
- Any contradiction in repo docs is recorded as a blocker, not narrated as a pass.

## Failure Mode

Fail the run if any repo-facing surface promotes one of these without fresh proof:

- playback-quality pose reconstruction;
- real-data parity with the synthetic benchmark bundle;
- fair commercial ACL comparator status from the synthetic table;
- Blender runtime closure;
- clean-clone verification;
- broad commercialization-safe closure;
- full CMU mirror authority when only the 10-clip fixture corpus is proven.

If mixed evidence appears, preserve the stricter interpretation and record the contradiction. Do not soften the failure by relying on unrelated secondary wins.

## Mac / RunPod / HF Requirement

- Mac: required for local repo inspection and command output capture.
- RunPod: not required for this governance pass.
- HF: read-only verification only if needed to compare custody copies. Do not upload, delete, or mutate any HF repo.
- GitHub: read-only only. The custody report says the local branch `chore/novelty-card-backfill-2026-04-22` has a gone upstream and needs human decision before later GitHub work.

## Step-By-Step Procedure

1. Confirm local scope.

   ```bash
   cd "/Users/Zer0pa/ZPE/ZPE Mocap/ZPE-Mocap"
   pwd
   git status --short
   git branch --show-current
   ```

   Treat any dirty files as other agents' work unless explicitly assigned. Do not revert them.

2. Re-read the current authority surface.

   ```bash
   sed -n '1,140p' README.md
   sed -n '1,120p' proofs/artifacts/2026-04-14_cmu_corpus_benchmark/summary.md
   python3 -m json.tool proofs/artifacts/2026-04-14_cmu_corpus_benchmark/results.json | sed -n '1,80p'
   ```

   Record the authority metrics exactly. Keep the limitation visible: external ingest failed with `HTTP Error 404: Not Found`, so the authority corpus is the committed 10-clip fixture set.

3. Inspect repo-facing docs for stale or inflated claims.

   ```bash
   rg -n "playback|runtime|Blender|commercialization-safe|clean-clone|synthetic|CMU|fixture|retrieval|indexing|ACL|parity" README.md docs code/README.md proofs -g '*.md' -g '*.json' -g '*.txt'
   ```

   Separate current interpretation docs from historical artifacts. Historical artifacts can retain lineage text, but current docs cannot promote stale interpretations.

4. Check the package surface boundary.

   ```bash
   sed -n '1,140p' code/README.md
   rg -n "README.md remains|proof authority|public Python surface|MotionSuffixIndex" code/README.md code/zpe_mocap
   ```

   Confirm package API claims are smaller than repo-level proof claims and that `MotionSuffixIndex` remains a retrieval/indexing surface.

5. Check legal and evidence boundaries.

   ```bash
   sed -n '1,140p' docs/LEGAL_BOUNDARIES.md
   ```

   Verify that external corpus clones, ACL build outputs, virtual environments, credentials, and other external material remain outside the tracked repo unless imported with lineage and license review.

6. Classify each finding.

   Use these statuses:

   - `PASS`: wording matches the current authority surface.
   - `BLOCKER`: current repo-facing wording overclaims or contradicts the authority metric.
   - `HISTORICAL_LINEAGE`: old proof artifact text is preserved but not promoted.
   - `NEEDS_HUMAN_DECISION`: branch/upstream or product-scope decision is required.

7. Stop before mutation.

   If edits are required, produce a scoped change list and stop unless the coordinator explicitly authorizes repo edits. Do not update handover docs to say the gate passed while any `BLOCKER` remains.

## Evidence To Record

- Current branch and `git status --short` output.
- The exact authority artifact paths inspected.
- The current authority metrics: `18.77232014335372x` mean compression ratio vs raw BVH float32, `32.45230144481235 mm` mean MPJPE, `82.51017542212895 deg` mean joint-angle RMSE, 10 selected CMU fixture clips.
- Synthetic-only support metrics, clearly labeled: `p@10 = 1.0` over 120 queries and query latency `p95 = 26.137510099943025 ms`.
- Any stale claim with file path, line number, quoted short phrase, and corrected interpretation.
- Confirmation that no GitHub mutation, upload, or artifact rewrite was performed.
