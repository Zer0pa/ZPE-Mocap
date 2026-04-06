## A2 Skip Record

Date: 2026-04-06

The action brief pins these Hugging Face dataset IDs:

- `EvanTHU/HumanML3D`
- `EvanTHU/KIT-ML`
- `Motion-X`
- `AMASS`

Access attempts against the exact pinned IDs were not executable in-lane:

- `https://huggingface.co/datasets/EvanTHU/HumanML3D` returned `401 Unauthorized`
- `https://huggingface.co/datasets/EvanTHU/KIT-ML` returned `401 Unauthorized`
- `https://huggingface.co/datasets/Motion-X` redirected to `https://huggingface.co/Motion-X/datasets`, which is an org page rather than a dataset repo
- `https://huggingface.co/datasets/AMASS` redirected to `https://huggingface.co/amass/datasets`, which is an org page rather than a dataset repo

Environment check in the repo venv also showed that neither `datasets` nor `huggingface_hub` is installed. I did not add new dependencies or substitute different dataset IDs because the brief pins the identifiers above and the task rule allows skipping when the download surface is stale or fails.

Result: A2 skipped pending corrected dataset repository IDs or working access credentials.
