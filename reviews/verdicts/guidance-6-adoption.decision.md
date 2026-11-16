# Decision: adopt the trialled guidance for the walk

Recorded by Fable (reviewer) on 2026-11-15.

## The user's words

I reported the trial (`reviews/verdicts/guidance-6-trial-001.md`) and recommended adopting paragraphs A, B and C
with one phrase of A reworded, because A asks for a search of the task tree that the tools do not offer. I
asked: "Adopt guidance 6 for the walk, with paragraph A reworded to match what the tools can search?" The user
asked what the question was; I restated it, with the cost (about 40% more tool calls in the trial) and the gap
it does not close (154). The user answered:

> Adopt it

## What is adopted (my reading, stated so the user can correct it)

From the next commit after the implementation below is accepted, every walk teacher's standing instructions end
with these three paragraphs. Entries already approved are not re-authored.

**A (reworded as proposed to the user).**
When a change alters what a function, constructor, attribute or parameter accepts, returns or stores (its type,
shape, name or meaning), search the whole parent tree, read together with the task diff, for every other
definition, subclass, caller and reader that supplies or consumes it, including files the task diff does not
touch. Inspect each one and say, case by case, whether it agrees with the changed form; name any that the diff
leaves on the old form and state what the inspected code would do with it. A search limited to the changed files
cannot establish that the change is complete.

**B (unchanged from the trial).**
When the task modifies, copies or closely follows a file, class or function that an earlier commit introduced,
find that commit's entry with the ancestor tools and read it before finalizing. Say which entries you read and
what they establish about the code the task relies on, including any guard, precondition or recorded defect; if
you read none, say so.

**C (unchanged from the trial).**
When one commit makes several edits, check whether any of them supplies a precondition another needs before
describing them as independent.

## How to implement it (mine; an implementation matter, not the user's words)

- Keep `guidance_version` 6 exactly as trialled, so the four trial packets still reproduce their sessions. Add
  the adopted text as `guidance_version` 7: the same three paragraphs with A as above. Version 7 replaces the
  version-6 text; it is not appended after it.
- `prepare()` writes 7 for new walk packets; validation accepts 7 under the current contract. Existing packets
  and runs are untouched and must still validate and reproduce byte-identical instructions.
- Request `guidance-7-adoption-001` with the patch, the suite, a check that packets at versions 5 and 6 produce
  unchanged instructions, and a check that the version-7 text equals this file's three paragraphs.
- Finish the commit in progress under guidance 5 first. Do not start another commit until that verdict.

## Not decided here

A fourth paragraph for the kind of gap seen at 154 (an existing mechanism reused from a new place). I told the
user I would trial that separately and report. It needs their approval of wording first.
