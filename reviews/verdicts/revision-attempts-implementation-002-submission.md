# Submission for review: revision-attempts-implementation-002 (written by the reviewer)

From Fable to the author. Date: 2026-11-18. Roles are swapped for this one item on the user's word ("you can
write that cant you? its not training code"): I wrote the patch, you review it and apply it or send it back.
Nothing in the live tree is changed. Do not let this delay commits.

## What it does

After a rejection the teacher can revise its own entry instead of starting over. Design as accepted in
`revision-attempts-implementation-001`: same packet bytes, only the previous annotation, that attempt's tool
call/result records and a pointer-only coverage request enter the teacher input; the rejected attempt is never
modified; nobody else edits prose.

- New `teacher/revision.py`: `author_revision` (supervisor entry point), `prior_document` (binds the four
  prior artifacts, extracts the final annotation and requires it to reproduce `draft.json` and `draft.md`),
  `RevisionSession`, `admit_coverage`, `reserve`, `verify_run`, `prior_view`, `coverage_report`.
- Imported calls are saved in the new run's `prior-evidence.json`. The new `raw-transcript.json` holds only
  calls the new session made. Validators merge both ledgers through a new optional `prior` argument on
  `validate_annotation`, `assemble_draft` and `verify_final`; every existing caller passes nothing.
- `approval_policy.assess`, `ancestor_context.approve_run` and `cycle.validate_run` load the imported ledger
  with `prior_view(run)`, which returns `[]` for an ordinary run and fails closed if a run has imported
  evidence without being recorded as a revision, or the reverse. A revision is always `full_review`.
- `cycle.validate_run` re-derives the exact teacher input from the bound files (`verify_run`) and replays
  imported calls against the packet, counted apart (`imported_replayed_calls`).
- `orchestration.run_ahead.prepared`: a revision is a `forward` retry whose spec carries
  `"revision": {"revision_of_run": ..., "coverage": {"path": ..., "sha256": ...}}`. No new queue kind.
- One reservation per rejected attempt at `.teacher/admin/revisions/<prior run>.json`, exclusive create,
  kept on failure. The authorization path and hash are recorded there, not in provenance or teacher input.
- `thread/tokenUsage/updated` is recorded verbatim to `token-usage.json` beside the run (condition 1).

## Deliberate differences from the accepted design: please judge them

1. **ID form** is `prior:<first 16 hex of the source transcript SHA-256>:<original id>`, not the full 64 hex.
   The full digest is in `prior-evidence.json` and provenance. Reason: 324/001 and 325/001 both failed on a
   mistyped 37-character id; a 108-character id cited a hundred times invites more, and the short form still
   fits the 64-character cap of the v3 diagnostics.
2. **Coverage stays outside the packet.** The packet manifest must be byte-identical to the prior attempt's
   and must not already carry a coverage attachment (then it stops for review, as designed). The coverage
   file is admitted by exact bytes and digest as today, plus a mechanical screen that refuses evidence ids
   and abbreviated commit ids. That screen is a floor, not a judgment: you still inspect the text.
3. **A revision of a revision is refused** (needs a new request), as is a chapter task and a trial run.

## Conditions from the 001 verdict

1. Token totals: recorded per run from the server event; the comparison for the first three revisions is
   still to be reported when they exist. The event's field names are unverified until a live run.
2. First live use: mark the request; I will compare line by line.
3. Leak test: `test_coverage_gate_runs_on_exact_bytes_and_refuses_facts` (a file stating a fact by short
   commit id is refused; a refused admission consumes no reservation) and
   `test_teacher_input_holds_only_annotation_records_and_coverage` (planted verdict, review file, ledger and
   prior commentary are absent; the rest of the input equals the fresh session's).
4. Same position and identical packet only: `test_only_the_same_position_and_identical_packet_are_importable`,
   `test_changed_or_missing_prior_artifacts_fail_closed`.
5. Suite: 357 tests, 17 new, all pass except three `test_codex_wire` errors that are
   `PermissionError` on my scratch path `/home/brandonrabe/exdev-rev` and fail the same way without the patch.
   Run the host-enabled suite in the live tree yourself; I have not.

## What is NOT covered: check these hardest

- No test drives `prepared()` with a revision spec, and none drives `cycle.validate_run` end to end on a
  revision (its two pieces, `verify_run` and imported replay, are tested apart). You know that fixture code; I do not.
- I assumed a rejected attempt leaves the queue in the same `retry_only` state a failed one does. Confirm.
- The revision input carries every prior tool result in the first message. For 323/001 that is several
  hundred kilobytes; whether the app-server accepts it is untested.
- `make_summary` binds the extra files; the kept/added/removed list in the request is still yours to write.
- My own `reviews/fable/check.py` does not yet know about imported evidence; I will fix that before the
  first revision request, it is not your concern.

## Files

- `reports/revision-attempts-implementation-002.patch` (applies to the live tree with v3: `git apply --check` passes)
- `reports/revision-attempts-implementation-002.hashes.json` (before and candidate hashes, 11 files)
- `reports/revision-attempts-implementation-002-suite.log`, `...-focused.log`

Reply in `reviews/requests/revision-attempts-implementation-002-review.md`: accepted and applied (with the new
production hash set and your suite result), or what to change. Apply only at a queue boundary.
- reports/revision-attempts-implementation-002.patch: `5f2142eddaef52b62e286e29a42c3171bb8f67902a2b846e4072eaf6489d2c58`
- reports/revision-attempts-implementation-002.hashes.json: `52ddcb45c80bef804db1b0cd2024b1fbe301e42b85c577736177001ff9a416f0`
- reports/revision-attempts-implementation-002-suite.log: `e4d1560e93ed8b43eb8c900043e1d7bb44412297e87d5cc6ce5db0bbf666cb22`
- reports/revision-attempts-implementation-002-focused.log: `1a9bccfc564ac371b8ee676071185e3a2f9dffafaaea5838c1456136ae13a946`
