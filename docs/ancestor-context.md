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

## Task messages and curated evidence

New packets carry the full task commit message as explicit opening-context input. System instructions identify it as the upstream author’s claim, not executable instructions or proof, and require checking it against the diff and eligible evidence. Old packets remain unchanged.

The walk reads `data/evidence/github/POSITION-eligible.json` when present and passes it through the packet builder’s task identity, cutoff and content-hash checks. A new input contract binds the complete source-ID/content-hash list and bundle fingerprint. Empty present bundles, dropped/partial evidence, changed/disappeared bundles and missing task messages fail before inference. Preparation and pre-launch checks enforce the bundle against disk; the session additionally checks the manifest contract. No eligible file is different from a present file silently ignored.

Rejected attempts are preserved. A resumed position allocates the next unused packet and run suffix; neither existing packets nor authored drafts are overwritten. The commit-message audit for positions 2–8 is recorded in `reports/commit-message-audit-002-008.json`; no earlier rerun was indicated by those comparisons.

Walk input contract v2 stops before packet creation when a task message contains
`#N` or a GitHub URL and no eligible bundle exists. Recovery with zero eligible
items must instead leave `POSITION-recovered-none.json` with `status` equal to
`recovered_none_eligible`, the exact `task_sha`, `cutoff`, sorted unique
`references` (from `teacher.walk_inputs.references`), and a nonempty
`recovery_report` identifying the curator's recovery record. This is a trusted
curator attestation, not proof inferred from an absent bundle. Never generate it
without recovering the referenced material. Preparation validates those fields;
the manifest binds the marker and its bytes, checked again before launch. An
empty eligible bundle still fails. This gate does not itself perform recovery.

New opening contexts include `task_author_name` from Git's author field. Evidence
catalogs preserve `author_login` from GitHub recovery (null when unavailable),
including when the evidence is a historical edit. These are attribution fields,
not independent corroboration or authorization. GitHub logins are those returned
at recovery time; no historical username reconstruction is claimed. Already saved
packets and drafts remain unchanged.

Walk input contract v4 also binds a separate, trusted catalog of GitHub issues
and pull requests that were created by the task cutoff and still open at that
cutoff, even when the commit message did not reference them. The opening context
contains titles and metadata only: number, issue/PR kind, title, author login,
creation time, as-of-cutoff open state, URL and availability. Available rows
also contain `repo_paths_mentioned`, a sorted, de-duplicated, capped navigation
list of repository files named in cutoff-bound issue text, plus an explicit
truncation flag. Traceback paths under install prefixes such as
`site-packages/` are normalized to repository-relative paths, and only paths
that exist in the task's parent tree survive. The hint exposes file names from
issue bodies or comments, but no prose, surrounding lines or excerpts. It is
navigation, not evidence; authors must fetch the item before using it.
Unavailable rows contain no hint. The opening catalog never contains bodies or
comments. It is capped, reports its limit and truncation state, and is distinct
from author-linked `evidence_catalog` entries.

Trusted recovery paginates title and close/reopen timelines and content edit
histories. Post-cutoff title changes are reversed for the catalog; items created
after the cutoff or closed before it are excluded. Body, comment and review text
is stored only when its as-of-cutoff representation can be established. Any
uncertain item is marked unavailable and cannot be fetched; current text is
never used as a fallback. GitHub does not expose a recoverable trace for every
comment deleted after the cutoff, so `available` means all still-recoverable
cutoff content was established, not that every object once visible is present.
Reading available content requires an explicit
`web_fetch` call recorded in the author transcript. Standing guidance requires
comparison of every row against the task diff and files read in the session,
including shared numbers, identifiers, file names, error text and path hints.
When there are at most ten rows, every available item whose title reports an
error or failure must be read. The item's own framing must be reported
faithfully and any relationship not stated by the commit author must be labeled
as inference with its concrete basis.
Legacy packets without this field retain their original prompt and replay shape.

Recovery is intentionally administrative and can be expensive: without
`--reuse`, it fetches full edit, comment, review and timeline history for every
discussion created by the target cutoff. Use `--reuse` after the raw histories
have been recovered and verified, especially once the repository has hundreds
of discussions. Range-derived retrospective filenames prevent later recovery
runs from overwriting an already accepted earlier audit.

