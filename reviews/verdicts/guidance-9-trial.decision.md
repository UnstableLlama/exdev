# Decision: trial of guidance version 9 (a fifth paragraph)

Recorded by Fable (reviewer) on 2026-11-15.

## The user's words

After 190 I reported that at 184, 188 and 190 the teacher had seen the relevant fact (a bypassed function, a
cache without a device key, a removed reshape that doubled as a check) and filed it under "not established"
instead of as a suspected finding, and asked whether to draft a guidance sentence. The user answered "Draft it".
I showed the exact wording below, the reasons, a trial plan with targets 184, 188, 190 and controls 189, 178, and
the risks. After my 191 report I asked "Approve the fifth guidance paragraph wording for a trial with controls?"
and the user answered:

> Approve trial

## What is approved (my reading, stated so the user can correct it)

A trial of the paragraph below, added after the four paragraphs of guidance 8, as `guidance_version` 9. **Not**
adoption for the walk: guidance 8 remains the walk's guidance until I report the trial result and the user says
to adopt.

**E. Removed or bypassed protection.**
When the task removes, comments out or bypasses a check, guard, conversion or initialisation, or replaces a call
that performed one, read the removed or bypassed code and say what it prevented or guaranteed. Then say whether
anything in the inspected code still prevents or guarantees it. If nothing does and the source shows an input or
call path that reaches the unguarded case, report it under findings as suspected, with its limits; do not leave
it only under uncertainty. If you could not establish a path that reaches it, say what you searched.

## The trial

1. Astra adds the paragraph, verbatim, as text selected when a packet's `guidance_version` is 9 or more, gated
   as version 8 is. The walk's packets keep version 8. Implementation request `guidance-9-implementation-001`,
   the suite, and a check that a version-8 packet's standing instructions are byte-identical before and after.
2. After that is accepted: five **trial** sessions, unassisted, on fresh scratch packets built with version 9 and
   the same cutoff evidence as the approved runs, for positions **184, 188, 190** and controls **189** and
   **178**. Trial packets and runs live under `.teacher/trials/`, are never approved, never ancestor context,
   never published, and are not journal attempts.
3. No reviewer material goes to the trial teachers: no coverage request, no verdict text, no ledger.
4. Astra files `reviews/requests/guidance-9-trial-001.md` with the five drafts, transcripts, coverage reports and
   tool-call and token counts. I compare each with the approved entry and report to the user.

Note on comparison: 178 and 184 to 190 were authored under guidance 8, so every comparison here isolates the new
paragraph, unlike most of the guidance-8 trial.

Pass (reviewer knowledge; must not reach a teacher): at 184, 188 and 190 the teacher reports, as suspected
findings on its own evidence, what the 184, 188 and 190 verdicts list under "Must fix" or "Reviewer finding" for
the bypassed or removed protection; at 189 (a removed zero-fill that is safely overwritten) and 178 (three
assertions the caller already enforces) no finding is added, and the extra tool calls are few.

## Order of work

The walk continues meanwhile on guidance 8. The implementation request does not need the walk paused. The trial
sessions may run between commits.
