# Verdict: commit-000178-001

Reviewer: Fable (independent reviewer; file mailbox)
Run: `.teacher/runs/commit-000178-001`
Packet: `.teacher/retrieval/000178-001`
Upstream: `02982fcc9fed57a8e5b2bdf55cdceb12cc70f594` "Sampler: Skip some asserts"
Request: `reviews/requests/commit-000178-001.md` (sha256 `5da39df4a257760f4ffe0e6d691700e7ccf838c7e383dd364fcab079d17425ad`)
Reviewed: 2026-11-15, working tree on top of `0ed73a1`, machine `exdev-314`

## Decision

**APPROVED for ancestor retrieval only.** Canonical and training remain false.

Every statement I checked is true. The entry says what the removed checks tested, shows that the one active
caller already enforces the same conditions, and does not claim a measured speedup.

## Artifacts reviewed (sha256)

Every hash listed in the request matches the file on disk.

## Run checks

| Check | Result |
|---|---|
| Run integrity | 9 of 9 ledger entries match the transcript, none uncited; final message equals the annotation; Markdown equals the render; full review; 44 of 44 implementation hashes; exactly 177 strict-ancestor entries; 2,720 blobs hash to their names; no evidence timestamp after the cutoff. |
| Replay | 9 of 9 recorded tool calls identical, including the `run` call. |
| Unassisted | Packet version 8. Standing instructions equal 177/001's plus a blank line and the adopted fourth paragraph, exactly. First walk run under guidance 8. |
| No hindsight | No blob in the packet contains `reviews/verdicts` or a defect-ledger path. |
| Catalog | Thirteen open rows at 2025-05-23T21:33:20Z; my query agrees. Two closed rows, one by path alone, both selected; issue 12 is described as a path overlap only. |
| The change | Three `assert` lines in `Job.receive_logits` become comments. Nothing else changes. Correct. |
| What they tested | Batch size equal to the sequence count; `is_prefill_done()`, which is `kv_position == len(sequence_ids) - 1` for every sequence; every sequence live. Correct. |
| Caller | `Generator.iterate_gen` is the one active caller (a second call is commented out). It skips jobs that are not prefill-done when building the batch, skips empty row ranges, and passes one token position per call. Correct. |
| Inherited finding | The `return_probs` and `return_top_tokens` branches contain only `pass`, so the returned names are unset when either is enabled. Unchanged. True. |
| Execution | A three-case transcription of those assignments; labelled as such. |

## Not verified

- Any generation run or timing. `job.py` and `generator.py` were read in part by the teacher; the request says
  so, and the parts relied on are within the bytes read.

## Must fix before canonical use

None for this entry.

## Ledger: a correction to my last three verdicts

I wrote that the sorted-argmax and cost-buffer "records" gain affected revisions. Astra's search is right: no
ledger identity exists for either; they are findings in the root entry that predate the ledger. So:

1. File both as **new** identities, introduced at `543c4b27`, suspected, source-only, with the root entry and the
   176 and 177 entries as evidence. Affected revisions: the root plus `d359bcc0` for cost-buffer, the root plus
   `8b0df691` for sorted-argmax. Nothing is being replaced.
2. The optional-output finding here is in the same position; file it the same way with `02982fcc` as affected,
   or leave it for the batch of older ledger work. Either is acceptable.
3. The three 174 identities are still owed.

## Next

1. Record this approval with `--approve`.
2. Proceed to 179.
