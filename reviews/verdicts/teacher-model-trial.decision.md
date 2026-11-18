# Decision: trial of GPT-6.1-Sol as the teacher model

Recorded by Fable (reviewer) on 2026-11-16.

## The user's words

> hmm. I wonder if we "need" astra for this or if 6.1 sol might do as good of a job? Can you try redoing a
> couple with 6.1 sol instead and compare the results? I notice we are burning through my gpt quota quite fast

## What is decided (my reading, stated so the user can correct it)

A comparison trial: a few already-reviewed commits are authored again by teacher sessions running
`gpt-6.1-sol` instead of `gpt-6-astra`, and I compare the entries. Nothing is adopted by this; changing the
walk's teacher model would be a separate decision by the user after the result. I read "this" as the teacher
sessions, which is where the tokens go; Astra as author and orchestrator in Codex is not part of this trial.

## The trial (mine; an implementation matter)

1. Implementation request `teacher-model-trial-implementation-001`: the teacher model becomes a parameter that
   only a trial supervisor can set. Walk and replacement runs stay pinned to `gpt-6-astra`, medium; validation
   must still reject any other model for a run offered for approval. Provenance and the transcript record the
   model actually used. Guidance text, tools, sandbox and budgets unchanged. The suite.
2. Trial sessions under `.teacher/trials/teacher-model-001/` only; never approved, never ancestor context.
   Model `gpt-6.1-sol`, reasoning effort **medium** (same as the walk, so the model is the only variable),
   guidance 11, each on a copy of the packet of the comparison run, unassisted, no reviewer material.
   Positions and the Astra run each is compared with:
   - **213** against the guidance-11 trial run (architecture; tensor headers; no finding expected).
   - **231** against the approved run (small; one numeric finding).
   - **239** against the approved run (one defect finding that needs tracing a value into unchanged code).
3. Request `teacher-model-trial-001`: drafts, transcripts, coverage, tool-call counts and token totals for
   both models side by side, and what the account's usage meter shows for the Sol sessions if it can be read.

What I will judge (reviewer knowledge; must not reach a teacher): whether each Sol entry is accurate against
the source and headers, whether it reports the finding the Astra entry has (231, 239) and the layout facts
(213), whether it invents anything, and the cost.

Weaknesses to state with the result: three positions, one run each.

## Meanwhile

The forward walk continues on `gpt-6-astra`. **Re-authoring replacements are on hold after any already
running** (my call, to save quota until the user has the result; if Sol is adopted the remaining replacements
could use it). The eleven-entry decision itself is unchanged.
