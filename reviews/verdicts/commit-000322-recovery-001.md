# Verdict: commit-000322-recovery-001

Reviewer: Fable. Date: 2026-11-18 (00:54 UTC). Stopped run: `.teacher/runs/commit-000322-001` (no draft
published; nothing to approve or reject as an entry).

## Decision

**Recovery authorised: one fresh attempt, 322/002, unassisted, when the user resumes.** Not before; the
user's 00:45 UTC stop order stands and no teacher run starts tonight. Stopping and filing this was right.

The failure is the validator doing its job: a `source_inspection` check on a finding cited only
`repo_grep` (and `run`), and the one repair turn removed `run` without adding a source read. That is a
citation fault in one finding, not evidence about the rest of the draft, which I have not seen and do not
judge. A new attempt gets a new packet by the normal route (hard links, not a copy), same contract 8 and
guidance 12, `gpt-6.2-sol` medium, no reviewer notes in teacher input.

## On resumption

1. Start 322/002 by the normal rerun route; keep 322/001 and its transcript as they are.
2. In the 322/002 request, say whether the plain-MLP allocation finding reappears and which source call
   backs it.
3. If 322/002 fails the same check, stop and file both refused finals side by side; I will then look at
   whether the validator message gives the teacher enough to fix it in one turn.
