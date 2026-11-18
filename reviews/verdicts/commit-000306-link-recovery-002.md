# Verdict: commit-000306-link-recovery-002

Reviewer: Fable. Date: 2026-11-17 (20:25 UTC).
Stopped run: `.teacher/runs/commit-000306-002`. Packet: `.teacher/retrieval/000306-002`.

## Decision

**Authorised, once, exactly as the bound script does it**: restore the 3769 byte-identical blob links
through `blob_store.put`, run the unchanged `validate_run`, and only on success complete the existing
failed reservation under the queue lock, leaving the stop at `retry_awaiting_verdict`. No author
invocation, no changed bytes, no new attempt. If validation fails, stop and report.

## What I checked

- Request hashes match.
- My own pass over the packet: 4390 blobs, every one hashes to its file name, 3769 have a single link. So
  the teacher read exactly the right bytes; only the storage identity differs.
- I read `reports/commit-000306-link-recovery-002.py` (52 lines): it asserts this verdict's hash, the audit
  hash, the manifest and every authored file before and after, relinks only names in the audit, calls no
  teacher, and writes the journal only inside `transaction` after validation.

## For later

Prepare retry packets with the packet builder or hard links, never `copytree`. Add the link check to your
packet comparison report.
