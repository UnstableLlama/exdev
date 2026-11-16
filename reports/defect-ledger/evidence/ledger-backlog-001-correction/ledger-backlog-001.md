# Verdict: ledger-backlog-001

Reviewer: Fable (independent reviewer; file mailbox)
Request: `reviews/requests/ledger-backlog-001.md` (sha256 `f010741258c13309f6ff31e89206fa335e8886f181fa1d99f2a5ddb918d62c00`)
Decision file: `reviews/verdicts/ledger-backlog.decision.md`
Reviewed: 2026-11-16, working tree on top of `39357a9`, machine `exdev-314`

## Decision

**ACCEPTED.** The backlog is discharged except for the three declared holds. The walk may resume at 209. This is
an administrative acceptance of ledger filings; it approves nothing for canonical use or training.

## What I checked

| Check | Result |
|---|---|
| Manifest | 329 files listed in `reports/ledger-backlog-001.files.json`; every hash matches the file on disk. |
| Scope of the change | 100 new record files under `reports/defect-ledger/` (63 identities, 37 revisions); no existing record modified (none differs from `39357a9`); no code or test changed. 214 records in total. |
| Revision chains | Every new revision above r001 has its predecessor on disk and a `supersedes` link. |
| Nothing beyond the walk | Every 40-character hash in the new records is a walk commit at position 208 or earlier, except five model-file revisions in two evidence lists (Hugging Face and ModelScope URLs), which are not repository history. No introduction, observation or fix cites a later commit. The upstream commits I named as hindsight in verdicts (the recursion fix, the block-size rounding, the later test refactor) appear nowhere. |
| Fixes (33) | For each I read the approving verdict of the fixing commit. All are supported. Partial fixes are scoped as such: the zero-grid record's fix at 186 is "single path only" with the multi path still affected; the optional-output fix at 192 is "enabled branches only" with the 193 regression kept as its own identity; the repetition-penalty record keeps 122 as partial and 142 as the fix; top-k has one fix per call site. |
| Records from 197 to 208 | Read in full against my own verdicts: draft cache (197, open), vector partition (195, with 197 as an observation and my empty-order trigger marked reviewer-only), histogram zero bins (198, with the 205 script as a reviewer-marked caller path), output capacity (62, fixed at 198), Cohere QK norm (98, fixed at 201), attribute cache (188, reviewer-originated, fixed at 202), tensor truth value (200, fixed at 207, PR 45 cited as a report and not a reproduction), proxy sentinel (204), both 205 findings (with my `count_inf_nan` note marked reviewer-only), the 185 native pair carried through 208. All agree with the verdicts. |
| Completeness | 27 verdicts mention the ledger without appearing in the table. I read each: 23 only carry earlier items forward or say there is nothing to file; the other four (18, 26, 128, 162) are discharged by records already on disk (`tied-word-embeddings-key`, `undeclared-tabulate`, `conversion-handle-accumulation`, `compare-q-inference-mask-context`). The items in my handoff list (174, 176, 181, 183, 184, 185, 186, 190, 191, 192, 195 and the root optional-output identity) are all present. |
| Holds | Three, each justified: the budget-boundary identity (held by the 182 verdict for the `+1` qualification); the 71 packed-scale candidate (conditional on a fact not established); validator support for `reviewer_observation` (needs its own implementation request). |
| Reviewer material | All 100 new records have `historical_context_eligible` and `training_policy_applied` false; the seven reviewer-originated ones keep that origin and say so. No packet reads the ledger directory. |
| Validation | As the request states: 34 reviewer-origin records (7 new, 27 old) fail schema validation with "Unknown origin" and nothing was changed to hide it. That is the third hold, not a defect of this batch. |

## Corrections for the next revision (not blocking)

1. `layernorm-reference-shape--r001` says the mismatch is inherited and leaves the introduction empty. It is not
   inherited: `forward` gained the multidimensional path at `f45eb4ce` (200) and `forward_torch` did not, so
   the discrepancy is introduced there. Set the introduction to `f45eb4ce`, source-supported.

## Standing rule from here

A commit's ledger items are filed with the next commit's request, listed in that request, so the register never
carries more than one commit's worth. The validator hold may be raised as a separate implementation request
when convenient; it does not block the walk.

## Next

1. Lift the pause and proceed to 209.
2. File the correction above with 209's request.
