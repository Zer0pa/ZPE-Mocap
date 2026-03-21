# Phase 1 Research: Boundary-Normalized Capability Audit

## Objective

Determine what can be executed honestly from the inner repo boundary at `/Users/Zer0pa/ZPE/ZPE Mocap/ZPE-Mocap`, classify the real blockers by type, and identify the next executable gate path without relying on stale workspace prose or proxy success surfaces.

## Sources Read

- `.gpd/PROJECT.md`
- `.gpd/ROADMAP.md`
- `.gpd/REQUIREMENTS.md`
- `.gpd/phases/01-boundary-normalized-capability-audit/01-CONTEXT.md`
- `README.md`
- `AUDITOR_PLAYBOOK.md`
- `PUBLIC_AUDIT_LIMITS.md`
- `proofs/release_readiness/2026-03-20_science_engineering_packet/08_MASTER_RUNBOOK.md`
- `proofs/release_readiness/2026-03-20_science_engineering_packet/09_GATE_M2_RUNTIME.md`
- `proofs/release_readiness/2026-03-20_science_engineering_packet/10_GATE_F_COMMERCIAL.md`
- `team_analysis_packet_2026-03-20/02_WAVE1_PRD.md`
- `code/scripts/_common.py`
- `code/scripts/gate_a_setup.py`
- `code/scripts/gate_b_build.py`
- `code/scripts/gate_c_benchmarks.py`
- `code/scripts/gate_d_falsification.py`
- `code/scripts/gate_e_runpod_readiness.py`
- `code/scripts/gate_f_commercial_closure.py`
- `code/scripts/gate_m2_live_runtime.py`
- `code/pyproject.toml`

## Hard Probes Run On 2026-03-20

### Environment And Tooling

- `df -h .`
  - Host volume has about `4.6 GiB` free. Disk pressure is real but not yet a blocker for small local dependency installs.
- `which adb`
  - Present at `/usr/local/bin/adb`.
- `which cmake`
  - Present at `/usr/local/bin/cmake`.
- `which git`
  - Present at `/opt/homebrew/bin/git`.
- `which blender`
  - Not found.
- `.env`
  - Missing from the repo root.
- `.venv`
  - Missing from the repo root.

### Python Capability

- `python3 --version`
  - `Python 3.14.0`
- `python3 -c "import numpy"`
  - Fails with `ModuleNotFoundError`.
- `python3 -c "from pxr import Usd"`
  - Fails with `ModuleNotFoundError`.
- `python3 -m unittest discover -s code/tests -v`
  - Fails immediately because `numpy` is missing.

## Current Executable Command Surface

The repo already contains the expected gate scripts under `code/scripts`:

- `gate_a_setup.py`
- `gate_b_build.py`
- `gate_c_benchmarks.py`
- `gate_d_falsification.py`
- `gate_e_appendix_ingestion.py`
- `gate_e_package.py`
- `gate_e_runpod_readiness.py`
- `gate_f_commercial_closure.py`
- `gate_m1_acl_comparator.py`
- `gate_m2_live_runtime.py`
- `gate_m3_corpus_stress.py`
- `gate_m4_replay_core_claims.py`

Important implementation detail:

- The scripts are written against the repo boundary, not the old outer-workspace layout.
- `_common.py` injects `code/src` into `sys.path`, so the scripts do not require an editable install to find the package.
- This does **not** remove dependency requirements: `numpy` is still required for most gates.

## Boundary Normalization Findings

### What Is Clean

- The inner repo remote and branch are already correct for `https://github.com/Zer0pa/ZPE-Mocap`.
- Repo-facing docs correctly downgrade historical claims and explicitly refuse to promote live runtime or commercial-safe closure prematurely.
- The output root is already normalized to `proofs/artifacts/2026-02-20_zpe_mocap_wave1`.

### What Is Still Mixed

- The outer workspace is still nested under a different parent git repo, so repo-local truth must keep outranking outer-shell history.
- Imported runbook content still carries translated historical paths and older assumptions.
- Earlier sanity claims are environment-specific: on the current 2026-03-20 machine state, the tests do **not** pass because `numpy` is absent.

### Governing Interpretation

- The boundary question is no longer “does code exist?” It is “what can this machine execute honestly from the repo boundary right now?”
- That means Phase 1 must classify environment drift and dependency drift as first-class blockers, not treat them as incidental setup noise.

## Gate-By-Gate Blocker Classification

### Gate A (`gate_a_setup.py`)

- **Readiness:** Near-ready.
- **Why:** Uses stdlib only plus repo-local schema and fixture writes.
- **Likely blocker class:** None currently visible.
- **Risk:** Low.
- **Value:** High first-step command because it establishes fixture lock and checkpoint surfaces cheaply.

### Gate B (`gate_b_build.py`)

