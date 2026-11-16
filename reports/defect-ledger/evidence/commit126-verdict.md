# Verdict: commit-000126-001

Reviewer: Fable (independent reviewer; file mailbox)
Run: `.teacher/runs/commit-000126-001`
Packet: `.teacher/retrieval/000126-001`
Upstream: `c8836d9f5abf58ca7967c08beb39a23be675e10e` "Print error code when failing to open Safetensors file"
Request: `reviews/requests/commit-000126-001.md`
Reviewed: 2026-11-14, working tree on top of `d0a2d08`, machine `exdev-314`

## Decision

**APPROVED for ancestor retrieval only.** Canonical and training remain false.

Every statement I checked is true and the finding is correct. The entry reads each of the four native routines
separately and so notices that the diagnostic was wired up differently in each.

This commit sits right on a discussion boundary and the packet handles it correctly: see the Cutoff row.

## Artifacts reviewed (sha256)

All twelve hashes in the request match the files on disk.

## Run checks

| Check | Result |
|---|---|
| Run integrity | 9 of 9 ledger entries match the transcript, none uncited; final message equals the annotation; Markdown equals the render; full review; 41 of 41 implementation hashes; exactly 125 strict-ancestor entries; 1,835 blobs hash to their names; no evidence timestamp after the cutoff. |
| Replay | 9 of 9 recorded tool calls identical. No `run` call. |
| Unassisted | Standing instructions byte-identical to 124/001's (125 was a merge and carried the extra merge line). |
| No hindsight | No blob in the packet contains `reviews/verdicts` or a defect-ledger path. |
| Cutoff | Issue 33 continues after this commit. The snapshot the session read ends with the comment of 2025-05-06T03:24:04Z; the cutoff is 17:29:43Z; the maintainer's next comment ("I added some more output") is at 17:31:50Z. Neither that comment nor anything later (the reporter's rerun, the stated cause, the later unrelated thread) occurs in the packet or the transcript. The "promise" the entry cites is the comment of 02:24:59Z, inside the cutoff. |
| Catalog | GitHub: open at the cutoff are 1, 4, 7, 10, 14, 22, 24, 26, 27, 28, 29, 33, 34. Matches the thirteen open rows. Two qualifying closed rows, 17 and 19, both closed in April. |
| Architecture trigger | Does not fire. |
| Open failure | `stloader_open_file`: on a null `fopen` result, `errno` is saved and `TORCH_CHECK(false, ...)` reports the filename, `strerror` and the number. Was `TORCH_CHECK(file, "Error opening file")`. Correct. |
| Python | Both the `defer` and `mt_fread` branches wrap the open in `try`, print the filename on `RuntimeError` and re-raise; the handle is cached only on success. The `python` backend and header reading are untouched. Correct. |
| Immediate read | Both worker error labels in `stloader_read` set `load_errnum = errno`; the post-join check formats it. The CUDA copy failure still prints `cudaGetErrorString`. Correct. |
| Deferred CPU | The worker sets `load_errnum`, but the post-join check is still `TORCH_CHECK(!load_failed, "I/O error reading tensor")`. Correct. |
| Deferred CUDA | The post-join check formats `load_errnum`, but the worker's error label sets only `load_failed`. Correct. |
| Discussions | Issue 33's traceback ends in `stloader_open_file` with the old message; the link is labelled inference. Issue 17 is an installation problem. Correct. |
| Finding `deferred-cuda-error-number` | Correct. In `stloader_deferred_cuda`, `load_errnum` is declared 0 (line 260) and never assigned; the message will read `strerror(0)` and `errno=0`. Suspected is right; nothing was induced. |

## Reviewer-only notes (never to a teacher)

- **Hindsight, from comments after the cutoff.** The reporter's rerun with this commit showed the cause the next day:
  a limit on the number of open files. That fits the source: `stloader_open_file` opens `STLOADER_THREADS` handles
  per file and the collection keeps them until `close()`; commit 119 raised that constant from 5 to 8. I expect a
  later commit to release or limit handles. When it arrives, the introducing commits to check are the one that
  added per-file handle caching and 119.
- In `stloader_read` the number reported for a CUDA copy failure, or for a short read that sets no `errno`, is
  whatever `errno` happens to hold in that worker thread. The entry does not claim otherwise.

## Not verified

- Any execution or induced failure.

## Must fix before canonical use

None for this entry.

## Follow-ups

1. Ledger: `deferred-cuda-error-number` is approved as drafted. The deferred CPU half (number captured, never
   reported) is the same oversight and belongs in the same record.

## Next

1. Record this approval.
2. Continue the walk at commit 127.
