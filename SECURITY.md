<p>
  <img src=".github/assets/readme/zpe-masthead.gif" alt="ZPE-Mocap Masthead" width="100%">
</p>

# Security

<p>
  <img src=".github/assets/readme/section-bars/scope.svg" alt="SCOPE" width="100%">
</p>

This policy covers vulnerability reporting for the ZPE-Mocap package, gate
scripts, and proof corpus. It does not cover other Zer0pa workstreams.

Current public acquisition surface:
`https://github.com/Zer0pa/ZPE-Mocap.git`

What counts as a security issue here:

- secrets, credentials, or tokens committed to the repo or proof artifacts
- supply-chain or dependency vulnerabilities affecting the packaged surface
- vulnerabilities in shipped code or scripts that could enable arbitrary code
  execution, privilege escalation, or unintended data exposure

What does not count as a security issue here:

- claim disputes about benchmark or proof interpretation
- negative benchmark results or falsification findings
- ordinary engineering regressions without security impact

<p>
  <img src=".github/assets/readme/section-bars/reporting-a-vulnerability.svg" alt="REPORTING A VULNERABILITY" width="100%">
</p>

Do not open a public issue for a security vulnerability.

Report privately through:

- `architects@zer0pa.ai`

Include:

- a clear description of impact and affected surface
- reproduction steps or proof of concept
- logs, traces, or artifacts with precise paths or attachments
- any suggested remediation, if you have one

<p>
  <img src=".github/assets/readme/section-bars/response-commitment.svg" alt="RESPONSE COMMITMENT" width="100%">
</p>

| Stage | Target timeframe |
| --- | --- |
| Acknowledgement | Within 48 hours |
| Initial assessment | Within 7 days |
| Remediation or mitigation plan | Within 30 days for confirmed issues |
| Public disclosure | Coordinated with the reporter |

We follow coordinated disclosure and will not take legal action against good
faith security researchers who follow this policy.

<p>
  <img src=".github/assets/readme/section-bars/secret-scan.svg" alt="SECRET SCAN" width="100%">
</p>

No standalone in-repo secret-scan artifact is currently promoted as a public
authority surface for ZPE-Mocap. If you discover a missed secret, report it
through the private channel above, not as a public issue.

<p>
  <img src=".github/assets/readme/section-bars/supported-versions.svg" alt="SUPPORTED VERSIONS" width="100%">
</p>

| Version | Supported |
| --- | --- |
| `0.1.x` staging package surface | Current |
| Earlier internal snapshots | Not supported |

Security fixes should be documented in `CHANGELOG.md`.

<p>
  <img src=".github/assets/readme/section-bars/out-of-scope.svg" alt="OUT OF SCOPE" width="100%">
</p>

If you are unsure whether a report is in scope, send it privately with the
evidence you have and note any gaps.

`LICENSE` is the legal source of truth for licensing terms. This file is an
operational summary only and is not legal advice.
