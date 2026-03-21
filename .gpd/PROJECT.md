# ZPE-Mocap Engineering Closure

## What This Is

This project treats `/Users/Zer0pa/ZPE/ZPE Mocap/ZPE-Mocap` as the sole authority surface for the ZPE-Mocap lane. The work is not about narrating readiness from imported proofs; it is about driving the repo to an evidence-backed commercialization wedge where final claim statuses are honest, reproducible, and grounded in repo-local gate artifacts.

## Core Research Question

Can ZPE-Mocap be advanced from a boundary-confused staging repo to an evidence-backed commercialization wedge with honest final statuses for the mocap claims?

## Scoping Contract Summary

### Contract Coverage

- Boundary authority must be normalized around the inner repo rather than the outer workspace shell.
- Gate M2 must end in live runtime evidence or an explicit IMP-backed blocked state; simulated-only checks do not count.
- Gate F must produce PASS, FAIL, or PAUSED_EXTERNAL only; INCONCLUSIVE residue is failure.

### User Guidance To Preserve

- **User-stated observables:** inner-repo boundary status, Gate M2 runtime status, final claim-status map.
- **User-stated deliverables:** repo-local receipts, runtime evidence artifacts, commercialization adjudication artifacts, and a roadmap tied to real gates.
- **Must-have references / prior outputs:** the Wave-1 PRD, repo-facing truth docs, the master runbook, the Gate M2 and Gate F runbooks, the boundary sanity logs, and the Comet boundary run.
- **Stop / rethink conditions:** any regression on the commercialization authority metric, any final claim left INCONCLUSIVE, or any unapproved compute escalation.

### Scope Boundaries

**In scope**

- Inner-repo-first execution and verification.
- Local compute on Mac M1 Air and Red Magic 10 Pro+ via ADB before any escalation.
- Real gate closure work around boundary truth, runtime evidence, and commercial-safe adjudication.

**Out of scope**

- Promoting imported historical prose as current truth.
- Treating lightweight unit tests, synthetic-only results, or simulated runtime checks as commercialization closure.
- Escalating to RunPod before a real IMP-COMPUTE case is evidenced and approved.
- Editing other sector repositories or mutating the GitHub board directly.

### Active Anchor Registry

- `Ref-wave1-prd`: `/Users/Zer0pa/ZPE/ZPE Mocap/team_analysis_packet_2026-03-20/02_WAVE1_PRD.md`
  - Why it matters: defines lane claims, falsification logic, and hard gates.
  - Carry forward: planning, execution, verification, writing.
  - Required action: read, use, compare.
- `Ref-readme`: `/Users/Zer0pa/ZPE/ZPE Mocap/ZPE-Mocap/README.md`
  - Why it matters: current repo-facing truth surface and downgraded claims.
  - Carry forward: planning, execution, verification, writing.
  - Required action: read, use.
- `Ref-master-runbook`: `/Users/Zer0pa/ZPE/ZPE Mocap/ZPE-Mocap/proofs/release_readiness/2026-03-20_science_engineering_packet/08_MASTER_RUNBOOK.md`
  - Why it matters: canonical gate order, fallback logic, and commercialization discipline.
  - Carry forward: planning, execution, verification, writing.
  - Required action: read, use, compare.
- `Ref-m2`: `/Users/Zer0pa/ZPE/ZPE Mocap/ZPE-Mocap/proofs/release_readiness/2026-03-20_science_engineering_packet/09_GATE_M2_RUNTIME.md`
  - Why it matters: runtime evidence bar.
  - Carry forward: planning, execution, verification.
  - Required action: read, use, compare.
- `Ref-f`: `/Users/Zer0pa/ZPE/ZPE Mocap/ZPE-Mocap/proofs/release_readiness/2026-03-20_science_engineering_packet/10_GATE_F_COMMERCIAL.md`
  - Why it matters: commercialization finality rule.
  - Carry forward: planning, execution, verification, writing.
  - Required action: read, use, compare.

### Carry-Forward Inputs

- `proofs/logs/20260320T152557Z_boundary_context.txt`
- `proofs/logs/20260320T152557Z_boundary_sanity_tests.log`
- `proofs/logs/20260320T152557Z_comet_run.json`
- GitHub issue `#1` and the Comet boundary run as traceability surfaces only, never as closure evidence.

### Skeptical Review

