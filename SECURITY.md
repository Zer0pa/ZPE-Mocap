# Security Policy

## Supported Scope

This policy covers the `zpe_mocap` Python package, the repo-local proof
artifacts, release metadata, and workflow surfaces used to build and publish
ZPE-Mocap.

What counts as a security issue here:

- arbitrary code execution, privilege escalation, or data exfiltration through
  package or CLI paths
- secrets, credentials, or tokens committed to the repo
- vulnerable workflow or release behavior
- supply-chain issues in declared dependencies

What does not count as a security issue here:

- benchmark losses
- codec-quality regressions
- documentation disputes about technical claims

## Reporting

Do not open a public issue for a security vulnerability.

Report privately through:

- GitHub Private Vulnerability Reporting
- `architects@zer0pa.ai`

Include:

- affected component
- reproduction steps or proof of concept
- severity and impact
- suggested remediation if you have one

## Response Targets

| Stage | Target timeframe |
|---|---|
| Acknowledgement | within 5 business days |
| Initial assessment | within 10 business days |
| Remediation or mitigation plan | post-triage, based on confirmed severity and scope |

We follow coordinated disclosure and will not take legal action against
good-faith security research that follows this policy.

Security fixes ship as patch releases and are recorded in `CHANGELOG.md`.
