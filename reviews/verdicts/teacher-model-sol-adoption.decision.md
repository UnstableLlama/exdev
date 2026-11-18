# Decision: GPT-6.1-Sol becomes the walk's teacher model

Recorded by Fable (reviewer) on 2026-11-16.

## The user's words

I reported the trial (`reviews/verdicts/teacher-model-trial-001.md`: Sol's entries for 213, 231 and 239 as
accurate as Astra's and slightly more thorough, nothing invented; 71 tool calls against 53 and 58% more tokens
on the one paired figure), then OpenAI's Codex rate card (Astra 250 / 25 / 1,250 credits per 1M input / cached
input / output tokens; GPT-6.1 Sol 50 / 2.5 / 250), which puts the 213 session at about 13 credits on Sol
against about 64 on Astra. I stated the caveats: three commits, one run each; the rate card is written for
credit plans and does not say the user's weekly meter uses the same weights. I recommended switching and
asked: "Switch the teacher sessions to Sol from the next commit?" The user answered:

> Switch teacher to Sol

## What is adopted (my reading, stated so the user can correct it)

From the next commit after the implementation below is accepted, walk teacher sessions run on `gpt-6.1-sol`
at medium reasoning effort, guidance 11. Entries already approved are not re-authored because of this.
Astra remains the author and orchestrator in Codex; that is not changed by this decision.

## How to implement it (mine; an implementation matter)

- Request `teacher-model-sol-adoption-001`: the walk default model becomes `gpt-6.1-sol`, medium. Validation
  and ancestor approval accept a run whose provenance and server-confirmed runtime are Sol/medium or, for
  runs already authored, Astra/medium; anything else, `trial_only` runs and runs under `.teacher/trials` are
  still rejected. Provenance and `teacher_runtime` record the model for every run. Instructions, tools,
  sandbox, budgets and the cloned catalog profile as in the trial. Existing packets, runs and approvals
  untouched and still valid. The suite.
- Finish any commit already in progress on Astra. Do not start another until the request is accepted.
- Each review request states the teacher model.

## Re-authoring

The hold placed in `teacher-model-trial.decision.md` ends when the adoption request is accepted. The nine
remaining replacements (103, 110, 141, 158, 164, 213, 214, 225, 234) then run on Sol under the accepted plan,
unchanged otherwise. 72/003 and 98/002 (Astra) stand.

## What I will watch (reviewer)

The first several Sol entries get the same full review as any other. If Sol misses a finding I can see, or
states something false, I report it to the user with the commit, and the user decides whether to go back.
A meter reading before and after a large Sol session, when one occurs with nothing else running.
