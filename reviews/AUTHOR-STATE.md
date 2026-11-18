# Author state (short). Read this after every context reset.

Written by Fable (reviewer) on 2026-11-17 18:35 UTC, on the user's word ("Yes, fresh thread"), for a fresh
author thread. Administrative only; never teacher input. Keep it under 8 KB: replace lines, do not append a
log. History goes to `reviews/ASTRA-REGISTER.md`.

## Why this file exists

The previous author thread (01a1da07-7653-7b81-8507-f69683828acb, 14 to 17 November) ended in a compaction
loop: after every compaction it re-read the current section of `reviews/ASTRA-TRACKING.md` (about 190 KB)
and filled up again. That thread is stopped. You are the same role (the author; the files call it Astra),
on `gpt-6.2-sol` medium since 22:52 UTC 17 November (user's order; before that `gpt-6.1-sol`), with the same rules.
Teacher: `gpt-6.2-sol` medium under accepted `teacher-model-implementation-003`; 6.1 runs are approval-only.
310 is recorded. Run-ahead cap three. Use the current handoff for the live boundary.

## Reading rules (these prevent the loop)

- After a reset read only: `reviews/AUTHOR-INSTRUCTIONS.md`, this file, and the "Procedure" and "Standing
  conditions" sections of `reviews/ASTRA-TRACKING.md` (find them with `grep -n '^## '`, read those line
  ranges only, about 3.5 KB).
- Never read whole: `ASTRA-TRACKING.md`, `ASTRA-REGISTER.md`, `reviews/fable/STATE.md`, the journal
  `reports/teacher-walk-001.json`, a transcript, or a log. Use `grep`, line ranges, or a small Python
  extraction of the fields you need. Cap command output (pipe through `head` or `cut`).
- From the journal read only `status`, `next_position`, `handover`, `advancement_pause`, `active_session`,
  `queue_stop`, or the one record you need.
- Reviewer files under `reviews/fable/` are not yours to edit.

## Where the walk is (18:35 UTC, 2026-11-17)

- Approved and recorded for ancestor retrieval only: commits2–309 (306/002 assisted in force;306/001 rejected history). Canonical/training false.
- **299–305**: approved and recorded; all recovery stops closed and ledger obligations accepted.
 299 baseline recovery consumed/closed, audit reports/commit-000299-approval-recovery-001-application.json.
 Canonical follow-ups:299/300 Ernie tokenizer BOS;302 lm_head versus lm_head.weight detection limits.
 Details in ASTRA-REGISTER; reviewer observations remain administrative only.
- **306**:002 assisted approved and recorded;001 rejected thin remains history, never in retrieval.
  Verdict reviews/verdicts/commit-000306-002.md sha256
  5ce849f8c332073e61f8ca88d945cc0ee052d1d5ca1bc6fe0cf388ae63efc44d.
  All23 request bindings/published request verified; unchanged host-enabled58-call replay passed.
  One carried odd activation tail, none new; r005 accepted in308 verdict; obligation closed.
  Link recovery consumed and closed;3769 identical links restored,4390 verified, no teacher rerun.
  Authored files/manifest unchanged. Application: reports/commit-000306-link-recovery-002.application.json.
  Retry stop cleared against306/002 verdict after ascending306 then307 approvals.
  Future retries: packet builder/hardlinks, never copytree; shared-link identity in comparison report.
- **307**: approved and recorded after306;11 request bindings/published request verified,
  unchanged host-enabled30-call queue replay passed. Verdict sha256
  a2ecd28cd3f3ef52d120f2427e7e48f714dc97ab24efd381835a06eb7d596786.
  Three carried root observations accepted, none new; reconcile checkpoint-token attribute,
  terminal-string bypass and multisequence enqueue undercount. Reconciled and submitted with308:
  checkpoint r003, terminal r003, first persisted generation-capacity r001 for existing root finding.
  All four306/307 records accepted in308 verdict; obligation closed.
  Report reports/commit-000306-307-ledger-001.json.
  No canonical follow-ups from306/307. Canonical/training false.
- **308**: approved and recorded for ancestor retrieval only;22 artifact bindings/published request
  verified, unchanged host-enabled28-call approval replay passed. Verdict sha256
  416516d81845fc89c7777242d0890cf581b3d5f04992046edced5b1072e674e2.
  Two suspected new findings accepted (explicit-load falls through, empty-history retry/edit),
  carried nonpositive codeblock index. Prepared two r001 records and codeblock r005;
  schema/evidence validated, reports/commit-000308-ledger-001.json. Accepted in309 verdict; obligation closed.
  Four306/307 ledger records accepted and closed. No blocking canonical follow-up; optional precision:
  get_input_ids tests _prefix but appends enclosing prefix (same value at both call sites).
  Reviewer observation remains administrative, never teacher input.
- **309**: approved/recorded;18 bindings/request verified, host24-call replay passed. Three308 records
  accepted. Suspected fewshot counter finding accepted; r001 prepared/validated, report
  reports/commit-000309-ledger-001.json; accepted in310 verdict, obligation closed. Canonical: returned logits (1,1,padded_vocab)
  float, [0,0] vocabulary vector; reviewer note administrative only.
- Validation repair policy is `validator-keep-rest-v2`, accepted and applied to the live files
  (`reviews/verdicts/validation-repair-implementation-004.md`). 300 is the first run under it.
- Everything since commit 235 is uncommitted. Do not commit or push unless the user asks.

## Your thread id

Your thread id is 01a1eac6-cc72-7af3-9172-36689bd69fc9 (also in `$CODEX_THREAD_ID`; check they agree). Put it on the `Reply-to thread:` line of every request and use
it for `--notify-thread`. The old id is dead; do not notify it.

## Request mechanics and open work

Use plain path/hash bullets and host replay for approval. Disclose repair sizes, ran-ahead positions and packet sparsity. Fresh attempts get new packets and bind coverage if assisted. Keep unaccepted implementation edits out of live runs. See tracking and register for the 002 implementation items, ledger origin support and housekeeping.

## Current handoff (2026-11-18)

325–329 recorded for ancestor retrieval only. Diagnostics v3 deployed after 325.
326–329 had no repair. Report actual feedback and outcome at first v3 repair.
328 accepted the 327 sparse-snapshot disclosure and filter-package r002. Both closed.
Canonical follow-ups for 325–329 are in tracking.
The user authorized the corrected author candidate for revision attempts 002.
Applied at the empty queue after 327, verified 50 production hashes, and launched
328. The 328 request binds the application audit, accepted verdict, and 349-test suite.
328 completed unassisted and is approved. Fable’s patch is withdrawn.
329 approved. Its suspected non-CUDA release asset name collision is validated
as ledger r001 in reports/commit-000329-ledger-001.json, due with 330.
330 running. It ran ahead of 329. Disclose the sparse snapshot in its request.
Flag first live revision for line-by-line review and report old/new token usage.
Use a fresh assisted attempt if pointer-only coverage is unavailable. If provider
usage accounting causes a run failure, report usage unavailable in the handoff.
Canonical/training false. No commit or push.
