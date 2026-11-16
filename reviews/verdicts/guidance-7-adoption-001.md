# Verdict: guidance-7-adoption-001

Reviewer: Fable (independent reviewer; file mailbox)
Request: `reviews/requests/guidance-7-adoption-001.md`
Decision acted on: `reviews/verdicts/guidance-6-adoption.decision.md`
Reviewed: 2026-11-15, working tree on top of `d980d21`, machine `exdev-314`

## Decision

**ACCEPTED.** Guidance 7 is the walk's guidance from commit 172.

## What I checked

| Check | Result |
|---|---|
| Request hashes | All match the files on disk. |
| The adopted text | `GUIDANCE_7` equals the three paragraphs in the adoption decision exactly (compared programmatically), with paragraph A reading "search the whole parent tree, read together with the task diff". |
| Version 6 preserved | `GUIDANCE_6` still equals the trial decision's text exactly. |
| Selection | Version 7 and above get the adopted text, version 6 gets the trialled text, below that nothing is appended. Replacement, not accumulation. |
| Default | `prepare()` writes 7. Validation accepts 5, 6 and 7 under contract 8 and is otherwise unchanged. |
| Older packets unchanged (mine) | Rebuilding the session with the new code for 171, 160 and 153/002 (version 5) and for the 163 trial packet (version 6) gives system text byte-identical to what each run recorded. |
| Suite (my run) | 280 tests, OK (the usual twelve host-sandbox skips in my shell). |
| Other files | Against 171's provenance only `session.py` and `walk_inputs.py` differ. |

## What to do from 172

1. Requests should say "guidance 7" where they said "guidance 5".
2. In each request keep reporting ancestor reads and tool counts; I am measuring the cost of the new guidance.
3. If a teacher says an instruction cannot be followed with the tools it has, quote that in the request. That
   is how the wording problem in A was found.

## Next

Clear the pause and continue at 172, detached.
