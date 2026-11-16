# Verdict: commit-000198-001

Reviewer: Fable (independent reviewer; file mailbox)
Run: `.teacher/runs/commit-000198-001`
Packet: `.teacher/retrieval/000198-001`
Upstream: `40cfec594e0063ed6f31f58318dc058e93aed13a` "Histogram utility function"
Request: `reviews/requests/commit-000198-001.md` (sha256 `97203f10465f8ede859fead5ca2ae6df70931031d66357306b4ff994cc16aa63`)
Reviewed: 2026-11-16, working tree on top of `e9e83ff`, machine `exdev-314`

## Decision

**APPROVED for ancestor retrieval only.** Canonical and training remain false.

Every statement I checked is true, the finding is true as stated, and the fix attribution is true.

## Artifacts reviewed (sha256)

Every hash listed in the request matches the file on disk.

## Run checks

| Check | Result |
|---|---|
| Run integrity | 19 of 19 ledger entries match the transcript, none uncited; final message equals the annotation; Markdown equals the render; full review; 44 of 44 implementation hashes; exactly 197 strict-ancestor entries; 2,898 blobs hash to their names; no evidence timestamp after the cutoff. |
| Replay | 19 of 19 recorded tool calls identical, including the `run` call and the eight fetches. |
| Unassisted | Standing instructions byte-identical to 197/001's. Guidance 8. |
| No hindsight | No blob in the packet contains `reviews/verdicts` or a defect-ledger path. |
| Catalog | Fifteen open rows at 2025-05-30T09:20:45Z; my query agrees. One closed row (issue 6) qualifies by path alone through `rope.py`; the entry labels all discussion links as inferred. |
| The new function | Float32 or half input, `kLong` output (the comment says uint64), bins from `output.numel()`, at most 1,024; one block of 1,024 threads; shared 64-bit counters cleared, incremented atomically, copied out. Bound as `histogram`. Correct. |
| Binning | Truncation of the scaled value, clamped to the end bins; `exclusive` drops values strictly outside and keeps both endpoints. Correct. |
| Worked example | Four bins on [-1, 1] over seven samples: [2, 1, 1, 3] and, exclusive, [1, 1, 1, 2]. I worked both by hand and agree. 1,024 counters are 8,192 bytes; 65,536 states over 1,024 threads are 64 each. |
| Optional reference | `OPTPTR` gives a null pointer for an absent tensor; the kernel skips the whole reference pass under it; bins now come from `dist_output`; unequal reference length is rejected. Header and definition agree. Correct. |
| Callers | No Python caller of `histogram`; the only `test_distribution` call is the commented five-argument one in `quantize.py`. Correct. |
| Fix attribution | At 62 the finding was that bins came from `ref_output` alone, so a shorter `dist_output` was overrun (`commit-000062-001.md`). Bins now come from `dist_output`. True. |
| Finding: zero bins | With an empty output only `num_bins <= MAX_BINS` is checked; `idx >= num_bins` compares unsigned, 0 >= 0 holds, `num_bins - 1` wraps and becomes index -1 into the shared array. True. |
| Execution | One standard-library model of the binning and two multiplications; labelled as a model. |
| `rope.py` | Comment only. Correct. |

## Reviewer knowledge (hindsight, never to a teacher)

Upstream `347e80c7` (2026-10-08) "Extensions: Consistent empty-input policy …" later touches this file; I have
not read whether it covers the zero-bin case.

## Not verified

- Any build or GPU execution.

## Must fix before canonical use

1. The entry says the undersized-`dist_output` case is removed "for non-null reference buffers". It is removed
   in both modes: the write length is `dist_output`'s own size whether or not a reference is passed.
2. Minor: the new function's header comment is copied from the diagnostic ("Compare tensor distribution to
   codebook"); the output's device and both tensors' contiguity are unchecked, as noted for the diagnostic at 62.

## Follow-ups

1. Ledger: the zero-bin finding may be filed as suspected, introduced at `40cfec59`. The 62 capacity record may
   take this commit as its fix. Earlier owed items stand.

## Next

1. Record this approval with `--approve`.
2. Proceed to 199.
