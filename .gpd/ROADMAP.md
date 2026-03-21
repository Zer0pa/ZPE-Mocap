# Roadmap: ZPE-Mocap Engineering Closure

## Overview

This roadmap drives the ZPE-Mocap inner repo toward an honest commercialization wedge. The sequence is deliberately narrow: establish the authoritative execution boundary, verify the real runtime path, build the commercial-safe adjudication path, and only then consider compute escalation if the repo-local evidence proves it is necessary.

## Phases

- [x] **Phase 1: Boundary-Normalized Capability Audit** - Verify the inner-repo authority surface, gate-script readiness, dependency state, and local execution limits.
- [x] **Phase 2: Gate M2 Runtime Evidence Path** - Execute the live runtime evidence path from the inner repo boundary and capture the resulting checkpoint state.
- [x] **Phase 3: Gate F Commercial Adjudication Path** - Map the mocap claims to commercial-safe evidence and explicit downgrade rules, then execute the adjudication path.
- [x] **Phase 4: Conditional Compute Escalation Or Closure Packaging** - Escalate only on evidenced IMP-COMPUTE, otherwise complete the closure pack from local execution.

## Phase Details

### Phase 1: Boundary-Normalized Capability Audit

**Goal:** Prove what can be executed honestly from the inner repo boundary, classify blockers, and identify the real next executable gate path.
**Depends on:** Nothing (first phase)
**Requirements:** REQ-01
**Success Criteria** (what must be TRUE):

1. The phase records the repo-local command surface for the gate scripts and identifies any path translation or environment blockers.
2. Boundary, dependency, access, storage, and compute blockers are classified from evidence instead of inferred from stale prose.
3. The phase output rejects GitHub, Comet, synthetic-only, and simulated-only status as closure proxies.

Plans:

- [x] 01-01: Restore repo-local baseline, replay Gate A and Gate B, and classify the remaining blockers.

### Phase 2: Gate M2 Runtime Evidence Path

**Goal:** Establish the live runtime evidence path for Gate M2 or the exact blocked-state logic needed to fail or downgrade it honestly.
**Depends on:** Phase 1
**Requirements:** REQ-02
**Success Criteria** (what must be TRUE):

1. Required runtime dependencies and local execution paths are identified and tested or ruled out from evidence.
2. Gate M2 success and failure signatures are grounded in repo-local commands and artifacts.
3. No simulated-only runtime evidence is promotable as a live pass.

Plans:

- [x] 02-01: Execute `gate_m2_live_runtime.py` from the repo-local environment and capture the runtime checkpoint plus USD runtime evidence.

### Phase 3: Gate F Commercial Adjudication Path

**Goal:** Establish how each final mocap claim reaches PASS, FAIL, or PAUSED_EXTERNAL under the local commercialization rules.
**Depends on:** Phase 1, Phase 2
**Requirements:** REQ-03
**Success Criteria** (what must be TRUE):

1. Each claim has a commercial-safe evidence path or a downgrade path.
2. Gate F artifacts can be interpreted without leaving any final claim INCONCLUSIVE.
3. Failures and PAUSED_EXTERNAL cases remain evidence-bound, not narrative-bound.

Plans:

- [x] 03-01: Execute the commercialization closure path across Gate M1, Gate M3, Gate M4, and Gate F with fresh repo-local artifacts.

### Phase 4: Conditional Compute Escalation Or Closure Packaging

**Goal:** Decide whether local evidence supports closure as-is or whether a user-approved compute escalation is genuinely required.
**Depends on:** Phase 1, Phase 2, Phase 3
**Requirements:** REQ-04
**Success Criteria** (what must be TRUE):

1. Any RunPod ask is backed by an explicit IMP-COMPUTE case.
2. If escalation is not needed, the closure pack can proceed from local evidence.
3. The final packaging path preserves receipt discipline and claim-status honesty.

Plans:

- [x] 04-01: Execute appendix packaging, RunPod readiness, and final Gate E closure without compute escalation.

## Progress

| Phase | Plans Complete | Status | Completed |
| ----- | -------------- | ------ | --------- |
| 1. Boundary-Normalized Capability Audit | 1/1 | Complete | 2026-03-20 |
| 2. Gate M2 Runtime Evidence Path | 1/1 | Complete | 2026-03-20 |
| 3. Gate F Commercial Adjudication Path | 1/1 | Complete | 2026-03-20 |
| 4. Conditional Compute Escalation Or Closure Packaging | 1/1 | Complete | 2026-03-20 |

### Phase 5: Refinement, performance, and evidence-hygiene augmentation

**Goal:** [To be planned]
**Depends on:** Phase 4
**Plans:** 0 plans

Plans:
- [ ] TBD (run plan-phase 5 to break down)

### Phase 6: Technical closure: real-corpus validation, Comet wiring, PyPI packaging, clean-clone verification, GitHub freshness

**Goal:** [To be planned]
**Depends on:** Phase 5
**Plans:** 0 plans

Plans:
- [ ] TBD (run plan-phase 6 to break down)
