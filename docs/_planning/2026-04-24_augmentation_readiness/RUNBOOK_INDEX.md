# ZPE-Mocap Runbook Index

## repo-truth-and-governance-runbook.md

- Purpose: align repo-facing claims to the active authority surface and identify overclaim drift.
- Owner/agent type: repo-truth and governance agent.
- Input artifacts: README, architecture/legal docs, planning docs, proof artifacts, custody report.
- Output artifacts: scoped reconciliation task list and truth-check notes.
- Acceptance gate: current docs state retrieval/indexing truth only and do not promote playback/runtime/commercial closure beyond proof.
- Failure mode: stale or inflated claims remain on repo-facing surfaces.
- Environment: Mac required; HF read-only optional; RunPod not required.

## artifact-and-hf-custody-runbook.md

- Purpose: verify machine-loss custody for large corpora, benchmark caches, and GitHub-required copies.
- Owner/agent type: HF custody verification agent.
- Input artifacts: custody central report, local external corpora, HF dataset repo state.
- Output artifacts: custody verification note and gap list.
- Acceptance gate: authoritative HF target exists under `Zer0pa` and expected large artifacts are visible there.
- Failure mode: missing HF authority, untracked large artifacts, or namespace drift.
- Environment: Mac and HF required; RunPod not required for current lane.

## proof-and-validation-runbook.md

- Purpose: produce the next real-corpus retrieval benchmark and its proof bundle without inflating claims.
- Owner/agent type: benchmark/proof agent.
- Input artifacts: CMU fixture proof bundle, CMU mirror/cache, benchmark code, current retrieval artifacts.
- Output artifacts: new real-corpus retrieval proof bundle under `proofs/artifacts/...`.
- Acceptance gate: benchmark uses real data, non-duplicate retrieval methodology, explicit corpus lineage, and retrieval/latency outputs.
- Failure mode: exact-match benchmark leakage, stale ingest dependence, or proof that still cannot promote retrieval authority.
- Environment: Mac required; HF required for large artifact custody; RunPod CPU optional only if corpus scale demands it.

## implementation-runbook.md

- Purpose: make the minimal code changes needed to support real-corpus retrieval authority.
- Owner/agent type: implementation agent.
- Input artifacts: benchmark/proof runbook outputs, current code paths, repo governance constraints.
- Output artifacts: benchmark/ingest code changes and any doc updates justified by proof.
- Acceptance gate: code path runs from a clean procedure and produces the intended proof artifacts.
- Failure mode: changes broaden product claims, introduce duplicate logic, or depend on unverifiable corpus paths.
- Environment: Mac required; HF required for corpus access/custody; RunPod optional CPU only.

## verification-and-release-readiness-runbook.md

- Purpose: verify that implementation outputs actually close the intended authority gap and do not overclaim.
- Owner/agent type: verification/release-readiness agent.
- Input artifacts: updated code, new proof bundle, repo-facing docs, custody state.
- Output artifacts: release-readiness verdict and remaining blockers list.
- Acceptance gate: repo truth, proof truth, and custody truth all agree.
- Failure mode: mixed evidence is narrated as a pass or repo-facing docs outrun proof.
- Environment: Mac required; HF read-only required; RunPod not required.

## Execution Order

1. `repo-truth-and-governance-runbook.md`
2. `artifact-and-hf-custody-runbook.md`
3. `proof-and-validation-runbook.md`
4. `implementation-runbook.md`
5. `verification-and-release-readiness-runbook.md`
