# ZPE-Mocap Novelty Card

**Product:** ZPE-Mocap
**Domain:** Skeletal motion trajectories and BVH-derived joint-motion streams.
**What we sell:** Motion fingerprint compression and retrieval for BVH archives where searchability matters more than playback-grade reconstruction.

## Novel contributions

1. **Dual-plane motion tokenization over local skeletal deltas** — The codec converts parent-relative local motion deltas into paired 8-way XY/XZ direction tokens plus millimeter magnitudes, rather than storing a conventional pose stream verbatim. That gives the lane a compact motion-fingerprint representation that is stable enough for deterministic retrieval while still decoding back into bounded motion structure. Code: [code/zpe_mocap/codec.py](../../../code/zpe_mocap/codec.py#L28), [code/zpe_mocap/codec.py](../../../code/zpe_mocap/codec.py#L145), [code/zpe_mocap/constants.py](../../../code/zpe_mocap/constants.py#L13). Nearest prior art: chain-code style directional quantization and motion-descriptor compression. What is genuinely new here: the specific use of paired XY/XZ directional tokens and magnitude channels on local skeletal deltas inside this Mocap codec.
2. **Deterministic hierarchical payload packaging for motion fingerprints** — The encoder packages rest pose, parent-relative token streams, periodicity metadata, and mirror-group hints into a deterministic `ZPMOC` payload with a stable digest and a fixed segment layout. That is the repo’s core transport format, not just a benchmark wrapper. Code: [code/zpe_mocap/codec.py](../../../code/zpe_mocap/codec.py#L175), [code/zpe_mocap/codec.py](../../../code/zpe_mocap/codec.py#L186). Nearest prior art: conventional binary container design and skeletal animation serialization. What is genuinely new here: the exact segmentation and metadata scheme used to carry this lane’s motion-token representation as a deterministic codec payload.
3. **Token-stream retrieval index for motion search** — The retrieval surface does not search raw BVH poses directly. It searches interleaved motion-token streams through a deterministic suffix-like k-gram index that is coupled to this codec’s representation. Code: [code/zpe_mocap/search.py](../../../code/zpe_mocap/search.py#L9), [code/zpe_mocap/search.py](../../../code/zpe_mocap/search.py#L80). Nearest prior art: inverted-index and k-gram retrieval systems. What is genuinely new here: the use of the lane’s interleaved XY/XZ motion tokens as the retrieval primitive for skeletal motion fingerprints.

## Standard techniques used (explicit, not novel)

- `zlib` compression
- SHA-256 digests
- JSON metadata packing
- uint8/int16 binary segment storage
- k-gram inverted indexing
- BVH parsing and fixture ingestion
- simple scale-space retargeting helper

## Compass-8 / 8-primitive architecture

YES — this lane uses an 8-way directional tokenization mechanic in [code/zpe_mocap/codec.py](../../../code/zpe_mocap/codec.py#L28) backed by [code/zpe_mocap/constants.py](../../../code/zpe_mocap/constants.py#L13). It is specific to this Mocap codec’s local motion-delta representation, not a portfolio-wide substrate claim.

## Open novelty questions for the license agent

- Should periodicity and mirror-group metadata remain part of the core motion-token codec contribution, or be scheduled as separate auxiliary novelty items?
- Should the retrieval index be scheduled as a distinct novelty item, or only as an ancillary component of the core motion-fingerprinting codec?
