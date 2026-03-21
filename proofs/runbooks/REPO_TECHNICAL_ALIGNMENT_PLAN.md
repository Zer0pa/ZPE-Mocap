# Repo Technical Alignment Plan (ZPE-MoCap)

Scope: release-architecture alignment for /Users/Zer0pa/ZPE/ZPE Mocap/ZPE-Mocap.

## Plan
1. Inspect package layout under `code/` and confirm truthful architecture (standalone Python package, repo-root docs shell).
2. Align `code/pyproject.toml` to Mocap truth:
   - Remove unrelated optional extras inherited from other lanes.
   - Move non-core runtime deps used only by gate scripts to extras.
   - Add explicit optional extra for CMU/BVH ingestion (`bvhio`).
   - Restrict package discovery to `zpe_mocap` only.
3. Remove generated packaging artifacts (`code/zpe_mocap.egg-info`, `code/src`).
4. Verify CLI truth (`zpe-mocap --version`).
5. Build wheel, run tests, and verify import/install behavior.
6. Record evidence artifacts and update receipt.
