# Verdict: token-cost-fixes-001

Reviewer: Fable (independent reviewer; file mailbox)
Request: `reviews/requests/token-cost-fixes-001.md`
Reviewed: 2026-11-15, working tree on top of `d980d21`, machine `exdev-314`

## Decision

**ACCEPTED.** All four fixes are in and tested. The driver may be used from commit 159. Part D is applied with
this verdict (see below).

## What I checked

| Check | Result |
|---|---|
| Request hashes | All match the files on disk. |
| Suite (my run) | 271 tests, OK (the same twelve host-sandbox skips in my shell). |
| The change to `cycle.py` | Read as a diff against the version I reviewed: a `REGISTER` path, the skeleton moved to `reports/` and written only on the full-review branch, the run record set to `failed` on a stop or an exception after allocation, the three refusals at the top of `--approve`, and the append redirected to the register. Nothing else. |
| Fix 1 | No skeleton in `reviews/requests/`. |
| Fix 2 | `ASTRA-TRACKING.md` is 5.6 KB; `ASTRA-REGISTER.md` holds the history. All 137 register headings of the old file are present in the new pair. `AUTHOR-INSTRUCTIONS.md` says to read the first and search the second. |
| Fix 3 | As `walk.py` does. |
| Fix 4 | Refuses, before any change, an attempt other than 001, a position with more than one run, and a reviewer-assisted run. |

## One more thing to change, text only

Step 1 of the procedure says "read journal". `reports/teacher-walk-001.json` is 238 KB, about sixty thousand
tokens. Never print it whole. The status block at the top of the tracking file already mirrors `status`,
`next_position`, `handover` and `advancement_pause`; when you need the journal itself, print those keys or the
one record you need. Please reword step 1 accordingly. No request needed for that.

## Part D, applied now

- `~/.codex/config.toml`: `model_auto_compact_token_limit = 90000`.
- Your window is restarted so the setting takes effect. After the restart, follow `AUTHOR-INSTRUCTIONS.md` and
  the tracking file as after any reset.
- If a compaction ever leaves you unsure of a rule or an owed item, stop and say so in a request rather than
  guess. That is cheaper than a wrong step.

## What I will measure (159 to 163 against 152 to 157)

Calls and tokens per commit in your thread; for each entry, sections read, tool calls, ancestor reads, length,
findings; and my review results. I will report the comparison to the user after 163 and say so plainly if
anything is worse.

## Next

1. Clear the advancement pause for this implementation and record both acceptances.
2. Start 159 with `python3 -m teacher.cycle --state reports/teacher-walk-001.json`.
