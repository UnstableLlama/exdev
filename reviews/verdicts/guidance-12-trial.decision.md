# Decision: trial a one-sentence addition to paragraph F (version 12)

Recorded by Fable (reviewer) on 2026-11-16.

## The user's words

I reported that header-reading entries keep omitting tensors the code names that the checkpoint does not hold
(214 in the guidance-11 trial, 98/002, 103/002, and 110/002, which I declined because it cost content the old
entry had), on both teacher models. I gave the sentence I would add, said the trial would rerun 98, 103, 110
and 214 on Sol with two controls and that adoption would be their decision from the result, and asked: "Trial
one added sentence in the header guidance before the remaining re-authoring runs?" The user answered:

> Yes, trial it

## What is decided (my reading, stated so the user can correct it)

A trial only. The walk default stays guidance 11 until the user decides on adoption from the result.

## Proposed text (version 12 = the guidance-11 text with paragraph F replaced by this)

**F (revised; the added sentence is the third).**
When the task adds or changes a model architecture, or code that names checkpoint tensors or depends on their
shapes or orientation, and tensor headers for reference checkpoints are listed in the evidence index, read the
headers of at least one reference checkpoint for each distinct configuration. Say which tensor names and shapes
the changed code relies on and whether each exists with that shape, and name any stored tensors the code never
reads. Check every tensor name the code requests, including alternate and optional names, against the names in
the header, and say which are absent and which path the code then takes. Do not describe tensor layout as
unestablished while headers are available and unread.

## The trial

1. Implementation request `guidance-12-implementation-001`: version 12 as above, its own branch; versions 5
   to 11 byte-identical; walk default stays 11; validator accepts 12. The suite.
2. Trial sessions on Sol, medium, unassisted, on copies of the packets with only `guidance_version` set to
   12, under `.teacher/trials/guidance-12-001/`, confined and unapprovable like the other trials. No
   reviewer material.
   Targets: **98, 103, 110, 214**. Controls: **243, 245** (no architecture; nothing should be added).
3. Request `guidance-12-trial-001` with drafts, transcripts, tool calls and tokens beside the guidance-11 runs
   (98/002, 103/002, 110/002, the guidance-11 trial run of 214, and the approved 243 and 245).

Pass (reviewer knowledge; must not reach a teacher): each target states which requested tensors are absent
and the path taken (98 and 103: no `lm_head` anywhere, tied path always; 110: the split between checkpoints
that store `lm_head` and those that rely on the fallback; 214: no stored output head), keeps what its
guidance-11 run had, and the controls gain nothing. Report the extra calls.

Weaknesses to state: wording written with these targets in view; one run each; 98 and 214's comparison runs
were authored by Astra, so model and wording are both changed there.

## Meanwhile

Replacements stay paused; the forward walk continues on guidance 11.
