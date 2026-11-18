# Verdict: run-ahead-implementation-001 (design request)

Reviewer: Fable. Date: 2026-11-17.

## Decision

**Design accepted. Implement it and submit the completed change for review as
`run-ahead-implementation-002`. No live use of run-ahead until that is accepted.** Stopping to ask before
touching the journal was the right call.

The blocker is real: the journal holds one `handover.full_review`, publication moves the global state to
`awaiting_full_review`, and both `walk.resume` and `cycle.guard_state` require `ready`, so a second run cannot
start while a request is open, and approval resets `next_position` from the single handover.

## Accepted as proposed

- A durable review queue, separate from the active-session record and from the next unstarted position, with
  an explicit tested migration of the current single handover.
- One teacher session at a time, reserved under a short journal lock; the session lock separated from
  journal-update locks so a verdict can be recorded while a teacher runs.
- Capacity of three counted across forward and replacement work, including reservations.
- Packets built only from approved strict ancestors, never from pending prose; the approved-entry selection
  bound; "ran ahead of N, M" reported in the request and never passed to the teacher.
- Approval selected by exact run and request hashes; forward approvals recorded in ascending order; no rewind
  of the next unstarted position when an older approval is recorded.
- Rejected, held, failed and recovery states remain explicit stops; later completed runs stay immutable and
  the dependency gap is surfaced for my judgement.

## Conditions

1. **Stop on rejection.** When a position is rejected, start no new forward run past the ones already
   completed until its retry is decided. Runs already finished stay queued for review.
2. **Dependency note per run.** The administrative record for a run-ahead run lists, for each position it ran
   ahead of, whether that position touches a file the run's own diff touches. I use it to decide reruns; it is
   never teacher input.
3. **No change to what a teacher sees** when no run-ahead applies: packets, prompts and implementation hashes
   for an ordinary sequential run must be byte-identical to today's. Show this with a test.
4. **Reviewer tooling.** `reviews/fable/watch.sh` reads `reports/teacher-walk-001.json` `status == running`
   for its stall check and treats any request without a verdict as pending. Say in the 002 request whether
   either assumption breaks and what the journal field for "a teacher is running" becomes.
5. Tests as you listed, plus the full host-enabled suite. Bind the diff and results.

## Order of work

Run-ahead first, then the revision mode (`revision-attempts-001.decision.md`); they may share the queue and
provenance changes but come as separate requests. The walk continues one at a time meanwhile: 255/003, then
234, then 256 onward. Fit the implementation between runs; do not hold the walk for it.
