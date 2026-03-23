<p>
  <img src="../.github/assets/readme/zpe-masthead.gif" alt="ZPE-Mocap Masthead" width="100%">
</p>

This FAQ is scoped to ZPE-Mocap only. Claims are limited to the synthetic
corpus evidence bundle currently in
`proofs/artifacts/2026-02-20_zpe_mocap_wave1/`.

<p>
  <img src="../.github/assets/readme/section-bars/architecture-and-theory.svg" alt="ARCHITECTURE AND THEORY" width="100%">
</p>

**Is ZPE-Mocap a compression codec or a search system?**

ZPE-Mocap is a motion-capture compression and retrieval stack. The core
claims are about deterministic encoding, search ranking, and latency on the
synthetic corpus. It is not positioned as a general-purpose compression codec
replacement without further real-corpus validation.

**Are the headline numbers based on real motion capture data?**

No. The promoted metrics in the README are synthetic-corpus results from the
2026-02-20 wave1 bundle. CMU real-corpus gates have not been run in this repo.

**Is there Blender or USD runtime validation?**

Not yet. Blender runtime proof remains unpromoted and is explicitly treated
as a gap in the current docs.

**How does this compare to ACL?**

The current comparison is a synthetic-corpus ACL comparator that reports ZPE
and ACL ratios on the same raw BVH32 baseline. It is not a claim of parity or
superiority, and ACL's published real-corpus numbers are not reproduced here
yet.

<p>
  <img src="../.github/assets/readme/section-bars/setup-and-verification.svg" alt="SETUP AND VERIFICATION" width="100%">
</p>

**What is the fastest way to verify the current state?**

Use `AUDITOR_PLAYBOOK.md` for the shortest repo-local verification path and
inspect the wave1 proof artifacts in
`proofs/artifacts/2026-02-20_zpe_mocap_wave1/`.

**Is this repo ready to be treated as a clean public release surface?**

No. This remains a staging repo whose promoted authority is bounded to the
current synthetic bundle and explicit non-claims.

<p>
  <img src="../.github/assets/readme/section-bars/integration-and-downstream-use.svg" alt="INTEGRATION AND DOWNSTREAM USE" width="100%">
</p>

**Where do I report a bug or evidence dispute?**

Use the GitHub issue templates in this repo, and route security issues to
`architects@zer0pa.ai`. See `docs/SUPPORT.md` for routing.

<p>
  <img src="../.github/assets/readme/section-bars/evidence-and-claims.svg" alt="EVIDENCE AND CLAIMS" width="100%">
</p>

**Can docs or GitHub polish upgrade the current claim status?**

No. Docs can clarify truth and improve auditability, but they cannot replace
missing CMU, Blender, or clean-clone evidence.

<p>
  <img src="../.github/assets/readme/section-bars/license-and-ip.svg" alt="LICENSE AND IP" width="100%">
</p>

**Where is the legal source of truth?**

`LICENSE` is the legal source of truth. `docs/LEGAL_BOUNDARIES.md` is a
boundary map only.
