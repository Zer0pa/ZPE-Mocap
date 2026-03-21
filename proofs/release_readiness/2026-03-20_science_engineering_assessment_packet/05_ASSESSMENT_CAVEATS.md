# Assessment Caveats

## Caveat 1: MOC-C007 Wording Versus Current Runtime Evidence

The original PRD wording for `MOC-C007` is "Blender roundtrip pass."

Current evidence state:
- [mocap_blender_roundtrip.json](/Users/Zer0pa/ZPE/ZPE%20Mocap/ZPE-Mocap/proofs/artifacts/2026-02-20_zpe_mocap_wave1/mocap_blender_roundtrip.json) is `PASS`, but its note still says the adapter path is simulated and the local Blender binary was not found.
- [usd_live_runtime_check.json](/Users/Zer0pa/ZPE/ZPE%20Mocap/ZPE-Mocap/proofs/artifacts/2026-02-20_zpe_mocap_wave1/usd_live_runtime_check.json) shows a real USD runtime pass via `python3.11`.
- [gate_m2.json](/Users/Zer0pa/ZPE/ZPE%20Mocap/ZPE-Mocap/proofs/artifacts/2026-02-20_zpe_mocap_wave1/checkpoints/gate_m2.json) records the live runtime gate as `PASS`.

Assessment consequence:
- If the team accepts the later max-wave rule that one live DCC/runtime path closes the runtime obligation, the lane remains closed.
- If the team insists that the original claim text requires a literal local Blender binary roundtrip, then `MOC-C007` is the one item to reopen.

## Caveat 2: Older Supporting Docs Lag The Final Gate State

These files still carry pre-closure notes that are narrower than the later gate checkpoints:
- [concept_resource_traceability.json](/Users/Zer0pa/ZPE/ZPE%20Mocap/ZPE-Mocap/proofs/artifacts/2026-02-20_zpe_mocap_wave1/concept_resource_traceability.json)
- [concept_open_questions_resolution.md](/Users/Zer0pa/ZPE/ZPE%20Mocap/ZPE-Mocap/proofs/artifacts/2026-02-20_zpe_mocap_wave1/concept_open_questions_resolution.md)
- [integration_readiness_contract.json](/Users/Zer0pa/ZPE/ZPE%20Mocap/ZPE-Mocap/proofs/artifacts/2026-02-20_zpe_mocap_wave1/integration_readiness_contract.json)

Those files should be treated as historical context, not as the sovereign end-state, because the later checkpoints and adjudication artifacts supersede them.

## Caveat 3: Repo-State Operational Notes

These are not PRD blockers, but they matter operationally:
- the repo is still uncommitted
- disk headroom is only about `2.2 GiB`
- `.gpd` health still warns that the generic convention lock is unset

## Recommended Team Decision

The science and engineering team should answer one explicit question:

Does the current combined evidence path for `MOC-C007` satisfy the PRD as written, or should the team require a literal Blender-binary rerun before calling the packet fully closed?
