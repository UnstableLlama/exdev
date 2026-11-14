# Astra: working with the reviewer

Read this at the start of every session and after any context reset. It
covers only the handoff with Fable, the independent reviewer. The walk itself
is defined by `docs/ancestor-approval-policy.md`, `docs/ancestor-context.md`
and `teacher/README.md`; if this file disagrees with those or with the user,
they win.

## User pause — 2026-11-13

**Paused by user for commit/push/archive. Do not start any teacher run until an
explicit restart.** Journal status is `paused_by_user`, `next_position: 75`.
Positions 2–74 have active ancestor-retrieval approvals (including mechanical
approvals); canonical/training remain false. Latest active entries are 71/002
(reviewer-assisted), 72/002 and 73/001–74/001 (unassisted). Rejected attempts stay
rejected. 39/005 remains approved and in force.

Owed first: **39/006, unassisted**, under
`reviews/verdicts/commit-000039-deci-references.decision.md`, then full review,
then commit 75. No 39/006 teacher run or request exists; commit 75 is unstarted.
Deci discovery and recovery are saved: five matching repositories have complete
configs/headers; a sixth, DeciLM-7B-instruct-GGUF, has only config.json and fails
the accepted evidence validator. The user choice between excluding this derived
representation and supporting explicitly incomplete config-only evidence is still
pending. See `reports/commit-000039-reference-recovery-006.json`. Preserve the four
NVIDIA references and original packets. Dependent readers are listed in
`reports/commit-000039-replacement-dependents-006.json`; do not re-author them
without authorization. 39/005 stays in force until 006 is reviewed.

Resume with contract 8 / guidance 5 / salience-v2 and Codex 0.167.0 first on PATH.
Reference discovery implementation 001 is accepted; latest full suite: 223
host-enabled tests passed. Discovery must cover every official publishing
organization, including the original publisher; record the organizations and why.
Recover new open/closed catalogs without rewriting historical bound bundles.
Prepared packets, caches, mirror and store may be local assets; verify them after
moving machines. On restart archive this pause, retain next_position 75 and
approved-entry selection, and complete the replacement before advancing the walk.

Open follow-ups from today's verdicts (administrative, never teacher input):

- Discovery: distinguish absent root config from unreadable evidence; organization
  coverage can span publishers. No further rebuild of 39 beyond the user decision.
- Count catalogs directly from bundles: 73 and 74 have seven open rows, not six.
- Report `run` file reads separately from repo_read metrics; binary image sections
  should be distinguished from incomplete text coverage (74's unread image was
  accepted explicitly).
- 71's FP32 MLP-intermediate finding remains suspected and draft-only. Packed-scale
  parent behavior and tensor truth tests need canonical follow-up, not teacher hints.
- 72's partial-rope-frequency-load is confirmed at source level, still suspected
  without execution. Establish its introducing commit before any ledger revision;
  keep one defect. Canonical use still needs tensor headers and the link to 71.
- 74's zero-block-scale is an ineffective guard with no wrong output shown; keep
  suspected. Preserve inherited detachment-diagnostic identity. Canonical follow-up:
  inspect the Humaneval figure, README removal and paged encoder launch bounds.
- Required architecture fixes 1 and 2 remain due before position 100; five older
  invalid ledger origins remain. Check closed-catalog issue 99 at position 560 and
  issue 233 at 1100. Assisted entries' use beyond ancestor retrieval is undecided.

Fable will commit/push/archive after `reviews/PAUSE-ACK.md`. That ACK is the author's
last write for this pause; no files may be changed after it until work is restarted.

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
