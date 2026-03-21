# Metric Scorecard

## Core Metrics

| Metric | Threshold | Observed | Margin | Status |
| --- | --- | --- | --- | --- |
| Compression ratio | `>= 10x` | `85.18929711318528x` | `+75.18929711318528x` | PASS |
| Joint-angle RMSE | `<= 1 deg` | `1.1579274767504938e-07 deg` | effectively zero | PASS |
| MPJPE | `<= 5 mm` | `1.190071935260623 mm` | `3.809928064739377 mm headroom` | PASS |
| Search P@10 | `>= 0.85` | `1.0` | `+0.15` | PASS |
| Search latency p95 | `< 100 ms` | `30.200581256212896 ms` | `69.7994187437871 ms headroom` | PASS |
| Retarget MPJPE | `<= 10 mm` | `0.0 mm` | `10.0 mm headroom` | PASS |
| Determinism | `5/5 identical hashes` | `5/5` | exact | PASS |
| Uncaught crash rate | `0%` | `0.0%` | exact | PASS |

## Baseline-To-Current Delta

Source: [before_after_metrics.json](/Users/Zer0pa/ZPE/ZPE%20Mocap/ZPE-Mocap/proofs/artifacts/2026-02-20_zpe_mocap_wave1/before_after_metrics.json)

| Measure | Baseline | Current |
| --- | --- | --- |
| Compression ratio | `1.0` | `85.18929711318528` |
| Joint RMSE deg | `999.0` | `1.1579274767504938e-07` |
| MPJPE mm | `999.0` | `1.190071935260623` |
| Search P@10 | `0.0` | `1.0` |
| Search p95 latency ms | `999.0` | `30.200581256212896` |
| Retarget MPJPE mm | `999.0` | `0.0` |
| Roundtrip | `UNTESTED` | `PASS` |

## Beyond-Brief Signals

Source: [innovation_delta_report.md](/Users/Zer0pa/ZPE/ZPE%20Mocap/ZPE-Mocap/proofs/artifacts/2026-02-20_zpe_mocap_wave1/innovation_delta_report.md)

- Compression stretch beyond the minimum brief: `+75.189x`
- Search latency headroom versus the PRD threshold: `69.799ms`
- Retarget headroom versus the PRD threshold: `10.000mm`
- Determinism and adversarial falsification were carried past the minimum metric bar.

## Quality Rubric Result

Source: [quality_gate_scorecard.json](/Users/Zer0pa/ZPE/ZPE%20Mocap/ZPE-Mocap/proofs/artifacts/2026-02-20_zpe_mocap_wave1/quality_gate_scorecard.json)

- Rubric status: `PASS`
- Total score: `46`
- Minimum required score: `45`
- Non-negotiables: all `true`

## Reviewer Focus

The metric surface itself is not the weak point. Review effort is better spent on closure semantics and evidence interpretation, especially around MOC-C007 and stale pre-max traceability notes.
