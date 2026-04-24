# ZPE-Mocap Proof And Validation Runbook

## Purpose

Produce the exact next proof that can improve the sovereign gate: a real-corpus retrieval benchmark that replaces synthetic retrieval as the headline retrieval authority. This runbook must not convert reconstruction weakness into a pass narrative.

## Owner / Agent Type

Benchmark and proof agent operating under retrieval-only scope.

## Input Artifacts

- `/Users/Zer0pa/ZPE/ZPE Mocap/ZPE-Mocap/proofs/artifacts/2026-04-14_cmu_corpus_benchmark/summary.md`
- `/Users/Zer0pa/ZPE/ZPE Mocap/ZPE-Mocap/proofs/artifacts/2026-04-14_cmu_corpus_benchmark/results.json`
- `/Users/Zer0pa/ZPE/ZPE Mocap/ZPE-Mocap/proofs/artifacts/2026-02-20_zpe_mocap_wave1/mocap_search_eval.json`
- `/Users/Zer0pa/ZPE/ZPE Mocap/ZPE-Mocap/proofs/artifacts/2026-02-20_zpe_mocap_wave1/mocap_query_latency.json`
- `/Users/Zer0pa/ZPE/ZPE Mocap/ZPE-Mocap/code/zpe_mocap/benchmark.py`
- `/Users/Zer0pa/ZPE/ZPE Mocap/ZPE-Mocap/code/zpe_mocap/search.py`
- `/Users/Zer0pa/ZPE/ZPE Mocap/ZPE-Mocap/code/zpe_mocap/cmu.py`
- `/Users/Zer0pa/ZPE/ZPE Mocap/external/cmu_github_mirror/`
- `/Users/Zer0pa/ZPE/ZPE Mocap/external/cmu_phase3_benchmark_cache/`

## Output Artifacts

- A new proof folder under `/Users/Zer0pa/ZPE/ZPE Mocap/ZPE-Mocap/proofs/artifacts/`
- Retrieval metrics JSON
- Latency metrics JSON
- Corpus manifest or benchmark split manifest
- Markdown summary with explicit limitations

## Acceptance Gate

Pass only if the new proof bundle:

- uses real corpus data;
- avoids exact query/library duplication;
- reports retrieval metrics such as `P@k` and/or median rank;
- reports latency under the same benchmark methodology;
- states corpus lineage and split methodology;
- explicitly says playback/reconstruction authority is still out of scope unless separately proven.

## Failure Mode

Fail the run if:

- query clips are present verbatim in the search library;
- the benchmark depends on synthetic-only retrieval data;
- the benchmark cannot run without the stale broken ingest path;
- the resulting proof still does not improve the real retrieval authority surface.

## Mac / RunPod / HF Requirement

- Mac: required for the first pass and expected to be enough.
- HF: required to confirm custody of large corpora and to store any large proof bundle if produced.
- RunPod: optional CPU only if corpus size or repeated benchmark sweeps become too slow or disk-heavy locally.
- GPU: not required.

## Procedure

1. Confirm current benchmark leakage risk.

   Inspect `/Users/Zer0pa/ZPE/ZPE Mocap/ZPE-Mocap/code/zpe_mocap/benchmark.py` and verify whether the current retrieval benchmark cycles exact clips into the library.

2. Define the next honest benchmark.

   Use the already available CMU mirror/cache first. Prefer one of these non-duplicate setups:

   - held-out clip retrieval by motion class or subject;
   - temporal-window retrieval where query windows are excluded from the library source segment;
   - cross-subset retrieval using distinct train/library/query partitions.

3. Avoid stale ingest dependence.

   If `code/scripts/cmu_ingest.py` is still tied to the broken `cgspeed` path, bypass it with the existing local/HF-custodied CMU mirror and cache rather than blocking on a new downloader.

4. Run the benchmark and emit proof artifacts.

   The proof bundle must capture:

   - corpus source path;
   - selection logic;
   - query/library split logic;
   - retrieval metrics;
   - latency metrics;
   - explicit non-playback limitation.

5. Compare against the current truth.

   Treat success as stronger real retrieval authority, not as playback closure and not as a license to promote broader commercial claims than the new proof supports.

## Exact Next Benchmark Recommendation

The most leverage-efficient next benchmark is:

`real CMU mirror retrieval on held-out query windows or held-out clips using the existing CMU mirror/cache, with P@10, median rank, and p95 latency reported under non-duplicate query/library splits`

This is a better next move than jumping immediately to HumanML3D, Motion-X++, or AMASS because it upgrades authority using already available corpora and existing repo machinery.
