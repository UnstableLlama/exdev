# Verdict: commit-000099-001

Reviewer: Fable (independent reviewer; file mailbox)
Run: `.teacher/runs/commit-000099-001`
Packet: `.teacher/retrieval/000099-001`
Upstream: `6c15b8c40f0d28807006ad65d2c9e31382a352b4` "Improve memory management a little while loading model"
Request: `reviews/requests/commit-000099-001.md`
Reviewed: 2026-11-14, working tree on top of `d0a2d08`, machine `exdev-314`

## Decision

**APPROVED for ancestor retrieval only.** Canonical and training remain false.

Every statement I checked is true. The entry describes the moved cleanup call and the new exception guard exactly, and
does not claim a memory saving that nobody measured.

The ledger record `exllamav3-cohere-qk-normalization--r001` is **accepted as recorded**.

**The walk stays stopped at 99**, as your request says. Position 100 needs the two overdue fixes first; see "Next".

## Artifacts reviewed (sha256)

All hashes in the request match the files on disk.

## Run checks

| Check | Result |
|---|---|
| Run integrity | 15 of 15 ledger entries match the transcript, none uncited; final message equals the annotation; Markdown equals the render; full review; 40 of 40 implementation hashes; exactly 98 strict-ancestor entries; 1,427 blobs hash to their names; no evidence timestamp after the cutoff. |
| Replay | 15 of 15 recorded tool calls identical. |
| Unassisted | Standing instructions byte-identical to 98/001's. |
| No hindsight | No blob in the packet contains `reviews/verdicts` or a defect-ledger path. The string `cohere-qk-normalization` occurs once, in the approved 98/001 draft as the teacher's own finding name, which is expected. |
| Catalog | GitHub: open at the cutoff are 1, 4, 7, 10, 14, 15, 21, 22, 24. Matches the nine open rows. |
| Diff claims | `free_mem()` is removed from the end of `_load_autosplit` and added after `self.config.stc.close()` in `load_gen`, so it now runs for single-device loads too and after the collection is closed. `free_mem` is `gc.collect()` then `torch.cuda.empty_cache()`. In `list_gpu_tensors` only the dictionary branch is wrapped in a bare `try` / `except: pass`. Nothing else changes. Correct. |
| Lifecycle claims | The moved call is still on the success path only, not in a `finally`, and is reached only when the generator is run to exhaustion. Consistent with 76/001. Correct. |
| Finding | `inherited-single-device-progress`: unchanged by this commit; same defect 76/001 records. |

## Ledger record

`exllamav3-cohere-qk-normalization--r001`: accepted. Suspected external compatibility, introduced at `875e503e`, the
teacher's observation from 98/001 plus mine on the same identity, no fix claimed, not eligible for historical context,
training policy not applied.

## Not verified

- The entry's statements about `SafetensorsCollection.close` and `extra_dummy_states`; the reads replay, I did not
  re-read those files.
- Any model load or memory measurement.

## Must fix before canonical use

1. `inherited-single-device-progress` is still classed `behavior_change`; see my note on 76/001.

## Next

1. Record this approval and the ledger acceptance.
2. Before position 100, implement required fixes 1 and 2 from
   `reviews/verdicts/reference-evidence-and-callee-implementation-001.md` (an administrative outcome for a trigger that is
   not a new architecture, with Git rename detection; and deriving the architecture string from the new file when the
   list is empty). Fix 3 is cheap and I would take it in the same change. File an implementation request and wait.
3. Do not author commit 100 until that request is accepted.
