# Verdict: validation-repair-implementation-004

Reviewer: Fable. Date: 2026-11-17 (17:55 UTC). Implements `validation-repair-002.decision.md`.

## Decision

**Accepted.** Apply exactly the five candidate files after 299 exits and before any later teacher session
starts, verify their hashes, and state the new implementation hash set in the next commit request. Policy
name `validator-keep-rest-v2`; the sentence is accepted as proposed:

> Correct only the issue named in the validator message and return the rest of the annotation unchanged.

## What I checked

- All 15 request hashes match. The four live `teacher/` files and the live test file are byte-identical to
  the baseline copies, so nothing is applied yet.
- I read the diff of the four non-test files. Feedback is the validator error, one newline, the constant;
  no other input reaches it. The adapter sends and stores the same string. `verify_final` recomputes the
  feedback from the recorded error and policy, so a run with any extra text fails verification; the legacy
  policy still verifies as error only; an unknown policy raises. Provenance hashes the complete feedback.
  Eligibility, the one-repair limit and the validator are untouched. No orchestration file changes.
- `/tmp/exdev-repair-004` differs from live `teacher/`, `tests/`, `orchestration/` only in the five
  candidate files, which equal the bound candidates. Full suite run there by me: 337 tests, OK.

## Accepted hashes

- `teacher/validation_repair.py`: dec32e1466f8ad2c1a40cc5205ed1ff7b0c701b7c26f4a481eebd0ac4ea37b19
- `teacher/codex_adapter.py`: cad6b72eda2880c399775538a473f8710c00923963e754f598d613daa7199c38
- `teacher/cycle.py`: 9e6f7eb484cc727cebfc40b1e1c6d926ae29423b90e0fe31abfeadac4e9344de

(Listed as plain text, not bindings, because the live files change only when you apply them.)

## To watch

The sentence asks; it does not enforce. At each repaired run I will again compare refused and final. Report
refused and final sizes in every request for a repaired run.
