# Verdict: validation-repair-implementation-001 (design request)

Reviewer: Fable. Date: 2026-11-17.

## Decision

**Design accepted. Implement it and submit the completed change as `validation-repair-implementation-002`. No
live use until that is accepted.** It matches the user's decision (`validation-repair-001.decision.md`) point
for point: one additional turn on the same thread, the validator's `str(error)` verbatim with no wrapper, one
repair only, rules and schemas unchanged, the refused annotation kept in the transcript, labelled
`validation_repair`, not counted as reviewer assistance.

## Accepted as proposed

- Only a refusal from JSON parsing or annotation validation is eligible; transport, runtime, budget and
  internal failures stay terminal.
- One tool-call budget spanning both turns.
- The approval-time verifier re-runs the original validation against the transcript prefix at the first
  final and requires the identical exception; then validates the selected final against the whole ledger.
- A successful first final takes today's path with byte-identical inputs.
- For revision mode, a repaired run is imported only through its verified final-selection record.

## Conditions

1. **Show the unchanged path.** A test that a run whose first final validates produces the same opening
   input, transcript shape and draft as today, apart from the new provenance field.
2. **Validator messages must not carry anything but the validator's own words.** Check every `ValueError`
   raised in `validate_annotation` and the JSON path: none may interpolate reviewer, ledger or other-attempt
   text. List them in the 002 request. If any message includes teacher-supplied text (an identifier, say),
   that is fine; say which.
3. **First live repaired run is flagged** in its request as the first, and I compare the refused and final
   annotations myself.
4. Full host-enabled suite plus the focused tests listed; bind the diff and results.

## Order of work

After this: revision mode. The walk's own order is unchanged and is waiting on the user's launch
authorisation for 255/004.
