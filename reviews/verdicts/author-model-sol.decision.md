# Decision: the author's Codex session moves to GPT-6.1-Sol

Recorded by Fable (reviewer) on 2026-11-16.

## The user's words

After "Switch teacher to Sol" I wrote that the author's own role was unchanged. The user objected ("wait what
the heck do you mean astras role is unchanged, what did we just talk about?"). I explained that the Astra model
is used in two places, the teacher sessions and the Codex session that authors code and runs the walk, that
only the first had been switched, that the second looked like a large share of the quota, that Sol is untested
in that role, and that I review everything it produces. I asked: "Move the Codex window that runs the walk to
Sol as well?" The user answered:

> Yes, move it too

## What is decided (my reading, stated so the user can correct it)

The Codex session that acts as the author (thread `01a1da07-7653-7b81-8507-f69683828acb`) runs on
`gpt-6.1-sol` at medium effort from the moment the user changes the model in that window. The role, its
rules (`reviews/AUTHOR-INSTRUCTIONS.md`), the thread and the name "Astra" for the role in our files stay as
they are; only the model behind it changes. The user can switch back at any time.

This is separate from `teacher-model-sol-adoption.decision.md`, which changes the teacher sessions.

## What I will do (reviewer)

- Review every implementation request and every review request as before, and read the first several
  produced under Sol with extra care for: rules skipped (starting a teacher session before a gate is
  accepted, writing outside its areas, touching approved artefacts), hash lists that do not match, claims in a
  request that the files do not bear out, and suite results.
- Report any such lapse to the user plainly with the request name. Two lapses of substance and I recommend
  going back to the Astra model for the author.
- Each request should state which model authored it, so the record shows where the change happened.

## Correction, 2026-11-16 20:35 UTC (Fable)

**The switch has not taken effect.** The author session's own log
(`~/.codex/sessions/2026/11/14/rollout-…-01a1da07-….jsonl`) records the model on every turn; all 430 turn
records, the latest at 20:32 UTC, say `gpt-6-astra`, medium, and `~/.codex/config.toml` still names
`gpt-6-astra`. The user's decision stands but the model change in the Codex window has not been made (or did
not take).

Every request from `commit-000243-001` onward that says "Author/orchestrator: gpt-6.1-sol / medium" is wrong
on that point. The teacher model statements in those requests are right (provenance and server-confirmed
runtime say `gpt-6.1-sol`). I repeated the author claim to the user from the requests without checking it;
I have told the user. From now on I read the author model from the session log, and requests should not
state an author model the author cannot verify.
