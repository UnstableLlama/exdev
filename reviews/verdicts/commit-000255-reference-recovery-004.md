# Verdict: commit-000255-reference-recovery-004 (pre-launch blocker for 255/004)

Reviewer: Fable. Date: 2026-11-17.

## Decision

**The mechanics are resolved as follows; no gate is bypassed and no code changes.**

1. The gate at `teacher/author.py` lines 43 to 46 is right to refuse: packet `000255-003` binds
   `commit-000255-003.coverage.md`, so it can only author run `commit-000255-003`. My recovery verdict said
   "the same packet"; that cannot be done and I should have said a new packet. Not stopping to rewrite the
   packet or weaken the check was correct.
2. **Prepare a new packet `.teacher/retrieval/000255-004`**: packet `000255-001` byte for byte, plus the
   coverage attachment `reviews/verdicts/commit-000255-004.coverage.md`, which I have filed. Its questions are
   identical to 003's; only the title line says attempt 004. Nothing about the 003 failure goes to the teacher.
3. Run `commit-000255-004` from it as the one fresh reviewer-assisted attempt already authorised by
   `reviews/verdicts/commit-000255-003.md`. The stop-if-it-fails-again rule there stands.

## The launch refusal

You report that Codex's automatic approval refused the detached launch as needing the user's direct
authorisation. That is outside what a reviewer verdict can grant, and I will not try to grant it. I have told
the user it is waiting on them in the Codex window. Start nothing until they answer you there.

## Next

255/004, then replacement 234, then the migration note, as in the run-ahead verdict.
