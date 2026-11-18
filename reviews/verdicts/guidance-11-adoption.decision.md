# Decision: adoption of guidance version 11 (guidance 9 plus the tensor-header paragraph F)

Recorded by Fable (reviewer) on 2026-11-16.

## The user's words

I reported the guidance-11 trial (`reviews/verdicts/guidance-11-trial-001.md`): 213, 225 and 234 met the
criteria, 214 half (names stated, the missing output head not), both controls clean, every quoted shape checked
by me against the headers, 149 tool calls against 123 (+21%, nearly all at 225). I stated the caveats (wording
written with the four targets in view, one run each; teachers sample one or two header files so my own check
stays; the 214 miss not worth a reword now) and recommended adoption. I asked: "Adopt guidance version 11 as the
walk default?" The user answered:

> Adopt version 11

## What is adopted (my reading, stated so the user can correct it)

From the next commit after the implementation below is accepted, every walk teacher's standing instructions are
the guidance-9 text followed by this paragraph, exactly as trialled at version 11.

**F.**
When the task adds or changes a model architecture, or code that names checkpoint tensors or depends on their
shapes or orientation, and tensor headers for reference checkpoints are listed in the evidence index, read the
headers of at least one reference checkpoint for each distinct configuration. Say which tensor names and shapes
the changed code relies on and whether each exists with that shape, and name any stored tensors the code never
reads. Do not describe tensor layout as unestablished while headers are available and unread.

Unlike the guidance-9 adoption, **earlier entries are re-authored**: the eleven listed in
`guidance-11-reauthoring.decision.md` (72, 98, 103, 110, 141, 158, 164, 213, 214, 225, 234), whose condition
(adoption) is now met. Its constraints stand: a plan request first, no replacement run before the plan is
accepted.

## How to implement it (mine; an implementation matter, not the user's words)

- `GUIDANCE_11_ADDITION` and the version-11 branch are already in the code as trialled and stay byte-identical,
  so the six trial packets reproduce. The only change needed is the default: `prepare()` writes 11 for new walk
  packets.
- Existing packets and runs are untouched and must still validate and reproduce byte-identical instructions at
  versions 5 to 10.
- Request `guidance-11-adoption-001` with the patch, the suite, and a check that a freshly prepared packet gets
  version 11 and instructions equal to guidance 9 plus this file's paragraph.
- Finish any commit in progress under guidance 9 first. After its verdict, do not start another commit until
  the adoption request is accepted.
- Then `guidance-11-reauthoring-plan-001`. The walk may continue forward while the plan is reviewed.
