# Verdict: commit-000114-001

Reviewer: Fable (independent reviewer; file mailbox)
Run: `.teacher/runs/commit-000114-001`
Packet: `.teacher/retrieval/000114-001`
Upstream: `86ee10b642019ab2b8be6bdaf8a9b7502f977e6e` "Fix min-P limits"
Request: `reviews/requests/commit-000114-001.md`
Reviewed: 2026-11-14, working tree on top of `d0a2d08`, machine `exdev-314`

## Decision

**APPROVED for ancestor retrieval only.** Canonical and training remain false.

Every statement I checked is true. One changed character; the entry says what one means (maximal filtering with ties
kept, not "off") and correctly separates it from the zero no-op added a minute earlier.

The ledger candidate `exllamav3-top-p-zero-assertion--r001` is **accepted as filed** (suspected, reviewer origin,
excluded from historical context and training). See below.

## Artifacts reviewed (sha256)

All fifteen hashes in the request match the files on disk.

## Run checks

| Check | Result |
|---|---|
| Run integrity | 7 of 7 ledger entries match the transcript, none uncited; final message equals the annotation; Markdown equals the render; full review; 41 of 41 implementation hashes; exactly 113 strict-ancestor entries; 1,700 blobs hash to their names; no evidence timestamp after the cutoff. |
| Replay | 7 of 7 recorded tool calls identical, including the `run` call. |
| Unassisted | Standing instructions byte-identical to 113/002's. |
| No hindsight | No blob in the packet contains `reviews/verdicts`, a defect-ledger path, the new candidate's id, or `reviewer_observation`. |
| Ancestor prose | The one ancestor read returns 113's entry; it equals the approved 113/002 annotation with evidence ids and the schema version removed. Nothing from failed 113/001. |
| Catalog | GitHub: open at the cutoff are 1, 4, 7, 10, 14, 21, 22, 24, 25, 26, 27, 28, 29, 30. Matches the fourteen open rows. |
| Architecture trigger | Does not fire. |
| Diff claim | `SS_MinP.__init__` asserts `0.0 <= min_p <= 1.0` where the parent asserted `0.0 <= min_p < 1.0`. Nothing else changes. Correct. |
| Filtering at one | Threshold is the maximum times `min_p` (row `amax` unsorted, first column sorted) and the comparison is `>=`, so at 1.0 only maxima and their ties survive; the state becomes `PROBS` or `PROBS_S`. `alt()` substitutes a no-op only for 0.0, so 1.0 takes the ordinary normalize-and-mask path. Correct (source verified at 113; unchanged here). |
| Callers | `ComboSampler` passes `min_p` to `SS_MinP` on the nonzero-temperature branch only; default 0.0; `DefaultSampler` uses 0.08. Correct. |
| Discussion | PR 30's author is `randoentity`; the body reports the zero assertions and asks whether 1.0 turns the filters off. The connection is labelled an inference. Correct. |
| Execution | Recorded output: acceptance changes only at 1.0 among the five values; masks `[0.6, 0, 0]` and `[0.4, 0.4, 0]`. Matches the prose. Python numbers only, as the entry says. |
| Reads | Both `repo_read` results complete (17,762 and 3,254 bytes, not truncated). |
| Findings | None, and I found none new. Zero `top_p` still asserts at this commit (the diff touches one `SS_MinP` line; `SS_TopP` is unchanged). |

## Ledger candidate (reviewer-only; never to a teacher)

`reports/defect-ledger/exllamav3-top-p-zero-assertion--r001.json` states my finding accurately: constructor assertion
`0.0 < top_p <= 1.0` against an `alt()` that names 0.0; reachable through `ComboSampler` and the chat example; status
suspected; no introduction, fix or execution claimed. The copied evidence file hashes to the 113/002 verdict. Accepted.

Origin limitation: `ledger/retrospectives.py` line 27 accepts only `authoring_observation` and `fix_derived`, so this
record, like the seven earlier `reviewer_observation` revisions, fails that validator. Leaving the validator alone and
keeping these records out of historical context and training is the right handling for now. Do not relabel reviewer
findings as authoring observations to make them pass.

## Not verified

- Any execution of the repository sampler.
- Which commit introduced the `SS_TopP` mismatch.

## Must fix before canonical use

None for this entry.

## Follow-ups

1. Ledger, when next revised: add `86ee10b6` to the top-p record's verified revisions (still present at 114).
2. Ledger, when next revised: the min-p identity (91, 92, 111) is fixed at 113; the 1.0 endpoint was rejected at 113
   only and accepted again at 114, one minute later. Record that as a one-commit regression, not a standing behaviour
   change. This replaces follow-up 3 of the 113/002 verdict.
3. Validator: teaching `ledger/retrospectives.py` the `reviewer_observation` origin is an implementation change and
   needs its own request. Not urgent; nothing reads these records yet.

## Next

1. Record this approval.
2. Continue the walk at commit 115.
