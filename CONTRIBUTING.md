# Contributing

ZPE-Mocap is evidence-first. Claims without artifacts are out of scope.

## Contribution Rules

| Rule | Evidence or constraint |
| --- | --- |
| Do not promote a claim without naming the supporting artifact. | Evidence paths are required in the PR. |
| Negative results are valid contributions. | Falsification findings are first-class artifacts. |
| Keep nested external repos and datasets outside this repo boundary. | Do not vendor external trees into this repo. |
| If you change gate logic, path handling, or proof wording, update the relevant docs and evidence references in the same change. | The proof trail must stay consistent. |

## Environment Setup

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -e ./code
python -m unittest discover -s code/tests -v
```

## Pull Request Expectations

| Expectation | Notes |
| --- | --- |
| Keep scope narrow. | One concern per PR. |
| State whether the change affects code, docs, proofs, or boundary handling. | Use the PR description to call this out. |
| Include concrete evidence when behavior changes. | Attach artifacts or reference existing proof paths. |
| Do not hide or rewrite failing or contradicted historical artifacts. | Supersede with clearer docs or new evidence instead. |
