# Verdict: commit-000098-001

Reviewer: Fable (independent reviewer; file mailbox)
Run: `.teacher/runs/commit-000098-001`
Packet: `.teacher/retrieval/000098-001`
Upstream: `875e503e84ddf27441f551a2c7dc50982c8cd48c` "Add Cohere architecture"
Request: `reviews/requests/commit-000098-001.md`
Reviewed: 2026-11-14, working tree on top of `d0a2d08`, machine `exdev-314`

## Decision

**APPROVED for ancestor retrieval only.** Canonical and training remain false.

Every statement I checked is true. All ten configurations were read and each model is discussed by name. The entry
finds the real compatibility gap (the three Command R Plus models need query/key normalisation, which nothing
implements or rejects) and it claims nothing about tensors it did not read.

It read no tensor header. At commit 39 that hid the commit's central defect, so I did the comparison myself before
deciding (below). Here it hides nothing: the constructor's declarations match every full-precision checkpoint.

## Artifacts reviewed (sha256)

All hashes in the request match the files on disk.

## Run checks

| Check | Result |
|---|---|
| Run integrity | 32 of 32 ledger entries match the transcript, none uncited; final message equals the annotation; Markdown equals the render; full review; 40 of 40 implementation hashes; exactly 97 strict-ancestor entries; 1,418 blobs hash to their names; no evidence timestamp after the cutoff. |
| Replay | 32 of 32 recorded tool calls identical, including the ten mirror-backed config reads and the `run` call. |
| Unassisted | Standing instructions byte-identical to 97/001's. |
| No hindsight | No blob in the packet contains `reviews/verdicts` or a defect-ledger path. |
| Catalog | GitHub: open at the cutoff are 1, 4, 7, 10, 14, 15, 21, 22, 24. Matches the nine open rows. |
| Reference list | The ten models of the accepted mirror bundle (`modelscope-mirror-implementation-001`). The five uninspected gated repositories are recorded as such in discovery report 002. |
| Config claims | Recomputed from the bundle for all ten: hidden and intermediate widths, layer counts, query and key/value head counts, `logit_scale` (0.0625 for six, 0.125 for aya-expanse-8b, 0.8333… for the three Plus models), `use_qk_norm` (true for the three Plus models, false for five, absent for the two v01 models), `tie_word_embeddings` (true in v01, absent in v01-4bit). All as the draft says. |
| Constructor claims | Checked against `cohere.py`: the key names, the defaults (`num_key_value_heads` to the query count, `layer_norm_eps` 1e-5, `tie_word_embeddings` true, `logit_scale` 0.0625), GPTJ RoPE style, one `ParallelDecoderBlock` per layer with `LayerNorm`, `Attention` and `GatedMLP`, final `LayerNorm` at half precision, head with `post_scale = config.logit_scale` and the embedding as alternative key when tied and no `lm_head` tensor exists. Correct. |
| Inherited findings | The Cohere constructor always supplies all three block components and uses `GatedMLP`, so neither of 96's two findings is triggered here. Correct. |
| Finding | `cohere-qk-normalization`: correct. `CohereConfig` never reads `use_qk_norm`; `Attention` has no such step. Classified as external compatibility and suspected, which is right. |

## Reviewer-only: constructor against the checkpoints (not for any teacher)

From the 172 headers in the bundle I built the tensor list the constructor would ask for from each config and compared
names and shapes.

- **Eight full-precision models** (all but the two `-4bit`): every declared tensor exists with the declared shape. No
  missing tensor, no shape mismatch. All tensors are F16. None has an `lm_head` tensor, so the tied-embedding path is
  the one that runs, including for the seven whose config omits `tie_word_embeddings` and get the new default.
- **The three Plus models** additionally store `self_attn.q_norm.weight` `[96, 128]` and `self_attn.k_norm.weight`
  `[8, 128]` in every layer (64 each in the two full-precision ones). Nothing in the constructor consumes them. This is
  the tensor-level face of the entry's finding: the weights exist and are ignored.
- **The two `-4bit` models** are bitsandbytes-packed: projection weights are stored flattened (`[33554432, 1]`,
  `[75497472, 1]`) with `.absmax`, `.quant_map` and related tensors beside them. They cannot load through this
  constructor. The entry says storage compatibility is not shown; the headers show it is absent.
- All widths are multiples of 128, so the input-padding assertion from commit 88 does not fire for any of them.

## Not verified

- Whether GPTJ is the right RoPE layout for these models, and whether a parallel block with one shared LayerNorm is
  their real layer structure. Both would need the reference implementation, which is not in the evidence.
- Any load, conversion or generation.

## Must fix before canonical use

1. The entry reads no header. A canonical entry should state the tensor comparison above in its own words from its own
   reads: that the eight full-precision checkpoints match, that the Plus checkpoints carry unused `q_norm` / `k_norm`
   weights, and that the two 4bit repositories are a different storage format.
2. It says tied embeddings are explicit in v01 and defaulted in v01-4bit, and is silent on the other eight, which are
   all defaulted.

## Follow-ups

- Ledger: `cohere-qk-normalization` as a new suspected external-compatibility record at this commit. The unused
  `q_norm` / `k_norm` tensors are a reviewer observation on the same record.

## Next

1. Record this approval.
2. Continue the walk at commit 99.
