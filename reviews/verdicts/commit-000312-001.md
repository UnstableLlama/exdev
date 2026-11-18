# Verdict: commit-000312-001 (teacher Sol 6.2, guidance 12, unassisted; no repair)

Reviewer: Fable. Date: 2026-11-17 (23:12 UTC). Upstream `415a55cc` "MMLU eval: More feedback during eval".
Run: `.teacher/runs/commit-000312-001`. Packet: `.teacher/retrieval/000312-001`.
Second entry on `gpt-6.2-sol` (2 of 3 full-depth reviews).

## Decision

**Approved for ancestor retrieval only. 312/001 is the entry in force for commit 312.** Canonical and
training stay false. Two new suspected findings accepted (progress totals use the count from before the
per-subject cap; skipping every subject or a negative cap reaches the inherited division by zero). One
carried (few-shot counter, 309).

Ran ahead of 311 (memory.py); irrelevant to the MMLU script, stands; 311 is approved, so record now. The
entry makes the checks that matter itself: one counter per subject does two jobs (admitted while
enqueueing, outstanding while scoring), the subject report fires when it returns to zero, `total_jobs` is
counted before the cap, zero and `None` both disable the cap because the test is truthiness, a negative cap
admits nothing, the skip is a slice of the sorted names so `-1` keeps the last, and the cap is a prefix of
the sorted rows and not a sample.

## Artifacts

Request hashes match. `check.py` clean: `gpt-6.2-sol` medium, 45 implementation hashes equal the accepted
003 set, 12 evidence calls all cited, final equals annotation, 310 of 311 ancestors (sparse, as disclosed),
4443 blobs, nothing after the cutoff. My plain replay matched 10 of 12; the other 2 are the `ancestor_read`
calls it refuses on a sparse packet.

## Run checks (mine, tree at `415a55cc`)

Diff read in full. `util/progress.py`: `__exit__` sets completed to the declared count when not transient,
so the Questions bar is forced full as the entry says. Enqueueing does not call `iterate`, so no counter
can reach zero before admission ends. As stated.

## Ledger

311 record eager-pydantic-import-in-memory-utility r001 accepted as filed (new identity at `48ade457`,
suspected, training false). File 312's two new and one carried with the next request.

## Must fix before canonical use

Nothing.
