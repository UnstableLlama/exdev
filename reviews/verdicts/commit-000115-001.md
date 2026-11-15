# Verdict: commit-000115-001

Reviewer: Fable (independent reviewer; file mailbox)
Run: `.teacher/runs/commit-000115-001`
Packet: `.teacher/retrieval/000115-001`
Upstream: `a7a6681e11d9bb99f5d1b9e8d223cb402ff80969` "Fix top-P limits as well"
Request: `reviews/requests/commit-000115-001.md`
Reviewed: 2026-11-14, working tree on top of `d0a2d08`, machine `exdev-314`

## Decision

**APPROVED for ancestor retrieval only.** Canonical and training remain false.

Every statement I checked is true. The entry sees what matters here: zero is not made into the "off" value the dead
`alt` branch and PR 30 expected; it becomes the strongest truncation, and it gets there through the ordinary
normalize, sort and mask path, keeping one candidate even when maxima tie.

The teacher found the unreachable `alt` branch on its own from the parent source. The packet contains nothing from my
113/002 finding or the ledger record.

## Artifacts reviewed (sha256)

All thirteen hashes in the request match the files on disk.

## Run checks

| Check | Result |
|---|---|
| Run integrity | 7 of 7 ledger entries match the transcript, none uncited; final message equals the annotation; Markdown equals the render; full review; 41 of 41 implementation hashes; exactly 114 strict-ancestor entries; 1,707 blobs hash to their names; no evidence timestamp after the cutoff. |
| Replay | 7 of 7 recorded tool calls identical, including the `run` call. |
| Unassisted | Standing instructions byte-identical to 114/001's. |
| No hindsight | No blob in the packet contains `reviews/verdicts`, a defect-ledger path, `top-p-zero`, `reviewer_observation` or `Reviewer-only`. (Eight blobs match "fable" case-insensitively; they are tokenizer vocabularies, the same eight as in 114's packet.) |
| Ancestor prose | The one ancestor read returns 114's entry, equal to the approved 114/001 annotation without evidence ids and schema version. |
| Catalog | GitHub: open at the cutoff are 1, 4, 7, 10, 14, 21, 22, 24, 25, 26, 27, 28, 29, 30. Matches the fourteen open rows. |
| Architecture trigger | Does not fire. |
| Diff claim | `SS_TopP.__init__` asserts `0.0 <= top_p <= 1.0` (was `0.0 < top_p <= 1.0`); `alt()` returns the no-op for `top_p == 1.0` only (was 1.0 or 0.0). Nothing else changes. Correct. |
| Problem | At the parent the assertion rejected 0.0 before `alt()` could substitute the no-op. Correct. |
| Path at zero | `CustomSampler` resolves `alt()` before `prep()` (verified at 113). With no substitution, `SS_TopP.prep` supplies `SS_Normalize` and `SS_Sort` as needed, and `run` requires `PROBS_N_S`. Correct. |
| Filtering at zero | `mask = cumsum <= top_p`; `probs[..., 1:] *= mask[..., 1:]`; state `PROBS_S`. With positive probabilities and `top_p = 0` the mask is false everywhere, position 0 is exempt, so exactly the first sorted candidate survives, ties included. Correct, with the entry's "valid positive-mass distribution" qualifier. |
| Sampling | `SS_Sample` on `PROBS_S` takes the argmax of the noised row and maps it through `state.indices`. Unchanged. Correct. |
| Callers | `ComboSampler` constructs `SS_TopP(top_p)` only on the nonzero-temperature branch, default 1.0; `TopPSampler` sends `top_p == 0` to `SS_Argmax`. Correct. |
| Discussion | PR 30 as at 113 and 114. Labelled an inference; the contrast with the PR's proposed omission is right. |
| Execution | Recorded output: acceptance changes only at 0 among the five values; at 0 the rows become `[0.6, 0, 0]` and `[0.4, 0, 0]`; at 1 both rows are returned unchanged by construction of the script. Matches the prose. Python numbers only, as the entry says. |
| Reads | Both `repo_read` results complete (17,763 and 3,254 bytes, not truncated). |
| Findings | None, and I found none. |

## Reviewer-only notes (never to a teacher)

- This commit **fixes** `exllamav3-top-p-zero-assertion`, eleven minutes and two commits after 113. The fix is not the
  one the dead branch implied: zero is accepted and made active, not neutral.
- Which of several tied maxima is "first" depends on `torch.sort`, which is not stable by default. The entry says
  "the first sorted maximum" and claims no more, which is right.

## Not verified

- Any execution of the repository sampler.

## Must fix before canonical use

None for this entry.

## Follow-ups

1. Ledger, when next revised: mark the top-p record fixed at `a7a6681e` (affected at 113 and 114 at least; introduction
   still not established), origin of the fix `fix_derived` from this entry, and note the semantics chosen.

## Next

1. Record this approval.
2. Continue the walk at commit 116.
