# Verdict: guidance-9-adoption-001

Reviewer: Fable (independent reviewer; file mailbox)
Request: `reviews/requests/guidance-9-adoption-001.md` (sha256 `f0c0880ca11385f04cda9b0818549de29f75e235d03519b67dc8f07581bf6184`)
Decision file: `reviews/verdicts/guidance-9-adoption.decision.md`
Reviewed: 2026-11-16, working tree on top of `e9e83ff`, machine `exdev-314`

## Decision

**ACCEPTED.** Guidance 9 is the walk default from 200. Version 10 is not adopted.

## What I checked

| Check | Result |
|---|---|
| Request hashes | All match the files on disk. |
| The change | One production line: `prepare()` writes `guidance_version=9`. `teacher/session.py` is unchanged since `e9e83ff`, so the version-9 and version-10 texts and their gates are as accepted. |
| The adopted text | `GUIDANCE_9_ADDITION` appears exactly in the adoption decision (compared programmatically). |
| Older packets unchanged (mine) | Rebuilding the session with the current code gives system text identical to the recorded transcript for 171 (version 5), the guidance-6 trial packet for 154, 177 (version 7), 199 (version 8), the guidance-9 trial packet for 190 and the guidance-10 trial packet for 188. |
| A version-9 packet (mine) | A hard-linked copy of the 199 packet with only `guidance_version` set to 9 gets instructions equal to the version-8 instructions plus a blank line plus paragraph E, and the same task message. The copy was deleted. |
| Suite (my run) | 280 tests, OK, with `codex` on the path. |
| Test change | The fixture test now expects default 9 and compares it with an explicit version-9 packet. |

## What to do from 200

1. Walk packets carry `guidance_version` 9. Requests say "guidance 9".
2. Keep reporting tool counts and ancestor reads per commit; the cost and effect comparison against 178 to 198
   is owed to the user after a few commits.
3. Trial outputs stay unapproved and are never ancestor context.

## Next

1. Proceed to 200.
