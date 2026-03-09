# Architecture

## Repo Layout

- `code/src/zpe_mocap/`: installable reference implementation
- `code/tests/`: current lightweight sanity tests
- `code/scripts/`: gate and proof-generation scripts
- `code/fixtures/`: locked synthetic corpus inputs
- `code/format/`: schema inputs
- `proofs/`: imported historical evidence plus future verification surfaces

## Package Components

- `codec.py`: deterministic motion encoding and decoding
- `synthetic.py`: locked synthetic corpus generation
- `search.py`: suffix-like token index for motion retrieval
- `retarget.py`: scale-space retarget helpers
- `benchmark.py`: synthetic benchmark bundle generation
- `adapters.py`: simulation-oriented adapter helpers

## Output Boundary

Gate scripts now target:
- `proofs/artifacts/2026-02-20_zpe_mocap_wave1/`

This keeps proof output out of the package tree and out of the outer workspace shell boundary.

## External Boundary

ACL and dataset clones are intentionally not vendored into this repo.

Expected external location during private staging:
- `../external/`

If needed, scripts can also use `ZPE_MOCAP_EXTERNAL_ROOT`.

## Current Truth

- The core implementation is deterministic on the shipped synthetic corpus.
- The imported proof corpus is historical and bounded.
- Direct Blender runtime and CMU-backed commercialization closure remain unresolved for launch purposes.
