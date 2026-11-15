# Verdict: commit-000080-001

Reviewer: Fable (independent reviewer; file mailbox)
Run: `.teacher/runs/commit-000080-001`
Packet: `.teacher/retrieval/000080-001`
Upstream: `24aa1b7c7c44324d1da0e86fdda9f60316b7d01f` "Add min-P sampler"
Request: `reviews/requests/commit-000080-001.md`
Reviewed: 2026-11-14, working tree on top of `d0a2d08`, machine `exdev-314`

## Decision

**APPROVED for ancestor retrieval only.** Canonical and training remain false.

Every statement I checked is true. The entry explains the new step, traces what the changed default actually executes,
and says plainly that the new default is a behaviour change and not an equivalent faster path.

## Artifacts reviewed (sha256)

All hashes in the request match the files on disk.

## Run checks

| Check | Result |
|---|---|
| Run integrity | 13 of 13 ledger entries match the transcript, none uncited; final message equals the annotation; Markdown equals the render; full review; 39 of 39 implementation hashes; exactly 79 strict-ancestor entries; 1,155 blobs hash to their names; no evidence timestamp after the cutoff. |
| Replay | 13 of 13 recorded tool calls identical, including the `run` call. |
| Unassisted | Standing instructions byte-identical to 79/001's. |
| No hindsight | No blob in the packet contains `reviews/verdicts` or a defect-ledger path. |
| Catalog | GitHub: open at the cutoff are 1, 4, 7, 10, 14, 15, 20 (19 closed since commit 79). Matches the seven open rows. |
| `SS_MinP` | Asserts `0 < min_p <= 1`. `PROBS_N`: threshold from `amax(dim=-1, keepdim=True)`; `PROBS_N_S`: threshold from `probs[:, :1]`. Both multiply by a `>=` mask and drop to the unnormalised state of the same sortedness. Any other state raises. `prep` returns `[SS_Normalize]` for `INIT`, `LOGITS`, `PROBS`, `LOGITS_S`, `PROBS_S`. Correct. |
| Default change | `DefaultSampler` goes from `SS_Temperature(0.75), SS_TopP(0.75)` to `SS_MinP(0.08), SS_Temperature(0.8)`. Correct. |
| Planning claim | `CustomSampler.__init__` sets `state = SS.INIT` once and never advances it, so every step's `prep` is asked about `INIT`. `SS_MinP` therefore gets a normalise step inserted before it. Correct. |
| Temperature after filtering | On probabilities `SS_Temperature` applies `pow_(1 / T)` and marks the state unnormalised. Zeroed weights stay zero, so the support is unchanged. Correct. |
| Sampling path | `SS_Sample` on unnormalised probabilities calls `gumbel_noise_log` then `argmax`, with no normalise or sort. Correct. |
| Finding | `inherited-sorted-argmax`: the two sorted branches of `SS_Argmax.run` assign to `state.state` and leave `state.sample` unset. Unchanged by this commit; same defect earlier entries record. Suspected and inherited are right. |

## Not verified

- The Gumbel kernel's handling of a zero weight (the logarithm of zero). The entry says the kernel logs each weight; I did not re-read `gumbel.cu`.
- Any sampling run. Nobody executed one; the entry says so.

## Must fix before canonical use

Reviewer-only.

1. The equality example (threshold exactly 0.04 keeps the 0.04 token) is binary64 arithmetic. The repository computes in
   float32, where a boundary token may fall either side. The entry labels the check as binary64 but a canonical entry
   should not present the boundary case as the sampler's behaviour.

## Next

1. Record this approval.
2. Continue the walk at commit 81.
