# Decision: repair feedback gains one fixed keep-everything-else sentence

Recorded by Fable (reviewer) on 2026-11-17, 17:35 UTC. Amends point 2 of `validation-repair-001.decision.md`.

## The user's words

After 297/001 (one evidence complaint; the teacher rewrote and shortened the whole annotation, five true
points lost) and the size report (four of five repaired finals shorter than the refused version), I
recommended "adding one fixed sentence to the repair feedback: fix only what the validator names and keep
everything else unchanged" and said it departs from the validator-message-only rule. The user answered:

> yeah lets do that.

## What is decided (my reading, stated so the user can correct it)

1. The repair feedback is the validator's message, verbatim, followed by **one fixed sentence**, the same
   for every run, telling the teacher to correct only what the message names and to return the rest of the
   annotation unchanged.
2. The sentence is a constant in the implementation. It carries nothing about the commit, the entry, the
   reviewer, the author or any other attempt. No per-run text may be added.
3. Everything else in `validation-repair-001.decision.md` stands: one repair per run, validator rules
   unchanged, labelling, scope.
4. The policy name changes (not `validator-only-v1`) so provenance shows which feedback a run received.

## What happens next

The author proposes the exact sentence and files `validation-repair-implementation-004` with the diff, tests
(feedback text is exactly message plus constant; nothing else can enter), the full suite, and new hashes. No
teacher session may start while the unaccepted edit is in the tree: develop it in a copy, or pause the walk
for the change. Until it is accepted, repair stays as it is.
