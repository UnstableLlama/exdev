# Decision: guidance on reading tensor headers (a sixth paragraph, to be trialled as version 11)

Recorded by Fable (reviewer) on 2026-11-16.

## The user's words

I reported, at 225 and again at 234, that four new-architecture entries in a row (213, 214, 225, 234) described
weight layout as unestablished although tensor headers for the reference checkpoints were in the packet, and
said I thought guidance should tell teachers to read them, which "would need a trial and your decision, as with
guidance 9". The user answered:

> yeah it looks like we do need to tell them to check the tensor headers though

## What is decided (my reading, stated so the user can correct it)

Teachers are to be told to read tensor headers. I read this as approval to go ahead on the same path as
paragraphs C, D and E: a trial of a specific paragraph first, then adoption on the user's word once they have
seen the result. The walk stays on guidance 9 until then. **The wording below is my proposal; the user has not
seen it.** Show it to them with the trial result, or before the trial if they ask.

**F (proposed).**
When the task adds or changes a model architecture, or code that names checkpoint tensors or depends on their
shapes or orientation, and tensor headers for reference checkpoints are listed in the evidence index, read the
headers of at least one reference checkpoint for each distinct configuration. Say which tensor names and shapes
the changed code relies on and whether each exists with that shape, and name any stored tensors the code never
reads. Do not describe tensor layout as unestablished while headers are available and unread.

## The trial (as for 8, 9 and 10)

1. Implementation request `guidance-11-implementation-001`: a packet with `guidance_version` 11 receives the
   guidance-9 text followed by F. **Not** the version-10 text: the code's `>= 10` branch currently substitutes
   the revised E, so version 11 needs its own branch that uses the version-9 paragraph E. Versions 5 to 10 stay
   byte-identical; the walk default stays 9. The suite, and a check of both.
2. After that is accepted: unassisted trial sessions on scratch packets at version 11 with the approved runs'
   cutoff evidence, under `.teacher/trials/guidance-11-001/` only; never approved, never ancestor context.
   Targets: **213, 214, 225, 234**. Controls: **229** and **231** (no architecture change; nothing should be
   added).
3. No reviewer material reaches the trial teachers.
4. Request `reviews/requests/guidance-11-trial-001.md` with drafts, transcripts, coverage, tool-call and token
   counts.

Pass (reviewer knowledge; must not reach a teacher): each target entry states layout facts from the headers
that the approved entry left unestablished (213: Q/K/V biases present and the unused `mtp_layers` tensors; 214:
unprefixed names and no stored output head; 225: the tower's tensors and the projector stored input-by-output;
234: the projector widths) and the controls gain nothing. Report the extra tool calls.

Weaknesses to state with the result: the wording was written with these four targets in view; one run per
position; 225 and 234 depend on headers being bound in those packets (check before running).

## Related, not part of this decision

- At 234 the reference bundle lacked `preprocessor_config.json` and `processor_config.json` although both exist
  at the pinned revisions. Astra owes an implementation request for recovery to gather them. F does not cover
  that; it is an evidence-gathering fix.
