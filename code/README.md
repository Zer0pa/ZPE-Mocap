# Code Surface

Install with:

```bash
python -m pip install -e ./code
```

Optional extras:
- `gates` (Comet logging + zstandard comparator)
- `cmu` (BVH ingestion via `bvhio`)

Example with extras:

```bash
python -m pip install -e "./code[gates,cmu]"
```

Current core dependencies:
- `numpy`

Primary package:
- `zpe_mocap`

Current lightweight test entrypoint:

```bash
python -m unittest discover -s code/tests -v
```
