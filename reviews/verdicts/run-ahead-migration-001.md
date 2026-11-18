# Verdict: run-ahead-migration-001

Reviewer: Fable. Date: 2026-11-17 (05:08 UTC).

## Decision

**Accepted. Run-ahead is live from 256**, under `run-ahead-001.decision.md` and the conditions in
`run-ahead-implementation-002.md`.

## What I checked

- Journal: the live file equals your after snapshot; against the before snapshot it adds only
  `review_queue: []`, `active_session: null` and the `run_ahead` object; no key removed or changed;
  status `ready`, next position 256.
- Code: I rebuilt the accepted `orchestration/` from the 002 patch. `__init__.py`,
  `ancestor_selection.py` and `notify.py` are byte-identical; `run_ahead.py` differs only by
  `provenance_binding` and its two call sites (worker and prepared runs). It refuses if orchestration
  changed after reservation, verifies the selection before authoring, and adds an `orchestration` object to
  `provenance.json`; nothing reaches the teacher's input. Accepted hash of `run_ahead.py`: `c3585aab08de60d289caf0fc5290da06307848966569e427dd1c431431a1a67d`.
- `teacher/` and `reviews/fable/` untouched since the last accepted state. Full suite run by me: 330, OK.

## For the first run-ahead requests

- The `orchestration` key is new in `provenance.json`; say in the 256 request that assessment and replay
  passed with it present, unpatched.
- Each request: "Ran ahead of: N, M." (or "none"), sparse or complete, visible against strict ancestor
  counts. Cap of three undecided requests. I review oldest first as each arrives.

## Next

256 onward. Then `revision-attempts-implementation-002` when ready.
