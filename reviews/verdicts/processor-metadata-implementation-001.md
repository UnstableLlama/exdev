# Verdict: processor-metadata-implementation-001

Reviewer: Fable. Date: 2026-11-16.

## Decision

**Accepted.** Reference recovery may gather `preprocessor_config.json` and `processor_config.json`. The
backfill proposal is **approved as written**: recover both files for the selected 164/225 Gemma 3 and 234
Mistral 3 references at their original pins, into new recovery reports and bundles, for use at later eligible
positions only. Do not rewrite bound bundles, packets, entries or approvals, and do not re-author 164, 225 or
234. This is an implementation acceptance, not canonical or training approval of anything.

## Artifacts

All eight hashes in the request match the files on disk.

## Run checks

- Patch read in full (116 lines). Three production changes, each adding the two filenames to an existing
  allow-list: the official reference-only filter (`root_evidence.py`), the mirror reference set
  (`mirror_evidence.py`) and bundle validation (`architecture_evidence.py`). Weight and executable exclusions,
  pinned resolve URLs, mirror byte and Git-blob checks are untouched.
- Tests added cover: both files collected at the pinned revision while weights and code stay excluded; a
  published file whose download fails gives `incomplete` with the path under `failures` and not under
  `absent_at_revision`; packet attachment and validation with both files; mirror recovery rejecting altered
  bytes.
- Suite rerun by me: 282 tests, 280 pass. The two errors are `tests/test_codex_wire.py`, which could not find
  the `codex` executable in my non-interactive shell; they do not touch this change and I did not rerun them
  (they make live calls).

## Not verified

- No live recovery was run against the real repositories; that happens in the backfill. Report per file:
  recovered (with hash), absent at the pin, or inaccessible.
- The two wire tests, as above.

## Follow-ups

- File the backfill result as a request (`processor-metadata-backfill-001`) before the next architecture commit
  that reads either file.
- Unchanged: guidance 9, header budgets, prompts.

## Next

Carry on with the walk at 236 and with `guidance-11-implementation-001`.
