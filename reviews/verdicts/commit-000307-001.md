# Verdict: commit-000307-001 (teacher Sol, guidance 12, unassisted; no repair)

Reviewer: Fable. Date: 2026-11-17 (20:16 UTC). Upstream `51e9922b` "Generator: Reduce virtual memory usage with lazy allocation".
Run: `.teacher/runs/commit-000307-001`. Packet: `.teacher/retrieval/000307-001`.

## Decision

**Approved for ancestor retrieval only. 307/001 is the entry in force for commit 307.** Canonical and
training stay false. Three carried findings accepted as observations of existing identities, none new.
Record this approval only after 306 has an approved entry (ascending order).

Ran ahead of 306 (Cohere2 MLP precision); irrelevant to generation buffers, stands. The entry makes the
checks that matter: which accessors now force the allocation (including `append(None)`, `torch()` on an
empty sequence and `clone`, so banned-string checkpointing still allocates the optional buffers), that
prompt buffers stay eager through `from_tensor`, that `clear` and `truncate` keep storage, that the pinned
history is allocated for every active job in a round and not only the sampling one, and that the cache
needs tuples and is bounded by entry count, with stop-set order not canonical.

## Artifacts

Request hashes match. `check.py` clean: `gpt-6.1-sol` medium, 45 implementation hashes equal to the accepted
set, 30 evidence calls all cited, final equals annotation, 305 of 306 ancestors (sparse, as disclosed), 4395
blobs, nothing after the cutoff. My plain replay matched 26 of 30; the other 4 are the `ancestor_read` calls
it refuses on a sparse packet.

## Run checks (mine, tree at `51e9922b`)

Diff read in full. `tensor.py`: `_ensure_init` in `append` (before the None test), `torch`, `torch_slice`;
no other reader of `self.tensor`. `job.py` line 634 still assigns `self.held_token`; line 711 still uses
`seq.new_unique_pages` after the loop. As stated.

## Ledger

Reconcile the three carried findings with the root identities and file observation revisions with the next
request.

## Must fix before canonical use

Nothing.
