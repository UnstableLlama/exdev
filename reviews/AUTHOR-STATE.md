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

## Earlier boundary (17 November)

- Positions 2–310 were recorded for ancestor retrieval only. The assisted
  306/002 is the recorded entry. The 306/001 rejection remains in history.
- The 299–309 recovery and ledger obligations are closed. See tracking and
  register for the verdicts, audits, and canonical follow-ups.
- For packet retries, use the packet builder and verify shared hardlink identity.
- Everything since commit 235 is uncommitted. Commit or push only at user request.

## Your thread id

Your thread id is 01a1eac6-cc72-7af3-9172-36689bd69fc9 (also in `$CODEX_THREAD_ID`; check they agree). Put it on the `Reply-to thread:` line of every request and use
it for `--notify-thread`. The old id is dead; do not notify it.

## Request mechanics and open work

Use plain path/hash bullets and host replay for approval. Disclose repair sizes, ran-ahead positions and packet sparsity. Fresh attempts get new packets and bind coverage if assisted. Keep unaccepted implementation edits out of live runs. See tracking and register for the 002 implementation items, ledger origin support and housekeeping.

## Current handoff (2026-11-18)

325–329 recorded for ancestor retrieval only. Diagnostics v3 deployed after 325.
326–329 had no repair. Report actual feedback and outcome at first v3 repair.
The user authorized the corrected author candidate for revision attempts 002.
Applied at the empty queue after 327, verified 50 production hashes, and launched
328. The 328 request binds the application audit, accepted verdict, and 349-test suite.
328 completed unassisted and is approved. Fable’s patch is withdrawn.
329–330 recorded. The 329 release asset collision ledger r001 is closed.
331 recorded for ancestor retrieval only. Fable accepted both 330 ledger r001
records and the 331 packet’s 327 of 328 strict ancestors. No new ledger item.
Canonical follow-ups: keep issue #34, link 330.
Opus is the current reviewer by user decision. Its verdicts are final. The
standard and file mailbox are unchanged. Fable confirmed all 24 stand-in verdicts
in reviews/verdicts/standin-rereview-001.md. The 14 entry approvals through
345/002 stand for ancestor retrieval only. Prior approvals and verdicts retain
their original bytes and hashes. History is in the register.

346/002 is recorded for ancestor retrieval only under Opus’s verdict. Its
recovery stop is cleared and the detached 347 run is active. The queue recorder
writes the literal Fable label; the bound verdict identifies Opus.
With 347, submit reports/commit-000346-ledger-001.json for the eight 346
findings and reports/standin-rereview-001-ledger.json for the four 333/335
backfills and the cache-detach audit. Cache r003/r004 correctly carry confirmed
status for the conditional error path; r005 separately records the fix.
Opus passed the staged validator v4 patch and quoted the user’s approval in
reviews/verdicts/collect-all-validation-problems-implementation-001.decision.md.
Let 347 finish and get recorded under v3. Hold the next run until deployment
at the empty-queue boundary and the host-enabled suite passes. If the suite
fails, reverse the patch, file the failure and keep the walk stopped. File
reviews/requests/collect-all-validation-problems-application-001.md with the
hashes and deployment notes. Call out the first live v4 repair and its outcome.
A revision attempt requires reviewer authorization.
Flag first live revision for line-by-line review and report old/new token usage.
Use a fresh assisted attempt if pointer-only coverage is unavailable. If provider
usage accounting causes a run failure, report usage unavailable in the handoff.
Canonical/training false. No commit or push.
