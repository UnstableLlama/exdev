# Verdict: commit-000177-001

Reviewer: Fable (independent reviewer; file mailbox)
Run: `.teacher/runs/commit-000177-001`
Packet: `.teacher/retrieval/000177-001`
Upstream: `8b0df6910382b84fd9225353c2eb4cd2708482fb` "Sampler: Don't set torch/random seed unless it's needed"
Request: `reviews/requests/commit-000177-001.md` (sha256 `cf0216e31b59a871bd26d41079687376aa6d2b49001a7637a0d9d8520eecaf5c`)
Reviewed: 2026-11-15, working tree on top of `0ed73a1`, machine `exdev-314`

## Decision

**APPROVED for ancestor retrieval only.** Canonical and training remain false.

Every statement I checked is true. The entry notes that the base-class edit supplies the attribute the
constructor edit needs, and carries the root entry's sorted-argmax finding correctly as inherited.

Ledger candidate `exllamav3-two-multiplier-resume-inconsistency--r001` is **accepted** (reviewer-originated,
suspected, source-only; its text matches the 176 verdict).

## Artifacts reviewed (sha256)

Every hash listed in the request matches the file on disk.

## Run checks

| Check | Result |
|---|---|
| Run integrity | 19 of 19 ledger entries match the transcript, none uncited; final message equals the annotation; Markdown equals the render; full review; exactly 176 strict-ancestor entries; 2,710 blobs hash to their names; no evidence timestamp after the cutoff. |
| Implementation hashes | 43 of 44 match the files on disk. `teacher/walk_inputs.py` differs because the adoption default (7 to 8) was applied at 21:19:24, after this run's validation report (21:18:20). The run's recorded implementation hashes are identical to 176/001's. The run did not use the changed file. |
| Replay | 19 of 19 recorded tool calls identical, including the `run` call. |
| Unassisted | Standing instructions byte-identical to 176/001's. Guidance 7, the last commit under it. |
| No hindsight | No blob in the packet contains `reviews/verdicts` or a defect-ledger path. |
| Catalog | Thirteen open rows at 2025-05-23T21:33:20Z; my query agrees. No closed row qualifies. |
| The change | `Sampler.__init__` sets `reqs_torch_seed = False`; `SS_Base.reqs_torch_seed()` returns False and `SS_Sample_mn` overrides it to True; `CustomSampler.__init__` ORs the steps' answers, from the supplied steps before alternatives and prerequisites; `forward` reseeds Torch and Python only when a seed is given and the flag is set. Correct. |
| Why the split | `SS_Sample` passes `rand_u32` to the native Gumbel-noise functions in every branch; `SS_Sample_mn` calls `torch.multinomial` with no generator. Correct. |
| Callers | `Job` passes `self.rng.randint(0, (1<<32)-1)` positionally on each call; none of the six preset classes uses `SS_Sample_mn`; the tests that do pass `rand_u32 = 0`. Correct. |
| Omitted seed | With no `rand_u32` the value is drawn from Python's generator and nothing is reseeded, also for multinomial chains. Correct. |
| Execution | Recorded output matches the prose for all four cases. A transcription with a recorder, as labelled. |
| Inherited finding | In `SS_Argmax.run` the two sorted branches assign to `state.state`, which the next line overwrites with `DONE`; `state.sample` is never set. Unchanged. True. |

## Not verified

- Any tensor execution, generation or timing.
- `exllamav3/generator/job.py` was read in one window only by the teacher; the call it relies on is in that window.

## Must fix before canonical use

None for this entry.

## Follow-ups

1. Ledger: the sorted-argmax record gains `8b0df691` as an affected revision; the cost-buffer affected revision and
   the three 174 identities are still owed.
2. `guidance-8-adoption-001` is expected next. No 178 before it is accepted.

## Next

1. Record this approval with `--approve`.
2. File the adoption request.
