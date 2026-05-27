# ZPE-Mocap

> Product-page mirror for `/encoding/ZPE-Mocap/`.
> Live public repo: [Zer0pa/ZPE-Mocap](https://github.com/Zer0pa/ZPE-Mocap).
> GitHub Markdown cannot reproduce the website typography, CSS, JavaScript, scroll behavior, or live bento layout; this README translates the product page into GitHub-safe Markdown evidence blocks.

## 0. Install / Developer Commands

The product page is the positioning authority. This section is the only retained developer-surface material from the previous root README.

```bash
Motion fingerprint index for archive search. Lossy skeletal BVH fingerprints support dedupe and retrieval, not playback. Install from PyPI: `pip install zpe-mocap
git clone https://github.com/Zer0pa/ZPE-Mocap.git
python -m pip install -e ./code
```

## Product Page Mirror

**Product-page title:** ZPE-Mocap · Find a mocap clip by motion fingerprint · Zer0pa

**Product-page description:** ZPE-Mocap · BVH archive fingerprint index · 18.77x CMU compression, Recall@10 0.583, p50 0.826 ms · same-source retrieval only · PyPI v0.1.1 stale

### Hero Translation

> 00 · ZPE-MOCAP · MOTION FINGERPRINT INDEXLIVE LANE · 235312Z Motion Capture Memory. A searchable motion archive — find any movement, not just any file · ZPE-Mocap · PyPI zpe-mocap 0.1.1 · github.com/Zer0pa/ZPE-Mocap A motion-capture archive stores everything and finds almost nothing. A choreographer, animator, or biomechanist looking for a specific gesture starts at the filename and ends up scrubbing. ZPE-Mocap changes what the archive can answer. It fingerprints BVH skeletons into a motion index: give it a movement, get back the clips that match in 0.826 ms, with the archive itself 18.77× smaller. Playback reconstruction and semantic naming are not in scope here.

## Positioning

| Field | Value |
| --- | --- |
| Section | encoding |
| Product route | /encoding/ZPE-Mocap/ |
| Live public repository | https://github.com/Zer0pa/ZPE-Mocap |
| Repo identity used here | ZPE-Mocap |
| Website display identity | ZPE-Mocap |
| Verdict | STAGED |
| Posture | always_in_beta |
| Headline metric | CMU compression 18.77× mean vs raw BVH float32; Recall@10 0.583; query latency p50 0.826 ms. |
| Honest blocker | No claim of playback-quality pose reconstruction.; No claim of real-data parity with the synthetic benchmark bundle.; No claim that the synthetic ACL comparison is a fair commercial benchmark. |
| Mechanics asset from product page | MOCAP.gif |

## Key Metrics

| Metric | Value | Baseline |
| --- | --- | --- |
| Mean compression ratio vs raw BVH float32 (CMU, 10 clips) | 18.77× |  |
| Retrieval Recall@1 vs random baseline (0.042) | 0.125 | 3.0× above random |
| Query latency p50 | 0.826 ms |  |
| Query latency p99 | 1.191 ms |  |

## Proof Anchors

| Path | State |
| --- | --- |
| proofs/artifacts/2026-04-14_cmu_corpus_benchmark/results.json | VERIFIED |
| proofs/artifacts/2026-04-14_cmu_corpus_benchmark/summary.md | VERIFIED |
| proofs/artifacts/2026-04-24_cmu_retrieval_benchmark/results.json | VERIFIED |
| proofs/artifacts/2026-04-24_cmu_retrieval_benchmark/summary.md | VERIFIED |
| proofs/artifacts/2026-02-20_zpe_mocap_wave1/mocap_compression_benchmark.json | VERIFIED |
| proofs/artifacts/2026-02-20_zpe_mocap_wave1/mocap_joint_fidelity.json | VERIFIED |

## What We Prove

- Canonical walk payload is byte-stable. Artifact: code/tests/fixtures/canonical_walk.json, code/tests/fixtures/canonical_walk_compressed.bin. Test: code/tests/test_roundtrip.py::test_canonical_walk_payload_matches_committed_binary.
- Canonical walk roundtrip remains numerically stable against the committed fixture. Artifact: code/tests/fixtures/canonical_walk_roundtrip.json. Test: code/tests/test_roundtrip.py::test_canonical_walk_roundtrip_matches_committed_json.
- Exact retrieval over the committed compressed walk fixture remains stable. Artifacts: code/tests/fixtures/canonical_walk.json, code/tests/fixtures/canonical_walk_compressed.bin. Tests: code/tests/test_search.py::test_retrieves_exact, code/tests/test_search.py::test_queries_compressed_library.
- Search ranking and retrieval metric primitives used by the CMU benchmark remain covered. Artifacts: code/zpe_mocap/search.py, code/zpe_mocap/metrics.py, code/scripts/benchmark_cmu_retrieval.py. Tests: code/tests/test_search.py, code/tests/test_metrics.py.
- The committed CMU fixture manifest remains fixed to the 10 checked-in BVH clips. Artifacts: code/fixtures/cmu/manifest.json, code/fixtures/cmu/bvh/*.bvh. Test: code/tests/test_cmu_offline.py::test_manifest_matches_committed_fixture_set.

## What We Do Not Claim

- Not a playback codec. ZPE-Mocap produces lossy fingerprints sized for retrieval and indexing, not playback-grade reconstruction. MPJPE (reconstruction fidelity) is not a design target and is not measured.
- Lossy by design. The encoding is intentionally lossy. A decoded fingerprint is not a faithful reconstruction of the source motion.
- ACL comparator is synthetic only. The 57.03× figure from the ACL Direct Compression Comparator runs on 10 synthetic clips (wave 1 fixture), not CMU real data. It is not CI-gated and is not the lane's compression claim. The aggregate CI-gated claim is the 18.77× CMU figure.
- Fingerprint-vs-playback non-commensurability. ZPE-Mocap and ACL do different jobs; a single ratio number cannot compare them. The ACL comparator is orientation material, not a ranking benchmark.
- Semantic action retrieval is not claimed. The retrieval scope is same-source clip retrieval across held-out non-overlapping windows. Cross-action semantic retrieval has not been evaluated.
- CMU corpus is 10 clips (fixture scale). The 18.77× compression figure is bounded to 10 checked-in CMU fixture clips. Scale-up to 100+ clips is an upcoming workstream, not a current claim.

## Blockers / Failures

> No claim of playback-quality pose reconstruction.; No claim of real-data parity with the synthetic benchmark bundle.; No claim that the synthetic ACL comparison is a fair commercial benchmark.

## Verification Surface

| Code | Check | Verdict |
| --- | --- | --- |
| T_01 | Canonical walk payload matches committed binary fixture | PASS |
| T_02 | Canonical walk roundtrip matches committed JSON fixture within numerical tolerance | PASS |
| T_03 | Synthetic encode/decode threshold smoke path | PASS |
| T_04 | Suffix-index exact retrieval remains stable | PASS |
| T_05 | Retrieval metric helpers used by the CMU benchmark remain stable | PASS |
| T_06 | CMU fixture manifest remains fixed to the committed 10-clip set | PASS |
| T_07 | Decode edge cases preserve expected shapes and fps | PASS |

## License

| Field | Value |
| --- | --- |
| License | SAL-7.0 |
| Authority source | proofs/artifacts/2026-04-24_cmu_retrieval_benchmark/results.json |

## Upcoming Workstreams

| Category | Summary |
| --- | --- |
| Active Engineering | CMU benchmark scale-up (10 → 100+ clips); pure data-ingestion work to close the proof-surface gap to a buyer-evaluable corpus. |
| Research-Deferred — Investigation Underway | Recall@1 lift via fingerprint primitives; current 0.125 needs lift to 0.25+ for archive-search buyers. |

## Related Repos

No related repos are declared on the product page frontmatter.

<details>
<summary>Full Visible Product-Page Bento Translation</summary>

This section preserves the product page cells as Markdown text blocks. It intentionally omits shared site navigation, footer chrome, CSS, and scripts.

### Bento Cell 1

> 00 · ZPE-MOCAP · MOTION FINGERPRINT INDEXLIVE LANE · 235312Z Motion Capture Memory. A searchable motion archive — find any movement, not just any file · ZPE-Mocap · PyPI zpe-mocap 0.1.1 · github.com/Zer0pa/ZPE-Mocap A motion-capture archive stores everything and finds almost nothing. A choreographer, animator, or biomechanist looking for a specific gesture starts at the filename and ends up scrubbing. ZPE-Mocap changes what the archive can answer. It fingerprints BVH skeletons into a motion index: give it a movement, get back the clips that match in 0.826 ms, with the archive itself 18.77× smaller. Playback reconstruction and semantic naming are not in scope here.

### Bento Cell 2

> 01 · THE GAPSTORED, NOT SEARCHABLE A motion archive captures everything and finds nothing — every search starts at the filename.

### Bento Cell 3

> 02 · MARKETSADJACENT CONTEXT Animation / VFXBVH archive owners Biomechanics labsresearch motion data ML motion preptraining-set dedupe Sports sciencegait & session archives 3D mocap market '30$0.52 B Motion capture sits inside these markets; none of them can yet search the archive beneath the file.

### Bento Cell 4

> 03 · VALUE BVHINDEX Every BVH archive that cannot yet be searched by the movement inside it.

### Bento Cell 5

> 04 · INSIGHT Motion capture stores the moment. ZPE-Mocap retrieves the movement.

### Bento Cell 6

> 05.1 · CURRENT TECHA LIBRARY WITH NO INDEX A BVH archive is a library with no index. Files are named by shoot, take, or date. Finding a specific gesture means scrubbing clips manually or trusting sparse metadata. At scale, movements are effectively lost.

### Bento Cell 7

> 05.2 · OUR TECHGIVE IT A GESTURE ZPE-Mocap fingerprints BVH skeletal trajectories into a compact motion index. Same-source queries return candidates at p50 0.826 ms with Recall@10 0.583 over 24 held-out windows. The index itself compresses raw BVH float32 by 18.77× on the 10-clip CMU mean — the archive becomes searchable and lighter at once.

### Bento Cell 8

> 05.3 · BENCHMARKSBOUNDED CMU EVIDENCE Compression18.77× Query p500.826ms Recall@100.58324 windows Checks7/710-clip CMU Same-source retrievalPASS CompressionPASS Semantic retrievalNOT CLAIMED Scope: 10 CMU clips, 24 held-out windows. Playback and semantic naming not claimed.

### Bento Cell 9

> 06 · MEASUREMENTFIXTURE-BOUNDED METRICS Every metric is bounded to its fixture window, no broader claim.

### Bento Cell 10

> 06.1 · COMPARATIVE PERFORMANCE · CMU BVH FIXTURE ZPE-Mocap18.77× smaller Recall@100.583 Query p500.826 ms raw BVH1.00× baseline Evidence: 2026-04-24 retrieval bundle · 10-clip CMU fixture · 24 held-out windows · BVH float32 baseline · Recall@5 0.417 · Recall@1 0.125 · p99 1.191 ms · Playback not claimed.

### Bento Cell 11

> 07 · KEY METRICSBOUNDED CMU EVIDENCE

### Bento Cell 12

> 07.1 · MEAN COMPRESSION 18.77× vs raw BVH float32 · 10-clip CMU mean

### Bento Cell 13

> 07.2 · RECALL @ 10 0.583 same-source held-out · 24-window set

### Bento Cell 14

> 07.3 · QUERY p50 0.826ms same-source retrieval · p99 1.191 ms

### Bento Cell 15

> 07.4 · REPO CHECKS 7 / 7 README verification · fixture / search

### Bento Cell 16

> 07.5 · PLAYBACK CLAIM none not playback-grade · not the design target

### Bento Cell 17

> 08 · RETRIEVAL SCOPEWHAT DETERMINISTIC MEANS HERE Committed fixtures, bounded retrieval, no playback claim.

### Bento Cell 18

> 08.1 · WHAT THE EVIDENCE ANCHORS The word deterministic is narrow here. The public evidence anchors byte-stable canonical payloads, a stable suffix-index retrieval path, and a fixed 10-clip CMU fixture manifest. Public three-platform parity is not yet anchored. Retrieval evidence is same-source held-out-window search: Recall@10 = 0.583, p50 0.826 ms. That is shape-fingerprint matching, not semantic labeling. Playback fidelity sits outside the design target and outside the claim.

### Bento Cell 19

> 08.2 · HONEST BLOCKER Honest Blocker · No playback-grade reconstruction. No semantic action retrieval. No broad motion platform. Recall@1 sits at 0.125. The CMU compression scale is 10 clips. Retrieval evidence is 24 held-out windows. The public PyPI release zpe-mocap 0.1.1 is stale pending the 0.1.2 cut.

### Bento Cell 20

> 09 FIVE PATHS FROM ONE MOTION FINGERPRINT.

### Bento Cell 21

> 09.1 · THE AMBITION Motion Capture Memory means a BVH archive you can search by what the body did, not by when the file was saved. Once a skeletal movement is a compact searchable fingerprint instead of a raw stream, retrieval replaces recollection as how studios, labs, and robotics teams operate their motion archives.

### Bento Cell 22

> 09.2 · WHAT WORKS NOW Working today: same-source fingerprint search at p50 0.826 ms, 18.77× CMU compression, Recall@10 0.583.

### Bento Cell 23

> 09.3 · WHAT'S STILL OPEN Still open: semantic retrieval, playback reconstruction, broader corpora, recall lift, PyPI 0.1.2 release.

### Bento Cell 24

> 09.4 · ARCHIVES · NEAR-TERM (12–24 MO) Mocap archives become searchable libraries An animation supervisor looking for a specific limp, recoil, or hand gesture types a reference clip instead of scrolling through filenames. The decades of capture sitting on studio drives stop being write-only storage and start answering questions.

### Bento Cell 25

> 09.5 · STORAGE · NEAR-TERM (12–24 MO) Studios stop throwing away takes When a session shrinks to roughly five percent of its raw size and stays queryable, a games or VFX studio can keep every alternate take rather than picking three to archive. The “we deleted it” conversation with directors goes away.

### Bento Cell 26

> 09.6 · TRAINING DATA · MID-TERM (24–48 MO) Robotics training sets get curated A humanoid-robotics team preparing imitation-learning data can deduplicate demonstrations at the movement level instead of by file hash. Near-identical takes get collapsed, rare gestures get up-weighted, and policy training starts from a balanced motion library rather than a filename pile.

### Bento Cell 27

> 09.7 · BIOMECHANICS · MID-TERM (24–48 MO) Sports labs query by movement pattern A sports-biomechanics analyst comparing a pitcher's delivery across two seasons stops watching tape and starts running queries: every jump with this hip-knee profile, every gait phase with this stride asymmetry. Longitudinal motion research becomes possible against a full-session archive.

### Bento Cell 28

> 09.8 · INDUSTRY STANDARD · PARADIGM (48 MO+) Movement gets a shared vocabulary Animation studios, biomechanics labs, robotics teams, and XR engineers cite the same gesture across capture rigs and file formats. A movement becomes something that can be referenced, compared, and reused across organizations — a shared language for what bodies do, not just what cameras recorded.

</details>

---

Source mapping: product route `/encoding/ZPE-Mocap/` -> live public repo `Zer0pa/ZPE-Mocap`. README generated from product-page authority plus retained install/dev commands only.
