<h1 align="center">ZPE-Mocap Legal Boundaries</h1>

This document is a compact boundary map. It does not override the license or
promoted authority surfaces.

## Legal Source Of Truth

`../LICENSE` is the legal source of truth for this repo. This document is an
operational map only.

## Package Surface

Tracked repo surface:

- `code/zpe_mocap/`
- `code/tests/`
- `code/scripts/`
- repo-facing docs and proofs

## Material Kept Outside The Repo

These remain outside the tracked repo boundary unless explicitly imported with
clear lineage and license review:

- ACL source and build outputs
- CMU and other external corpus clones
- local virtual environments
- local `.env` files and credentials

## Evidence Boundary

- `proofs/artifacts/2026-04-14_cmu_corpus_benchmark/` is the current real-data
  authority surface for retrieval/indexing claims.
- Imported wave1 synthetic artifacts remain lineage and ceiling context, not the
  commercial front door.
- Repo-facing docs are the current interpretation layer for what the live beta
  surface supports today.
- Docs can promote retrieval/indexing posture backed by the CMU fixture
  benchmark. Docs cannot promote playback, Blender, clean-clone, or broader
  commercialization closure without fresh artifact-backed proof.

## Go Next

- Legal source: `../LICENSE`
- Front door: `../README.md`
- Package surface: `../code/README.md`
- Architecture map: `ARCHITECTURE.md`
