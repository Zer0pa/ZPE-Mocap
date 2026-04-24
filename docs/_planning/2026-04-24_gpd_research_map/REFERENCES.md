# Reference and Anchor Map

**Analysis Date:** 2026-03-19

## Active Anchor Registry

| Anchor ID | Anchor | Type | Source / Locator | Why It Matters | Contract Subject IDs | Required Action | Carry Forward To |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `anchor-prd-wave1` | Wave-1 lane PRD | prior artifact | `PRD_ZPE_MOCAP_SECTOR_EXPANSION_WAVE1_2026-02-20.md` | Defines mission objective, claim matrix, hard gates, and Appendix D/E obligations | `MOC-C001..MOC-C007` | Read and preserve as governing contract | planning, execution, verification |
| `anchor-runbook-master` | Master gate runbook | method | `runbooks/RUNBOOK_ZPE_MOCAP_MASTER.md` | Defines execution order, failure signatures, determinism policy, and commercialization closure rules | `MOC-C001..MOC-C007` | Use as operational control surface | execution, verification |
| `anchor-repo-readme` | Repo reality statement | prior artifact | `ZPE-Mocap/README.md` | Distinguishes current repo truth from imported historical claims and bounds simulated/runtime surfaces |  | Read before promoting any imported evidence | planning, writing |
| `anchor-architecture-doc` | Repo architecture note | method | `ZPE-Mocap/docs/ARCHITECTURE.md` | Summarizes the code/proofs/docs split and current unresolved launch blockers |  | Keep visible when planning new implementation or staging work | planning, execution |
| `anchor-core-benchmarks` | Core benchmark outputs | benchmark | `artifacts/2026-02-20_zpe_mocap_wave1/mocap_compression_benchmark.json`; `mocap_joint_fidelity.json`; `mocap_position_fidelity.json`; `mocap_search_eval.json`; `mocap_query_latency.json`; `mocap_retarget_eval.json` | Primary evidence for Wave-1 quantitative claims | `MOC-C001..MOC-C006` | Compare against new runs; do not narrate around regressions | verification, writing |
| `anchor-runtime-artifacts` | Runtime compatibility record | benchmark | `artifacts/2026-02-20_zpe_mocap_wave1/mocap_blender_roundtrip.json`; `usd_live_runtime_check.json`; `integration_readiness_contract.json` | Shows the tension between simulated adapter success and incomplete live runtime proof | `MOC-C007` | Treat as bounded evidence, not clean live-runtime closure | verification, writing |
| `anchor-traceability` | Resource traceability bundle | background | `artifacts/2026-02-20_zpe_mocap_wave1/concept_resource_traceability.json`; `concept_open_questions_resolution.md`; `residual_risk_register.md` | Tracks proxy substitutions, external comparators, and unresolved license/access gaps | `MOC-C001..MOC-C007` | Preserve substitutions and claim-impact mapping | planning, verification |
| `anchor-claim-delta` | Claim promotion surface | prior artifact | `artifacts/2026-02-20_zpe_mocap_wave1/claim_status_delta.md`; `commercialization_claim_adjudication.json` | Records how claims moved from `UNTESTED` and which statuses remain bounded by external constraints | `MOC-C001..MOC-C007` | Reconcile before any future handoff | verification, writing |
| `anchor-acl-baseline` | ACL comparator baseline | benchmark | `external/acl/README.md`; `artifacts/2026-02-20_zpe_mocap_wave1/acl_direct_comparator_table.json` | External compression baseline and direct comparator attempt surface | `MOC-C001` | Use only with same-corpus caveats and explicit comparability bounds | planning, verification |
| `anchor-dataset-baselines` | External dataset and DCC references | background | `artifacts/2026-02-20_zpe_mocap_wave1/concept_resource_traceability.json` | Names LAFAN1, CMU, Mixamo, bvhio, usdBVHAnim, and MoMa as required comparison or closure anchors | `MOC-C001`, `MOC-C003`, `MOC-C006`, `MOC-C007` | Keep visible for future gap-closing phases | planning, research |

## Benchmarks and Comparison Targets

- Compression ratio against raw BVH float32 and ACL baseline.
  - Source: `PRD_ZPE_MOCAP_SECTOR_EXPANSION_WAVE1_2026-02-20.md`, `artifacts/2026-02-20_zpe_mocap_wave1/mocap_compression_benchmark.json`
  - Compared in: `src/zpe_mocap/benchmark.py`
  - Status: matched for synthetic proxy corpus; direct ACL parity remains bounded
- Joint-angle RMSE, MPJPE, search P@10, search latency, and retarget MPJPE thresholds.
  - Source: `PRD_ZPE_MOCAP_SECTOR_EXPANSION_WAVE1_2026-02-20.md`
  - Compared in: `scripts/gate_c_benchmarks.py`, `artifacts/2026-02-20_zpe_mocap_wave1/`
  - Status: matched on current synthetic artifacts
- Blender/USD runtime readiness.
  - Source: `scripts/gate_m2_live_runtime.py`, `artifacts/2026-02-20_zpe_mocap_wave1/mocap_blender_roundtrip.json`
  - Compared in: max-wave runtime gate
  - Status: contested because simulated adapter success coexists with absent Blender runtime

## Prior Artifacts and Baselines

- `artifacts/2026-02-20_zpe_mocap_wave1/mocap_max_stress_benchmark.json`: stress replay bundle used to keep max-wave claims visible.
- `artifacts/2026-02-20_zpe_mocap_wave1/runpod_readiness_manifest.json`: escalation path for `IMP-COMPUTE` scenarios.
- `META_ORCHESTRATOR_MASTER_PRD_2026-03-09.md`: repo-hardening contract that explicitly forbids promoting simulated claims as runtime truth.
- `PHASE_4_5_HANDOFF_2026-03-09.md`: handoff note that captures blind-clone, runtime, and stale-path caveats.

## Open Reference Questions

- Which artifact should be treated as the single authoritative claim-status surface when root and packaged proof copies disagree?
- Is there a direct ACL same-corpus run that can replace literature-only comparison without proxy caveats?
- Which future artifact should supersede the current simulated `mocap_blender_roundtrip.json` record with true live-runtime proof?
- What commercial-safe external dataset closes the CMU/LAFAN1/Mixamo/BABEL/RELI11D gaps without leaving `PAUSED_EXTERNAL` residue?

## Background Reading

- `external/acl/docs/error_metrics.md`: useful for incumbent-comparator framing, but not currently the repo’s governing truth surface.
- `ZPE-Mocap/AUDITOR_PLAYBOOK.md`: current repo-facing reading guide for evidence hygiene and public-audit boundaries.
- `ZPE-Mocap/PUBLIC_AUDIT_LIMITS.md`: explains lineage preservation and why stale imported claims are not authoritative.

---

_Reference map: 2026-03-19_
