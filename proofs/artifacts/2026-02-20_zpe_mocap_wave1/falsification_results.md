# Falsification Results

Historical wave1 synthetic falsification summary. Current front-door authority for this repo is the CMU fixture benchmark in `proofs/artifacts/2026-04-14_cmu_corpus_benchmark/`.

## Campaign Outcomes
- DT-MOC-1: PASS - malformed hierarchies rejected without crash
- DT-MOC-2: PASS - high-velocity clip handled
- DT-MOC-3: PASS - mirror-corruption scenario contained
- DT-MOC-5: PASS - true clip dominates suffix-index stress
- DT-MOC-4: PASS - 5/5 hash match

## Crash Accounting
- uncaught_exceptions: 0
- uncaught_crash_rate: 0.000000

## Determinism
- status: PASS
- unique_hashes: 1

## Substitutions
- External LAFAN1/Mixamo/CMU/USD runtime sources were proxied via deterministic in-lane fixtures; comparability impact recorded in concept_resource_traceability.json.
