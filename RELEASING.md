<p>
  <img src=".github/assets/readme/zpe-masthead.gif" alt="ZPE-Mocap Masthead" width="100%">
</p>

<p>
  <img src=".github/assets/readme/section-bars/release-notes.svg" alt="RELEASE NOTES" width="100%">
</p>

This file defines the release gate logic for ZPE-Mocap. A release tag is not
valid unless the gates below are backed by in-repo evidence.

<table width="100%" border="1" bordercolor="#111111" cellpadding="14" cellspacing="0">
  <thead>
    <tr>
      <th align="left" width="34%">Gate</th>
      <th align="left" width="18%">Required</th>
      <th align="left" width="48%">Evidence Path</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td valign="top">Synthetic-corpus gate chain (A-F, M1-M4)</td>
      <td valign="top"><code>YES</code></td>
      <td valign="top"><code>proofs/artifacts/2026-02-20_zpe_mocap_wave1/</code></td>
    </tr>
    <tr>
      <td valign="top">CMU real-corpus gate chain</td>
      <td valign="top"><code>YES</code></td>
      <td valign="top"><code>proofs/artifacts/&lt;cmu_run&gt;/</code> (not yet present)</td>
    </tr>
    <tr>
      <td valign="top">Clean-clone verification</td>
      <td valign="top"><code>YES</code></td>
      <td valign="top"><code>proofs/logs/&lt;clean_clone_run&gt;.json</code> (not yet present)</td>
    </tr>
    <tr>
      <td valign="top">PyPI wheel build + install verification</td>
      <td valign="top"><code>YES</code></td>
      <td valign="top"><code>proofs/artifacts/.../pypi_package_build.json</code></td>
    </tr>
    <tr>
      <td valign="top">Docs truth alignment</td>
      <td valign="top"><code>YES</code></td>
      <td valign="top"><code>README.md</code> plus `docs/` surfaces</td>
    </tr>
  </tbody>
</table>

If any required gate lacks evidence, the release is not valid.

<p>
  <img src=".github/assets/readme/zpe-masthead.gif" alt="ZPE-Mocap Masthead" width="100%">
</p>
