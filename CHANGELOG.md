<p>
  <img src=".github/assets/readme/zpe-masthead.gif" alt="ZPE-Mocap Masthead" width="100%">
</p>

# Changelog

<p>
  <img src=".github/assets/readme/section-bars/unreleased.svg" alt="[UNRELEASED]" width="100%">
</p>

## Unreleased

- Benchmarks: add `code/scripts/benchmark_cmu_public_corpus.py` for a reproducible 100-sequence public CMU subset run with cache-backed downloads and artifact emission.
- Tests: add `code/tests/test_cmu_benchmark_helpers.py` for CMU benchmark tree parsing, deterministic subset selection, and summary table helpers.
- Benchmarks: publish `proofs/artifacts/2026-04-08_cmu_public_corpus_benchmark/` with CMU public-subset results (`zpe_ratio_mean=20.3016x`, `joint_angle_rmse_deg_mean=80.3369`, `mpjpe_mm_mean=44.3691`) and explicit AMASS/Mixamo/Blender blocker notes.
- Examples: add a real-CMU Blender preview scaffold under `proofs/artifacts/2026-04-08_cmu_public_corpus_benchmark/blender_preview_ready/`.
- Examples: add runnable BVH, CMU, and Blender-preview demos under `examples/`.
- Tests: add clean-install, example-smoke, CMU real-BVH, manifest-diagnostic, and zip-safety coverage.
- Benchmarks: add `BENCHMARKS.md` methodology surface and published synthetic benchmark rows.
- Packaging: add `test` and `docs` optional dependency groups.
- README: add evidence-first synthetic-only positioning, personas, ecosystem links, quick start, install guidance, and corrected latency references.
- Packaging: normalize `code/pyproject.toml` metadata with expanded classifiers and project URLs.
- Docs: align `LICENSE` and `code/LICENSE` to the live `ZPE-IMC` SAL v6.0 text.
- Docs: transfer `zpe-masthead-option-3.4.gif`, `zpe-masthead-option-3.5.gif`, and `zpe-masthead-option-3.6.gif` into `.github/assets/readme/`.
- Docs: place animated masthead GIFs in `README.md` to mirror the `ZPE-IMC` reference positions.
- Docs: normalize shared repo docs to the `ZPE-IMC` documentation pattern while preserving ZPE-Mocap-specific evidence boundaries.

## 2026-03-21
- Docs: align README visual system.
- Docs: align governance, releasing, roadmap, citation, and FAQ surfaces.
- Docs: align GitHub templates and assets copy.
- Docs: add a canonical doc registry for the `docs/` surface.
