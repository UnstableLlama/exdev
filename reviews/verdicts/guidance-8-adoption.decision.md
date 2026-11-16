# Decision: adoption of guidance version 8 (the fourth paragraph)

Recorded by Fable (reviewer) on 2026-11-15.

## The user's words

I reported the trial (`reviews/verdicts/guidance-8-trial-001.md`): both targets found, both controls clean,
roughly double the teacher's tool calls on commits where the paragraph applies, and the limits (two targets, two
controls, wording written from the targets, one clean comparison). I recommended adoption and asked: "Adopt the
fourth paragraph as the walk's guidance from the next commit?" The user answered:

> Adopt it

## What is adopted (my reading, stated so the user can correct it)

From the next commit after the implementation below is accepted, every walk teacher's standing instructions end
with the three paragraphs of guidance 7 followed by this paragraph, exactly as trialled. Entries already approved
are not re-authored.

**D.**
When the task starts calling an existing function, method or mechanism from a place that did not call it before,
or copies code that calls it, search the parent tree for its existing callers and read the code around each call.
Compare the conditions, guards, argument preparation and error handling there with the new call; name any that
the new call omits and state what the inspected code would do without it. If there are no other callers, say so.

## How to implement it (mine; an implementation matter, not the user's words)

- The version-8 text is already in the code as trialled and stays byte-identical, so the four trial packets
  reproduce. The only change needed is the default: `prepare()` writes 8 for new walk packets.
- Existing packets and runs are untouched and must still validate and reproduce byte-identical instructions at
  versions 5, 6 and 7.
- Request `guidance-8-adoption-001` with the patch, the suite, and a check that a freshly prepared packet gets
  version 8 and instructions equal to guidance 7 plus this file's paragraph.
- Finish any commit in progress under guidance 7 first. After its verdict, do not start another commit until the
  adoption request is accepted.

## Owed afterwards

After a few commits under guidance 8: cost and effect against 172 to 176, as was done for 7.
