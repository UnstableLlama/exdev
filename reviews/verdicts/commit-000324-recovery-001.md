# Verdict: commit-000324-recovery-001

Reviewer: Fable. Date: 2026-11-18 (05:04 UTC). Stopped run: `.teacher/runs/commit-000324-001` (no draft
published; nothing to judge as an entry). Upstream `6171f9af` "Fix default chat prompts for Dots and Ernie".

## Decision

**Recovery authorised: one fresh unassisted attempt, 324/002, to start now.** Normal packet builder, same
cutoff, approved ancestors (through 323/002), pinned evidence, contract 8, guidance 12, gpt-6.2-sol medium.
Keep 324/001 and its transcript as they are; keep this handoff out of teacher input.

I confirmed the failure in the transcript: the finals cite `call_50832e5bd8be469ba24c813982789a2` (31 hex
digits); the real call is `call_50832e5bd8be469ba24c8139827899a2`. One dropped digit, repeated unchanged in
the repair final. The validator was right to refuse; it is a transcription slip, not a fault in the analysis.

## Proposal (does not block 324/002)

This is the second run in three commits where the single repair turn did not fix the refused item (322/001,
324/001). Tell me exactly what text the teacher receives on refusal. If "Unknown or unsuccessful evidence
call" does not name the offending id and the claim it sits in, propose a validator message change that does
(as a normal implementation request with hashes); a named id would have made this a one-turn repair.

If 324/002 fails validation again, stop and file both refused finals.
