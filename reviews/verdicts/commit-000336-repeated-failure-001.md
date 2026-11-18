# Verdict: commit-000336-repeated-failure-001

Reviewer: Opus (stand-in). Provisional; Fable re-reviews after the token reset.
Date: 2026-11-18 (08:06 UTC). Stopped runs: `.teacher/runs/commit-000336-001` and `.teacher/runs/commit-000336-002`
(no draft from either; nothing to judge as an entry). Upstream `37f80fb9` "Fix typo".

## Decision

**Stopped at 336, waiting for the user. Do not start a third attempt and do not release the queue.** The limit set in
`reviews/verdicts/commit-000336-recovery-002.md` has been reached, and only the user can lift it. I have asked them.

## What I checked myself

- Request hashes: 14 checked, 0 bad.
- Both runs failed the same way: status `failed`, `ValueError`, transcript of system and user messages only, no token
  usage, and `Codex reported an authoring error` from `codex_adapter.py:242`. The walk state is `stopped_failure` at 336
  with no cycle process running.
- The cause is not established. The adapter drops the event payload, and `codex_transport.py` deletes the teacher's
  temporary Codex state and its stderr when the process ends, so neither survives a failure.
- What the evidence does rule out: adding the 335 entry did not change the outcome, and the author's log read 94% of
  the weekly quota at the time. 335 authored normally minutes before the first failure.

## Requested now (preparation only)

File a normal implementation request with hashes that keeps, for a failed run, the Codex `error` event payload and the
app-server stderr, with credentials redacted. It must not change teacher input, the packet or the model. Do not apply
it to a live run until it has been reviewed, and do not launch anything for 336 until the user has answered.
