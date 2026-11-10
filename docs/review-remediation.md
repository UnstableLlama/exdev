# Review remediation and authoring restart

The project sequence is Encyclopedia and graph construction, training-data generation from those resources, then model training. The current remediation concerns the first stage.

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

## Evidence and runner checkpoint

Eligible issue/PR evidence for entries 9 and 10 is recovered. Entry 9 can see pre-cutoff issue edit-event text; PR 3 was created 43 seconds after its commit and is excluded. Entry 10 can see the eligible issue body, PR body and two comments. Historical edit-event text is explicitly not certified as a complete historical body. Raw retrievals remain local; the [report](../reports/github-evidence-recovery.json) records provenance and eligibility.

The nine repository/source tools, packet builder, Bubblewrap supervisor and provider-neutral fresh-session driver are implemented as a candidate. All 116 tests pass with host sandbox tests enabled after the root coverage changes. Real packets for entries 9 and 10 passed [boundary checks](../reports/teacher-boundary.json). See the [review guide](teacher-boundary.md) and [runner instructions](../teacher/README.md).

The five graph tools now use an ancestor-only packet bridge, including isolated native queries and ancestry-filtered symbol history. All five passed real-packet checks for entries 9 and 10; mutations and task/future graph requests were denied. No global graph timeline is exposed to the runner.

## Still pending

The Codex Astra adapter and editorial v2 candidate are implemented and tested. Approved ancestor-prose export is implemented. Independent boundary review, review of fresh authoring output, the full first-25 rewrite, promotion into the canonical corpus and the real training-trace dry run remain unfinished. Existing drafts and administrative reviews are excluded from packets. No canonical entries were rewritten or training traces generated by these checks. Initial live root-entry output is retained separately for review. The candidate schemas are not frozen.

Merge conflict-resolution provenance still needs finer comparison against parent symbol bodies; current `merge_arrival` labels do not establish whether the merge itself introduced a change. Raw-log compression and a bounded verified graph snapshot cache are follow-up infrastructure work.

The adapter starts a fresh filesystem-isolated Codex process per entry and an ephemeral thread, with an explicit restricted model-tool profile. A local fake-provider test verifies the real outbound 14-tool inventory and a historical tool round trip. It does not substitute a fixture for a corpus entry. Editorial v2 separates pending review metadata from evidence-anchored claims. See [the v2 contract](editorial-v2.md).

[Approved ancestor context](ancestor-context.md) now binds reviews to exact draft, transcript and provenance hashes. It rejects incomplete ancestry or edited approvals, excludes review metadata from model context, and gives approved prose explicit citation IDs. The root restart packet is prepared with no ancestor prose and an index of its task-diff file sections.

The second isolated root-entry attempt produced a schema-valid review candidate with six chapters and thirteen source reads. The first attempt was rejected for placing chapter anchors in the ancestor-links field; its raw response is preserved. Neither attempt replaced the canonical root entry, approved a draft or generated a training trace. See [the candidate report](../reports/root-authoring-candidate.json).

## Root coverage remediation

Fable rejected candidate 002 for insufficient coverage, despite accurate sampled claims and a valid schema. It must not replace the canonical root entry. The next root attempt requires separate subsystem tasks with explicit file assignments, complete-read validation, and high reasoning effort for the root and chapter sessions. The quantizer chapter must inspect the Python and CUDA quantizers and `doc/exl3.md`, with function-level mappings to the pinned papers and reference implementation. The ten assignments and complete-read checks are now implemented; the first quantizer chapter completed in a fresh Astra/high session and awaits independent editorial review.

Historical external evidence has been recovered for QTIP v3, QuIP# v2, the pinned QTIP reference code, and all five architecture references. See [the recovery report](../reports/root-evidence-recovery.json). Gemma 2 uses the user-authorized public `unsloth/gemma-2-2b` mirror at `25319945f7fd83b8b903e12081777b7eef2ba993` (2024-09-03), before the root cutoff. Its provenance is retained as mirror evidence; byte identity with the gated Google repository has not been verified. Only metadata, tokenizer files and safetensors headers were retrieved, with no tensor weight payloads. Raw evidence remains in the local evidence store for packet construction.

Section-relative `git_show` truncation and assigned-range coverage checks are implemented and tested. Recovery alone does not mean that an author has inspected these sources or that a revised root entry is ready for approval.

The [quantizer chapter report](../reports/root-quantizer-candidate.json) records 26 successful tool calls, complete assigned coverage and exact draft replay. The chapter contains function-level paper mappings and source-level discrepancy observations, not measured GPU results. A chapter cannot be approved through the complete-entry approval path or supplied as a complete ancestor entry. The other nine chapter runs, synthesis and canonical promotion remain pending.

## Next checkpoint after quantizer review

Fable accepted the quantizer as a template, subject to stronger treatment of constants, useful `run` computations, cross-references and a fresh rerun rather than hand repair. Instruction revision 2 and catalog-bound chapter references are implemented; old draft prose is unchanged. The remaining nine chapters have not started under these changes. Run them next, then rerun the quantizer last under the [revision policy](chapter-revisions.md). The [retrospective defect policy](defect-retrospectives.md) defines later sample filtering and human overlays; its ledger and sample-policy engine remain to be implemented before training-data generation.
