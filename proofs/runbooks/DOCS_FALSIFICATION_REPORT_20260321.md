# Docs Falsification Report (2026-03-21)

Scope: evidence in repo docs and runbooks only. No live-render verification executed in this pass.

## Unsupported Claims Removed or Downgraded
- Commercial-safe posture explicitly remains downgraded; CMU-backed closure is not promoted.
  Evidence: `/Users/Zer0pa/ZPE/ZPE Mocap/ZPE-Mocap/PUBLIC_AUDIT_LIMITS.md`
- Repo-facing docs explicitly do not promote CMU-backed commercialization closure or direct Blender runtime proof.
  Evidence: `/Users/Zer0pa/ZPE/ZPE Mocap/ZPE-Mocap/proofs/release_readiness/2026-03-20_science_engineering_packet/04_PUBLIC_AUDIT_LIMITS.md`

## Path or Render Issues Found
- Stale absolute paths exist in imported runbooks (historical references).
  Evidence: `/Users/Zer0pa/ZPE/ZPE Mocap/ZPE-Mocap/proofs/runbooks/README.md`
- Some artifacts retain stale absolute paths as lineage.
  Evidence: `/Users/Zer0pa/ZPE/ZPE Mocap/ZPE-Mocap/proofs/release_readiness/2026-03-20_science_engineering_packet/04_PUBLIC_AUDIT_LIMITS.md`
- No render failures were documented in the reviewed sources.

## Remaining Owner Inputs
- CMU corpus presence and CMU-backed closure evidence are not established in-repo.
  Evidence: `/Users/Zer0pa/ZPE/ZPE Mocap/ZPE-Mocap/PUBLIC_AUDIT_LIMITS.md`
- Direct Blender runtime proof is not established.
  Evidence: `/Users/Zer0pa/ZPE/ZPE Mocap/ZPE-Mocap/PUBLIC_AUDIT_LIMITS.md`
- Clean-clone reproducibility is not established.
  Evidence: `/Users/Zer0pa/ZPE/ZPE Mocap/ZPE-Mocap/PUBLIC_AUDIT_LIMITS.md`

## Live vs Local Drift
- Historical note: local working docs and live public docs diverged during the process; silent drift is failure.
  Evidence: `/Users/Zer0pa/ZPE/ZPE Mocap/ZPE-Mocap/proofs/runbooks/REPO_DOCS_PLAYBOOK_CANONICAL_2026-03-21.md`
- No explicit resolution evidence for live-vs-local drift is recorded in the reviewed sources.