New merge packets also expose `merge_facts`: the task tree ID, each parent's
tree ID, every parent with an identical tree, and the first-parent diff base.
Trusted packet-building code computes these directly from Git. Tree equality
establishes repository-content equality, not an absence of new ancestry or
eligible discussion. Merge approval policy is unchanged: all merges still need
full review. Standing authoring guidance asks for contributor attribution when
supported, without treating matching display names as proof of identity.

## Dependency-change inspection

Standing authoring guidance requires `repo_grep` on the parent tree for imports
of added or removed declared dependencies before describing impact. Package and
module names can differ (for example pillow/PIL); inspect matches and the task
diff. Empty static searches do not establish absence of dynamic or external use.
Commit 11 remains approved only for ancestor retrieval, with canonical-use
coverage blockers recorded in its administrative review. Its draft, transcript
and provenance remain unchanged, including its pre-gating guidance wording.

## Architecture references and changed dispatch (contract v5)

New walk packets use guidance version 2. When dispatch changes, the teacher is
asked to inspect selected callees in the parent tree and distinguish their
limits and preconditions from an inferred author rationale. Legacy packets
without this version retain their prior prompt; retrieval remains report-only.

Trusted preparation compares the task with its first parent. It detects newly
registered architecture keys in model registry dictionaries (including renamed
registry files under `exllamav3/models/`) and newly added files defining model
or config classes. A triggered task requires `POSITION-references.json` next
to its other evidence bundles before authoring. Preparation verifies task,
cutoff, trigger, selection provenance, architecture identity and required roles.

The curator supplies a selection JSON list with `architecture`, `repo`, `reason`
and `candidates_considered`. Prefer repositories named by the task or eligible
discussions, otherwise the defining organisation's reference; include multiple
reasonable choices. Do not consult later fixes, issues or reviewer hindsight.

```sh
python3 -m teacher.architecture_evidence --task TASK_SHA --selection SELECTION.json --output data/evidence/github/POSITION-references.json --cache LOCAL_CACHE
```

Recovery pins the latest revision at or before the task cutoff. It retrieves
config.json, tokenizer configuration files and safetensors headers using the
root evidence tools and exact byte ranges; it never retrieves weight payloads.
A repository with no eligible revision contributes no objects and an explicit
`no_eligible_revision` selection report. Missing required roles or other recovery
failures block preparation. New class files without registry additions still
require a curator selection report; config identity is checked against its
reported architecture. The selection report remains administrative, while only
neutral evidence objects reach the teacher. Contract v5 binds the reference
bundle hash and object signatures independently of referenced GitHub evidence.
Changing or omitting an attached object fails validation. Old packets are not
modified or re-exported.

Architecture-location guard (implementation revision 002): the trusted inventory
also scans `exllamav3/architecture/`. For a non-root task, finding no model/config
classes in either known directory is an error, not an empty trigger. A future
move to an unknown location therefore stops preparation for curator inspection.
Root tasks are exempt from that location guard. Rename/merge false positives
and post-simplification identity derivation remain required follow-ups before
position 100; this location fix does not resolve those separate cases.

## Evidence source index (walk contract v6, guidance v3)

New packets group model evidence by repository and pinned revision, with dates,
attaching commit identities and role counts. Referenced discussion objects are
grouped by discussion URL, kind and number; a recovered title history supplies
its cutoff-correct title when available. No title is invented when legacy
metadata lacks one. Bodies and headers are not opening-context content.
Direct task discussion listings remain; direct model files use the same compact
index as ancestor model files.

The builder scans historical packet manifests, filters their task identities to
strict ancestors, then independently checks each object's created and revision
dates against the new task cutoff. Only evidence metadata and checksum-verified
blobs are copied, never reviews, old prompts, coverage requests or curator notes.
Evidence is collected from every packet for a strict ancestor, including failed
and superseded attempts: evidence availability is distinct from approval of
authored prose. Exact repeated content is deduplicated, retaining attaching ancestors. Historical
unreferenced-discussion snapshots remain governed by their separate open-item
catalog and are not converted into a closed-discussion archive.

The initial index is an 8 KiB byte page with a truncation flag and next offset.
`evidence_index` pages the source list, then object metadata for an `index_id`.
Concatenate byte pages before parsing JSON. Object rows supply exact coordinates
for existing `hf_fetch`, `safetensors_header`, and `web_fetch` tools. Optional
`source_id` selects a historical object; without it, web reads prefer the latest
eligible attached revision. Index pages are navigation, never claim evidence.
All objects, index rows and coverage input are bound into the input contract;
authoring checks blob presence and hashes before provider invocation.

