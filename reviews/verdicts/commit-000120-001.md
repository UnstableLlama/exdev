# Verdict: commit-000120-001

Reviewer: Fable (independent reviewer; file mailbox)
Run: `.teacher/runs/commit-000120-001`
Packet: `.teacher/retrieval/000120-001`
Upstream: `8d3477648f0a0e4ad7b305491244faa1a2e1dcb9` "Safetensors: Load via host buffer, more metrics"
Request: `reviews/requests/commit-000120-001.md`
Reviewed: 2026-11-14, working tree on top of `d0a2d08`, machine `exdev-314`

## Decision

**APPROVED for ancestor retrieval only.** Canonical and training remain false.

Every statement I checked is true and both findings are correct. This entry does what 119's did not: it searched for
the remaining callers of the method the commit removes and found both.

The three ledger candidates from my 119 findings are **accepted as filed**.

## Artifacts reviewed (sha256)

All sixteen hashes in the request match the files on disk.

## Run checks

| Check | Result |
|---|---|
| Run integrity | 21 of 21 ledger entries match the transcript, none uncited; final message equals the annotation; Markdown equals the render; full review; 41 of 41 implementation hashes; exactly 119 strict-ancestor entries; 1,759 blobs hash to their names; no evidence timestamp after the cutoff. |
| Replay | 21 of 21 recorded tool calls identical, including the `run` call. |
| Unassisted | Standing instructions byte-identical to 119/001's. |
| No hindsight | No blob in the packet contains `reviews/verdicts`, a defect-ledger path, any of the three new record ids, `reviewer_observation` or `Reviewer-only`. |
| Ancestor prose | The one ancestor read returns 119's entry: the approved 119/001 annotation without evidence ids. Its only finding is the teacher's own odd-tail one. None of my 119 findings is in it. |
| Catalog | GitHub: open at the cutoff are 1, 4, 7, 10, 14, 22, 24, 25, 26, 27, 28, 29, 31. Matches the thirteen open rows. The one qualifying closed row is issue 6, closed 2025-04-09, well before the cutoff. |
| Architecture trigger | Does not fire. |
| Native change | `stloader_deferred_cuda` gains `max_chunk_size` in the header, definition and binding. A file-scope `host_buffers[STLOADER_THREADS]`; each worker allocates its slot with `cudaMallocHost` on first use and reuses it; the per-job `malloc`/`free` are gone; `cudaMemcpy` becomes `cudaMemcpyAsync` and is still followed by `cudaDeviceSynchronize()`; `stloader_close_file` frees the slots. Correct. |
| Python change | `MAX_DEFERRED_LOAD_CHUNK` 8 MiB to 2 MiB; both groups sorted by `-bytesize`; the one caller passes the chunk size. Correct. |
| Metrics | `STCMetrics` replaces the two counters; `deferred_tensors` and `bytes_loaded` are incremented in `get_tensor` when the request is queued, `total_chunks`, `deferred_passes` and the flush time in `end_deferred_load`; `abort_deferred_load` rolls nothing back; bandwidth divides by `1024**3` and is labelled GB. `-lm` prints `config.stc.metrics`. Correct. |
| Execution | Recorded output: 2,097,152; 16,777,216; 67,108,864; one element uncovered for 1, 3 and 1,048,577 elements, none for 2. Matches the prose. |
| Finding `metrics-wrapper-compatibility` | Correct. At the task, `Model.get_load_metrics` (`model.py` 371) and `VariantSafetensorsCollection.get_metrics` (`safetensors.py` 531) still call `stc.get_metrics()`, which `SafetensorsCollection` no longer has. No in-tree caller of `get_load_metrics`. Suspected is right. |
| Finding `inherited-bf16-odd-tail` | Correct, and correctly described as carried over: `stloader.cu` is not in the diff, and 2 MiB is still an even number of elements. Same identity as 119's `deferred-bf16-odd-tail`; do not open a second ledger record. |

## Ledger candidates (reviewer-only; never to a teacher)

`exllamav3-variant-collection-loader-api--r001`, `exllamav3-sliced-fp16-padding-target--r001` and
`exllamav3-fused-fp32-weight-conversion--r001` state my 119 findings accurately, with the right conditions and limits
(public `st_variants` with no in-tree caller; intermediate size above 55,296 and quantized slices unaffected; float32
only, BF16 unaffected), status suspected, introduced at `647bb7d5`, no execution or fix claimed. Accepted. The
validator limitation for reviewer origins stands as ruled at 114.

None of the three is fixed by this commit: the eager branches of `get_tensor`, `Linear.load_fp16` and the variant
class are untouched. This commit adds two more places where the variant class falls behind: its `get_metrics` (the
entry's finding) and `-lm`, which reads `config.stc.metrics`, an attribute the variant class does not have.

## Reviewer-only notes (never to a teacher)

- The staging buffers are process-global and are freed whenever any file's handles are closed, not when the last user
  finishes. Two collections loading on different threads would share and could free each other's buffers. The entry's
  limits mention concurrent collections as unmeasured. No in-tree code does this.
- `cudaMallocHost` is unchecked; on failure the worker reads into a null pointer and reports an I/O error.

## Not verified

- Any compilation or execution.

## Must fix before canonical use

None for this entry.

## Follow-ups

1. Ledger, when next revised: add `8d347764` to the affected revisions of the three accepted records and of the
   odd-tail record; add the `-lm` and `get_metrics` gaps to the variant record or link the entry's finding to it.

## Next

1. Record this approval.
2. Continue the walk at commit 121.
