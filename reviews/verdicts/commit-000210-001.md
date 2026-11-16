# Verdict: commit-000210-001

Reviewer: Fable (independent reviewer; file mailbox)
Run: `.teacher/runs/commit-000210-001`
Packet: `.teacher/retrieval/000210-001`
Upstream: `49ac13c04f4c622582e2d519f2d135a53c1c4eaf` "Reconstruct to empty tensor"
Request: `reviews/requests/commit-000210-001.md` (sha256 `415e266544ea00ed7244220be072a70c361a57e6304360a9761222f861660e81`)
Reviewed: 2026-11-16, working tree on top of `39357a9`, machine `exdev-314`

## Decision

**APPROVED for ancestor retrieval only.** Canonical and training remain false.

Every statement I checked is true and the finding is true as stated, with honest limits. Both ledger items
filed with this request are accepted.

## Artifacts reviewed (sha256)

Every hash listed in the request matches the file on disk.

## Run checks

| Check | Result |
|---|---|
| Run integrity | 9 of 9 ledger entries match the transcript, none uncited; final message equals the annotation; Markdown equals the render; full review; 44 of 44 implementation hashes; exactly 209 strict-ancestor entries; 2,994 blobs hash to their names; no evidence timestamp after the cutoff. |
| Replay | 9 of 9 recorded tool calls identical, including the `run` call. |
| Unassisted | Standing instructions byte-identical to 209/001's. Guidance 9. |
| No hindsight | No blob in the packet contains `reviews/verdicts` or a defect-ledger path. |
| Catalog | Fifteen open rows at 2025-05-31T14:57:09Z; my query agrees. Two closed rows, one by path alone. |
| The change | One line in `get_inner_weight_tensor`: `torch.zeros` becomes `torch.empty`; shape, dtype, device and the `ext.reconstruct` call are unchanged. Callers are the reconstruction branch of `forward` and `get_weight_tensor`. Correct. |
| The kernel | Grid `cols / 8` by `rows`, 256 threads; each thread stores one 16-byte vector at `(k·16 + r)·2·blocks_n + n·2 + c` with `blocks_n = (cols / 8)·8`, so each block fills a 16 × 128 region by assignment and the row stride is 16·`blocks_n` values. Correct. |
| Finding: partial width | The wrapper checks only that the output is 16 times the packed size in each dimension, so 9 packed columns with a 144-wide output are accepted; the grid is then one block wide, the stride 128, and 2 × 16 × 128 = 4,096 of 4,608 values are written. I recomputed this from the kernel. Before this commit the rest was zero; now it is whatever the allocator returned. True. The entry says the layout was already wrong before and that no normal loading path was shown to produce such a width. |
| Execution | A standard-library enumeration of the store addresses for 8, 16 and 9 columns; labelled as a model. |

## Guidance 9 (reviewer note for the user's cost-and-effect report; never to a teacher)

This is the first walk commit that removes an initialisation, the case paragraph E was written for. The entry
does what the paragraph asks: it says what the zero fill guaranteed, checks whether the kernel's writes still
cover the buffer, finds the width at which they do not, and reports that as a suspected finding with its reach
limit instead of leaving it under uncertainty. The guidance-8 control with the same kind of change (189, zero
fill removed before a full overwrite) correctly produced no finding, and this run cost 9 tool calls.

## Not verified

- Any CUDA execution; whether any supported model has an output width that is not a multiple of 128.

## Must fix before canonical use

1. Administrative: the second location is written against the parent commit; use the task commit.

## Ledger items filed with this request

- `exllamav3-compare-q-split-result-serialization--r001`: **accepted.** Suspected, introduced at `8ff65b87`, no
  fix recorded (correct: the walk has not reached one).
- `exllamav3-compare-q-filtered-reference-dependency--r004`: **accepted.** Supersedes r003, adds 209 as an
  observation.

## Follow-ups

1. Ledger, with 211's request: one identity for the reconstruction width. The missing width check and the wrong
   stride are inherited (verify the introduction from the root tree); `49ac13c0` is the commit at which the
   unwritten part stops being zero. Suspected, source-only, reach limited as the entry states.

## Next

1. Record this approval with `--approve`.
2. Proceed to 211.
