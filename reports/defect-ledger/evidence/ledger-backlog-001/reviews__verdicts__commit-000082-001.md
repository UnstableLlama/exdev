# Verdict: commit-000082-001

Reviewer: Fable (independent reviewer; file mailbox)
Run: `.teacher/runs/commit-000082-001`
Packet: `.teacher/retrieval/000082-001`
Upstream: `702ebab361d2d07f513bc8702fe46f49dcd69608` "Add sampler test cases"
Request: `reviews/requests/commit-000082-001.md`
Reviewed: 2026-11-14, working tree on top of `d0a2d08`, machine `exdev-314`

## Decision

**APPROVED for ancestor retrieval only.** Canonical and training remain false.

Every statement I checked is true, and the finding is real: the new test-only sampling step returns a column position
where a sorted pipeline needs a token id, and none of the new cases would notice.

## Artifacts reviewed (sha256)

All hashes in the request match the files on disk.

## Run checks

| Check | Result |
|---|---|
| Run integrity | 11 of 11 ledger entries match the transcript, none uncited; final message equals the annotation; Markdown equals the render; full review; 39 of 39 implementation hashes; exactly 81 strict-ancestor entries; 1,171 blobs hash to their names; no evidence timestamp after the cutoff. |
| Replay | 11 of 11 recorded tool calls identical, including the `run` call. |
| Unassisted | Standing instructions byte-identical to 81/001's. |
| No hindsight | No blob in the packet contains `reviews/verdicts` or a defect-ledger path. |
| Catalog | GitHub: open at the cutoff are 1, 4, 7, 10, 14, 15, 20. Matches the seven open rows. |
| `SS_Sample_mn` | Subclass of `SS_Sample`, exported. `run` accepts `PROBS_N_S` and `PROBS_N` only, calls `torch.multinomial(state.probs, num_samples = 1)`, sets `DONE`. `prep` returns `[SS_Normalize]` for `INIT`, `LOGITS`, `PROBS`, `LOGITS_S`, `PROBS_S`. Correct. |
| `return_state` | New keyword, default false. The final assertion becomes `return_state or state == DONE`; the per-step assertion against running after `DONE` is untouched. Returns the state object when set. Correct. |
| Test cases | Four cases as described: temperature 0.75 then top-p 0.95; min-p 0.16; sort then min-p 0.16; top-k 5 with no sampling step. Comparisons slice to the expected width; no case has `expect_sample`. The two histogram tests gain `.unsqueeze(-1)`. Correct. |
| Fixture arithmetic | Because construction-time planning always asks `prep` about `INIT`, a normalise step is inserted before `SS_Sample_mn` in every case, so the inspected probabilities are renormalised after filtering. The fixture rows sum to 1 (0.79139 + 0.20861; 0.10154 + 0.16741 + 0.27600 + 0.45505), which agrees with that and with the teacher's transcription. |
| Finding | `multinomial-sorted-token-mapping`: correct. `SS_Sample` maps sorted positions through `state.indices`; `SS_Sample_mn` does not. Two of the three new uses run on sorted distributions. Suspected is the right status; reach is the tests only, as stated. |

## Not verified

- The tests themselves. They need a GPU at `cuda:2`; nobody ran them and the entry says so.

## Must fix before canonical use

Reviewer-only.

1. The entry does not say that `torch.multinomial` returns shape `(rows, 1)` where the other sampling branches produce
   `(rows,)`, nor that `expect_sample`, if a case ever used it, is built as a float tensor. Both are small; neither is
   wrong in the entry.

## Next

1. Record this approval.
2. Continue the walk at commit 83.
