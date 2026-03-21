# Resource And Commercial Closure

## Appendix E Resource Attempts

Source: [max_resource_lock.json](/Users/Zer0pa/ZPE/ZPE%20Mocap/ZPE-Mocap/proofs/artifacts/2026-02-20_zpe_mocap_wave1/max_resource_lock.json)

Attempted resources:
- Kaiwu multimodal mocap+bio: attempted, not accessible
- BABEL (AMASS): attempted, license-gated
- RELI11D: attempted, no accessible data endpoint found
- LAFAN1 baseline: attempted, available
- CMU Mocap baseline: attempted, available
- Mixamo retarget alternative: attempted, account-gated

Appendix E gate result:
- `E-G1..E-G5` all close `PASS`

## Impracticality Decisions

Source: [impracticality_decisions.json](/Users/Zer0pa/ZPE/ZPE%20Mocap/ZPE-Mocap/proofs/artifacts/2026-02-20_zpe_mocap_wave1/impracticality_decisions.json)

Recorded `IMP-*` outcomes:
- `IMP-ACCESS` for Kaiwu
- `IMP-LICENSE` for BABEL
- `IMP-ACCESS` for RELI11D
- `IMP-ACCESS` for Mixamo

These did not remain silent skips. Each one has command-level evidence and a declared fallback path.

## Commercial-Safe Closure

Source: [max_claim_resource_map.json](/Users/Zer0pa/ZPE/ZPE%20Mocap/ZPE-Mocap/proofs/artifacts/2026-02-20_zpe_mocap_wave1/max_claim_resource_map.json)

Commercial-safe closure logic now uses CMU-based alternatives where direct commercial-safe access to the original target resource was blocked.

Claim outcomes:
- `MOC-C001..MOC-C005`: close with commercial-safe non-locomotion coverage present
- `MOC-C006`: closes via commercial-safe CMU substitute with retarget evidence
- `MOC-C007`: closes via commercial-safe CMU substitute and the current runtime evidence path

## Final Commercial Verdict

Source: [commercialization_claim_adjudication.json](/Users/Zer0pa/ZPE/ZPE%20Mocap/ZPE-Mocap/proofs/artifacts/2026-02-20_zpe_mocap_wave1/commercialization_claim_adjudication.json)

- `F-G1`: PASS
- `F-G2`: PASS
- `final_claim_status`: all seven claims `PASS`
- `resource_claim_status`: all seven claims `PASS`

## Reviewer Question

The main question is not whether resource failures were hidden. They were logged correctly. The question is whether the team accepts the CMU-based commercial-safe substitution logic for the blocked resources as sufficient for final claim closure.
