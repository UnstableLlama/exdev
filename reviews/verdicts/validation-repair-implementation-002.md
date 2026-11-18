# Verdict: validation-repair-implementation-002 (completed implementation)

Reviewer: Fable. Date: 2026-11-17.

## Decision

**Accepted for live use.** It implements the accepted design and the user's decision
(`validation-repair-001.decision.md`), and meets the four conditions of the 001 verdict. The implementation
set for new runs is the tree as it stands with this patch; 254's provenance hashes are superseded for
`ancestor_context.py`, `approval_policy.py`, `author.py`, `codex_adapter.py` and `cycle.py`, plus the new
`validation_repair.py`.

## What I checked

- Request hashes match (20 of 20). The patch reverse-applies cleanly to the working tree, so the tree is the
  reviewed baseline plus this patch for the files it touches. `teacher/editorial.py` is unchanged: the
  validator's rules are the same.
- **Full host-enabled suite run by me: 326 tests, OK** (54 s). The production journal was untouched.
- Read the session-loop change in `codex_adapter.py` and the entry point in `author.py`:
  - the feedback turn's only input is `str(error)`; the same string is what the transcript records;
  - it happens at most once (`repair is not None` re-raises), on the same thread, with the same model, effort
    and output schema;
  - the refusal record and the refused final are saved before the feedback turn starts;
  - transcript-integrity checks (`evidence_ledger`, `observed_reads`) and a packet-unchanged check run outside
    the catch, so those failures stay terminal;
  - `feedback_sent` is set only after the server acknowledges the turn.
- **Message audit (condition 2), verified against the source.** `editorial.py` raises nineteen fixed strings,
  seven schema-shape suffixes on a schema path, and three terminal internal messages; `coverage.py` adds
  `Required evidence not fully read: ` followed by packet section identifiers. `eligible()` admits exactly
  the listed families and nothing with reviewer, ledger or other-attempt text. The variable parts are schema
  paths, packet identifiers, and characters or digit counts from the teacher's own JSON.
- A first final that validates takes today's path; only provenance gains the policy fields (condition 1,
  covered by the identity test).

## Conditions carried into use

1. The first live repaired run is flagged in its request; I compare refused and final annotations myself.
2. A repaired run always goes to full review (as implemented).

## 255/004

It may run with repair **enabled**. The user's decision applies to every run from this acceptance on, and
this is exactly the failure it was made for. Use the new packet `000255-004`. If your launch authorisation
from the user was tied to the earlier description and Codex asks again, ask them again; do not work round it.

## Order of work

255/004, replacement 234, the run-ahead migration note, then 256 onward. Revision mode is the remaining
implementation.
