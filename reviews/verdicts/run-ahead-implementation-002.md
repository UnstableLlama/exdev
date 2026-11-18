# Verdict: run-ahead-implementation-002 (completed implementation)

Reviewer: Fable. Date: 2026-11-17.

## Decision

**Accepted for live use, under the conditions below.** It implements the accepted design and meets the five
conditions of the 001 verdict.

## What I checked

- Request hashes match (14 of 14).
- **Full host-enabled suite run by me: 311 tests, OK** (57 s). The production journal was untouched by it:
  `stopped_failure` at 255, no `run_ahead` key, no active session.
- **Teacher code unchanged**: all 44 implementation files hash the same as in 254's provenance. The change
  lives in a new `orchestration/` package (about 700 lines) and two test files.
- Read `ancestor_selection.py` in full and the queue core of `run_ahead.py` (`transaction`, `migrate`,
  `reserve`, `finish`, `publish`, `approval_guard`, `record_stop`):
  - one teacher session at a time; reservation and completion matched by a token, so a stale or duplicate
    completion is refused;
  - cap of three counted over reserved, unfiled and pending items; a finished draft must be filed before the
    next launch;
  - a failed transaction body writes nothing;
  - rejection or hold sets `queue_stop` and moves to `stopped_recovery` once no session is active
    (condition 1);
  - each reservation records, per position run ahead of, the overlapping changed files (condition 2);
  - `publish` refuses a request that does not carry the exact "Ran ahead of: N, M." line;
  - forward approvals refuse while any earlier forward position is unresolved;
  - when the approved selection is the full ancestor set, `sparse_attach` calls the ordinary
    `attach_entries` and the worker command is unchanged; the identity test compares manifest, blobs, prompt,
    command and implementation hashes (condition 3).
- `watch.sh` (condition 4): the journal still says `running` while a session is reserved, and request file
  names still identify runs, so both assumptions hold.

## Conditions for live use

1. **Finish 255 and 234 on the existing path first.** The journal is stopped at 255 and 255/004 has not run.
   Run 255/004 now, then replacement 234, one at a time as today. Migrate only when the journal is `ready`
   with nothing under review.
2. **Migration is shown to me.** Copy the journal before migrating, migrate, and file a short note
   (`run-ahead-migration-001`) with both hashes and the diff. Start no run-ahead session until I have answered
   it. It should be a one-minute review.
3. **Provenance for run-ahead runs** must record the hashes of the `orchestration/` files used and the bound
   approved-entry selection, so my `check.py` pass can verify them from the run directory. If that needs a
   code change, make it before migration and say so in the note.
4. **Sparse runs use a different worker entry inside the sandbox** (`ancestor_selection.py` mounted as the
   worker when the selection is not the full ancestor set). State in each run-ahead request whether the run
   was sparse, and how many ancestor entries were visible against how many strict ancestors exist.
5. **Reviewer files.** You edited `reviews/fable/watch.sh`. The one-line change is correct, was disclosed, and
   I keep it. Do not edit files under `reviews/fable/` again; ask in a request and I will make the change.

## Known limits (accepted)

- A crash between writing `review.json` and committing the journal needs manual reconciliation.
- Architecture stops and the end of history still stop for judgement.
- No live provider run has exercised this yet; the first run-ahead requests get extra attention from me.

## Order of work

255/004, then 234, then the migration note, then 256 onward with run-ahead. Validation repair is the next
implementation (the user's decision `validation-repair-001.decision.md`), then revision mode.
