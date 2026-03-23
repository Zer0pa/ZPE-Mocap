<p>
  <img src="../../.github/assets/readme/zpe-masthead.gif" alt="ZPE-Mocap Masthead" width="100%">
</p>

# Code Surface

ZPE-Mocap ships a deterministic Python reference implementation plus the gate
and proof-generation scripts used by the repo-local authority surface.

The package-facing API is intentionally smaller than the repo-level truth
surface. `README.md` remains the only location for promoted metrics.

<p>
  <img src="../../.github/assets/readme/section-bars/install.svg" alt="INSTALL" width="100%">
</p>

Repo-local editable install from the repository root:

```bash
python -m pip install -e "./code[cmu,gates,dev]"
```

Minimal install if you only need the package surface:

```bash
python -m pip install -e ./code
```

<p>
  <img src="../../.github/assets/readme/section-bars/quick-start.svg" alt="QUICK START" width="100%">
</p>

Quick smoke path after install:

```bash
python -m zpe_mocap.cli --version
python -m unittest discover -s code/tests -v
```

<p>
  <img src="../../.github/assets/readme/section-bars/public-api-contract.svg" alt="PUBLIC API CONTRACT" width="100%">
</p>

The intended public Python surface is:

- `encode_clip`
- `decode_zpmoc`
- `MotionSuffixIndex`
- `MotionClip`
- `generate_clip`
- `retarget_clip`
- `GLOBAL_SEED`

CLI entrypoint:

- `zpe-mocap`

<p>
  <img src="../../.github/assets/readme/section-bars/optional-dependency-groups.svg" alt="OPTIONAL DEPENDENCY GROUPS" width="100%">
</p>

- `cmu`: BVH ingestion via `bvhio`
- `gates`: Comet logging plus `zstandard` comparator support
- `dev`: build and test tooling

<p>
  <img src="../../.github/assets/readme/section-bars/cli.svg" alt="CLI" width="100%">
</p>

Current lightweight CLI surface:

```bash
zpe-mocap --version
```

<p>
  <img src="../../.github/assets/readme/section-bars/compatibility-note-for-parallel-tracks.svg" alt="COMPATIBILITY NOTE FOR PARALLEL TRACKS" width="100%">
</p>

The package README is a package surface only. Gate acceptance, proof
authority, commercialization status, and public-claim discipline remain
governed by the repo root and `proofs/` artifacts.
