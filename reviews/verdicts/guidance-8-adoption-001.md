# Verdict: guidance-8-adoption-001

Reviewer: Fable (independent reviewer; file mailbox)
Request: `reviews/requests/guidance-8-adoption-001.md` (sha256 `960cc5bfdc6f163e4522d4fe1b983af32406e87ec44762ca1fe89666b431fdda`)
Decision file: `reviews/verdicts/guidance-8-adoption.decision.md`
Reviewed: 2026-11-15, working tree on top of `0ed73a1`, machine `exdev-314`

## Decision

**ACCEPTED.** Guidance 8 is the walk default from 178.

## What I checked

| Check | Result |
|---|---|
| Request hashes | All match the files on disk. |
| The change | One production line: `prepare()` writes `guidance_version=8`. `teacher/session.py` has the same hash as in the accepted trial gate, so the version-8 text and its gate are unchanged. |
| The adopted text | `GUIDANCE_8_ADDITION` equals paragraph D in the adoption decision exactly (compared programmatically). |
| Older packets unchanged (mine) | Rebuilding the session with the current code gives system text identical to the recorded transcript for 177 (version 7), 171 (version 5), the guidance-6 trial packet for 154 (version 6) and the guidance-8 trial packet for 154 (version 8). |
| Suite (my run) | 280 tests, OK, with `codex` on the path. |
| Test change | The fixture test now expects default 8, checks it equals an explicit version-8 packet, and keeps the version 5, 6 and 7 checks. |

## What to do from 178

1. Walk packets carry `guidance_version` 8. Requests say "guidance 8".
2. Keep reporting tool counts and ancestor reads per commit; the cost and effect comparison against 172 to 177
   is owed to the user after a few commits.
3. Trial outputs stay unapproved and are never ancestor context.

## Next

1. Proceed to 178.
