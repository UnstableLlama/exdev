# Verdict: commit-000302-001 (teacher Sol, guidance 12, unassisted; no repair; architecture commit)

Reviewer: Fable. Date: 2026-11-17 (19:17 UTC). Upstream `d42d6238` "Add SmolLM3 architecture".
Run: `.teacher/runs/commit-000302-001`. Packet: `.teacher/retrieval/000302-001`.

## Decision

**Approved for ancestor retrieval only. 302/001 is the entry in force for commit 302.** Canonical and
training stay false. One finding accepted as a new identity: `base-config-missing-rope-mask`. Clear the
recovery stop against this verdict and resume at 303.

The entry makes the central checks itself, and they equal my own pass over the same packet made before the
request arrived: all three configs, both two-shard headers of 3B and Base (326 BF16 tensors each, no
`lm_head`, no biases, K/V [512, 2048]), the meaning of `no_rope_layers` (RoPE where the entry is 1, so
layers 3, 7, ..., 35 are unrotated), that the list is read and not derived from the interval, and that the
Base config has only `no_rope_layer_interval` and therefore fails the `no_default` read before
construction. It keeps the ONNX repository at the configuration boundary.

## Artifacts

Request hashes match (18 of 18). `check.py` clean: `gpt-6.1-sol` medium, 45 implementation hashes equal to
the accepted set, 44 evidence calls all cited and none bad, replay 44 of 44, final equals annotation, 301 of
301 ancestors, 4357 blobs, nothing after the cutoff. Complete packet, ran ahead of nothing, first-packet
route as authorised.

## Run checks (mine)

Diff read in full. From the packet's blobs: Base config has no `no_rope_layers`, no `layer_types`,
`tie_word_embeddings` true; 3B and ONNX have the 36-entry list with zeros at every fourth index and no
`tie_word_embeddings` key; names of the two header sets are identical. `attn.py` builds RoPE only when
settings are given (line 225) and rotates only when it exists. All as the entry states.

## Must fix before canonical use

The constructor tests `has_tensor("lm_head")`, not `lm_head.weight` (the same pattern as `mistral3.py`,
reviewer observation, still not stated by any entry). Harmless for these checkpoints, which have no head
tensor; a canonical entry should say what that test can and cannot detect.
