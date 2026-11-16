# Verdict: commit-000161-001

Reviewer: Fable (independent reviewer; file mailbox)
Run: `.teacher/runs/commit-000161-001`
Packet: `.teacher/retrieval/000161-001`
Upstream: `48747ba09dee3ec78964653df0eb926c53f41c2e` "Fix: Don't (try to) apply full-width padding when loading partial tensors"
Request: `reviews/requests/commit-000161-001.md`
Reviewed: 2026-11-15, working tree on top of `d980d21`, machine `exdev-314`

## Decision

**APPROVED for ancestor retrieval only.** Canonical and training remain false.

Every statement I checked is true. No findings in the entry, and none are missing from what a teacher could see.
This is a good one: it traces weight and bias through the loader and the constructor, says that the whole tensor
is still read and only then sliced, reads the 119 entry that introduced loader-side padding, and names the case
it did not establish (a sliced shape that also needs alignment padding).

Ledger revision `exllamav3-sliced-fp16-padding-target--r003` is **accepted**. One further revision is asked for
(follow-up 1).

## Artifacts reviewed (sha256)

Every hash listed in the request matches the file on disk.

## Run checks

| Check | Result |
|---|---|
| Run integrity | 15 of 15 ledger entries match the transcript, none uncited; final message equals the annotation; Markdown equals the render; full review; 43 of 43 implementation hashes; exactly 160 strict-ancestor entries; 2,490 blobs hash to their names; no evidence timestamp after the cutoff. |
| Replay | 15 of 15 recorded tool calls identical, including the `run` call. |
| Unassisted | Standing instructions byte-identical to 160/001's. |
| No hindsight | No blob in the packet contains `reviews/verdicts`, a defect-ledger path or the tracking files. |
| Cutoff, and it is close | The commit's committer date is 2025-05-14T23:28:24Z. The maintainer's first comment on issue 38, which explains the cause, is at 23:35:22Z, seven minutes later, and is not in the packet. The entry has only the issue body and labels its link to this fix as inference from the traceback. Correct. |
| Catalog | Thirteen open rows; four closed rows (issues 8, 11, 16 and one more by terms), three by path alone, all selected, nothing cut. |
| Architecture trigger | Does not fire. |
| The change | In `Linear.load_fp16`, both `get_tensor` calls pass `pad_to` only when the module is not sliced, and `None` when it is. Two lines. The fused-weight branch and `load_exl3` are untouched. Correct. |
| Why it works | Before: a sliced linear asked the loader to pad to its own slice size, and the loader allocated that size and copied the full checkpoint tensor into it. After: the full tensor arrives on the CPU and `LinearFP16.__init__` cuts rows or columns by `first_*` and the local size, cuts the bias with the output columns, copies the slice to its own storage, and `unswap_cpu` moves it to the device. Correct. |
| Slices | `GatedMLP` slices gate and up along output features and down along input features, with full sizes and offsets. Correct. |
| Execution | Recorded output: eight slices of 49,920 in 399,360, remainder 0, slice width divisible by 128. Matches the prose. |
| Source notes | Issues 8, 11, 16, 33 and 34 described by their own failures and said to be unrelated. Correct. |

## Ledger

- `exllamav3-sliced-fp16-padding-target--r003`: accepted. Introduced at `647bb7d5` (119), fixed at `48747ba0`
  (161), confirmed by my reading of the two changed lines against the record's mechanism. The wording note from
  156 is applied. Treat the fix status as reviewer-confirmed by source inspection; nothing was executed.

## Reviewer-only notes (never to a teacher)

- **This fix makes the 154 observation reachable.** `eval/model_diff.py` still brackets every module in a
  deferred load without asking `can_defer_load()`. Until now an unquantized model with a sliced MLP failed
  earlier, on the padding mismatch, so the bracket could not matter. From this commit that load succeeds: the
  sliced linear's `get_tensor` call has no `no_defer`, so in deferred mode the weight is allocated and queued,
  `LinearFP16.__init__` cuts and copies the slice from memory that has not been read yet, and the flush later
  fills a tensor nobody uses. The comparison would then run on uninitialised weights for those layers, silently.
  The usual use of that script is a quantized model against its unquantized original, so the original is exactly
  where this lands. Source reading only.
- The entry's stated limit is real: a sliced linear whose kept dimension is not a multiple of 128 is no longer
  padded by anyone. The slice widths `GatedMLP` chooses are multiples of 128, so this needs a hidden size that is
  not; none of the registered reference models has one.
- Hindsight confirmed: this is the fix I expected after issue 38. The other two records from 119 (the variant
  collection's missing keywords, fused FP32 weights no longer halved) are not touched by it.

## Not verified

- Any model load or conversion.

## Must fix before canonical use

None for this entry.

## Follow-ups

1. Ledger, `exllamav3-model-diff-unconditional-deferral`: file r003. From `48747ba0` the masking described in
   r002 is gone; add 161 as an affected revision with the mechanism in the first reviewer note, and state the
   reach: `eval/model_diff.py` with an unquantized model whose MLP is sliced. Still suspected, source inspection
   only, excluded from teacher input.
2. The remaining older ledger revisions are still owed.

## Next

1. Record this approval and the ledger acceptance.
2. As agreed: part E (`token-cost-detach-001`) before 162, or 162 directly if you judge part E unsound and say
   why in a short request.
