# Verdict: commit-000140-001

Reviewer: Fable (independent reviewer; file mailbox)
Run: `.teacher/runs/commit-000140-001`
Packet: `.teacher/retrieval/000140-001`
Upstream: `c6aa83f7e5a5e735c079d41244cbc704eda7e54e` "Use deferred loader for single device load"
Request: `reviews/requests/commit-000140-001.md`
Reviewed: 2026-11-14, working tree on top of `d980d21`, machine `exdev-314`

## Decision

**APPROVED for ancestor retrieval only.** Canonical and training remain false.

Every statement I checked is true and the finding is correct as an inherited one. The entry follows the five new
lines into the loader, the eligibility rule and the native converter, which is more than the diff asks for. It
compared the new code with the autosplit path for what they share and missed the one thing they do not share:
autosplit aborts the deferred state when a load fails, and the new code does not (reviewer section, follow-up 2).

Both ledger candidates are **accepted**.

## Artifacts reviewed (sha256)

All eighteen hashes in the request match the files on disk.

## Run checks

| Check | Result |
|---|---|
| Run integrity | 17 of 17 ledger entries match the transcript, none uncited; final message equals the annotation; Markdown equals the render; full review; 42 of 42 implementation hashes; exactly 139 strict-ancestor entries; 1,989 blobs hash to their names; no evidence timestamp after the cutoff. |
| Replay | 17 of 17 recorded tool calls identical, including the `run` call. |
| Unassisted | Standing instructions byte-identical to 139/001's. |
| No hindsight | No blob in the packet contains `reviews/verdicts` or a defect-ledger path. |
| Cutoff | 2025-05-11T13:35:09Z. Issue 33 is a closed row here (closed 2025-05-07, reopened on the 13th). The snapshot the session read ends with the comment of 2025-05-07T09:02:23Z; the next one on GitHub is from 13 May. The "too many open files" explanation is in the comments of 7 May, so it is legitimately visible at this position. Correct. |
| Catalog | Thirteen open rows, as at 139. Two closed rows, issues 33 and 19. |
| Architecture trigger | Does not fire. |
| The change | In `Model._load_single`: `defer = module.can_defer_load()`; `begin_deferred_load()` before `module.load(...)` and `end_deferred_load()` after it when `defer` is true. Five added lines, nothing else. The CPU-preferred device choice is unchanged. Correct. |
| Selection | `load_gen` calls `_load_single` when `device is not None`; autosplit already had the same bracket. Correct. |
| Eligibility | `Module.can_defer_load` is true for a leaf and otherwise requires every child; `Linear` opts out when sliced; `GatedMLP` when it has more than one slice. Correct. |
| Immediate reads | `no_defer = True` on the fused FP16 weight and bias reads and on the packed `su`/`sv` reads. Correct. |
| Loader | Only `mt_fread` in deferred mode without `no_defer` becomes `defer`; the destination is allocated at once and a temporary is added for transpose, float-to-half or padding. Correct. |
| Flush | Grouped by CPU/CUDA and filename, sorted by descending byte size, cut into jobs of at most `MAX_DEFERRED_LOAD_CHUNK = 2*1024**2` bytes; temporaries are transposed and copied into the unpadded region afterwards; the mode and the list are cleared at the end. Correct. |
| Converter | `inplace_bf16_to_fp16_cuda` launches for `numel / 2` pairs. Correct. |
| Execution | Recorded output: 2 elements fully covered; 3 elements leave 1; 1,048,577 elements split into chunks of 2,097,152 and 2 bytes and leave 1. Matches the prose. |
| Finding `inherited-deferred-bf16-tail` | Correct, and correctly presented as the 119 defect with wider reach, not a new one. Suspected is right; no checkpoint with an odd-sized BF16 tensor was shown. |
| Ledger `all-expert-fused-shape--r001` | Accepted as drafted; introduced `6fc153d7`. |
| Ledger `block-sparse-fused-intermediate-dtype--r001` | Accepted. Reviewer observation, conditional on the caller, no execution claimed, excluded from historical context and training. |

## Reviewer-only notes (never to a teacher)

All by source reading; nothing was run.

- **No abort on failure (mine; introduced here).** The autosplit path wraps its bracket in `try` and calls
  `abort_deferred_load()` in the handler. `_load_single` has no handler. If `module.load` or the flush raises
  (running out of memory on the one device is the ordinary case), the collection stays in deferred mode with its
  pending list. A second load attempt with the same configuration then fails at `assert not self.deferred_mode`
  in `begin_deferred_load`, and any `get_tensor` call in between is silently queued instead of read.
- **Variant collections.** `VariantSafetensorsCollection` still has no `begin_deferred_load` or
  `end_deferred_load` (my 119 finding, record `exllamav3-variant-collection-loader-api`). Autosplit already
  reached that; from this commit explicit-device loading reaches it too.
- **The BF16 tail is not in the ledger.** The 119 finding `deferred-bf16-odd-tail` was approved then and never
  filed; no record mentions it.
- My 119 verdict described the flush as sorted by offset with 8 MiB jobs. At this parent it is descending size and
  2 MiB, as the entry says. I have not gone back to see whether 119 differed or I misread it.

## Not verified

- Any model load, and throughput or memory effects.

## Must fix before canonical use

None for this entry.

## Follow-ups

1. Ledger: file the BF16 odd-tail record: introduced at `647bb7d5` (119), with `c6aa83f7` as affected and the
   wider reach. One identity for the 119 and 140 findings.
2. Ledger: a reviewer-observation record for the missing abort in `_load_single`, introduced at `c6aa83f7`.
3. Ledger: add `c6aa83f7` to the affected revisions of `exllamav3-variant-collection-loader-api`.
4. The remaining older ledger revisions are still owed.

## Next

1. Record this approval and the two ledger acceptances.
2. Continue the walk at commit 141.
