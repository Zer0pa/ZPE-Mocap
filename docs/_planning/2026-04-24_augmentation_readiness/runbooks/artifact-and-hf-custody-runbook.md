# ZPE-Mocap Artifact And HF Custody Runbook

## Purpose

Define the custody verification procedure for ZPE-Mocap augmentation PRD readiness. This runbook verifies where large external corpora, benchmark caches, and GitHub-required copies are held. It is a read-only verification pass: do not upload to Hugging Face, mutate GitHub, or claim playback/runtime readiness.

## Owner / Agent Type

Artifact custody agent with local filesystem and HF read-only inspection authority. The agent reports custody gaps and machine-loss risk, but does not perform uploads or deletes without a separate explicit authorization.

## Input Artifacts

- `/Users/Zer0pa/Status_Packets/2026-04-24_HF_Custody_Central_Report/lane_reports/ZPE-Mocap_HF_CUSTODY_REPORT.md`
- `/Users/Zer0pa/Status_Packets/2026-04-24_HF_Custody_Central_Report/STATUS_ROLLUP.md`
- `/Users/Zer0pa/Status_Packets/2026-04-24_HF_Custody_Central_Report/LANE_GAP_BRIEFS.md`
- `/Users/Zer0pa/ZPE/ZPE Mocap/ZPE-Mocap/README.md`
- `/Users/Zer0pa/ZPE/ZPE Mocap/ZPE-Mocap/docs/_planning/2026-04-23_WORKSTREAM_PLAN.md`
- `/Users/Zer0pa/ZPE/ZPE Mocap/external/cmu_github_mirror/`
- `/Users/Zer0pa/ZPE/ZPE Mocap/external/cmu_phase3_benchmark_cache/`
- HF dataset repo: `Zer0pa/ZPE-Mocap-artifacts`
- Non-authoritative legacy HF namespace to avoid: `Architect-Prime/ZPE-Mocap-artifacts`

## Output Artifacts

- Custody verification note for the PRD readiness packet, if requested by the coordinator.
- A read-only evidence log containing local paths, HF repo identity, dry-run counts, and any missing expected paths.
- A gap list for later authorized upload or GitHub commit work.
- No uploaded files, no deleted files, no GitHub commit, and no changed HF repo state.

## Acceptance Gate

Pass only if read-only checks confirm the central custody report's ZPE-Mocap position:

- Authoritative HF dataset repo is private `Zer0pa/ZPE-Mocap-artifacts`.
- Live repo SHA recorded in the custody report is `f1e6548c7ad8827b9b579b519c785689962afab9`, unless a newer authorized custody pass supersedes it.
- Expected HF paths include `external/cmu_github_mirror/`, `external/cmu_phase3_benchmark_cache/`, `github-required/README.md`, and `github-required/docs/_planning/2026-04-23_WORKSTREAM_PLAN.md`.
- Dry-run scope remains consistent with the custody report's `136` files and `166.5M` total for the listed include paths, allowing only clearly explained upstream-authorized drift.
- No ZPE-Mocap model repo, checkpoint upload, bucket upload, or RunPod salvage path is required by current evidence.
- GitHub-required files have HF custody copies but still need a later human GitHub branch/commit decision.

## Failure Mode

Fail and escalate if any of the following occur:

- The authoritative HF repo is missing, public when expected private, inaccessible, or under the wrong namespace.
- Expected CMU cache or `github-required` paths are absent from HF dry-run output.
- A local large artifact, benchmark cache, proof bundle, model checkpoint, or RunPod salvage path is found with no HF or repo custody copy.
- A model file appears locally (`.pt`, `.pth`, `.ckpt`, `.safetensors`, `.onnx`) without a documented custody target.
- The procedure would require an upload, delete, repo rename, commit, or push to reach closure.

Do not convert a custody gap into a pass narrative. Record the gap and stop for authorization.

## Mac / RunPod / HF Requirement

- Mac: required for local path inspection and comparison to the custody report.
- HF: required for read-only `hf datasets info` and `hf download --dry-run` verification. No upload, delete, or metadata mutation.
- RunPod: not required. The central custody report says pod `7k3riasglemecu` was inspected read-only and no ZPE-Mocap/CMU lane artifact path was found beyond unrelated system/package paths.
- GitHub: not required for this pass. GitHub remains read-only; later commit/push work needs a human decision because the local upstream branch is gone.

## Step-By-Step Procedure

