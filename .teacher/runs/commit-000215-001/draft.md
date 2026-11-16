# 4e493719fbbb25c91142a65bfbc56791f18ccaec


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/4e493719fbbb25c91142a65bfbc56791f18ccaec) · [Evidence ledger](draft.json)

Normalizes one Gemma3-related projector tensor spelling in parsed safetensors headers, keeping collection indexing and descriptor lookup consistent.

- [Normalize the projector key before indexing tensors](#loading-tokenization)

## Problem

The change addresses a tensor-name mismatch by mapping multi_modal_projector.mm_input_projection_weight to multi_modal_projector.mm_input_projection.weight. Previously, header keys were indexed verbatim. [source; call_7396e2704b144eadacb5d29d15fab305, call_269b558ce46e4a1aaf9e91747a060b29]

## Reasoning

Normalization belongs in the parsed header as well as the collection index: get_tensor, get_tensor_size and list_tensors use the indexed key to retrieve header[key]. Renaming only the index would leave those lookups inconsistent. [source; call_7396e2704b144eadacb5d29d15fab305, call_269b558ce46e4a1aaf9e91747a060b29]

## Impact

The replacement applies globally to the exact matching name, without checking architecture. It changes the in-memory namespace, not tensor shapes, offsets or on-disk bytes; the original spelling is not retained as an alias. [source; call_7396e2704b144eadacb5d29d15fab305]

## Source Notes

The root loading-tokenization entry was read. It establishes the existing separation between Python name/offset interpretation and bulk tensor loading, and records limited header validation. Inspection of the parent and task diff shows that this change adds no file-bound or overlapping-range validation. [source; call_98efa572178847778eb7ea5c46a54987, call_269b558ce46e4a1aaf9e91747a060b29, call_7396e2704b144eadacb5d29d15fab305]

Issue #33, “Error converting model,” reports file-opening failures and later GLM sampling trouble; issue #38, “Error converting nvidia/Llama-3_1-Nemotron-Ultra-253B-v1,” reports a padding-size mismatch. Their connection here is inferred only from safetensors.py traceback overlap, not evidence that either motivated this key rename. [inference; call_8ec61a978436474a9ceddaec9c771d18, call_8f2937786f21458a9388167eb5cfdb11, call_352b0144b6a84bd8ac06786f5b3d6377, call_7396e2704b144eadacb5d29d15fab305]

<a id="loading-tokenization"></a>

## Normalize the projector key before indexing tensors

read_header first parses the JSON and records the payload start. It then collects matching key/value pairs before deleting and reinserting them, avoiding mutation during dictionary iteration. The original descriptor is reused unchanged. [source; call_7396e2704b144eadacb5d29d15fab305]

The sole direct read_header caller found is SafetensorsCollection.add_tensor_files. Its additional name-fix check is redundant for this mapping because read_header has already removed the old key. The stored header and tensor_file_map nevertheless agree, preserving the existing size, listing and tensor-read interfaces. [source; call_f57b6c10a8aa4f6bb61323af16fff34a, call_889a5777332441a5bc2a7113af7b50e7, call_269b558ce46e4a1aaf9e91747a060b29, call_7396e2704b144eadacb5d29d15fab305]

A bounded standard-library transcription verified descriptor identity and payload-offset preservation, idempotence, and the collision rule: if both spellings exist, the legacy spelling's descriptor replaces the canonical descriptor. This checks dictionary semantics, not repository I/O. [execution; call_2cc5d415c4584d82ad2fb37fe0dcd157]

## Authoring-time findings — pending review

### header-name-collision (suspected; behavior_change)

Normalization silently collapses two distinct header entries when both spellings exist.

Trigger: A scanned safetensors header contains both mapped spellings with different descriptors.

Expected: An ambiguous collision should be rejected or explicitly resolved rather than silently discarding the canonical descriptor.

Actual: read_header deletes the legacy key and unconditionally overwrites the canonical key with its descriptor. Collection override accounting cannot report this within-header collision because it sees only the normalized header.

Locations: 4e493719fbbb25c91142a65bfbc56791f18ccaec:exllamav3/loader/safetensors.py — read_header

Source evidence: call_7396e2704b144eadacb5d29d15fab305, call_269b558ce46e4a1aaf9e91747a060b29, call_f57b6c10a8aa4f6bb61323af16fff34a

scalar_transcription: Transcribed normalization selected the legacy descriptor when both keys were supplied. [call_2cc5d415c4584d82ad2fb37fe0dcd157]. Limits: Synthetic dictionary only; no affected checkpoint established. Reach is the inspected add_tensor_files → read_header path, not a demonstrated model failure.

## Uncertainty and limits

No real checkpoint loading, conversion or GPU execution was performed. The Python check transcribed only dictionary normalization.

The parent tree contains Gemma3 definitions but no literal mm_input_projection occurrence. The author's Gemma3 motivation is therefore not independently verified against an affected checkpoint or a model-specific consumer.

Whole-tree searches located the direct read_header caller and all file_headers references; dynamic or external consumers remain unestablished.
