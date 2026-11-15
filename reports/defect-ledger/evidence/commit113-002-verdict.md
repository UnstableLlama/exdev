# Verdict: commit-000113-002

Reviewer: Fable (independent reviewer; file mailbox)
Run: `.teacher/runs/commit-000113-002`
Packet: `.teacher/retrieval/000113-002`
Upstream: `1d4920f25a27b077bf69f1dee3b5a55fcaf7e0f0` "Fix min-P limits"
Request: `reviews/requests/commit-000113-002.md`
Reviewed: 2026-11-14, working tree on top of `d0a2d08`, machine `exdev-314`

## Decision

**APPROVED for ancestor retrieval only.** Canonical and training remain false.

Every statement I checked is true. Seven changed lines; the entry gets both ends of the interval right, including the
quiet removal of 1.0, and explains correctly why the no-op costs no normalization.

## Artifacts reviewed (sha256)

All fourteen hashes in the request match the files on disk.

## Run checks

| Check | Result |
|---|---|
| Run integrity | 7 of 7 ledger entries match the transcript, none uncited; final message equals the annotation; Markdown equals the render; full review; 41 of 41 implementation hashes; exactly 112 strict-ancestor entries; 1,693 blobs hash to their names; no evidence timestamp after the cutoff. |
| Replay | 7 of 7 recorded tool calls identical, including the `run` call. |
| Unassisted | Standing instructions byte-identical to 112/001's. System message, opening message and manifest byte-identical to the failed 113/001's; nothing from that attempt or from a reviewer was added. |
| No hindsight | No blob in the packet contains `reviews/verdicts` or a defect-ledger path. |
| Catalog | GitHub: open at the cutoff are 1, 4, 7, 10, 14, 21, 22, 24, 25, 26, 27, 28, 29, 30. Matches the fourteen open rows. |
| Architecture trigger | Does not fire. |
| Diff claim | `SS_MinP.__init__` asserts `0.0 <= min_p < 1.0` where it asserted `0.0 < min_p <= 1.0`, and gains `alt()` returning `SS_NoOp()` when `min_p == 0.0`. Nothing else changes. Correct. |
| Problem | `ComboSampler` defaults `min_p = 0.0` and its nonzero-temperature branch constructs `SS_MinP(min_p)` unconditionally (`presets.py`). Correct. |
| Alternative step | `CustomSampler.__init__` calls `step.alt()`, replaces the step if one is returned, and only then calls `prep` on the replacement and appends it (`custom.py` 448 to 457 at the parent). `SS_NoOp.run` is `pass` and it inherits `SS_Base.prep`, which returns `None`. So zero min-p adds no `SS_Normalize`, masks nothing, and the no-op stays in the list. Correct. |
| Active filtering | `PROBS_N`: threshold is the row `amax` times `min_p`, result state `PROBS`. `PROBS_N_S`: threshold is the first column times `min_p`, result state `PROBS_S`. Comparison is `>=`. Unchanged by the patch. Correct, including "unnormalized while preserving whether it is sorted". |
| Endpoint one | With `>=`, 1.0 would keep the maximum and its ties; the new assertion rejects it. The patch gives no reason. Correct. |
| Other samplers | The zero-temperature branch never constructs `SS_MinP` (verified at 111). `DefaultSampler` uses `SS_MinP(0.08)`. Correct. |
| Ancestor note | The entry for 111 (`7deeb0ff`) carries the finding that the default still fails at nonzero temperature. Correct. |
| Discussion | PR 30's body reports assertion errors for zero `min_p` and `top_p`. The entry labels the connection an inference and notes the patch substitutes a step where the PR omits it. Correct. |
| Execution | The recorded output shows the six endpoint predicates and threshold 0.3 retaining 0.6 and 0.3 from [0.6, 0.3, 0.1]. Matches the prose. Python numbers only, as the entry says. |
| Reads | Both `repo_read` results are complete (17,663 and 3,254 bytes, not truncated), so every cited line was in evidence. |
| Findings | None in the entry. One inherited defect it does not record is below. |

## Reviewer-only: zero top-p still asserts (never to a teacher)

`SS_TopP.__init__` asserts `0.0 < top_p <= 1.0` while `SS_TopP.alt()` returns a no-op for `top_p == 1.0 or top_p == 0.0`.
With assertions on, the 0.0 half of that `alt` cannot be reached: construction fails first. It is reachable through
`ComboSampler(top_p = 0)` and through `examples/chat.py`, which passes `args.top_p` straight in. This is the other half
of what PR 30 reports. Commit 113 does not touch it, so it is inherited and not this entry's fault; the entry's
"changes min-p only" is true but stops short of saying top-p zero still fails. No ledger record or earlier verdict
mentions it. Introducing commit not established.

## Not verified

- Any execution of the repository sampler.
- Which commit introduced the `SS_TopP` mismatch.

## Must fix before canonical use

1. A canonical entry should say that zero `top_p`, the other case in PR 30, still fails after this commit.

## Follow-ups

1. Ledger: the `SS_MinP` zero defect seen at 91, 92 and 111 under three names is one identity and is **fixed at 113**.
   Merge and close it when the ledger is next revised.
2. Ledger: file the `SS_TopP` zero assertion as a new record (reviewer finding, this verdict).
3. Behaviour change worth a row when the ledger is revised: `min_p = 1.0`, valid before, now fails the assertion.

## Next

1. Record this approval.
2. Continue the walk at commit 114.
