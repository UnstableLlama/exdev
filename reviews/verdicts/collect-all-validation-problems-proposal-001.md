# Verdict: collect-all-validation-problems-proposal-001

Reviewer: Fable. Date: 2026-11-18.

## Decision

**The design passes review. It is not in force and nothing may be applied until the user says so.**

You may prepare the implementation as a patch plus tests and file it as a normal implementation request, without
applying it and without delaying the walk. I will review it; applying it then needs the user's word, which I will
quote in that verdict.

## What I checked

- Request hashes 0 bad.
- The two cases it cites are as I verified them in `commit-000345-recovery-001` (re-reviewed) and
  `commit-000346-recovery-001`: in each, the first final held two problems and the single repair message named one.
- The proposal keeps what matters: validation stays strict, the repaired annotation is fully revalidated, the
  feedback is derived only from the candidate, its transcript and the validator rules, no replacement citation or
  expected answer is given, and older repair policies still replay.

## Conditions on the implementation

1. Still one repair turn. No second repair.
2. A rejected reference is reported by its path and the rejected value only, as v3 does now. Never list valid call
   IDs or a nearest match.
3. A method/evidence refusal names the path, the finding ID and the supported tool kinds, as the present
   `AnnotationDiagnostic` does, and nothing more.
4. Dependent checks are skipped, not guessed: say in the patch notes which checks depend on which.
5. New policy name; `validator-claim-diagnostics-v3` transcripts must replay unchanged. Include replays of 345/001
   and 346/001 showing the message each would have received under the new policy.
6. Bound the message; state total and omitted counts when the bound is hit.
