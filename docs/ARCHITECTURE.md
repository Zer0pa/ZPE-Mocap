<h1 align="center">ZPE-Mocap Architecture</h1>

<p align="center">
  <img src="../.github/assets/readme/zpe-masthead.gif" alt="ZPE-Mocap Masthead" width="100%">
</p>

<p align="center">
  This document maps runtime structure, proof routing, and authority boundaries. It does not restate README metrics.
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
      <td valign="top"><code>code/src/zpe_mocap/</code></td>
      <td valign="top">Installable reference implementation (codec, search, synthetic generation, retargeting).</td>
    </tr>
    <tr>
      <td valign="top"><code>code/tests/</code></td>
      <td valign="top">Lightweight sanity tests for the reference stack.</td>
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
      <td valign="top"><code>code/format/</code></td>
      <td valign="top">Schema inputs and format definitions.</td>
    </tr>
    <tr>
      <td valign="top"><code>proofs/</code></td>
      <td valign="top">Imported evidence bundle and proof logs for the current authority surface.</td>
    </tr>
    <tr>
      <td valign="top"><code>docs/</code></td>
      <td valign="top">Architecture, legal boundaries, support routing, and documentation index.</td>
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
      <td valign="top"><a href="../proofs/artifacts/2026-02-20_zpe_mocap_wave1/"><code>proofs/artifacts/2026-02-20_zpe_mocap_wave1/</code></a></td>
      <td valign="top">Current authority bundle for synthetic-corpus evidence.</td>
    </tr>
    <tr>
      <td valign="top"><a href="../proofs/README.md"><code>proofs/README.md</code></a></td>
      <td valign="top">Proof navigation, logs, and evidence lineage.</td>
    </tr>
    <tr>
      <td valign="top"><a href="../code/README.md"><code>code/README.md</code></a></td>
      <td valign="top">Package-facing install and runtime usage. Keeps implementation detail out of the front door.</td>
    </tr>
    <tr>
      <td valign="top"><a href="../AUDITOR_PLAYBOOK.md"><code>AUDITOR_PLAYBOOK.md</code></a></td>
      <td valign="top">Shortest honest audit path across the repo evidence surface.</td>
    </tr>
    <tr>
      <td valign="top"><a href="../PUBLIC_AUDIT_LIMITS.md"><code>PUBLIC_AUDIT_LIMITS.md</code></a></td>
      <td valign="top">Explicit non-claims and limits on public audit inference.</td>
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
      <th align="left" width="30%">Module</th>
      <th align="left" width="70%">Responsibility</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td valign="top"><code>codec.py</code></td>
      <td valign="top">Deterministic motion encoding and decoding.</td>
    </tr>
    <tr>
      <td valign="top"><code>synthetic.py</code></td>
      <td valign="top">Locked synthetic corpus generation.</td>
    </tr>
    <tr>
      <td valign="top"><code>search.py</code></td>
      <td valign="top">Suffix-like token index for motion retrieval.</td>
    </tr>
    <tr>
      <td valign="top"><code>retarget.py</code></td>
      <td valign="top">Scale-space retarget helpers.</td>
    </tr>
    <tr>
      <td valign="top"><code>benchmark.py</code></td>
      <td valign="top">Synthetic benchmark bundle generation.</td>
    </tr>
    <tr>
      <td valign="top"><code>adapters.py</code></td>
      <td valign="top">Simulation-oriented adapter helpers.</td>
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
      <td valign="top"><code>synthetic.generate_clip</code> builds deterministic inputs for tests and proofs.</td>
    </tr>
    <tr>
      <td valign="top">Compression</td>
      <td valign="top"><code>codec.encode_clip</code> serializes motion payloads into deterministic ZPMOC form.</td>
    </tr>
    <tr>
      <td valign="top">Decompression</td>
      <td valign="top"><code>codec.decode_zpmoc</code> reconstructs motion clips from encoded payloads.</td>
    </tr>
    <tr>
      <td valign="top">Search</td>
      <td valign="top"><code>search</code> builds and queries the token index for retrieval evaluation.</td>
    </tr>
    <tr>
      <td valign="top">Retargeting</td>
      <td valign="top"><code>retarget</code> applies scale-space mapping for motion alignment.</td>
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
      <td valign="top">The reference implementation is deterministic on the shipped synthetic corpus.</td>
    </tr>
    <tr>
      <td valign="top">Proof corpus</td>
      <td valign="top">The imported proof bundle is historical and bounded to the wave1 synthetic corpus.</td>
    </tr>
    <tr>
      <td valign="top">Runtime validation</td>
      <td valign="top">Blender runtime verification and CMU-backed commercialization closure remain unpromoted.</td>
    </tr>
  </tbody>
</table>

<p align="center">
  For the current authority metrics and promoted values, see <a href="../README.md"><code>README.md</code></a>.
</p>

<a id="output-boundaries"></a>
<h2 align="center">Output And External Boundaries</h2>

<table width="100%" border="1" bordercolor="#111111" cellpadding="14" cellspacing="0">
  <thead>
    <tr>
      <th align="left" width="34%">Boundary</th>
      <th align="left" width="66%">Notes</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td valign="top">Proof output target</td>
      <td valign="top"><code>proofs/artifacts/2026-02-20_zpe_mocap_wave1/</code> retains proof output outside the package tree.</td>
    </tr>
    <tr>
      <td valign="top">External datasets</td>
      <td valign="top">ACL and dataset clones are intentionally not vendored into this repo.</td>
    </tr>
    <tr>
      <td valign="top">Expected external location</td>
      <td valign="top"><code>../external/</code> or <code>ZPE_MOCAP_EXTERNAL_ROOT</code> when referenced by scripts.</td>
    </tr>
  </tbody>
</table>

<p>
  <img src="../.github/assets/readme/section-bars/contributing-security-support.svg" alt="CONTRIBUTING, SECURITY, SUPPORT" width="100%">
</p>

<a id="go-next"></a>
<h2 align="center">Go Next</h2>

<table width="100%" border="1" bordercolor="#111111" cellpadding="14" cellspacing="0">
  <thead>
    <tr>
      <th align="left" width="38%">If you need to...</th>
      <th align="left" width="62%">Open this</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td valign="top">Inspect promoted metrics and current authority</td>
      <td valign="top"><a href="../README.md"><code>README.md</code></a></td>
    </tr>
    <tr>
      <td valign="top">Navigate the documentation surface</td>
      <td valign="top"><a href="README.md"><code>docs/README.md</code></a></td>
    </tr>
    <tr>
      <td valign="top">Understand legal boundaries</td>
      <td valign="top"><a href="LEGAL_BOUNDARIES.md"><code>docs/LEGAL_BOUNDARIES.md</code></a></td>
    </tr>
    <tr>
      <td valign="top">Follow the audit trail</td>
      <td valign="top"><a href="../AUDITOR_PLAYBOOK.md"><code>AUDITOR_PLAYBOOK.md</code></a></td>
    </tr>
  </tbody>
</table>
