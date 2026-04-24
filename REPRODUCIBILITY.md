# ZPE-Mocap Reproducibility

## Canonical Inputs

The canonical repo-local inputs for reproducibility are:

- `code/fixtures/cmu/manifest.json`
- `code/fixtures/cmu/bvh/02_01.bvh`
- `code/fixtures/cmu/bvh/02_03.bvh`
- `code/fixtures/cmu/bvh/05_01.bvh`
- `code/fixtures/cmu/bvh/13_29.bvh`
- `code/fixtures/cmu/bvh/16_15.bvh`
- `code/fixtures/cmu/bvh/35_01.bvh`
- `code/fixtures/cmu/bvh/49_02.bvh`
- `code/fixtures/cmu/bvh/69_04.bvh`
- `code/fixtures/cmu/bvh/86_01.bvh`
- `code/fixtures/cmu/bvh/126_07.bvh`
- `code/fixtures/locked_corpus_v1.json`
- `code/tests/fixtures/canonical_walk.json`
- `code/tests/fixtures/canonical_walk_compressed.bin`
- `code/tests/fixtures/canonical_walk_roundtrip.json`

These inputs support the committed CMU fixture benchmark, the locked synthetic
corpus, and the roundtrip/search regression fixtures used by the Python
reference implementation.

## Golden-Bundle Hash

The canonical golden-bundle hash will be populated by the `receipt-bundle.yml`
workflow in Wave 3 of the Portfolio Hardening Program. This repo does not yet
publish that receipt surface.

## Verification Command

Use the repository verification path from the README:

```bash
git clone https://github.com/Zer0pa/ZPE-Mocap.git
cd ZPE-Mocap
python -m venv .venv
source .venv/bin/activate
python -m pip install -e ./code
python -m unittest discover -s code/tests -v
```

For CMU BVH ingestion and the optional gate stack, install the documented extras
from `code/README.md`:

```bash
python -m pip install -e "./code[cmu,gates,dev]"
```

## Supported Runtimes

- Python reference implementation from the repo root
- Python package surface from `./code`

No additional public runtime surfaces are declared by this repo at present.
