# Research Gaps and Open Issues

**Analysis Date:** 2026-03-19

## Incomplete Closure Paths

**Live Runtime Closure:**
- What exists: simulated adapter roundtrip plus runtime probing logic.
- What's missing: clean live Blender-backed proof that can close `MOC-C007` without qualification.
- Files: `src/zpe_mocap/adapters.py`, `scripts/gate_m2_live_runtime.py`, `artifacts/2026-02-20_zpe_mocap_wave1/mocap_blender_roundtrip.json`
- Impact: runtime and integration-readiness claims remain bounded.
- Difficulty estimate: Moderate

**Comparator Closure:**
- What exists: ACL literature baseline and a direct comparator artifact surface.
- What's missing: unambiguous same-corpus direct comparator evidence accepted by the current repo truth surface.
- Files: `src/zpe_mocap/benchmark.py`, `artifacts/2026-02-20_zpe_mocap_wave1/acl_direct_comparator_table.json`, `concept_resource_traceability.json`
- Impact: compression superiority/parity framing stays partial.
- Difficulty estimate: Moderate

## Unchecked Limits

**Real-Corpus Generalization:**
- Limit: move from locked synthetic corpus to real BVH/FBX/dataset-backed motion libraries.
- Expected behavior: thresholds should remain within claim gates or claims must be downgraded.
- Current status: Partially checked only through proxy substitutions.
- Files: `fixtures/locked_corpus_v1.json`, `artifacts/2026-02-20_zpe_mocap_wave1/concept_resource_traceability.json`
- Why it matters: the governing authority metric should survive beyond synthetic motion.

**Clean Clone Boundary:**
- Limit: rerun from a fresh repo boundary rather than inherited workspace state.
- Expected behavior: install, tests, and gate commands should succeed with the same evidence conclusions.
- Current status: Not checked.
- Files: `ZPE-Mocap/README.md`, `PHASE_4_5_HANDOFF_2026-03-09.md`
- Why it matters: staging and external audit readiness depend on boundary-clean reproducibility.

## Unjustified Approximations

**Simulated Adapter Success as Runtime Proxy:**
- Where used: `src/zpe_mocap/adapters.py`, `scripts/gate_m2_live_runtime.py`
- Justification status: Numerical evidence only for the surrogate path
- What could go wrong: live Blender or USD integration could fail despite simulated roundtrip passing
- How to justify: run actual Blender/USD roundtrip in a fresh environment and preserve command evidence
- Priority: High

**Synthetic Corpus as Commercialization Proxy:**
- Where used: `src/zpe_mocap/synthetic.py`, `scripts/gate_c_benchmarks.py`
- Justification status: Partial proof
- What could go wrong: claim thresholds and latency may not transfer to real motion diversity
- How to justify: execute dataset-backed replay with explicit legal/commercial adjudication
- Priority: High

## Missing Cross-Checks

**Root vs Packaged Mirror Drift Check:**
- What to verify: root code/artifacts and `ZPE-Mocap/` mirror remain identical where intended
- Method: hash or diff mirrored code and proof trees
- Expected outcome: no silent drift between authoritative and packaged surfaces
- Files to modify: `src/`, `artifacts/`, `ZPE-Mocap/code/`, `ZPE-Mocap/proofs/`
- Priority: High

**Artifact Status Consistency Check:**
- What to verify: `PASS` labels never outrun the caveats recorded in runtime and resource artifacts
- Method: scan packaged/public surfaces against `integration_readiness_contract.json`, `claim_status_delta.md`, and `commercialization_claim_adjudication.json`
- Expected outcome: no simulated-only result is presented as live truth
- Files to modify: `ZPE-Mocap/README.md`, `ZPE-Mocap/docs/`, root reports
- Priority: High

## Numerical Concerns

**Latency Representativeness:**
- Problem: `query_latency_p95_ms` is measured on deterministic synthetic token streams and may understate real-library variance.
- Files: `src/zpe_mocap/benchmark.py`, `artifacts/2026-02-20_zpe_mocap_wave1/mocap_query_latency.json`
- Symptoms: latency regression on heterogeneous corpora or different hardware.
- Resolution: add corpus-diversity and hardware-note stratification to latency evidence.

## Project Consistency Issues

**Simulated vs Ready Tension:**
- Concern: `integration_readiness_contract.json` can read stronger than the underlying runtime caveat because compatibility fields remain simulated while some max-wave gates are marked `PASS`.
- Files: `artifacts/2026-02-20_zpe_mocap_wave1/integration_readiness_contract.json`, `mocap_blender_roundtrip.json`
- Impact: users can mistake bounded compatibility for proven live integration.
- Resolution path: downgrade wording or replace with live-runtime proof.

## Missing Generalizations

**Real Dataset and DCC Coverage:**
- Current scope: synthetic corpus, simulated adapters, bounded external references.
- Natural extension: real BVH/FBX ingest, CMU/LAFAN1/BABEL-backed replay, and live Blender/USD closure.
- Difficulty: Hard
- Blocks: commercialization-safe launch claims and stronger external benchmarking.

## Documentation Gaps

**Authoritative Surface Ambiguity:**
- What's undocumented: explicit rule for which duplicate file wins when root and packaged mirror drift.
- Files: root reports, `ZPE-Mocap/README.md`
- Impact: future agents can select stale or secondary truth surfaces.

## Stale or Dead Content

**Imported Historical Paths and PASS Language:**
- What: imported reports preserve absolute machine paths and some overstated historical phrasing by design.
- Files: `REPO_HARDENING_REPORT_2026-03-09.md`, `PHASE_4_5_HANDOFF_2026-03-09.md`, `ZPE-Mocap/proofs/README.md`
- Action: keep archived, but do not promote as current authority without repo-facing reinterpretation.
- Risk: future planning can pick the wrong evidence layer.

## Missing Literature Connections

**Comparator and Dataset Closure Sources:**
- What: exact same-corpus ACL comparator methodology and commercial-safe external dataset adjudication still need a final authoritative crosswalk.
- Why relevant: they govern whether current synthetic `PASS` results survive maximalization and commercialization gates.
- Priority: High

## Placeholder and Stub Content

**No Live Blender Binary Path:**
- What: runtime gate records `blender binary not found` while keeping simulated adapter artifacts in play.
- Files: `scripts/gate_m2_live_runtime.py`, `artifacts/2026-02-20_zpe_mocap_wave1/mocap_blender_roundtrip.json`
- Needed for: true closure of `MOC-C007`

## Priority Ranking

**Critical (blocks correctness):**
1. Live runtime evidence is still simulated or unavailable while related readiness surfaces can be read as stronger than that caveat.
2. Real-corpus generalization and same-corpus comparator closure are not fully re-proven from the current repo boundary.

**High (blocks completeness):**
1. Root and packaged mirror duplication can drift silently.
2. Clean-clone verification from the repo boundary has not been run.
3. External dataset/commercial-safe closure remains dependent on partial or paused evidence.

**Medium (improves quality):**
1. Latency evidence needs broader corpus and hardware context.
2. Repo docs should explicitly state the precedence rule between root and packaged mirrors.

**Low (nice to have):**
1. Add figure or dashboard surfaces so evidence bundles are easier to inspect without reading raw JSON.

---

_Gap analysis: 2026-03-19_
