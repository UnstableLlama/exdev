# Verdict: commit-000236-001

Reviewer: Fable. Date: 2026-11-16. Upstream `9a24e0ce` "Update multimodal example".

## Decision

**Approved for ancestor retrieval only.** Canonical and training stay false. The finding
`mistral-template-prefix` is **accepted as true**.

## Artifacts

Request hashes match. `check.py` clean: manifest and provenance agree, 44 implementation hashes, 15 evidence
calls all cited, final equals annotation, 235 ancestors, 3248 blobs, catalog consistent, nothing after the
cutoff (2025-06-03T01:10:21Z). Instructions identical to 235's run. Guidance 9.

## Run checks

- Replay: 15 of 15 calls identical.
- Diff read at parent `ec00ef3f` and task: `get_stop_conditions` gains a `mistral` case returning the tokenizer
  EOS; `multimodal.py` defaults to `mistral3`, with `gemma3` still selectable through the new `match`. As the
  entry says.
- Callers: I listed every use of `format_prompt` and `get_stop_conditions` under `examples/` at the task. The
  four other scripts set `llama3`; only `multimodal.py` reaches the new branch, in both its streaming and
  non-streaming paths. As the entry says.
- The finding: parent `format_prompt` has `f"<s>[INST] {sp}\n\n n{p}[/INST]"`, a space and a literal `n` before
  the user text. The teacher's execution output is what that line produces. Before this commit no example
  selected the Mistral format; now the default example does. This is the pattern I have been watching (a new
  caller reaching an already described defect) and the teacher caught it unprompted, from the ancestor entry.
- Statements about the vision model (`PixtralImageProcessorFast` assertion, patch-size agreement, row
  separators) match `mistral3.py` at the parent.
- PR 25 is marked as contextual inference, which is right; nothing links it to this commit.

## Not verified

- Whether the stray characters change model output in practice. Nobody ran a model.
- Whether this "quick and dirty" template otherwise matches the reference chat template for Mistral Small 3.1.
  The entry does not claim it does.

## Reviewer knowledge (hindsight; must not reach a teacher)

- Upstream `fcce0e69` (2025-11-10, "Fix example Mistral template") changes that line: it
  removes the `n`, leaving `{sp}\n\n{p}`. That confirms the finding. The fix is far ahead of the walk.
- From 234: the image-size overflow (112 patches against a 110-wide table) is now on the default example's
  path. Not this commit's doing and not expected in the entry.

## Follow-ups

- Ledger item owed with the next request: `mistral-template-prefix`, introduced where the Mistral case of
  `format_prompt` first appears (the "usage" ancestor the entry cites; give the position), made reachable from
  an example at 236, no fix at or before the walk position. Eligibility flags false.

## Next

Record the approval and proceed to 237.
