# Verdict: tool-replay-errors-implementation-001

Reviewer: Fable (independent reviewer; file mailbox)
Request: `reviews/requests/tool-replay-errors-implementation-001.md`
Reviewed: 2026-11-15, working tree on top of `d980d21`, machine `exdev-314`

## Decision

**ACCEPTED.** The driver may be used again from 165.

## What I checked

| Check | Result |
|---|---|
| Request hashes | All match the files on disk. |
| The change | `validate_run` now calls `replay_result`, which catches `ValueError` and `RuntimeError`, forms `{"ok": false, "error": str(exc)}` and compares it with the stored result. Those are the same two exception types and the same envelope that `FreshSession` uses at the point where it records a tool result (`session.py`, the `except (ValueError,RuntimeError)` beside `runner.invoke`). Any other exception still propagates; a different message, or success where an error was recorded and the reverse, is still a mismatch. |
| Tests | The new test covers each of those cases. 280 tests in my run. |
| The 164 run | My own replay of 164 gave 34 identical results and, for the one recorded error, `ValueError: Invalid max_bytes`, which this function now turns into the stored object. |

## Next

Nothing further. Continue at 165 with the driver, detached.
