# User decision: reference configurations for new architectures, and following a changed dispatch

Recorded by: Fable (independent reviewer; file mailbox)
Decided by: the user, in chat, 2026-11-13 ("yeah we always want reference configs if a commit adds a new arch"; "again I'd say yes")
Relates to: `reviews/verdicts/commit-000037-001.md`, `reviews/verdicts/commit-000039-001.md`, `reviews/verdicts/commit-000041-001.md`

## Why

- Commit 39 registered a new architecture and was authored with an empty evidence catalog. The draft's main stated limit was the absence of any reference configuration. The root entry, by contrast, was authored with pinned Hugging Face configurations and tensor headers.
- Three drafts (37, 39, 41) stopped at "the source does not explain why" when a nearby file in the parent tree bore on the question. At commit 41 the changed line chooses between two kernels and the draft never opened the one it routes to.

Canonical and training remain false throughout. Nothing in this file is teacher input; only the general guidance sentence in Decision 2 and the evidence objects in Decision 1 reach a teacher.

## Decision 1: attach reference configurations when a commit adds a new architecture

What the reviewer will check:

1. **Trigger, decided by trusted code.** A task commit that adds a key to the architecture registry (`exllamav3/models/architectures.py` or its successor) or adds a new model/config class file under `exllamav3/models/`. The teacher's own type label does not select it.
2. **What is attached.** For each newly registered architecture, at least one public model repository of that architecture: `config.json`, the tokenizer configuration files, and safetensors headers. Same roles and tools as the root evidence (`teacher/root_evidence.py`): immutable revision identifiers, no weight payloads.
3. **As of the cutoff.** The pinned revision must have been committed at or before the task's cutoff. If no such revision exists, attach nothing and record that in the recovery report; do not use a later revision.
4. **Selection is recorded and made without later knowledge.** The recovery report names each chosen repository, why it was chosen (for example: the model the commit message names, or the reference model of the organisation that defines the architecture string), and the candidates considered. The choice must not be made by consulting later commits, later issues or a known defect. Prefer the model the commit message or the eligible discussion names. Where there is a real choice, attach more than one rather than picking the one that makes a point.
5. **Offered, not explained.** The objects appear in the evidence catalog with neutral descriptions. No note says what to look for.
6. **Bound into the contract** like other evidence, so a changed object fails validation. Packets built before this decision keep their recorded context and replay.
7. **Tests** for the trigger (registry key added; class file added; neither), the cutoff filter on revisions, the no-weights rule, and the legacy case.
8. **Documented** next to the existing evidence rules.

## Decision 2: a guidance rule for changed dispatch (standing guidance)

Add one general rule, in the style of the existing ones. Suggested wording; Astra may adjust the phrasing but not widen the meaning:

> When a change alters which function, kernel or code path is selected (a threshold, flag, default, dispatch table or registry entry), read the selected callee or callees in the parent tree before describing the effect. Report what their own limits, tiers or preconditions show, as source inspection. State a conclusion about the author's reason as inference, and say that the rationale is unestablished only after that inspection.

- It names no file, commit, architecture or defect.
- It does not ask for more ancestor reads; retrieval stays report-only.

## Order of work

1. Commit 43 is already authored under the current guidance and is reviewed as such.
2. Implement both decisions, with tests, before authoring commit 44 or later. Say so in a request file, with the new guidance and contract versions, so the implementation can be reviewed with the next run.
3. Then resume the walk.

## Not decided here

**Whether to re-author commits 39 and 41 under the new rules.** The catalog-hints decision did re-author the two commits that motivated it, under strict no-hindsight packets. The same could be done here (39 with reference configurations, 41 with the dispatch rule), and it would matter most for 39, because position 44 fixes a line 39 introduced and will read 39's entry as an ancestor. I have asked the user. Until there is an answer, do not re-author either, and do not author commit 44.

If building this shows a serious cost or a conflict with the no-hindsight boundary, say so in a request file before proceeding.
