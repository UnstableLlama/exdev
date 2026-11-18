# Decision: the teacher may repair a validator refusal once, in the same session

Recorded by Fable (reviewer) on 2026-11-17, about 00:45 UTC.

## The user's words

After 255/003 completed its work and was discarded by `validate_annotation` for a citation label
("Source inspection requires source evidence"), I asked: "Let the teacher fix its own citation errors in the
same session instead of losing the run?" and recommended allowing it. The user answered:

> Yes, allow it

## What is decided (my reading, stated so the user can correct it)

1. When the automatic validator refuses a teacher's final annotation, the validator's own error message may
   be returned to the teacher **once**, in the same session, and the teacher may answer with a corrected
   complete annotation. It may make further tool calls first if the repair needs them (for example a direct
   file read to support a check).
2. Only the validator's message is returned, verbatim. Nothing from the reviewer, the author, a verdict, the
   ledger or any other attempt. The author adds no explanation or hint.
3. One repair per run. If the second annotation is refused too, the run fails as it does today and the
   existing recovery rules apply.
4. The validator's rules are not weakened or changed by this.
5. Labelling: a run that used its repair is marked as such in provenance and in the request
   (`validation_repair: true`, with the refused annotation and the message kept in the transcript). It is not
   reviewer-assisted on that account.
6. Scope stays ancestor retrieval only; canonical and training stay false. Whether repaired entries are
   eligible for anything beyond that is a later question.

## What happens next

The author files an implementation request (where in the session loop the message is returned, the exact
wording wrapped around it if any, replay and validation of the repaired run, provenance, tests). I review it
before it is used. It is the smallest of the three pending changes and saves the most waste, so it comes
**first**, ahead of run-ahead and revision mode. 255/004 already authorised runs under today's rules.
