<p>
  <img src=".github/assets/readme/zpe-masthead.gif" alt="ZPE-Mocap Masthead" width="100%">
</p>

# Contributing

ZPE-Mocap welcomes contributions from engineers, reviewers, and falsifiers.
This repo is evidence-first and boundary-conscious. Claims without artifacts
are out of scope. Treat every contribution as a proof trail that a cold
reader can validate.

Read this before opening a PR. The bar here is evidence, not intention.

<p>
  <img src=".github/assets/readme/section-bars/before-you-start.svg" alt="BEFORE YOU START" width="100%">
</p>

ZPE-Mocap operates under the same practical rules as the `ZPE-IMC` reference
surface:

- Negative results are first-class artifacts.
- Claims require evidence paths.
- External datasets and vendor trees stay outside this repo boundary.
- Docs, code, and proof language must remain mutually consistent.

<p>
  <img src=".github/assets/readme/section-bars/licensing-of-contributions.svg" alt="LICENSING OF CONTRIBUTIONS" width="100%">
</p>

By submitting a contribution you agree that:

- Your contribution is licensed to Zer0pa under the terms of the Zer0pa
  Source-Available License v6.0.
- You retain copyright in your contribution.
- `LICENSE` is the legal source of truth. This file is an operational summary
  only and is not legal advice.

<p>
  <img src=".github/assets/readme/section-bars/environment-setup.svg" alt="ENVIRONMENT SETUP" width="100%">
</p>

Current public contributor acquisition surface:
`https://github.com/Zer0pa/ZPE-Mocap.git`

```bash
git clone https://github.com/Zer0pa/ZPE-Mocap.git
cd ZPE-Mocap
python -m venv .venv
source .venv/bin/activate
python -m pip install -e "./code[cmu,gates,dev]"
python -m unittest discover -s code/tests -v
```

If setup or tests fail, include the exact command, terminal output, and any
relevant environment details in the PR or issue.

<p>
  <img src=".github/assets/readme/section-bars/running-the-test-suite.svg" alt="RUNNING THE TEST SUITE" width="100%">
</p>

Minimum contributor test path:

```bash
python -m unittest discover -s code/tests -v
python -m zpe_mocap.cli --version
```

If your change affects gate logic, proof-generation scripts, packaging, or
doc truth surfaces, include the exact command set you ran and the artifacts
or paths you checked.

<p>
  <img src=".github/assets/readme/section-bars/what-we-accept.svg" alt="WHAT WE ACCEPT" width="100%">
</p>

- Bug fixes with a reproducible case.
- Documentation corrections backed by current repo truth.
- Evidence-path cleanup that improves auditability without inflating claims.
- Packaging, install, or gate-surface fixes with concrete before/after evidence.
- Honest falsification or downgrade findings.

<p>
  <img src=".github/assets/readme/section-bars/what-we-do-not-accept.svg" alt="WHAT WE DO NOT ACCEPT" width="100%">
</p>

- Claim inflation that outruns the current proof surface.
- Repo changes that vendor external datasets or private material.
- PRs that alter or obscure failing historical artifacts instead of superseding
  them honestly.
- Evidence-free changes to gate logic or README truth statements.

<p>
  <img src=".github/assets/readme/section-bars/pr-process.svg" alt="PR PROCESS" width="100%">
</p>

1. Keep scope narrow.
2. Run the minimum relevant verification path.
3. Name the evidence paths in the PR.
4. State whether the change affects code, docs, proofs, or repo boundary handling.
5. Do not leave evidence-impact sections blank when behavior or claims changed.

<p>
  <img src=".github/assets/readme/section-bars/commit-style.svg" alt="COMMIT STYLE" width="100%">
</p>

- Use present tense and imperative mood.
- Keep commits atomic.
- Reference the affected gate, artifact, or doc surface when it improves traceability.

<p>
  <img src=".github/assets/readme/section-bars/issues.svg" alt="ISSUES" width="100%">
</p>

Use the issue templates in `.github/ISSUE_TEMPLATE/`. Before filing, check
`README.md`, `AUDITOR_PLAYBOOK.md`, `PUBLIC_AUDIT_LIMITS.md`, and
`docs/README.md` so you do not reopen an already-documented boundary.

<p>
  <img src=".github/assets/readme/section-bars/questions.svg" alt="QUESTIONS" width="100%">
</p>

Use `docs/SUPPORT.md` for routing. Security issues go through `SECURITY.md`.
