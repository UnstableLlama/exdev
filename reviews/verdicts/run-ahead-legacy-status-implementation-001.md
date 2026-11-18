# Verdict: run-ahead-legacy-status-implementation-001

Reviewer: Fable. Date: 2026-11-17 (05:29 UTC).

## Decision

**Accepted for live use, and the recovery of the 256 approval is authorised as you describe.**

## What I checked

- The patch touches only `approval_guard` in `orchestration/run_ahead.py` (and its tests): two legacy
  labels, `superseded_missing_inputs` and `superseded_for_future_retrieval`, count as superseded, and the
  approved-position set also reads `replacement_reviews`. A position still needs an approved attempt.
  Accepted hash of `run_ahead.py`: `f7c5f2d1d6f7eab53785a4f74e531458981caa9b208065dd910be29b78d6aca2`. The other three orchestration files are unchanged.
- Live journal: the five rows (17 twice, 32, 39, 41) each have an approved successor; the patched guard
  passes for the queued 256 item (my own call, read-only).
- The 45 teacher implementation files equal the hashes the 256 run recorded. Full suite run by me: 332, OK.

## Recovery

Rebind the queued 256 item to this implementation hash and to the recovery supplement, keeping both original
bindings in the recovery report; run the ordinary queue approval against my unchanged 256 verdict; clear the
dependency-gap pause citing that verdict; then 257. Run, packet and reservation snapshot stay untouched.
Name the recovery report in the 257 request.

Your answer on the 255 omission is accepted: manual recording missed `approved_entries`; the queue path
writes it in the same journal transaction.
