# Verdict: commit-000216-001

Reviewer: Fable (independent reviewer; file mailbox)
Run: `.teacher/runs/commit-000216-001`
Packet: `.teacher/retrieval/000216-001`
Upstream: `27c13b11e32af575c9684dd3d2905c55ef6eab9a` "Enable indexed embeddings"
Request: `reviews/requests/commit-000216-001.md` (sha256 `2f4678f719ee3fa2262c0605b584d934e30aa01a74a1e70cf2c592ba9c0165cf`)
Reviewed: 2026-11-16, working tree on top of `39357a9`, machine `exdev-314`

## Decision

**APPROVED for ancestor retrieval only.** Canonical and training remain false.

Every statement I checked is true and the finding is true as stated. One latent change in the embedding
module's dtype handling is missing (below). The ledger item filed with this request is accepted.

## Artifacts reviewed (sha256)

Every hash listed in the request matches the file on disk.

## Run checks

| Check | Result |
|---|---|
| Run integrity | 23 of 23 ledger entries match the transcript, none uncited; final message equals the annotation; Markdown equals the render; full review; 44 of 44 implementation hashes; exactly 215 strict-ancestor entries; 3,078 blobs hash to their names; no evidence timestamp after the cutoff. |
| Replay | 23 of 23 recorded tool calls identical, including the `run` call. |
| Unassisted | Standing instructions byte-identical to 215/001's. Guidance 9. |
| No hindsight | No blob in the packet contains `reviews/verdicts` or a defect-ledger path. |
| Catalog | Sixteen open rows at 2025-06-01T23:54:25Z; my query agrees. Five closed rows, three by path alone, none cut. |
| The container | IDs are handed out from 1,000,000,000 by a process-wide allocator; an `MMEmbedding` reserves one per embedding row, overwrites the `-1` placeholders of the caller's token template in place, and keeps row 0 of it as the token list; the default alias contains the first ID. Correct. |
| Tokenizer | With embeddings supplied, the text is split on the escaped aliases and each alias is replaced by its token list; `encode` passes the list through in both branches; `re` is already imported. Correct. |
| Generator and job | `generate` takes one list for a single prompt or one per prompt; `Job` keeps the list (default empty); the main model's prefill and the batched forward pass both receive `indexed_embeddings`. Correct. |
| Embedding lookup | With an active range it allocates an uninitialised output, fills ordinary positions from the table, scales by the square root of the width if the module normalises, then writes the supplied rows unscaled; IDs at or above one billion that belong to no supplied container stay uninitialised. With no active range it takes the old path. Correct. |
| Finding: draft prefill | `Generator.iterate` calls `job.prefill` (line 278) before `iterate_draftmodel_gen` (282), where the new assertion is; `Job.prefill` calls `draft_model.prefill` without `indexed_embeddings`, so the draft model's embedding table is indexed with IDs from one billion. True, with the stated conditions. |
| Execution | A standard-library model of the ID ranges and alias substitution; labelled. |

## Reviewer finding (not in the entry)

`Embedding.forward` now begins with `out_dtype = out_dtype or self.out_dtype or x.dtype`, evaluated while `x` is
still the integer ID tensor. Before, a module with no output dtype and a call with none returned the table's own
dtype (`to2` with two `None`s does nothing). Now that case resolves to the IDs' integer dtype and the
embeddings would be cast to integers on both paths. No constructor in the tree reaches it: the parameter
defaults to `torch.float` and none of the eleven model definitions overrides it. Latent, source reading only.

## Not verified

- Any tokenizer, model or GPU execution; device agreement between supplied embeddings and the module.

## Must fix before canonical use

1. State the dtype fallback above and that it is unreachable from the tree's own constructors.

## Ledger items filed with this request

- `exllamav3-header-name-collision--r001`: **accepted.** Suspected, behaviour change, introduced at `4e493719`,
  synthetic reach only, no fix.

## Follow-ups

1. Ledger, with 217's request: the draft-prefill finding as suspected, introduced at `27c13b11`.

## Next

1. Record this approval with `--approve`.
2. Proceed to 217.
