# Approved ancestor context

A fresh teacher receives earlier explanations only after an administrative reviewer approves exact artifacts. Ancestor approval does not promote an entry into the canonical Encyclopedia or make it training eligible.

Ordinary runs use the existing replay and fingerprint check:

```sh
python3 -m teacher.ancestor_context approve --run RUN_DIRECTORY --packet ORIGINAL_PACKET --reviewer REVIEWER --note 'Review rationale'
```

Root assemblies use the original selection, packet map and chapter plan. Approval rebuilds the assembly, replays the selected drafts, verifies its JSON and Markdown and binds the assembly/provenance hashes. The approved chapter file assignments are copied from that verified plan into the administrative review record.

```sh
python3 -m teacher.retrieval --assembly ASSEMBLY_DIRECTORY --selection SELECTION_JSON --packets PACKET_MAP_JSON --plan CHAPTER_PLAN_JSON --reviewer REVIEWER --note 'Review rationale'
```

The user-supplied Fable review accepts `.teacher/assemblies/root-002`. Its administrative review record now permits ancestor export. The immutable assembled Markdown still carries its original pending-review banner; the separate review record is authoritative. Canonical and training approval remain false.

## Retrieval packets

New `teacher.packet` CLI packets select `ancestor_context_mode: retrieval_v1` and editorial schema 5. Attach graph data before explanations so the search index includes those graph records:

```sh
python3 -m teacher.packet --task TASK_SHA --destination NEW_PACKET
python3 -m teacher.graph_packet --packet NEW_PACKET --store store
python3 -m teacher.ancestor_context attach --packet NEW_PACKET --run APPROVED_ENTRY_OR_ASSEMBLY
```

Repeat `--run` for each strict ancestor. Attachment requires exactly one approved replacement for every strict Git ancestor. Pending, edited, duplicate, unrelated and future entries fail closed. Identity, parents and cutoff must match Git history. Exported blobs contain authored explanations and basis/verification labels, without evidence ledgers, old-session citation arrays, reviewer notes, raw transcripts or provider metadata. Saved original artifacts are unchanged.

The opening prompt contains at most 8 KiB of catalog bytes. The catalog lists commit SHA, Git title, short summary, chapter IDs/titles/focus, the count of files touched and at most three file examples. Complete changed-file lists stay in the search index, not the catalog. Focus is a labeled excerpt from the first authored chapter claim (or problem claim), capped at 400 characters with an explicit truncation flag. Catalog entries are newest-first in reverse topological history order. The catalog itself stays in the packet and can be paged; it is not all injected at startup. Newly authored ordinary entries require a nonempty summary of at most 1,000 characters under schemas 4 and 5. Schemas 2–4 remain supported for replay.

One packet-only `ancestor_read` tool supports three modes:

- `catalog`: browse the catalog with byte `offset` and `max_bytes` (maximum 16 KiB).
- `search`: supply a case-sensitive `file` and/or `symbol` substring. Both filters must match when supplied together. `offset` counts grouped entry/chapter targets; `limit` is at most 50. Results are newest-first by history position, grouped by entry SHA and chapter ID, with `match_count`, distinct `match_basis` values and at most three file/symbol examples. Paging counts targets; `total_matching_records` preserves the underlying row count. Graph coverage is reported.
- `content`: supply ancestor `commit` and optional `chapter`; read prose using byte `offset` and `max_bytes` (maximum 16 KiB).

Catalog/content pages can end inside JSON or a UTF-8 character. Follow `next_offset` while `truncated` is true and concatenate bytes before parsing complete JSON; split UTF-8 pages use base64, consistent with existing source tools. Search results are structured records, bounded by both record count and page bytes. There is no regex execution or live lookup.

Search is built mechanically. Git changed-file lists index ordinary entries. Root files join to chapters through the approved plan. Root graph snapshot symbols join to those chapter assignments by file; later commits use their scoped graph symbol events. Structured finding locations add explicitly labeled authored matches. No model-selected topics or retrospective administrative findings ledger is imported. A symbol-file join means the symbol is in a chapter's assigned file, not that the chapter discusses that symbol. Missing graph coverage is reported; an empty result does not establish absence of discussion.

All search targets and reads are restricted to approved strict ancestors. Search/catalog calls are navigation, rejected as claim evidence. Content reads are ordinary recorded tool calls, citable by their current session IDs and hashed results, carrying the ancestor/chapter identity and byte range. In retrieval mode an ancestor link also requires a successful, nonempty prose page read in the same session. Reading a chapter qualifies its entry; this is not a full-entry-read requirement. Historical prose is not current execution evidence. Findings still require inspected source; execution claims still require a successful current-session `run`.

The original 256 KiB inline path and `ancestor:<sha>` citations remain available only for legacy packets. Its limit has not changed. Retrieval bounds initial catalog and individual read sizes; packet storage, index construction and lookup work still grow with history, and accumulated tool responses remain subject to the existing session/tool-call budgets.

The author rejects incomplete ancestor context before inference. All source, evidence, graph and prose attachment must finish before authoring so the manifest fingerprint binds the exact packet. The actual Codex protocol passes a local fake-provider test with all 15 allowed tools, a citable ancestor read and a schema-5 response. The user supplied Fable’s code review and real-packet boundary probes, accepting this path for commit 2. This is recorded in `reports/ancestor-retrieval-review-001.json`, without claiming formal certification. The three follow-up fixes pass the revised suite and the second-commit authoring run uses a new packet. No training trace is generated by this workflow.

Commit 2 is approved for ancestor context by the user-supplied Fable review, recorded in `reports/commit-000002-review-001.json`. Its authored draft remains unchanged. Commit 3 uses the standing authoring instructions and a fresh packet with the compact catalog; no review-directed task focus was added.

The [two-tier approval and sampling policy](ancestor-approval-policy.md) governs new runs starting at commit 4. Retrieval usage is reported in coverage.json without becoming an authoring or approval requirement.

New packets select `ancestor_matches_version: 1`. Their opening context includes up to 12 matching entry/chapter targets for the task’s exact changed paths, newest-first, sharing the coverage metric’s mechanical index calculation. The target list is byte-bounded (4 KiB), explicitly navigation-only, and reports truncation; file search remains available for the rest. It introduces no retrieval requirement or task-specific advice. Older packet versions retain their original opening context. Retrospective records and administrative known-limit companions are never exported.

## Attribution to ancestor prose

Editorial schema 5 adds `basis: ancestor` in every claim field. It is required when all evidence references are ancestor content reads (or supplied legacy ancestor context). An ancestor label requires at least one ancestor-prose reference. Catalog/search responses remain invalid evidence; ancestor prose never satisfies an execution claim or the source requirement for a finding.

Mixed primary-source/ancestor citations may use source or inference when the primary evidence substantively supports the claim. The teacher is instructed to use ancestor when reporting what an earlier entry says, even with supplementary diff context, and to split claims when appropriate. The validator checks reference types, not semantic support; irrelevant primary citations cannot legitimately turn inherited prose into independently verified evidence.

Previously accepted drafts, including commit 7, retain their schema and labels for exact replay. Their review record flags the old attribution convention; they are not silently relabeled. The `ancestor_read` description explicitly states its 16,384-byte cap, which remains distinct from source tools with 65,536-byte caps.