- **Readiness:** Blocked.
- **Immediate blocker:** `numpy` missing.
- **Blocker class:** Dependency drift.
- **Secondary risk:** No repo `.venv`; execution currently depends on system Python state.
- **Value:** High. It is the smallest real smoke that exercises codec, search, and retarget surfaces.

### Gate C (`gate_c_benchmarks.py`)

- **Readiness:** Blocked upstream.
- **Immediate blocker:** same `numpy` dependency problem as Gate B.
- **Blocker class:** Dependency drift.
- **Secondary risk:** benchmark runtime unknown until Gate B passes.
- **Value:** High once Gate B is healthy because it emits the core claim artifacts.

### Gate D (`gate_d_falsification.py`)

- **Readiness:** Blocked upstream.
- **Immediate blocker:** same `numpy` dependency problem.
- **Blocker class:** Dependency drift.
- **Secondary risk:** deterministic stress results may expose additional code-level issues after dependencies are installed.

### Gate M1 (`gate_m1_acl_comparator.py`)

- **Readiness:** Not yet ready.
- **Expected blocker classes:** external dependency/access drift around ACL sources or comparator binaries.
- **Current evidence basis:** runbook and PRD only; no fresh repo-local probe yet in this phase.
- **Priority in Phase 1:** classify, not execute.

### Gate M2 (`gate_m2_live_runtime.py`)

- **Readiness:** Blocked on this machine state.
- **Immediate blockers:** `blender` not installed, `pxr` not installed, `.env` absent.
- **Blocker classes:** runtime dependency drift and local resource/access gap.
- **Important discipline:** M2 must not be promoted from simulated evidence. The absence of runtime binaries is decisive Phase 1 evidence.

### Gate M3 / Gate M4

- **Readiness:** Not Phase 1 ready.
- **Why:** They depend on earlier core-gate health and likely on larger resource surfaces.
- **Expected blocker classes:** upstream dependency chain, possible compute pressure, and possibly missing dataset/runtime resources.

### Gate E-G5 (`gate_e_runpod_readiness.py`)

- **Readiness:** Logic appears executable.
- **Constraint:** It only becomes meaningful once `impracticality_decisions.json` exists and real `IMP-COMPUTE` evidence has been recorded.
- **Interpretation:** This is not a compute trigger; it is a downstream packaging reaction to a compute trigger.

### Gate F (`gate_f_commercial_closure.py`)

- **Readiness:** Logic appears executable but semantically premature.
- **Constraint:** It depends on `max_claim_resource_map.json` and the core claim artifacts already existing.
- **Interpretation:** The script itself is not the blocker. Missing upstream evidence is.

## Local Hardware And Runtime Interpretation

### Mac M1 Air

- Suitable for immediate Phase 1 work: venv creation, dependency installation, tests, Gate A, and likely Gate B.
- Possibly suitable for Gate C and Gate D, but not yet evidenced in this phase.

### Red Magic 10 Pro+ Via ADB

- `adb` exists locally, which means the mobile path is not blocked at the tool-install layer.
- Device presence, authorization, and actual runtime utility are still unknown.
- This is a conditional secondary surface, not the first unblocker for Phase 1.

### RunPod

- No current evidence supports escalation.
- The right threshold is not “a gate looks heavy.” The right threshold is “an actual `IMP-COMPUTE` blocker has been evidenced after local execution attempts.”

## False Progress To Reject

- Repo docs being cleaner than the imported packet.
- Existing historical artifacts remaining present in `proofs/artifacts`.
- GitHub issue `#1` remaining open and visible.
- The Comet boundary run existing.
- Tests or gates passing only in some previous environment while failing now on the current machine.
- Simulated runtime evidence being treated as a live-runtime substitute.

## Recommended Next Executable Path

### Immediate Next Plan

1. Create a repo-local `.venv` and install the package from `code/` so dependency state is explicit instead of ambient.
2. Re-run the current unit-test surface and capture whether dependency normalization restores the expected local sanity baseline.
3. Run `gate_a_setup.py` to establish a fresh repo-local checkpoint and fixture lock from the inner repo boundary.
4. Run `gate_b_build.py` as the first real gate smoke to test whether the dependency-normalized boundary is actually executable.
5. Stop there and classify the result:
   - If Gate B passes, Phase 2 can research Gate M2 from a healthier local baseline.
   - If Gate B fails, the next phase must narrow around code or dependency repair before broader gate fanout.

### Why This Is The Right Next Step

- It attacks the real blocker stack that exists **today** on this machine.
- It avoids pretending that runtime and commercialization work can proceed while even the local dependency baseline is broken.
- It preserves the user’s “no process theater” instruction by using the smallest evidence-bearing execution path.

## Phase 1 Verdict

**Research outcome:** actionable and sufficiently grounded.

**Best next action:** plan and execute a single bounded Phase 1 plan focused on:

- repo-local environment normalization,
- baseline test replay,
- Gate A execution,
- Gate B smoke execution,
- blocker classification receipt.
