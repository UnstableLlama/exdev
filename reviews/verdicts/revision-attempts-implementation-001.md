# Verdict: revision-attempts-implementation-001 (design request)

Reviewer: Fable. Date: 2026-11-17.

## Decision

**Design accepted. Implement after run-ahead and submit the completed change as
`revision-attempts-implementation-002`. No revision teacher session until that is accepted.**

It matches the user's decision (`revision-attempts-001.decision.md`): same packet bytes, the teacher's own
previous annotation and tool records, a pointer-only coverage request, a complete replacement written by the
teacher, nobody else editing prose, the rejected attempt untouched.

## Accepted as proposed

- Separate `author_revision` entry point; ordinary `author` unchanged; one revision per rejection, reserved
  atomically; a failed revision does not free the reservation.
- Teacher input limited to the mechanically extracted prior annotation, the prior call/result pairs and the
  coverage request. Verdict text, `review.json`, ledger material, prior prompts and commentary, and other
  attempts are excluded, with tests that plant such material and show it is absent.
- The new transcript stays truthful: imported calls live in a separate `prior-evidence.json` under a reserved
  `prior:<sha>:<id>` namespace; the citation resolver merges the two ledgers; prior and new calls are replayed
  and counted separately.
- The proposed instruction text, as an additional mode instruction that leaves guidance 5 to 12 alone.
- Provenance fields and the request template with a kept / added / removed / corrected list.
- Stopping for review when the packet already carries an attempt-specific coverage attachment.

## Conditions

1. **Measure whether it is cheaper.** A revision starts with the whole earlier transcript in context (the two
   recent rejected runs are about 270 KB and 520 KB of transcript). Record input, cached-input and output
   token totals for each revision and for the fresh attempt it replaces, and report them in the request for
   the first three revisions. This needs the long-owed `token-usage-retention-001`; fold it in here. If
   revisions turn out to cost more than fresh attempts, I will tell the user.
2. **First live use is watched.** The first revision request gets a line-by-line comparison from me against
   the attempt it revises; say in that request that it is the first.
3. **Leak test on the coverage file.** The pointer-only admission check must run on the exact coverage bytes
   supplied, and the test fixtures must include a coverage file that states a fact, which must be refused.
4. **No silent reuse across positions or packets.** A prior record is importable only from the same position,
   same task SHA and byte-identical packet; show the refusal cases.
5. Full host-enabled suite plus the focused tests you list; bind the diff and results.

## Order of work

Unchanged: the walk continues one at a time (255/003, then 234, then 256 onward); run-ahead implementation
first, this second, as separate requests, fitted between runs.
