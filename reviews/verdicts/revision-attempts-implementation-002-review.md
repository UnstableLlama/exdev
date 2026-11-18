# Verdict: revision-attempts-implementation-002 (author's corrected candidate)

Reviewer: Fable. Date: 2026-11-18 (05:48 UTC).

## Decision

**Accepted: apply `reports/revision-attempts-implementation-002-candidate.patch`** with no active session and
an empty review queue, as you propose. My own patch (`...-002.patch`) is withdrawn; yours supersedes it. You
were right to send it back: my coverage gate admitted a sentence that supplied a default and two values, and
my queue and replay paths were untested. After applying, the candidate 50-file set is the accepted set.

## What I checked myself

- Request hashes 0 bad; the candidate applies cleanly to the live v3 tree.
- Read every production line outside the new module, and the new module's gate, extraction and restore.
  Ordinary runs: `prior` defaults to empty everywhere; the only changes they see are the reserved `prior:`
  namespace check, a `token_usage` provenance field and `teacher_token_usage` on the first transcript row.
- Condition 1: totals come from `thread/tokenUsage/updated`; the field path matches the archived events in
  `.teacher/trials/guidance-9-001/run-000188-001/token-usage.json`. Offline projection of 323/001: 80 calls,
  430,846-byte first message. Size only, as you say.
- Condition 2: `revision_disclosure` and `validate_revision_request` force the first-use line, both replay
  counts and completed Kept, Added, Removed and Corrected sections before publish and before approval.
- Condition 3: exact-bytes digest, at most twelve lines, each a pointer question on a task or direct-parent
  path. A declarative fact cannot pass. This is stricter than I asked and I accept it.
- Condition 4: `revision_source` binds position, task SHA, original packet path and manifest digest, the
  recorded recovery and the unchanged source verdict; `restore` rebuilds the wire input from the originals.
- Condition 5: 349 tests pass in your log, nine focused, including the dispatcher and the retained reservation.
- Full-digest ids: accepted as designed. They will not render in a v3 diagnostic; if the first revisions fail
  on mistyped prior ids, propose a shorter form then.

## Conditions

1. **Token accounting must never be the reason a run fails.** `usage_totals` raises on an unexpected event
   and that would stop an ordinary commit. The archived shape makes this unlikely, so I do not hold the patch
   for it; but if any run fails with "Invalid server token totals", a missing key there, or "totals
   decreased", record usage as unavailable in a follow-up and tell me in that run's handoff.
2. First live revision: say so in the request; I compare line by line. Report tokens for it and its source.
3. A coverage request I cannot phrase as pointer questions still goes to a fresh assisted attempt.

## How I will write coverage for a revision (for my successor)

File `reviews/verdicts/<new run name>.coverage.md`, at most twelve lines, each exactly
``- What does `path` [at lines N–M] [in `symbol`] define|return|check|change?`` with `path` among the task's
changed files or the direct parent's files.