Guidance v3 requires reading every listed model's config.json before claiming a
mapping, dimension or default is corroborated, naming the models read and limiting
claims when any was not read. It does not require reading every tensor header.
Legacy packets keep their original opening context, tool schema and replay.

## Configuration-reading amendment (contract v7, guidance v4)

New model source rows include `architectures`, copied from the pinned config.json
key, or an empty list when the key is absent. The field is navigation metadata,
covered by the index digest and checked against the configuration blob during
packet validation. Invalid non-list values fail preparation rather than inventing
an architecture. Earlier packet indexes and guidance remain unchanged.

Guidance v4 replaces v3's optional limiting clause: when multiple indexed models
include an architecture the task registers or whose model/configuration class it
modifies, read every matching model's config.json before finalizing. Name each
model and report mapping, dimension and default checks per model. Report failed
reads; skipping a model is not an opt-out. Tensor headers remain claim-driven.
This implements `config-reading-amendment.decision.md`; rejected attempt 39/003
is retained unchanged, 39/002 stays active, and 39/004 will be unassisted after
implementation acceptance.

### Closed discussion salience (contract v8 / guidance 5)

New packets have a separate `closed_discussion_catalog`. Open discussion selection
is unchanged. Candidates include all issues and PRs created and closed by the
committer cutoff, with no age window. Reopened discussions are classified by their
state at the cutoff. Recovery enumerates all discussions created by the latest
audit cutoff, then reconstructs each earlier state, title, body and comments.
Unknown timelines/content are excluded. Closed candidates additionally require a
known root body and full eligible bodies: historical edit-event summaries alone
are excluded rather than scored as complete text. Later comments and titles do
not contribute. Referenced discussion URLs are not duplicated in this catalog.

`teacher/closed_discussions.py` defines `salience-v2`. Task terms come only from
the task message, changed paths (including basename tokens), and lexical identifiers
on added/removed code lines. Quoted literals and line comments are excluded from
those code lines; prose-only diffs contribute their message and paths. Identifiers
retain underscores, are lowercased, and have minimum length 4. The fixed stop set
in that module excludes common prose and repository scaffolding words. The general stop list was extended after examining the positions 2–68 audit;
it is fixed at runtime and never learned from teacher inputs. This lexical extraction is not a semantic
parser and may miss identifiers in unusual syntax.

For each remaining term t, df(t) counts eligible closed candidates containing it
in their cutoff title/body/comments. Score = sum(1 / df(t)^2) over distinct terms shared with the **commit message only**, using exact rational
arithmetic. Path and diff-identifier terms cannot qualify or rank a row; they may
appear in matched_terms after that row qualifies. Gate >= 1; cap 20. Thus one term
unique among candidates can qualify, while a shared term alone cannot. Ties use
kind then number. No closure recency contributes. This navigation heuristic can
miss synonyms and can match unrelated code vocabulary; it does not certify relevance.

Rows expose kind/number, title, author, created/closed times, `state: closed`, URL,
existing parent-tree path hints and matched terms. **Matched terms expose words
from discussion text.** They contain no score, body or excerpt. Initial navigation
is byte-paged at 8 KiB; `evidence_index(index_id="closed_discussions", offset=...)`
returns subsequent pages (16 KiB maximum). The cap-truncation flag is distinct
from byte-page truncation; rows beyond the top-20 cap are not served. Fetch a listed
body with `web_fetch`. Navigation calls remain catalog-only, not claim evidence.
One added guidance sentence extends the existing catalog reading rule and requires
faithful title/framing and inference labels with a concrete basis for claimed links.

The closed bundle digest and a digest of the full catalog plus served-object
metadata are contract-bound; every fetched blob remains content-addressed. Closed
snapshots are excluded from the general ancestor evidence index, so later packets
must apply their own cutoff and salience gate. Old packets retain their original
context, contract validation and replay. The audit reports total known closed discussions, full-body-eligible candidates
and unknown-state exclusions at every position. The commits 2–68 audit is report-only;
its rows do not authorize re-authoring. Commit 69 waits for implementation review
before its next unassisted attempt. No commit 70 is authorized before that sequence.
