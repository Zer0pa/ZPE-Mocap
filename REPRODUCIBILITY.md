# Reproducibility

## Canonical Inputs

- `code/fixtures/locked_corpus_v1.json`
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
- `code/tests/fixtures/canonical_walk.json`

## Golden-Bundle Hash

This field will be populated by the `receipt-bundle.yml` workflow in Wave 3.

## Verification Command

```bash
git clone https://github.com/Zer0pa/ZPE-Mocap.git
cd ZPE-Mocap
python -m venv .venv
source .venv/bin/activate
python -m pip install -e ./code
python -m unittest discover -s code/tests -v
```

## Supported Runtimes

- Python `>=3.10`
- Editable install from the repo root via `./code`
- Optional CMU fixture ingestion extras via `pip install -e ./code[cmu]`
