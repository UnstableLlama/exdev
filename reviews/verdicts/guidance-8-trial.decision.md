# Decision: trial of guidance version 8 (a fourth paragraph)

Recorded by Fable (reviewer) on 2026-11-15.

## The user's words

I showed the exact wording below and said I would trial it on 154 and 140. The user asked "what do you think"; I
recommended a trial, said passing on the two commits it was written from is weak evidence, and proposed adding
control commits. After my 174 report I asked "Approve the fourth guidance paragraph wording for a trial with
controls?" and the user answered:

> Approve trial

## What is approved (my reading, stated so the user can correct it)

A trial of the paragraph below, added after the three paragraphs of guidance 7, as `guidance_version` 8. **Not**
adoption for the walk: guidance 7 remains the walk's guidance until I report the trial result and the user says
to adopt.

**D. Existing mechanisms called from a new place.**
When the task starts calling an existing function, method or mechanism from a place that did not call it before,
or copies code that calls it, search the parent tree for its existing callers and read the code around each call.
Compare the conditions, guards, argument preparation and error handling there with the new call; name any that
the new call omits and state what the inspected code would do without it. If there are no other callers, say so.

## The trial

1. Astra adds the paragraph, verbatim, as text selected when a packet's `guidance_version` is 8 or more, gated
   as earlier versions are. The walk's packets keep version 7. This is an implementation change: request
   `guidance-8-implementation-001`, the suite, and a check that a version-7 packet's standing instructions are
   byte-identical before and after.
2. After that is accepted: four **trial** sessions, unassisted, on fresh scratch packets built with version 8 and
   the same cutoff evidence as the approved runs, for positions **154** and **140**, and controls **157** and
   **156**. Trial packets and runs live under `.teacher/trials/`, are never approved, never ancestor context,
   never published, and are not recorded as attempts in the journal.
3. No reviewer material goes to the trial teachers: no coverage request, no verdict text, no ledger.
4. Astra files `reviews/requests/guidance-8-trial-001.md` with the four drafts, transcripts, coverage reports and
   tool-call and token counts. I compare each with the approved entry and report to the user.

Pass (reviewer knowledge; must not reach a teacher): at 154 and 140 the teacher finds, on its own evidence, what
the new call drops that the existing callers have; at 157 (a new call site that is fine) and 156 (no new call
site) the entry is not padded with speculation or false findings, and the extra tool calls are few. If the
controls show the word "mechanism" being stretched to commits it does not fit, I will propose cutting it to
"function or method" before any adoption.

## Order of work

The walk continues meanwhile on guidance 7. The implementation request does not need the walk paused. The trial
sessions may run between commits.
