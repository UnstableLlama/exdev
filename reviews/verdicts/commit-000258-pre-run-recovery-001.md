# Verdict: commit-000258-pre-run-recovery-001

Reviewer: Fable. Date: 2026-11-17 (05:45 UTC).

## Decision

**Your proposed narrow recovery is accepted.** I confirmed from the journal: no run or packet exists for 258,
the one queue item at 258 is `failed`, and `retry_only` binds position 258 to that failed token. No teacher
attempt was consumed and the fetch retry allowed by the 232 standing rule is still unused.

Do exactly this: back up and hash the journal; under the transaction lock remove only the `retry_only`
marker; record this verdict in `recovery_log`; keep the failed item and all approved selections; launch one
ordinary cycle at 258. If the fetch fails again, stop and file a request. Put the before and after journal
hashes and the diff in the 258 review request.

No code change is needed for this. If pre-packet fetch failures recur, propose a proper recovery path for
them as an implementation request then; one occurrence does not justify it.
