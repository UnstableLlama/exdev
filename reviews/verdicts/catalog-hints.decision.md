# User decision: make the unreferenced-discussion catalog findable

Recorded by: Fable (independent reviewer; file mailbox)
Decided by: the user, in chat, 2026-11-11 ("yes")
Relates to: `reviews/verdicts/commit-000017-002.md`, `reviews/verdicts/commit-000032-001.md`, `reviews/verdicts/commit-000033-001.md`

## Why

Three open issues so far were on point for the commit being authored. The teacher read one (issue 11 at commit 33, whose title names the error) and missed two (issue 6 at commit 17, issue 8 at commit 32), whose titles did not make the connection obvious. The user has approved both remedies below.

Canonical and training remain false throughout.

## Decision 1: a reading rule (standing guidance)

Add guidance, sent only when the packet has an unreferenced catalog:

- Before finalizing, compare every catalog row against the task diff and the files read in the session. Read any item whose title shares a number, identifier, file name or error text with them, and any item whose path hint (below) names a file the task touches or the session read.
- When the catalog has ten items or fewer, read every item that reports an error or failure, whether or not anything matches.
- The existing rules still apply: report the item's own title and framing, and label any link to the task as inference with its concrete basis.

## Decision 2: a file-path hint on each catalog row

What the reviewer will check:

1. **Computed by trusted code.** For each catalog item, recovery code extracts repository-relative paths mentioned in the item's as-of-cutoff text (body and comments at or before the cutoff only) and keeps those that exist in the task's parent tree. Paths inside tracebacks count; strip install prefixes such as `site-packages/` so `…/site-packages/exllamav3/ext.py` resolves to `exllamav3/ext.py`.
2. **Navigation only.** The row gains one field, for example `repo_paths_mentioned`, holding a sorted, de-duplicated, capped list of paths, with a truncation flag. No prose, no line numbers' surrounding text, no excerpts.
3. **As of the cutoff.** A path that appears only in a later comment or a later edit must not appear. Unavailable items get no hint.
4. **Bound into the contract.** The hint is part of the catalog bundle hash and the walk input contract, so a changed hint fails validation like any other catalog change.
5. **Legacy packets unchanged.** Packets without the field keep their recorded opening context and replay.
6. **Tests.** Extraction from a traceback, prefix stripping, cutoff filtering, parent-tree filtering, the cap, and the legacy case.
7. **Documented** in `docs/ancestor-context.md`, including that the hint exposes file names taken from issue text.

Expected results on the two known cases: issue 6 at commit 17 should list `exllamav3/ext.py` among others; issue 8 at commit 32 should list whatever repository files its traceback names (I have not enumerated them).

## Decision 3: re-author commits 17 and 32

- Re-author commit 17 as `commit-000017-003` and commit 32 as `commit-000032-002`, each stopping for full review.
- **No hindsight.** Each re-authoring must use a packet built for that commit: ancestor entries strictly before it (through 16 for commit 17, through 31 for commit 32), the evidence and catalog as of its own cutoff, and nothing from later commits or later reviews of later commits. Current standing guidance applies; state in the request which guidance version was used.
- The currently approved attempts (`commit-000017-002`, `commit-000032-001`) stay approved and unchanged until a replacement is approved. On approval the replacement supersedes the old attempt for future retrieval.
- **Dependents.** List the later runs whose transcripts read the superseded entries. Do not re-author them automatically; the reviewer will say whether any needs it. The expected change is additive (issue context), so most should stand.
- Do these two before continuing past the current position, so later entries retrieve the corrected ancestors.

## Order of work

1. Implement the guidance and the hint, with tests; say so in a request file.
2. Rebuild the catalogs for commits 17 and 32 with hints; re-author both; stop for review after each.
3. Resume the walk at the next unauthored commit.

If building this shows a serious cost or a conflict with the no-hindsight boundary, say so in the request file before re-authoring.
