# Contributing

Contributions in this repo are evidence-first.

## Ground Rules

- Do not promote a claim without naming the supporting artifact.
- Negative results are valid contributions.
- Keep nested external repos and datasets outside this repo boundary.
- If you change gate logic, path handling, or proof wording, update the relevant docs and evidence references in the same change.

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -e ./code
python -m unittest discover -s code/tests -v
```

## Pull Requests

- Keep scope narrow.
- State whether the change affects code, docs, proofs, or boundary handling.
- Include concrete evidence when behavior changes.
- Do not hide or rewrite failing/contradicted historical artifacts; supersede them with clearer docs or new evidence.
