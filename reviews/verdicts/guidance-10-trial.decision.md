# Decision: trial of guidance version 10 (the fifth paragraph, revised)

Recorded by Fable (reviewer) on 2026-11-16.

## The user's words

I reported the guidance-9 trial as mixed (`reviews/verdicts/guidance-9-trial-001.md`): 190 and 184's bias found,
188's device-less cache still under uncertainty, both controls clean, about a fifth more tool calls. I
recommended: "revise and re-test, not adopt yet. I would add one clause so the first sentence also covers 'a call
that used to run every time and now runs once or only under a condition', then re-run 188 and the two controls
(three sessions). If 188 still does not move, I would adopt the paragraph as originally worded for what it does
achieve." I asked "What should happen with the fifth guidance paragraph?" and the user answered:

> Revise and re-test

## What is approved (my reading, stated so the user can correct it)

A trial, not adoption, of the fifth paragraph with exactly the clause I quoted to the user inserted in its first
sentence, as `guidance_version` 10. The user saw the clause in quotation marks but not the whole revised
paragraph; the full text below was shown to them in my reply at the time of this decision. Nothing else in the
paragraph changes. Guidance 8 remains the walk's guidance.

**E, revised.**
When the task removes, comments out or bypasses a check, guard, conversion or initialisation, replaces a call
that performed one, or changes a call that used to run every time so that it now runs once or only under a
condition, read the removed or bypassed code and say what it prevented or guaranteed. Then say whether anything
in the inspected code still prevents or guarantees it. If nothing does and the source shows an input or call path
that reaches the unguarded case, report it under findings as suspected, with its limits; do not leave it only
under uncertainty. If you could not establish a path that reaches it, say what you searched.

## The trial

1. Astra adds this text, verbatim, as what a packet with `guidance_version` 10 or more receives after the
   guidance-8 text **in place of** the version-9 paragraph. Version 9 keeps its trialled text so the five
   guidance-9 trial packets reproduce. The walk's packets keep version 8. Implementation request
   `guidance-10-implementation-001`, the suite, and a check that version-8 and version-9 packets' standing
   instructions are byte-identical before and after.
2. After that is accepted: three **trial** sessions, unassisted, fresh scratch packets at version 10 with the
   approved runs' cutoff evidence, for position **188** and controls **189** and **178**. Under
   `.teacher/trials/` only; never approved, never ancestor context, not journal attempts.
3. No reviewer material goes to the trial teachers.
4. Astra files `reviews/requests/guidance-10-trial-001.md` with drafts, transcripts, coverage and tool-call and
   token counts.

Pass (reviewer knowledge; must not reach a teacher): at 188 the kernel-attribute cache keyed without a device is
reported as a suspected finding with its limits; 189 and 178 gain no finding.

What I told the user I would recommend afterwards: if 188 moves and the controls stay clean, adopt the revised
text; if 188 does not move, adopt the version-9 text for what it achieves and say what it does not catch. Either
adoption needs the user's decision.

## Order of work

The walk continues meanwhile on guidance 8. The trial sessions may run between commits.
