# Project Structure

**Analysis Date:** 2026-03-19

## Directory Layout

```text
[project-root]/
+-- src/zpe_mocap/                 # main reference package
+-- scripts/                       # execution gates and artifact builders
+-- tests/                         # unit-level sanity checks
+-- fixtures/                      # deterministic locked corpus input
+-- format/                        # schema definition
+-- artifacts/                     # evidence bundle and checkpoints
+-- runbooks/                      # operational and acceptance procedures
+-- ZPE-Mocap/                     # packaged mirror repo with docs/proofs/code
+-- external/                      # comparator and dataset staging area
+-- .gpd/research-map/             # generated research mapping docs
```

## Directory Purposes

**`src/zpe_mocap/`:**
- Purpose: authoritative implementation of codec, synthetic corpus, metrics, search, retarget, validation, and utility layers.
- Contains: `.py`
- Key files: `src/zpe_mocap/codec.py`, `src/zpe_mocap/benchmark.py`, `src/zpe_mocap/search.py`

**`scripts/`:**
- Purpose: gate-by-gate execution and proof packaging.
- Contains: `.py`
- Key files: `scripts/gate_c_benchmarks.py`, `scripts/gate_e_package.py`, `scripts/gate_m2_live_runtime.py`

**`tests/`:**
- Purpose: minimal sanity coverage for encode/decode thresholds and exact retrieval.
- Contains: `.py`
- Key files: `tests/test_codec.py`, `tests/test_search.py`

**`fixtures/` and `format/`:**
- Purpose: locked corpus input and schema lock.
- Contains: `.json`
- Key files: `fixtures/locked_corpus_v1.json`, `format/ZPMOC_SCHEMA_V1.json`

**`artifacts/2026-02-20_zpe_mocap_wave1/`:**
- Purpose: quantitative evidence, claim deltas, readiness contracts, and checkpoints.
- Contains: `.json`, `.md`, `.txt`
- Key files: `mocap_max_stress_benchmark.json`, `claim_status_delta.md`, `quality_gate_scorecard.json`

**`runbooks/`:**
- Purpose: execution order, hard gates, and failure signatures.
- Contains: `.md`
- Key files: `runbooks/RUNBOOK_ZPE_MOCAP_MASTER.md`, `runbooks/RUNBOOK_GATE_M2.md`, `runbooks/RUNBOOK_GATE_F.md`

**`ZPE-Mocap/`:**
- Purpose: packaged repo-facing mirror with docs, proofs, and duplicated code surface.
- Contains: `docs/`, `proofs/`, `code/`
- Key files: `ZPE-Mocap/README.md`, `ZPE-Mocap/docs/ARCHITECTURE.md`, `ZPE-Mocap/code/src/zpe_mocap/codec.py`

## Key File Locations

**Theory / Derivations:**
- `PRD_ZPE_MOCAP_SECTOR_EXPANSION_WAVE1_2026-02-20.md`: governing contract, claim matrix, and acceptance gates.
- `META_ORCHESTRATOR_MASTER_PRD_2026-03-09.md`: repo-hardening and evidence-hygiene extension of the contract.

**Computation / Numerics:**
- `src/zpe_mocap/codec.py`: encode/decode container and token transform logic.
- `src/zpe_mocap/benchmark.py`: benchmark harness and determinism hash.
- `src/zpe_mocap/search.py`: retrieval index.
- `src/zpe_mocap/synthetic.py`: synthetic corpus generator.

**Data / Results:**
- `fixtures/locked_corpus_v1.json`: locked synthetic corpus configuration.
- `artifacts/2026-02-20_zpe_mocap_wave1/`: generated evidence bundle and checkpoint trail.

**Figures / Visualization:**
- Not detected as a dedicated figure directory in the current root. Evidence is predominantly JSON/Markdown rather than plots.

**Configuration / Parameters:**
- `.env`: runtime bootstrap for external-resource attempts.
- `src/zpe_mocap/constants.py`: output root, seeds, skeleton constants, label inventory.
- `format/ZPMOC_SCHEMA_V1.json`: schema lock.

## Document Dependency Graph

**Operational Structure:**
- `runbooks/RUNBOOK_ZPE_MOCAP_MASTER.md` drives gate order and claim policy.
- `scripts/gate_a_setup.py` initializes `artifacts/2026-02-20_zpe_mocap_wave1/`.
- `scripts/gate_c_benchmarks.py` reads `src/zpe_mocap/benchmark.py` and writes core benchmark JSON.
- `scripts/gate_d_falsification.py` and `scripts/gate_m3_corpus_stress.py` extend evidence with determinism and stress outputs.
- `scripts/gate_e_package.py` consumes earlier JSON and writes claim deltas, scorecards, readiness contracts, and residual risks.
- `scripts/gate_f_commercial_closure.py` adjudicates final status vocabulary for commercialization-safe closure.

**Packaged Mirror Dependencies:**
- `ZPE-Mocap/code/` mirrors `src/`, `scripts/`, and `tests/`.
- `ZPE-Mocap/proofs/` mirrors `artifacts/` and `runbooks/`.
- `ZPE-Mocap/docs/` rewrites the truth surface for repo-facing staging.

## Naming Conventions

**Files:**
- Gate executors: `gate_[stage]_[purpose].py`
- Evidence artifacts: `mocap_[metric_or_gate].json`
- Status narratives: `*_REPORT_YYYY-MM-DD.md`, `claim_status_delta.md`

**Variables in Code:**
- Units are embedded in names: `positions_m`, `angles_deg`, `magnitudes_mm`, `p95_ms`
- Claim and gate identifiers are short uppercase IDs: `MOC-C007`, `gate_m2`

**Labels and Claims:**
- Motion classes: `walk`, `turn_left`, `turn_right`, `run`, `jump`, `punch`, `crouch`, `sidestep`, `idle`, `fall_recover`
- Claim IDs remain stable across scripts and artifacts.

## Where to Add New Content

**New Derivation / Contract Rule:**
- Contract prose: root PRD or `runbooks/`
- Packaged interpretation: `ZPE-Mocap/docs/`

**New Observable / Computation:**
- Implementation: `src/zpe_mocap/`
- Gate integration: `scripts/`
- Test: `tests/`
- Artifact output: `artifacts/2026-02-20_zpe_mocap_wave1/`

**New Dataset:**
- Raw or staged external assets: `external/`
- Locked synthetic or manifest-like config: `fixtures/`
- Traceability and adjudication: `artifacts/2026-02-20_zpe_mocap_wave1/`

**New Limiting Case / Cross-Check:**
- Operational rule: `runbooks/`
- Execution script: `scripts/`
- Evidence file: `artifacts/2026-02-20_zpe_mocap_wave1/`

## Build and Execution

**Package Installation:**

```bash
python -m pip install -e ./code
python -m pip install -e .
```

**Running Computations:**

```bash
python3 scripts/gate_c_benchmarks.py
python3 scripts/gate_m2_live_runtime.py
python3 scripts/gate_f_commercial_closure.py
```

**Running Tests:**

```bash
python -m unittest discover -s tests -v
python -m unittest discover -s code/tests -v
```

## Special Directories

**`external/`:**

- Purpose: comparator and dataset staging, including ACL and Ubisoft dataset clones.
- Generated: mixed; treated as external baseline context.
- Committed: yes in this workspace, but not the authoritative project truth surface.

**`ZPE-Mocap/`:**

- Purpose: inner packaged repo snapshot.
- Generated: partially curated by staging/hardening work.
- Committed: yes.

---

_Structure analysis: 2026-03-19_
