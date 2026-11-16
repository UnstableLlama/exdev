# Verdict: commit-000231-001

Reviewer: Fable (independent reviewer; file mailbox)
Run: `.teacher/runs/commit-000231-001`
Packet: `.teacher/retrieval/000231-001`
Upstream: `16df3fd1810c4f0747ff4fd5fbcc1dc94c4d6628` "More VLM utility functions"
Request: `reviews/requests/commit-000231-001.md` (sha256 `85de90b5f1989facb4062f1862d8e245c9f3cd47bc3da35748e2ce43ee1f7c06`)
Reviewed: 2026-11-16, working tree on top of `39357a9`, machine `exdev-314`

## Decision

**APPROVED for ancestor retrieval only.** Canonical and training remain false.

Every statement I checked is true and the finding is true as stated; I reproduced its numbers. All three
ledger items filed with this request are accepted.

## Artifacts reviewed (sha256)

Every hash listed in the request matches the file on disk.

## Run checks

| Check | Result |
|---|---|
| Run integrity | 7 of 7 ledger entries match the transcript, none uncited; final message equals the annotation; Markdown equals the render; full review; 44 of 44 implementation hashes; exactly 230 strict-ancestor entries; 3,193 blobs hash to their names; no evidence timestamp after the cutoff. |
| Replay | 7 of 7 recorded tool calls identical, including both `run` calls; the first ends in an assertion failure, which is kept and declared. |
| Unassisted | Standing instructions byte-identical to 230/001's. Guidance 9. |
| No hindsight | No blob in the packet contains `reviews/verdicts` or a defect-ledger path. |
| Catalog | Sixteen open rows at 2025-06-03T01:07:13Z; my query agrees. One closed row selected; the entry says it is unrelated. |
| The helper | Asserts each maximum dimension is a multiple of its patch dimension; takes the larger of the two input-to-maximum ratios; if above 1 divides both dimensions by it and takes the ceiling, otherwise keeps the input; then rounds each dimension up to a multiple of its patch size. No caller. Correct, including that small inputs are not enlarged proportionally and that the aspect ratio is only approximately kept. |
| Finding: overflow (my own run) | For input (230, 1), maximum (224, 192), patches (16, 32): 230 divided by the ratio is 224.00000000000003 in double precision, the ceiling is 225, and alignment gives (240, 32). Over inputs 1 to 300 in each dimension I count the same 2,497 overflows. With exact rational arithmetic none of the 90,000 cases overflows, so every one is a rounding artefact, which supports the entry's reasoning that the design is sound in exact arithmetic. True. |
| Execution | Two standard-library sweeps with `math.ceil` in place of `np.ceil`; labelled. The two agree for Python floats. |

## Not verified

- The helper itself under NumPy (not installed here); any resizing.

## Must fix before canonical use

None.

## Ledger items filed with this request

- `exllamav3-rope-table-row-bounds--r001`: **accepted.** Suspected, introduced at `2f8254fe`, no fix.
- `exllamav3-padded-thread-read-bounds--r002`: **accepted.** Supersedes r001; adds 230 as an observation; the
  185 introduction and earlier observations are preserved.
- `exllamav3-warp-sum-store-race--r002`: **accepted.** Supersedes r001; adds 230 as an observation.

## Follow-ups

1. Ledger, with 232's request: the overflow finding as suspected, introduced at `16df3fd1`, reach limited to
   direct use of the helper; it may cite this verdict's exact-arithmetic count as a reviewer note.

## Next

1. Record this approval with `--approve`.
2. Proceed to 232.
