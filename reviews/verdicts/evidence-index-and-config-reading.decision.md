# User decision: read every attached configuration, and offer all earlier evidence through an index

Recorded by: Fable (independent reviewer; file mailbox)
Decided by: the user, in chat, 2026-11-13:
- On reading every attached configuration: "absolutely read every one".
- On carrying evidence forward: "absolutely offer all reference evidence, i would say offer literally everything, but dont flood the context with non critical stuff in full, but they should know its available in an index or table of context".
Relates to: `reviews/verdicts/commit-000039-002.md`, `commit-000044-001.md`, `commit-000045-001.md`, `commit-000055-001.md`

## Why

- At commit 39 four reference models were attached and the teacher opened one, the only one that could not distinguish the two readings of the head-count line.
- At commits 44, 45 and 55 those same reference models were older than the cutoff and directly relevant, and were not offered at all, because evidence is attached per commit and does not carry forward.

Canonical and training remain false throughout. Nothing in this file is teacher input except the guidance sentence in Decision 1 and the index in Decision 2.

## Decision 1: read every attached configuration (standing guidance)

Add one general rule. Suggested wording; Astra may adjust phrasing but not widen the meaning:

> When reference configurations for more than one model are supplied or listed in the evidence index, read every model's config.json before stating that a mapping, dimension or default is corroborated. Name the models read. If any was not read, say so and limit the claim to those that were.

- It applies to configuration files, not to every tensor header.
- It names no model, architecture or defect.

## Decision 2: an index of everything already attached to ancestors

The user's instruction is to offer everything and not to flood the context. I am recording that as follows.

What the reviewer will check:

1. **What is offered.** Every evidence object that was attached to the packet of any strict ancestor of the task: reference model files and headers, and referenced issue or pull-request objects. All of it is older than the task's cutoff by construction, but the builder must still check each object's dates against the task's own cutoff and drop anything that fails.
2. **How it is offered: an index, not content.** The opening context gains a compact index. One row per source, not per object: for a model repository, the repository, pinned revision and date, the ancestor that attached it, and counts by role (for example "4 configuration files, 22 headers"); for a discussion, its kind, number, title and the ancestor that attached it. No file bodies, no excerpts, no reviewer or curator notes.
3. **Fetched on demand** with the existing tools (`hf_fetch`, `safetensors_header`, `web_fetch`), which must serve indexed objects exactly as they serve directly attached ones.
4. **Bounded.** The index has a size cap and a truncation flag, like the ancestor catalog. If it is truncated, the remainder must be reachable by paging, so "offered" stays true.
5. **Evidence attached for the task itself is unchanged** and still listed directly. While doing this, apply the same no-flooding rule to it: a new-architecture commit should list its reference models by source with counts, not one row per header. (Commit 39's opening catalog had 205 rows.)
6. **Ancestors only.** A branch commit sees what its own ancestors had attached, not what was attached on the other side of a later merge.
7. **Navigation, not instruction.** The index says what exists. It does not say what to look for or which commit it is relevant to, beyond naming the ancestor that attached it.
8. **Bound into the contract.** The index content and the objects it can serve are hashed into the walk input contract; a changed or missing object fails validation. Packets built before this decision keep their recorded context and replay.
9. **Tests:** an ancestor's objects appear in a descendant's index; a non-ancestor's do not; an object dated after the task cutoff is dropped; the cap and paging; fetch of an indexed object; contract binding; the legacy case.
10. **Documented** next to the existing evidence rules.

## Scope and order

- **Forward only.** No earlier commit is re-authored for this decision. In particular commit 39 is not authored a third time (see its attempt 002 verdict).
- Finish any run already in progress and have it reviewed under the current contract. Then implement both decisions, with tests, before authoring further commits, and describe the implementation in a request so it can be reviewed.
- Required fixes 1 and 2 from the earlier implementation verdict are still due before position 100; doing them in the same change is welcome.

## Not included

"Offer literally everything" could also be read to cover discussions that were already closed at the cutoff, which the unreferenced catalog deliberately leaves out. I have not included that; it would change an earlier decision (`commit-000017-001.decision.md`). If the user wants it, it is a separate decision.

If building this shows a serious cost or a conflict with the no-hindsight boundary, say so in a request file before proceeding.
