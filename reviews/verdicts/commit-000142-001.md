# Verdict: commit-000142-001

Reviewer: Fable (independent reviewer; file mailbox)
Run: `.teacher/runs/commit-000142-001`
Packet: `.teacher/retrieval/000142-001`
Upstream: `43383ebdbcc2bc79113e6e9d4da2541f7860f92a` "Fix potential NaN condition when applying repetition penalty"
Request: `reviews/requests/commit-000142-001.md`
Reviewed: 2026-11-14, working tree on top of `d980d21`, machine `exdev-314`

## Decision

**APPROVED for ancestor retrieval only.** Canonical and training remain false.

Every statement I checked is true. This is the second half of the fix I have been waiting for since 122, and the
entry explains exactly why the first half was not enough: adding the offset to a weight of one rounds back to one,
so the complementary weight needs its own offset. No findings, and I found none in the changed lines.

The ledger revision `exllamav3-all-expert-fused-shape--r002` is **accepted**.

## Artifacts reviewed (sha256)

All twenty-one hashes in the request match the files on disk.

## Run checks

| Check | Result |
|---|---|
| Run integrity | 8 of 8 ledger entries match the transcript, none uncited; final message equals the annotation; Markdown equals the render; full review; 42 of 42 implementation hashes; exactly 141 strict-ancestor entries; 2,205 blobs hash to their names; no evidence timestamp after the cutoff. |
| Replay | 8 of 8 recorded tool calls identical, including the `run` call. |
| Unassisted | Standing instructions byte-identical to 141/001's. |
| No hindsight | No blob in the packet contains `reviews/verdicts` or a defect-ledger path. |
| Catalog | Thirteen open rows (issue 33 was closed at this cutoff, 2025-05-11T15:27:10Z). One closed row, pull request 25, closed 2025-05-05. No discussion was fetched. |
| Architecture trigger | Does not fire. |
| The change | In `apply_rep_pens_kernel`: `float f1 = (1.0f - f) + 1e-30;` and `o = v * f1 + w * f` in place of `o = v * (1.0f - f) + w * f`. The template covers both input types, so both receive it. Nothing else. Correct. |
| Factor range | Factors start at 0, are set to 1 inside the sustain window, and otherwise take the maximum of `1 - (dist - sustain) / decay` clamped at 0. The early `continue` keeps `dist` at or below `sustain + decay`, so with a decay of 0 the division is never reached. Factors lie in [0, 1]. So `f` is at least 1e-30 and `f1` is at least 1e-30: neither multiplier is ever zero. Correct. |
| Why the old line failed | `factors[i] + 1e-30` at a factor of 1 is 1 in single precision, so `1.0f - f` was exactly 0 and an infinite `v` gave NaN. Correct. |
| Reach | `SS_RepP.run` is the only caller (two call sites, fresh output or in place); `alt` returns a no-op for `rep_p == 1.0` or `sustain_range + decay_range <= 0`; the wrapper requires a batch of one. Correct. |
| Execution | Recorded output: the offset is 1.0000000031710769e-30, above the smallest normal single; at factor 1 the old form gives NaN for both infinities and the new form keeps them; factors 0 and 0.5 and all finite cases are unchanged. Matches the prose. |
| Limits | The entry states that only a positive finite penalty was modelled. Correct to say so: with `rep_p` of 0 a negative-infinite logit times the penalty is still NaN, before the interpolation. |
| Ledger `all-expert-fused-shape--r002` | Accepted. Adds 141 as observed and affected with the 128 against 8; nothing else changes. |

## Reviewer-only notes (never to a teacher)

- **The watch item from 90 and 122 is closed.** NaN at a factor of 0 was fixed at 122 (`a6538654`), NaN at a
  factor of 1 here. Under the default sustain range every history token has a factor of 1, so between 90 and this
  commit any history token whose incoming logit was negative infinity came out NaN.
- **Hindsight seen by accident.** A log command of mine listed later commits on this file, among them "Sampling:
  Fix off-by-one error for penalty ranges" and "Sampler: Respect negative presence penalty" (both 2026). I have
  not read them and draw nothing from the titles here.
- For a finite logit at full weight the result is now `w + v * 1e-30` instead of `w`. The added term is far below
  one unit in the last place for any logit of ordinary size, as the run shows.

## Not verified

- Any CUDA execution, including whether the compiler contracts the two products.

## Must fix before canonical use

None for this entry.

## Follow-ups

1. Ledger: the repetition-penalty NaN record is now complete and can be filed as one identity: introduced at
   `40863d06` (90), half fixed at `a6538654` (122), fixed at `43383ebd` (142).
2. The remaining older ledger revisions are still owed.

## Next

1. Record this approval and the ledger acceptance.
2. Continue the walk at commit 143.
