# Verdict: commit-000215-001

Reviewer: Fable (independent reviewer; file mailbox)
Run: `.teacher/runs/commit-000215-001`
Packet: `.teacher/retrieval/000215-001`
Upstream: `4e493719fbbb25c91142a65bfbc56791f18ccaec` "Kludge for broken tensor keys (Gemma3)"
Request: `reviews/requests/commit-000215-001.md` (sha256 `58badf23186ed5c2945e48b74951013ca05782becb90087379b4889bc40cadf4`)
Reviewed: 2026-11-16, working tree on top of `39357a9`, machine `exdev-314`

## Decision

**APPROVED for ancestor retrieval only.** Canonical and training remain false.

Every statement I checked is true and the finding is true as stated. One consequence of the change, probably
its purpose, is missing (below).

## Artifacts reviewed (sha256)

Every hash listed in the request matches the file on disk.

## Run checks

| Check | Result |
|---|---|
| Run integrity | 11 of 11 ledger entries match the transcript, none uncited; final message equals the annotation; Markdown equals the render; full review; 44 of 44 implementation hashes; exactly 214 strict-ancestor entries; 3,067 blobs hash to their names; no evidence timestamp after the cutoff. |
| Replay | 11 of 11 recorded tool calls identical, including the `run` call. |
| Unassisted | Standing instructions byte-identical to 214/001's. Guidance 9. |
| No hindsight | No blob in the packet contains `reviews/verdicts` or a defect-ledger path. |
| Catalog | Sixteen open rows at 2025-06-01T23:51:47Z; my query agrees. One closed row by path alone. |
| The change | A one-entry table maps `multi_modal_projector.mm_input_projection_weight` to `multi_modal_projector.mm_input_projection.weight`. `read_header` collects matching keys, deletes each and reinserts its descriptor under the new name; `add_tensor_files` repeats the mapping when indexing, which is redundant after `read_header`. No architecture check; the old name is not kept. Correct. |
| Header and index agree | `list_tensors`, sizes and reads look up `header[key]` with the indexed key, so both had to change. Correct. |
| Finding: collision | If a header held both spellings, the reinsertion overwrites the canonical entry with the legacy one and the override counter never sees it. True; synthetic, with no affected file shown, as the entry says. |
| Execution | A standard-library transcription of the renaming; labelled. |

## Reviewer finding (not in the entry)

**The new name is written into converted models.** `Gemma3VisionModel.get_additional_compiled_tensors` lists every
tensor with the prefix `multi_modal_projector`, and `compile_model` copies each listed key from the source
collection into the output file under that same key. Before this commit a converted multimodal Gemma 3 model
kept the original spelling; from this commit it stores `multi_modal_projector.mm_input_projection.weight`. So the
change is not only an in-memory namespace: it alters the tensor name in conversion output, and models converted
before and after differ in that key (the reader normalises the old spelling either way). The entry searched for
the literal name and for "Gemma3" but not for the prefix consumer. Source reading only.

## Reviewer knowledge (never to a teacher)

The reference Gemma 3 checkpoints gathered at 164 do store the tensor as
`multi_modal_projector.mm_input_projection_weight`, so the spelling the commit targets is real. That evidence
belongs to an earlier position's bundle and was not in this packet.

## Not verified

- Any loading or conversion.

## Must fix before canonical use

1. State the conversion consequence above. The Impact sentence "changes the in-memory namespace, not … on-disk
   bytes" is true of the source files but reads as if nothing on disk is affected.

## Follow-ups

1. Ledger, with 216's request: the collision finding as suspected, classification as filed (behaviour change),
   introduced at `4e493719`, synthetic reach only.

## Next

1. Record this approval with `--approve`.
2. Proceed to 216.
