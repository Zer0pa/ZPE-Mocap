# 2026-04-24 Remote Custody

## Objective

Ensure ZPE-Mocap can be deleted locally and reconstructed from remote state without relying on this Mac.

## GitHub Custody

- Repo: `https://github.com/Zer0pa/ZPE-Mocap`
- Hygiene branch: `codex/h1-lane-hygiene-mocap`
- Authority branch: `chore/novelty-card-backfill-2026-04-22`
- Metadata recovery branch: `chore/true-sal-v7-restamp-2026-04-22`
- Custody release tag: `custody-zpe-mocap-2026-04-24`

Small, current planning artifacts are stored in-repo under `docs/_planning/`.

## External Artifact Custody

Large or out-of-repo artifacts are stored on the GitHub custody release because Hugging Face CLI auth failed on this Mac during the custody pass after:

```bash
unset HF_TOKEN
unset HUGGINGFACE_HUB_TOKEN
unset HF_HOME
hf auth whoami
```

Observed result:

```text
Error: Not logged in
```

## Restore Steps

1. Clone the repo:

   ```bash
   git clone https://github.com/Zer0pa/ZPE-Mocap
   cd ZPE-Mocap
   ```

2. Fetch the working branches you need:

   ```bash
   git fetch origin chore/novelty-card-backfill-2026-04-22
   git fetch origin codex/h1-lane-hygiene-mocap
   git fetch origin chore/true-sal-v7-restamp-2026-04-22
   ```

3. Download the assets from the `custody-zpe-mocap-2026-04-24` GitHub release and extract them next to the repo so the lane path shape is restored.

4. If you need the real-data retrieval benchmark exactly as executed on 2026-04-24, restore `external/cmu_github_mirror/` before rerunning the retrieval benchmark because the committed proof bundle records that corpus root.

## Notes

- The committed proof bundles remain authoritative.
- Playback or reconstruction authority is still not claimed.
- This file is operational custody metadata, not a product-facing truth surface.