1. Read the ZPE-Mocap custody report first.

   ```bash
   sed -n '1,220p' /Users/Zer0pa/Status_Packets/2026-04-24_HF_Custody_Central_Report/lane_reports/ZPE-Mocap_HF_CUSTODY_REPORT.md
   ```

   Treat this report as the starting custody ledger, not as permission to upload.

2. Confirm local repo and large external paths exist.

   ```bash
   test -d "/Users/Zer0pa/ZPE/ZPE Mocap/ZPE-Mocap" && echo "repo present"
   test -d "/Users/Zer0pa/ZPE/ZPE Mocap/external/cmu_github_mirror" && echo "cmu_github_mirror present"
   test -d "/Users/Zer0pa/ZPE/ZPE Mocap/external/cmu_phase3_benchmark_cache" && echo "cmu_phase3_benchmark_cache present"
   find "/Users/Zer0pa/ZPE/ZPE Mocap/external/cmu_github_mirror" -type f | wc -l
   find "/Users/Zer0pa/ZPE/ZPE Mocap/external/cmu_phase3_benchmark_cache" -type f | wc -l
   ```

   If either local path is absent, do not mark failure automatically; compare against HF custody and record the observed state.

3. Search locally for model/checkpoint files.

   ```bash
   find "/Users/Zer0pa/ZPE/ZPE Mocap/ZPE-Mocap" "/Users/Zer0pa/ZPE/ZPE Mocap/external" \
     -type f \( -name '*.pt' -o -name '*.pth' -o -name '*.ckpt' -o -name '*.safetensors' -o -name '*.onnx' \) \
     -print
   ```

   The expected result for this lane is no model/checkpoint custody need. Any hit becomes a custody gap until assigned a target.

4. Verify HF identity read-only.

   ```bash
   hf auth whoami
   hf datasets info Zer0pa/ZPE-Mocap-artifacts
   ```

   Record the authenticated user/orgs and repo visibility/SHA. Do not run `hf upload`, `hf repo delete`, or any metadata-mutating command.

5. Verify expected HF paths with dry-run only.

   ```bash
   hf download Zer0pa/ZPE-Mocap-artifacts \
     --repo-type dataset \
     --dry-run \
     --include 'external/cmu_github_mirror/**' \
     --include 'external/cmu_phase3_benchmark_cache/**' \
     --include 'github-required/**'
   ```

   Record file count, total size, and representative expected paths. The custody report baseline is `136` files totaling `166.5M`.

6. Confirm the wrong namespace is non-authoritative.

   ```bash
   hf datasets info Architect-Prime/ZPE-Mocap-artifacts
   ```

   This command may fail depending on permissions. Whether it succeeds or fails, do not use this namespace as the ZPE-Mocap authority. The authoritative target remains `Zer0pa/ZPE-Mocap-artifacts`.

7. Confirm GitHub-required copies are custody copies, not GitHub closure.

   ```bash
   hf download Zer0pa/ZPE-Mocap-artifacts \
     --repo-type dataset \
     --dry-run \
     --include 'github-required/README.md' \
     --include 'github-required/docs/_planning/2026-04-23_WORKSTREAM_PLAN.md'
   ```

   Record that these copies reduce machine-loss risk but do not replace a later GitHub commit/push decision.

8. Classify custody state.

   Use these statuses:

   - `CUSTODY_CONFIRMED`: local and HF evidence match the central report.
   - `NO_MODEL_NEEDED`: no model/checkpoint files found.
   - `NO_RUNPOD_REQUIRED`: no lane RunPod salvage path is required.
   - `GITHUB_DECISION_PENDING`: small docs have HF custody copies but GitHub is still the authority.
   - `CUSTODY_GAP`: an artifact exists without confirmed custody.

9. Stop before mutation.

   If a gap is found, write the missing source path, proposed target, size, and risk. Do not upload or delete anything during this pass.

## Evidence To Record

- Timestamp and machine path where checks ran.
- `hf auth whoami` result, including user/org context.
- `hf datasets info Zer0pa/ZPE-Mocap-artifacts` result, including privacy state and SHA.
- Dry-run file count and total size for `external/cmu_github_mirror/**`, `external/cmu_phase3_benchmark_cache/**`, and `github-required/**`.
- Representative verified HF paths: `external/cmu_github_mirror/`, `external/cmu_phase3_benchmark_cache/`, `github-required/README.md`, `github-required/docs/_planning/2026-04-23_WORKSTREAM_PLAN.md`.
- Local counts for the two CMU external directories.
- Model/checkpoint search result.
- Explicit statement that no HF upload, HF delete, GitHub mutation, or RunPod mutation was performed.
- Any custody gap with exact local path, expected target, current risk, and required authorization.
