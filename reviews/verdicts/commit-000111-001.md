# Verdict: commit-000111-001

Reviewer: Fable (independent reviewer; file mailbox)
Run: `.teacher/runs/commit-000111-001`
Packet: `.teacher/retrieval/000111-001`
Upstream: `7deeb0fff8c860f98021d3c7844d16e7ad9899c9` "Treat temp = 0 as greedy sampling in combo sampler preset"
Request: `reviews/requests/commit-000111-001.md`
Reviewed: 2026-11-14, working tree on top of `d0a2d08`, machine `exdev-314`

## Decision

**APPROVED for ancestor retrieval only.** Canonical and training remain false.

Every statement I checked is true. The entry is precise about what "greedy" means here: the maximum after masking and
penalties, with every filter skipped, and only at a temperature of exactly zero.

## Artifacts reviewed (sha256)

All hashes in the request match the files on disk.

## Run checks

| Check | Result |
|---|---|
| Run integrity | 10 of 10 ledger entries match the transcript, none uncited; final message equals the annotation; Markdown equals the render; full review; 41 of 41 implementation hashes; exactly 110 strict-ancestor entries; 1,679 blobs hash to their names; no evidence timestamp after the cutoff. |
| Replay | 10 of 10 recorded tool calls identical, including the `run` call. |
| Unassisted | Standing instructions byte-identical to 110/001's. |
| No hindsight | No blob in the packet contains `reviews/verdicts` or a defect-ledger path. |
| Catalog | GitHub: open at the cutoff are 1, 4, 7, 10, 14, 21, 22, 24, 25, 26, 27, 28, 29. Matches the thirteen open rows. |
| Architecture trigger | Does not fire. |
| Diff claims | After the two penalty steps the stack now branches: `temperature == 0.0` appends `SS_Argmax()` alone; otherwise the previous six steps are appended unchanged. So at zero temperature `min_p`, `top_k`, `top_p` and `temp_last` are not consulted, and `SS_MinP` is never constructed. Correct. |
| Argmax path | Neutral penalties become no-ops and leave the state at `INIT`; active ones leave unsorted `LOGITS`. `SS_Argmax` assigns `state.sample` in both of those states (it is the sorted states that have the inherited defect), so this path is not affected by it. Correct. |
| Finding | `nonzero-default-min-p`: correct, and correctly scoped. `ComboSampler()` with its defaults (temperature 1.0, `min_p` 0.0) still builds `SS_MinP(0.0)` and fails the assertion. Same defect as 91's `combo-default-min-p` and 92's `chat-min-p-disable`. |

## Not verified

- Any sampler construction or generation.

## Must fix before canonical use

1. Ledger identity: this is a fourth observation on the `SS_MinP` zero defect, not a new record. One side effect worth
   recording there: at temperature 0 the defect is now unreachable through `ComboSampler`.

## Next

1. Record this approval.
2. Continue the walk at commit 112.
