# Decision: adoption of guidance version 12 (paragraph F with the added sentence)

Recorded by Fable (reviewer) on 2026-11-16.

## The user's words

I reported the guidance-12 trial (`reviews/verdicts/guidance-12-trial-001.md`): a partial pass. 214 met; 98
and 110 improved (mechanism stated, absence stated for the checkpoint read; 110's split between checkpoints
not found); 103 not met; both controls clean; all findings retained; one new true observation at 98; 22% more
tool calls and, on 214, nearly three times the tokens. I said differences between checkpoints are still
missed and that I would keep that comparison at review, stated the caveats (wording written with the targets
in view, one run each), recommended adoption, and asked: "Adopt the added sentence as the walk's guidance
(version 12)?" The user answered:

> Adopt version 12

## What is adopted (my reading, stated so the user can correct it)

From the next commit after the implementation below is accepted, every walk teacher's standing instructions
are the guidance-11 text with paragraph F replaced by the revised F, exactly as trialled at version 12:

**F.**
When the task adds or changes a model architecture, or code that names checkpoint tensors or depends on their
shapes or orientation, and tensor headers for reference checkpoints are listed in the evidence index, read the
headers of at least one reference checkpoint for each distinct configuration. Say which tensor names and shapes
the changed code relies on and whether each exists with that shape, and name any stored tensors the code never
reads. Check every tensor name the code requests, including alternate and optional names, against the names in
the header, and say which are absent and which path the code then takes. Do not describe tensor layout as
unestablished while headers are available and unread.

## Re-authoring

The replacement pause ends when the adoption request is accepted. The remaining replacements then run at
guidance 12 on Sol under the accepted plan: **110** (a fresh attempt, authorised here; 110/002 stays
declined), then 141, 158, 164, 213, 214, 225, 234. 72/003, 98/002 and 103/002, approved at guidance 11,
stand; they are not redone for this change.

## How to implement it (mine; an implementation matter)

- `GUIDANCE_12_ADDITION` and its branch are in the code as trialled and stay byte-identical so the six trial
  packets reproduce. The only change needed is the default: `prepare()` writes 12 for new walk packets.
- Existing packets and runs untouched and still valid at versions 5 to 11.
- Request `guidance-12-adoption-001` with the patch, the suite, and a check that a freshly prepared packet
  gets version 12 and instructions equal to this file's text.
- Finish any commit in progress under guidance 11 first; start no other until the request is accepted.

## What stays with the reviewer

Comparing branch-deciding tensors across every reference checkpoint (which store them, which do not). I do
this at review from the headers on disk and record it in the verdict.
