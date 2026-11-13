# Astra: working with the reviewer

Read this at the start of every session and after any context reset. It
covers only the handoff with Fable, the independent reviewer. The walk itself
is defined by `docs/ancestor-approval-policy.md`, `docs/ancestor-context.md`
and `teacher/README.md`; if this file disagrees with those or with the user,
they win.

## Recorded pause for machine move (2026-11-13)

**Paused by the user. Do not author commit 70 until the user restarts the loop.**
Commit 69/003 is approved for ancestor retrieval only, unassisted, and supersedes
69/002 for future retrieval. 69/002 stays approved on record; 69/001 stays rejected.
The salience implementation and all requested replacements are reviewed and closed.
There is no outstanding review handoff. Fable is handling the commit and push.

Resume at **commit 70, contract 8 / guidance 5 / salience-v2**. Confirm the journal
and `reports/commit-000069-review-003.json` on the new machine. On explicit restart,
archive the user pause, clear `advancement_pause`, set status `ready`, and retain
`next_position: 70`; do not reset approved-entry selection. Prepare cutoff-eligible
open and closed catalogs before invoking the walk. Preserve historical bound
bundles: the closed-catalog recovery helper currently regenerates earlier positions,
so retain their exact bytes when recovering a new position. Prepared packets,
evidence cache, mirror and store may be ignored local assets; check availability
on the new machine rather than assuming a Git checkout contains them.

Use Codex 0.167.0 first on PATH (the default binary previously broke wire tests).
Latest accepted implementation suite: 221 host-enabled tests. Canonical/training
remain false. Required architecture fixes 1 and 2 are due before position 100;
five older invalid ledger origins remain open. Check closed-catalog issue 99 at
position 560 and issue 233 at 1100. Observed parent-file reads through `run` should
be reported separately from `repo_read`-only metrics. No teacher receives verdicts
or these administrative notes.

## Where things stand

Do not trust a summary for this, including one in this file. Read:

- `reports/teacher-walk-001.json`: `status`, `next_position`, `handover`,
  `replacement_reviews`, `advancement_pause`.
- The newest files in `reviews/verdicts/`, including every `*.decision.md`
  (user policy decisions, binding on both of us).

## The mailbox

You and Fable exchange files, so the user does not have to carry messages.

- You write `reviews/requests/<run-name>.md` when the walk stops for full
  review (a full-review draft, a replacement attempt, or sampled mechanical
  drafts in the handover).
- Fable writes exactly one reply, `reviews/verdicts/<run-name>.md`. Fable
  changes nothing else: not the run directory, `review.json` or the journal.
  Recording the outcome is your job.
- A verdict may be written in a cloud session and arrive on a branch. If one
  is overdue, `git fetch origin` and look before assuming it is late.

## What a request needs

The reviewer checks your statements against disk, so give it things to check:

- Run directory, packet path, upstream SHA, and the commit title copied from
  `git log`, not retyped. (The commit 17 attempt 003 request got it wrong.)
- SHA-256 of `draft.json`, `draft.md`, `raw-transcript.json`,
  `provenance.json`, the packet manifest, and any evidence bundle you cite.
- For a replacement: which run it supersedes, the decision file it acts on
  (path and hash), and which later runs read the old prose.
- Any implementation change since the last review, its report, and the test
  result. Any `reports/defect-ledger/` records you want covered.
- Sampled mechanical runs included in this handover.
- Your current Codex thread id, on a line `Reply-to thread: <uuid>`. Fable
  uses it to wake you.

Requested scope is always ancestor retrieval only.

## After you write a request

You do not need the user to relay. When the verdict is written, Fable queues
a message to your thread ("Verdict ready: <path>") with `codex queue
--resume`, which wakes you. If you can also watch `reviews/verdicts/` in the
background, do, but the queued message is the signal to rely on. When it
arrives, act on the verdict:

1. Check that the artifact hashes listed in the verdict match the run
   directory. If they do not, the verdict does not apply; say so in a new
   request.
2. **Approved:** record it with
   `python3 -m teacher.ancestor_context approve --run RUN --packet ORIGINAL_PACKET --reviewer Fable --note '...'`,
   citing the verdict's path and SHA-256 in the note. For a replacement, mark
   the old attempt superseded for future retrieval; edit neither run.
   Then do what the verdict's "Next" section says and resume the walk.
3. **Rejected:** do not repair the prose. Use the rejection path in the
   approval policy, rebuild affected packets, and author a fresh attempt
   directory.
4. **HELD:** stop and tell the user. A held verdict is a question for them.

Put the verdict's follow-ups into your own tracking so they are not lost.
"Must fix before canonical use" items do not block ancestor retrieval.

## Lines that do not move

- Nothing from a review reaches the teacher. No verdict text, expected
  answers or reviewer notes in a packet, prompt or standing instruction.
  A lesson from a review becomes a general change only through a user
  decision file. The user decision `thin-entries-and-retroactive.decision.md`
  permits separate pointer-only coverage requests for fresh attempts; inspect
  them for conclusions, hindsight and length quotas before binding their exact
  hash. Verdicts and reviewer findings still never become teacher input.
- Approval means ancestor retrieval only. Canonical and training stay false.
- Authored runs are immutable. A fix is a new attempt.
- A commit sees its strict ancestors and evidence as of its cutoff, nothing
  later.
- Policy questions go to the user, not to Fable and not decided by you.
- Run `EXDEV_SANDBOX_TESTS=1 python3 -m unittest discover -s tests` before
  asking for review of an implementation change.

## Talking to the user

One plain line when you write a request and one when you record a verdict.
No long summaries unless asked.
