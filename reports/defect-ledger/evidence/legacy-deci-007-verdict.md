# Verdict: commit-000039-007

Reviewer: Fable (independent reviewer; file mailbox)
Run: `.teacher/runs/commit-000039-007`
Packet: `.teacher/retrieval/000039-006` (shared with 006, as authorized)
Upstream: `75c7366bb2e2a7671e38d079f9e5f54945b78006` "Support DeciLM (Nemotron)"
Request: `reviews/requests/commit-000039-007.md`
Reviewed: 2026-11-14, working tree on top of `d0a2d08`, machine `exdev-314`

## Decision

**REJECTED.** It contains a statement that is false, labelled as source. No coverage request; no further attempt.

**39/005 stays the entry in force. Commit 39 is held for the user; the walk is not.** Resume at commit 75.

Canonical and training remain false.

## The false statement

> nvidia/Llama-3_1-Nemotron-Ultra-253B-CPT-v1 and nvidia/Llama-3_1-Nemotron-Ultra-253B-v1 each supply 16384 hidden
> width, 128 query heads, sixteen KV heads on active attention ... these configuration values fit the builder's
> corresponding mappings

The configurations do not state a key/value head count. They have `n_heads_in_group: 16`. The draft read that field the
way the code under review reads it and reported the result as a fact about the models. Every `k_proj` stored for both
Ultra models is `[1024, 16384]`, which is 8 heads of 128, not 16. The run read no tensor header, and the draft says so,
but the limit does not withdraw the claim. This is the error 39/004 was rejected for.

The same sentence for Super ("eight KV heads") is true only because 64 / 8 = 8.

It also has no head-count finding, and the older-Deci incompatibility is prose only, not a structured finding. Your
request describes all three points accurately.

## Artifacts reviewed (sha256)

All fourteen hashes in the request match. Provenance is byte-identical to 006's, as expected for the same packet and
implementation.

## Run checks

| Check | Result |
|---|---|
| Run integrity | 39 of 39 ledger entries match the transcript, none uncited; final message equals the annotation; Markdown equals the render; full review; 39 of 39 implementation hashes; 38 strict ancestors; 768 blobs hash to their names. (`check.py` assumes the packet is named after the attempt; I pointed it at `000039-006`.) |
| Replay | 39 of 39 recorded tool calls identical on this machine. |
| Unassisted | Standing instructions byte-identical to 006's. The transcript contains no coverage-request field and nothing from the 006 verdict. |
| Tool use | 12 config fetches, 9 repository reads, 0 tensor headers. |
| Empty-block finding | Correct, suspected, same hazard 005 and 006 report. |
| Deci prose | True: five use `num_key_value_heads_per_layer`, the GGUF config a global count, none has `block_configs`. |

Reference list, catalog and parent-tree facts are unchanged from the 006 review and were not rechecked.

## Dependents

None affected; nothing is superseded. 44/003 continues to read the head-count defect from 39/005.

## For the user

Commit 39 has now had two unassisted attempts on the Deci packet. Neither kept the head-count defect, because neither
compared tensor headers on a model where the bug shows. 39/005 (assisted, NVIDIA only) has it. The open question is
recorded in my notes and put to the user; it does not block the walk.

## Follow-ups (reviewer-only; none of this goes to a teacher)

- The older-Deci incompatibility is correct in both 006 and 007 and is in no entry in force. Record it in the defect
  ledger as an external-compatibility observation at commit 39, source run 39/006 (`legacy-decilm-config`).
- `reviews/fable/check.py` should take the packet path from the request when it differs from the attempt name. Mine to fix.

## Next

1. Record this rejection. 39/005 remains in force; 006 and 007 stay rejected on record.
2. Make the ledger entry above.
3. Resume the walk at commit 75. File it and wait for my verdict as usual.
