# Verdict: commit-000128-001

Reviewer: Fable (independent reviewer; file mailbox)
Run: `.teacher/runs/commit-000128-001`
Packet: `.teacher/retrieval/000128-001`
Upstream: `4710c012a51fcadbee12be0f3fd6cf64ade2a60b` "Don't hold on to file handles during conversion/compilation"
Request: `reviews/requests/commit-000128-001.md`
Reviewed: 2026-11-14, working tree on top of `d0a2d08`, machine `exdev-314`

## Decision

**APPROVED for ancestor retrieval only.** Canonical and training remain false.

Every statement I checked is true. Two added lines; the entry explains why closing is safe (tensors are already in
memory, headers and the key map survive, files reopen on demand) and is honest that it adds no cleanup on failure.

This is the first teacher session on the shared blob store, and it behaved exactly like the ones before it.

## Artifacts reviewed (sha256)

All sixteen hashes in the request match the files on disk.

## Run checks

| Check | Result |
|---|---|
| Run integrity | 10 of 10 ledger entries match the transcript, none uncited; final message equals the annotation; Markdown equals the render; full review; 42 of 42 implementation hashes (`teacher/blob_store.py` is the new one); exactly 127 strict-ancestor entries; 1,849 blobs hash to their names; no evidence timestamp after the cutoff. |
| Replay | 10 of 10 recorded tool calls identical. No `run` call. |
| Unassisted | Standing instructions byte-identical to 127/001's. |
| No hindsight | No blob in the packet contains `reviews/verdicts` or a defect-ledger path. |
| Shared store | The packet's blobs are mode 444 hard links (the one I examined has 112 links). `check.py` and the replay needed no change. |
| Cutoff | Issue 33's snapshot ends with the reporter's comment of 2025-05-07T03:12:14Z, which contains "Too many open files (errno=24)". The cutoff is 08:15:29Z. The maintainer's reply at 08:19:06Z, and the reporter's confirmation after it, are in neither the packet nor the session. The entry's link to the issue is labelled inference. Correct. |
| Catalog | GitHub: open at the cutoff are 1, 4, 7, 10, 14, 22, 24, 26, 27, 28, 29, 33, 34. Matches the thirteen open rows. The qualifying closed row is issue 21. |
| Architecture trigger | Does not fire. |
| Diff claim | `compile.py`: `qtensors_stc.close()` after each module's tensors are read and added to `file_dict`. `convert_model.py`: `module.config.stc.close()` after each module or slice is loaded and the clone messages are printed. Nothing else. Correct. |
| `close()` | Calls `ext.stloader_close_file` for every cached handle list and sets the entry to `None`; headers and `tensor_file_map` are untouched, so the next `get_tensor` reopens. The native routine `fclose`s each handle and frees the pinned staging buffers (120). Correct. |
| Compilation | `get_tensors` returns tensors already read into memory; `.contiguous()`; kept in `file_dict`; `save_file` runs after the inner loop. Closing cannot invalidate them. Correct. |
| Conversion | The new call is before `qmaps = module.get_qmaps()`, so it also runs for modules with nothing to quantize; the later reload uses in-memory tensors. Correct. |
| No failure path | Neither call is in a `finally`. Correct. |
| Discussions | 34 is a Cholesky failure, 21 a Windows build failure. Unrelated, as the entry says. |
| Findings | None, and I found none in the change itself. |

## Reviewer-only notes (never to a teacher)

- **Where the failure came from.** The collection has cached per-file handles since the first commit, with
  `STLOADER_THREADS` handles per file: five until commit 119, eight from 119 on. Conversion writes one `qtensors`
  file per module and compilation reads them all through one collection, so open streams grew by eight per module.
  The reporter's job failed at `model.layers.48`. That is consistent with a limit of 512 open streams once the
  source shards' handles are counted too, but I did not establish the limit or the shard count. If so, 119's change
  from five to eight is what brought a model of this depth under the limit, and this commit is the fix.
- The 126 verdict predicted this fix from comments after that commit's cutoff. Here the cause was inside the cutoff
  and the teacher found it in the snapshot on its own.

## Not verified

- Any conversion, or a count of open handles.

## Must fix before canonical use

None for this entry.

## Follow-ups

1. Ledger, when next revised: a fix-derived record for handle accumulation during conversion and compilation, fixed
   at `4710c012`. Introduction: per-file caching at the first commit, made worse at `647bb7d5` (five to eight handles
   per file). Suspected; no execution.

## Storage follow-ups from the request

- The twelve skipped tests are the environment-gated sandbox and integration tests; noted, and consistent with what
  I saw. Nothing further needed.
- The hard-link note is in the documentation. Good.

## Next

1. Record this approval.
2. Continue the walk at commit 129.
