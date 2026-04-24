<h1 align="center">ZPE-Mocap Architecture</h1>

<p align="center">
  <img src="../.github/assets/readme/zpe-masthead.gif" alt="ZPE-Mocap Masthead" width="100%">
</p>

<p align="center">
  This document maps runtime structure, proof routing, and authority
  boundaries. It does not restate README metrics.
</p>

<p>
  <img src="../.github/assets/readme/section-bars/repo-shape.svg" alt="REPO SHAPE" width="100%">
</p>

<a id="repo-layout"></a>
<h2 align="center">Repo Layout</h2>

<table width="100%" border="1" bordercolor="#111111" cellpadding="14" cellspacing="0">
  <thead>
    <tr>
      <th align="left" width="32%">Path</th>
      <th align="left" width="68%">Role</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td valign="top"><code>code/zpe_mocap/</code></td>
      <td valign="top">Installable reference implementation.</td>
    </tr>
    <tr>
      <td valign="top"><code>code/tests/</code></td>
      <td valign="top">Lightweight sanity tests for the package surface.</td>
    </tr>
    <tr>
      <td valign="top"><code>code/scripts/</code></td>
      <td valign="top">Gate and proof-generation scripts.</td>
    </tr>
    <tr>
      <td valign="top"><code>code/fixtures/</code></td>
      <td valign="top">Locked synthetic corpus inputs.</td>
    </tr>
    <tr>
      <td valign="top"><code>proofs/</code></td>
      <td valign="top">Imported evidence bundle, logs, and runbooks.</td>
    </tr>
    <tr>
      <td valign="top"><code>docs/</code></td>
      <td valign="top">Architecture, FAQ, legal boundary, and support routing docs.</td>
    </tr>
  </tbody>
</table>

<p>
  <img src="../.github/assets/readme/section-bars/runtime-proof-wave-1.svg" alt="RUNTIME PROOF (WAVE-1)" width="100%">
</p>

<a id="authority-routing"></a>
<h2 align="center">Authority And Proof Routing</h2>

<table width="100%" border="1" bordercolor="#111111" cellpadding="14" cellspacing="0">
  <thead>
    <tr>
      <th align="left" width="30%">Surface</th>
      <th align="left" width="70%">Authority and notes</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td valign="top"><a href="../README.md"><code>README.md</code></a></td>
      <td valign="top">Front-door truth and the only location for promoted metrics and authority snapshots.</td>
    </tr>
    <tr>
      <td valign="top"><a href="../proofs/artifacts/2026-04-24_cmu_retrieval_benchmark/"><code>proofs/artifacts/2026-04-24_cmu_retrieval_benchmark/</code></a></td>
      <td valign="top">Current retrieval authority bundle for real-data held-out-window search over the CMU mirror.</td>
    </tr>
    <tr>
      <td valign="top"><a href="../proofs/artifacts/2026-04-14_cmu_corpus_benchmark/"><code>proofs/artifacts/2026-04-14_cmu_corpus_benchmark/</code></a></td>
      <td valign="top">Current compression and fidelity authority bundle for the committed 10-clip CMU fixture corpus.</td>
    </tr>
    <tr>
      <td valign="top"><a href="../proofs/artifacts/2026-02-20_zpe_mocap_wave1/"><code>proofs/artifacts/2026-02-20_zpe_mocap_wave1/</code></a></td>
      <td valign="top">Historical synthetic-ceiling bundle retained for lineage, search behavior, and latency evidence only.</td>
    </tr>
    <tr>
      <td valign="top"><a href="../code/README.md"><code>code/README.md</code></a></td>
      <td valign="top">Package-facing install and runtime usage.</td>
    </tr>
    <tr>
      <td valign="top"><a href="../proofs/logs/README.md"><code>proofs/logs/README.md</code></a></td>
      <td valign="top">Repo-local verification log surface reserved for future captures.</td>
    </tr>
  </tbody>
</table>

<p>
  <img src="../.github/assets/readme/section-bars/what-this-is.svg" alt="WHAT THIS IS" width="100%">
</p>

<a id="package-components"></a>
<h2 align="center">Package Components</h2>

<table width="100%" border="1" bordercolor="#111111" cellpadding="14" cellspacing="0">
  <thead>
    <tr>
      <th align="left" width="30%">Module or surface</th>
      <th align="left" width="70%">Responsibility</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td valign="top"><code>codec.py</code>, <code>search.py</code>, <code>synthetic.py</code></td>
      <td valign="top">Deterministic encoding, retrieval, and synthetic corpus generation surfaces referenced by the package API.</td>
    </tr>
    <tr>
      <td valign="top"><code>retarget.py</code>, <code>bvh_loader.py</code>, <code>cmu.py</code></td>
      <td valign="top">Retargeting and corpus-ingestion helpers.</td>
    </tr>
    <tr>
      <td valign="top"><code>benchmark.py</code>, <code>constants.py</code>, <code>cli.py</code></td>
      <td valign="top">Benchmark assembly, package constants, and the CLI surface.</td>
    </tr>
  </tbody>
</table>

<a id="runtime-flow"></a>
<h2 align="center">Runtime Flow (Reference Path)</h2>

<table width="100%" border="1" bordercolor="#111111" cellpadding="14" cellspacing="0">
  <thead>
    <tr>
      <th align="left" width="28%">Step</th>
      <th align="left" width="72%">Runtime path</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td valign="top">Synthetic corpus generation</td>
      <td valign="top"><code>generate_clip</code> builds deterministic inputs for tests and proofs.</td>
    </tr>
    <tr>
      <td valign="top">Compression</td>
      <td valign="top"><code>encode_clip</code> serializes motion payloads into deterministic ZPMOC form.</td>
    </tr>
    <tr>
      <td valign="top">Decompression</td>
      <td valign="top"><code>decode_zpmoc</code> reconstructs motion clips from encoded payloads.</td>
    </tr>
    <tr>
      <td valign="top">Search</td>
      <td valign="top"><code>MotionSuffixIndex</code> handles retrieval evaluation.</td>
    </tr>
    <tr>
      <td valign="top">Gate replay</td>
      <td valign="top"><code>code/scripts/gate_*.py</code> produces artifact-backed checkpoints and reports.</td>
    </tr>
  </tbody>
</table>

<p>
  <img src="../.github/assets/readme/section-bars/open-risks-non-blocking.svg" alt="OPEN RISKS (NON-BLOCKING)" width="100%">
</p>

<a id="boundaries"></a>
<h2 align="center">Boundaries And Current Truth</h2>

<table width="100%" border="1" bordercolor="#111111" cellpadding="14" cellspacing="0">
  <thead>
    <tr>
      <th align="left" width="34%">Surface</th>
      <th align="left" width="66%">Status</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td valign="top">Determinism</td>
      <td valign="top">The reference implementation remains deterministic, and retrieval is now exercised on real BVH windows as well as the shipped synthetic corpus.</td>
    </tr>
    <tr>
      <td valign="top">Proof corpus</td>
      <td valign="top">Promoted proof is split between the 10-clip CMU fixture benchmark and a 24-file held-out retrieval benchmark over the external CMU mirror.</td>
    </tr>
    <tr>
      <td valign="top">Runtime validation</td>
      <td valign="top">Playback-grade reconstruction, Blender runtime verification, and clean-clone commercialization closure remain unpromoted.</td>
    </tr>
    <tr>
      <td valign="top">External datasets</td>
      <td valign="top">ACL and corpus clones stay outside the tracked repo boundary; promoted metrics may cite derived proof artifacts from bounded external slices when the artifact states its scope.</td>
    </tr>
  </tbody>
</table>
