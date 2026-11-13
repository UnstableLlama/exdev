# Amendment: the configuration-reading rule has no opt-out

Recorded by: Fable (independent reviewer; file mailbox)
Authority: the user's decision of 2026-11-13, "absolutely read every one", already recorded in `evidence-index-and-config-reading.decision.md`. This file corrects my wording of that decision; it is not a new policy.
Relates to: `reviews/verdicts/commit-000039-003.md`

## What went wrong

My suggested sentence ended "If any was not read, say so and limit the claim to those that were." Commit 39 attempt 003 used that clause to read one of four attached models. That is the opposite of what the user asked for.

A rule to read every listed model would be wrong the other way: at later commits the index lists models of every architecture attached so far, most of them irrelevant. The rule has to say which models, and the teacher has to be able to tell which those are without opening them.

## Decision

### 1. Index rows for models name their architecture

For each model source in the evidence index, trusted code adds an `architectures` field copied from that model's pinned `config.json` (the value of its `architectures` key). It is navigation metadata, bound into the index digest like the rest. If the configuration has no such key, the field is an empty list.

### 2. Replace the guidance sentence

Replace the current configuration-reading sentence with this. Astra may adjust phrasing but not add an opt-out:

> When the evidence index lists more than one model whose architectures include an architecture that the task adds or changes, read the config.json of every such model before finalizing. Name each model read and say, model by model, whether the mappings, dimensions and defaults you describe hold for it. If a read fails, say so.

- "Adds or changes" means the task diff registers that architecture or modifies its model or configuration class.
- It applies to configuration files only. Tensor headers are read as needed to support what the entry claims.
- It names no model, architecture or defect.

### 3. Versioning

A new guidance version, set only on new packets. Earlier packets keep their recorded prompts and replay.

## Order of work

Implement both parts with tests (the field present and bound; the sentence present for the new guidance version and absent for older ones), send a short implementation request, and after acceptance author `commit-000039-004` unassisted. The remaining replacements (44/002, 45/002, 55/002) follow as already decided.
