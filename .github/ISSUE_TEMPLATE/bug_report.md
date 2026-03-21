---
name: Bug Report
about: Something is broken — codec failure, crash, wrong output
labels: bug
assignees: ''
---

<p>
  <img src="../assets/readme/zpe-masthead.gif" alt="ZPE-Mocap Masthead" width="100%">
</p>

<p>
  <img src="../assets/readme/section-bars/bug-report.svg" alt="BUG REPORT" width="100%">
</p>

**Describe the bug**
A clear description of what is broken and what you expected instead.

**Component**
Which component is affected?

- [ ] `zpe_mocap` package
- [ ] Gate scripts (`code/scripts/`)
- [ ] Proof artifacts (`proofs/`)
- [ ] CLI (`zpe-mocap`)
- [ ] Documentation

**To reproduce**
Exact commands and inputs to reproduce the issue.

**Expected output**
What should have happened.

**Actual output**
What actually happened. Include full error output.

**Verification check**
Before filing: did the minimal tests pass?

- [ ] Yes — `python -m unittest discover -s code/tests -v`
- [ ] No — output differs (details attached)

**Environment**

- Python version:
- OS:
- Install method (`pip install -e ./code` / wheel / other):
- Relevant dependency versions:

**Evidence**
If this touches codec behavior, attach or link before/after metrics, logs, or a
minimal reproducible artifact. Reports without a reproducible case may be
closed with a request for more information.
