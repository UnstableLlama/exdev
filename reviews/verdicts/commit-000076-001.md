# Verdict: commit-000076-001

Reviewer: Fable (independent reviewer; file mailbox)
Run: `.teacher/runs/commit-000076-001`
Packet: `.teacher/retrieval/000076-001`
Upstream: `448815bc1cf7b17e714a52fe6f70bcb53da48147` "Add callback to model loader, and load_gen option"
Request: `reviews/requests/commit-000076-001.md`
Reviewed: 2026-11-14, working tree on top of `d0a2d08`, machine `exdev-314`

## Decision

**APPROVED for ancestor retrieval only.** Canonical and training remain false.

Every statement I checked is true, and the entry finds the two things about this change that are easy to miss: the
terminal progress tuple arrives before cleanup, and the explicit-device branch delivers no notifications.

## Artifacts reviewed (sha256)

All hashes in the request match the files on disk.

## Run checks

| Check | Result |
|---|---|
| Run integrity | 11 of 11 ledger entries match the transcript, none uncited; final message equals the annotation; Markdown equals the render; full review; 39 of 39 implementation hashes; exactly 75 strict-ancestor entries; 1,121 blobs hash to their names; no evidence timestamp after the cutoff. |
| Replay | 11 of 11 recorded tool calls identical, including the `run` call. |
| Unassisted | Standing instructions byte-identical to 75/001's. |
| No hindsight | No blob in the packet contains `reviews/verdicts` or a defect-ledger path. |
| Catalog | Cutoff is eight minutes after commit 75's; the same seven rows are open (1, 4, 7, 10, 14, 15, 19), checked against GitHub at 75. |
| Diff claims | `load` becomes `load_gen`; a new `load` forces `generator=False` and exhausts it. `_load_autosplit` calls the callback and optionally yields `(idx, len(modules))` at the top of the per-module loop, outside the inner device-retry loop, then `(len, len)` after the loop. `dummy_state = None`, `unset_memory_fraction`, `free_mem` and `stc.close()` all follow that last yield. The single-device branch still calls the unchanged `_load_single(progressbar, device)`. All as the draft says. |
| Inference-mode note | `@torch.inference_mode` moved to the new `load`; `load_gen` has none. Correct, and labelled untested. |
| Example claims | `examples/loading.py` loads and unloads five times, attaches then detaches a cache, and iterates `load_gen` with plain `for` loops. Correct. |
| Finding | `single-device-progress`: correct at source level. Suspected is the right status. |

## Not verified

- The stress test's device arguments (`cuda:1`, optional `cuda:2`); I confirmed the read replays but did not re-read the file.
- Any execution of the loader.

## Must fix before canonical use

Reviewer-only.

1. `single-device-progress` is classed `behavior_change`. Nothing that worked before changed; a new interface is
   incomplete on one branch. A canonical entry or ledger record should class it accordingly.
2. The `load_gen` docstring added here ends mid-sentence ("Don't specify a callback function when using the"). The
   entry does not mention it.

## Next

1. Record this approval.
2. Continue the walk at commit 77.
