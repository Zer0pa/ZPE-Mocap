# Phase 05 Research: Refinement, Performance, and Evidence-Hygiene Augmentation

## User Constraints
- Treat the inner repo as the sole authority surface.
- Do not promote proxies (docs, tests, GitHub, Comet activity) as closure evidence.
- Prefer local or RunPod-executed, reproducible measurements over narrative claims.
- Keep local disk disposable; store heavy artifacts on RunPod or external traceability systems when permissible.

## Active Anchor References
- `Ref-wave1-prd`: `/Users/Zer0pa/ZPE/ZPE Mocap/team_analysis_packet_2026-03-20/02_WAVE1_PRD.md`
- `Ref-readme`: `/Users/Zer0pa/ZPE/ZPE Mocap/ZPE-Mocap/README.md`
- `Ref-master-runbook`: `/Users/Zer0pa/ZPE/ZPE Mocap/ZPE-Mocap/proofs/release_readiness/2026-03-20_science_engineering_packet/08_MASTER_RUNBOOK.md`
- `Ref-m2`: `/Users/Zer0pa/ZPE/ZPE Mocap/ZPE-Mocap/proofs/release_readiness/2026-03-20_science_engineering_packet/09_GATE_M2_RUNTIME.md`
- `Ref-f`: `/Users/Zer0pa/ZPE/ZPE Mocap/ZPE-Mocap/proofs/release_readiness/2026-03-20_science_engineering_packet/10_GATE_F_COMMERCIAL.md`
- `handoff_manifest.json`: `proofs/artifacts/2026-02-20_zpe_mocap_wave1/handoff_manifest.json`

## Mathematical Framework
This phase is an engineering refinement pass. Use deterministic gate outputs, timing/throughput metrics, and resource/latency measurements as the measurable objects. The framework is comparative: baseline vs refined implementation, with explicit deltas and reproducible gates.

## Standard Approaches
- Profiling-driven optimization: identify hotspots, then quantify improvements (latency, throughput, memory).
- Evidence hygiene: prune stale or redundant artifacts, keep authoritative gate outputs and receipts only.
- Regression hardening: re-run decisive gates after any code or packaging change.
- Resource discipline: keep local environments disposable; rehydrate from lockfiles or receipts when needed.

## Existing Results to Leverage
- Gate pass checkpoints and commercialization adjudication artifacts under `proofs/artifacts/2026-02-20_zpe_mocap_wave1/`.
- The assessment packet and master runbook for acceptance rules and non-proxy constraints.

## Don't Re-Derive
- Claim definitions and acceptance rules in the PRD and runbooks.
- Gate logic already encoded in `code/scripts/`.

## Computational Methods
- Use existing gate scripts for timing and validation outputs.
- Use basic profiling (time/perf counters) and log-based deltas rather than new benchmarking frameworks.
- RunPod is permitted for heavy or long-running profiling; local machine remains lean.

## Limiting Cases
- If optimization targets are claimed, verify no regression against gate pass artifacts.
- If performance improvements are claimed, ensure they hold under the existing max-load artifacts.

## Dimensional Analysis and Natural Scales
- Units already established: degrees (RMSE), millimeters (MPJPE), milliseconds (latency), dimensionless ratios for compression and search.
- Report deltas in the same units and compare against prior gate baselines.

## Common Pitfalls
- Mistaking log cleanup or doc edits for performance improvement.
- Deleting authoritative artifacts when cleaning disk.
- Optimizing based on single-run noise without re-checking gates.

## Validation Strategies
- Re-run relevant gates after any change.
- Compare performance metrics against the `before_after_metrics.json` baseline.
- Require at least one explicit regression check to confirm no new failures.
