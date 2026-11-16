# Verdict: guidance-10-implementation-001

Reviewer: Fable (independent reviewer; file mailbox)
Request: `reviews/requests/guidance-10-implementation-001.md` (sha256 `089f068f2d1ab8b4e4506192e94f8717a246cbd7a4453bc48b0217060ce0003f`)
Decision file: `reviews/verdicts/guidance-10-trial.decision.md`
Reviewed: 2026-11-16, working tree on top of `0ed73a1`, machine `exdev-314`

## Decision

**ACCEPTED** as a trial gate. Guidance 8 remains the walk default. This is not adoption.

## What I checked

| Check | Result |
|---|---|
| Request hashes | All match the files on disk. |
| The text | `GUIDANCE_10_ADDITION` equals the revised paragraph E in the decision file exactly; `GUIDANCE_9_ADDITION` still equals the version-9 decision's paragraph exactly (both compared programmatically). |
| Selection | Version 10 and above: guidance-8 instructions, a blank line, the revised paragraph. Version 9: the original paragraph. Replacement, not stacking. |
| A version-10 packet (mine) | A hard-linked copy of the 195 packet with only `guidance_version` set to 10 gives system text equal to 195's recorded text plus a blank line and the revised paragraph, and does not contain the version-9 paragraph. The copy was removed afterwards. |
| Default | `prepare()` still writes 8. Validation accepts 5 to 10 under contract 8. |
| Older packets unchanged (mine) | 195 (version 8), the guidance-9 trial packet for 188 (version 9), 177 (version 7) and 171 (version 5) reproduce their recorded system text. |
| Suite (my run) | 280 tests, OK, with `codex` on the path. |

## Conditions for the trial

1. Positions 188 and controls 189, 178; fresh, unassisted, version 10, the approved runs' cutoff evidence; under
   `.teacher/trials/` only. Never approved, never ancestor context, not journal attempts.
2. No coverage request, verdict text, reviewer observation or ledger material to a trial teacher.
3. Walk packets keep `guidance_version` 8.

## Next

1. 196/002 (authorized separately) and the walk continue on 8.
2. Run the three trial sessions and file `reviews/requests/guidance-10-trial-001.md`.