- **Weakest anchor:** local hardware may still be insufficient for live runtime or commercial-safe replay.
- **Disconfirming observation:** runtime or commercial closure cannot be evidenced or downgraded honestly from the repo boundary.
- **False progress to reject:** clean docs, green unit tests, GitHub issue presence, or Comet activity presented as gate closure.

### Open Contract Questions

- Which parts of the user-provided closure brief are not yet recoverable from the local corpus?
- Which imported historical artifacts remain safe to carry forward after stale path normalization?
- Can the current lane hardware satisfy the runtime and commercialization gates without compute escalation?

## Physics Subfield

Computational motion-compression verification and evidence-bound engineering closure.

## Mathematical Framework

Threshold-based claim adjudication over deterministic codec, fidelity, search, runtime, and commercialization gates. Phase 1 focuses on command-surface and evidence-path verification rather than new analytical derivations.

## Notation Conventions

Use the existing lane claim IDs (`MOC-C001` through `MOC-C007`) and gate IDs (`A` through `F`, `M1` through `M4`, `E-G1` through `F-G2`) exactly as defined in the local runbooks.

## Unit System

Use the units already established by the lane artifacts and scripts: degrees for joint-angle RMSE, millimeters for MPJPE, milliseconds for latency, and dimensionless ratios for compression and search metrics.

## Computational Tools

- Python package under `code/src/zpe_mocap`
- Gate scripts under `code/scripts`
- Local Mac execution first
- Red Magic 10 Pro+ via ADB as a mobile/runtime adjunct if needed
- Comet for run logging only
- GitHub issue tracking for lane traceability only

## Requirements

### Validated

- Approved project contract persisted in `.gpd/state.json` on 2026-03-20.

### Active

- [ ] REQ-01: Prove the inner repo is the execution authority and classify all current boundary, dependency, and disk-space blockers from repo-local evidence.
- [ ] REQ-02: Establish an honest Gate M2 runtime path with either live evidence or explicit IMP-backed blocked-state handling.
- [ ] REQ-03: Establish a commercial-safe claim adjudication path that resolves final statuses to PASS, FAIL, or PAUSED_EXTERNAL only.
- [ ] REQ-04: Prepare a conditional compute-escalation path only if a real IMP-COMPUTE blocker is evidenced.

### Out of Scope

- Broad product polish outside evidence-bearing gate work.
- Cross-repo cleanup that does not move the authoritative closure metric.

## Key References

- `/Users/Zer0pa/ZPE/ZPE Mocap/team_analysis_packet_2026-03-20/02_WAVE1_PRD.md`
- `/Users/Zer0pa/ZPE/ZPE Mocap/ZPE-Mocap/README.md`
- `/Users/Zer0pa/ZPE/ZPE Mocap/ZPE-Mocap/AUDITOR_PLAYBOOK.md`
- `/Users/Zer0pa/ZPE/ZPE Mocap/ZPE-Mocap/PUBLIC_AUDIT_LIMITS.md`
- `/Users/Zer0pa/ZPE/ZPE Mocap/ZPE-Mocap/proofs/release_readiness/2026-03-20_science_engineering_packet/08_MASTER_RUNBOOK.md`
- `/Users/Zer0pa/ZPE/ZPE Mocap/ZPE-Mocap/proofs/release_readiness/2026-03-20_science_engineering_packet/09_GATE_M2_RUNTIME.md`
- `/Users/Zer0pa/ZPE/ZPE Mocap/ZPE-Mocap/proofs/release_readiness/2026-03-20_science_engineering_packet/10_GATE_F_COMMERCIAL.md`

## Target Publication

Not a paper-writing project. The decisive output is an honest closure pack for the repo and lane.

## Constraints

- Available disk headroom is currently tight on the host volume.
- External datasets and runtime dependencies may remain absent from the repo boundary.
- Other collaborators may act in parallel, so work must remain scoped and non-destructive.

## Key Decisions

| Decision | Rationale | Outcome |
| --- | --- | --- |
| Use recommended GPD defaults for this workstream | Keeps research, plan checking, and verification enabled without supervised pause churn | Approved |
| Treat GitHub and Comet as traceability only | Prevents proxy wins | Approved |
| Start with a boundary-and-capability phase | The gate scripts exist already; the first need is to verify what can run honestly from this repo boundary | Approved |

_Last updated: 2026-03-20 after project initialization_
