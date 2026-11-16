# Decision: adoption of guidance version 9 (the fifth paragraph, as first trialled)

Recorded by Fable (reviewer) on 2026-11-16.

## The user's words

I reported the guidance-10 trial (`reviews/verdicts/guidance-10-trial-001.md`): not passed, 188's device-less
cache still under limits, both controls clean, 44 tool calls against 35. I recommended adopting the version-9
paragraph without the extra clause, said what it achieved in its trial (`reviews/verdicts/guidance-9-trial-001.md`:
190, 184's bias and 188's native checks became findings, controls clean, about a fifth more tool calls), what it
misses (cases like 188's cache) and the weaknesses of the evidence (wording written with the targets in view, one
run per position, the version-9 run at 184 lost a finding). I asked: "Adopt the version 9 fifth paragraph
(without the extra clause) as the walk's guidance?" The user answered:

> Adopt version 9

## What is adopted (my reading, stated so the user can correct it)

From the next commit after the implementation below is accepted, every walk teacher's standing instructions end
with the four paragraphs of guidance 8 followed by this paragraph, exactly as trialled at version 9. Entries
already approved are not re-authored. The version-10 text is not adopted.

**E.**
When the task removes, comments out or bypasses a check, guard, conversion or initialisation, or replaces a call
that performed one, read the removed or bypassed code and say what it prevented or guaranteed. Then say whether
anything in the inspected code still prevents or guarantees it. If nothing does and the source shows an input or
call path that reaches the unguarded case, report it under findings as suspected, with its limits; do not leave
it only under uncertainty. If you could not establish a path that reaches it, say what you searched.

## How to implement it (mine; an implementation matter, not the user's words)

- The version-9 text (`GUIDANCE_9_ADDITION`) is already in the code as trialled and stays byte-identical, so the
  five guidance-9 trial packets reproduce. The version-10 text also stays, so its three trial packets reproduce;
  no walk packet is prepared at version 10. The only change needed is the default: `prepare()` writes 9 for new
  walk packets.
- Existing packets and runs are untouched and must still validate and reproduce byte-identical instructions at
  versions 5 to 8 and 10.
- Request `guidance-9-adoption-001` with the patch, the suite, and a check that a freshly prepared packet gets
  version 9 and instructions equal to guidance 8 plus this file's paragraph.
- Finish any commit in progress under guidance 8 first. After its verdict, do not start another commit until the
  adoption request is accepted.

## Owed afterwards

After a few commits under guidance 9: cost and effect against 178 to 198, as was done for 7 and 8.
