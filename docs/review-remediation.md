# Review remediation and authoring restart

This incorporates Fable's review and the agreed qualifications. Infrastructure can be prepared in the current administrative session. The current session has seen later source and reports, so it must not author the replacement historical corpus.

## Order

1. Fix inherited stdin, enforce ancestor-only entry links/context, and establish merge integration/de-duplication policy.
2. Recover eligible issue/PR body and comment evidence using content-edit information rather than general update timestamps. Record retrieval and historical eligibility separately.
3. Build the nine repository/source tools and a restricted teacher runner. The runner controls cutoffs, allowed files and network evidence; it does not expose raw stores, source mirrors, administrative reports or unrestricted shell.
4. Revise entry fields for review bookkeeping and structured evidence/confidence, then redo entries 1–25 in fresh sandboxed authoring contexts. Preserve a canonical root commit entry with linked subsystem chapters; snapshots must stand alone.
5. Run a real trace dry run against the tool contracts and entry schema before advancing the authored corpus.

Fresh contexts must be scoped per task/entry to its permitted ancestry. One fresh session that subsequently carries unrelated branch explanations forward would recreate the same leak. A sub-agent inheriting this conversation, or an unrestricted new session merely asked not to read future files, does not meet this requirement. Fresh authoring contexts receive only eligible input packets and restricted tools, not this review, retrospective diagnostics, or the old authoring conversation. Existing drafts remain available for administrative comparison outside those contexts.

## Completed groundwork

- Git subprocess reads use closed stdin, so root empty-tree hashing cannot wait on the caller's interactive stdin.
- The entry helper builds its context from strict Git ancestors and rejects links outside that set. Annotation fields cannot override identity/provenance fields. All existing first-25 links pass the ancestry check, but that does not establish isolation of their original authoring context.
- Every merge retains its identity and parent list. Merge policy records which branch commits it integrates and defaults to no independent training example. Clean merges receive integration summaries; remerge differences, tree-preserving merges and unsupported cases require separate review. A tree-preserving merge does not by itself prove `-s ours` was used, and modern remerge output is diagnostic evidence rather than a perfect reconstruction of the historical merge strategy.
- The pinned history contains 168 merges: 134 integration-summary cases and 34 resolution-review cases. Entry 10 integrates entry 9. The future-wide inventory in `reports/merge-policy.json` is administrative-only, not teacher context.
- First-parent symbol events remain intact. `symbol_event_provenance` and `symbol_history` expose `merge_arrival` versus `direct_commit` plus parent identities. Training example selection must use this provenance rather than count arriving branch edits as independent new fixes.
- Storage growth was measured and projected before resuming the walk. The duplicate uncompressed snapshot in SQLite was replaced by a verified compressed-archive reference. See [storage decision](../reports/graph-storage-projection.md).

## Still pending

Eligible issue-evidence recovery, the nine tools and enforced teacher sandbox, the new editorial schema, fresh authoring, and the trace dry run remain unfinished. The existing entry helper's checks are defense in depth, not a sandbox. No entries were rewritten as part of this infrastructure remediation. Type heuristics remain provisional; raw mining identities/diffs were not rewritten. The next step is issue/PR evidence eligibility, followed by the runner boundary.
