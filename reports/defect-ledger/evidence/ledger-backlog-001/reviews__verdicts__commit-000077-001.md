# Verdict: commit-000077-001

Reviewer: Fable (independent reviewer; file mailbox)
Run: `.teacher/runs/commit-000077-001`
Packet: `.teacher/retrieval/000077-001`
Upstream: `1f5a43fc72f3c45d6db757c7907d4793ec88f026` "Fix docstring and import"
Request: `reviews/requests/commit-000077-001.md`
Reviewed: 2026-11-14, working tree on top of `d0a2d08`, machine `exdev-314`

## Decision

**APPROVED for ancestor retrieval only.** Canonical and training remain false.

A re-export and a docstring correction, described accurately. Every statement I checked is true.

## Artifacts reviewed (sha256)

All hashes in the request match the files on disk.

## Run checks

| Check | Result |
|---|---|
| Run integrity | 13 of 13 ledger entries match the transcript, none uncited; final message equals the annotation; Markdown equals the render; full review; 39 of 39 implementation hashes; exactly 76 strict-ancestor entries; 1,128 blobs hash to their names; no evidence timestamp after the cutoff. |
| Replay | 13 of 13 recorded tool calls identical. |
| Unassisted | Standing instructions byte-identical to 76/001's. |
| No hindsight | No blob in the packet contains `reviews/verdicts` or a defect-ledger path. |
| Catalog | GitHub: open at the cutoff are 1, 4, 7, 10, 14, 15, 19. Matches the seven open rows. |
| Diff claims | `exllamav3/__init__.py` adds `CacheLayer_quant` to the existing `.cache` import; the `Cache` docstring replaces the `CacheLayer_q4, CacheLayer_q6` wording and adds `k_bits` and `v_bits`. Nothing else changes. |
| Parent-tree claims | `exllamav3/cache/__init__.py` already imported `CacheLayer_quant`, so the package import did not fail before. `Cache.__init__` defaults `layer_type` to `CacheLayer_fp16` and forwards `**kwargs` to each layer. `CacheLayer_quant` takes both bit counts as required arguments, asserts 2 to 8 for each, and sizes the key and value tensors from them separately. Correct. |
| Finding | `inherited-detach-diagnostic`: the assertion message in `detach_from_model` is unchanged by this commit. Same defect as ledger `exllamav3-cache-detach-count-diagnostic`; suspected and inherited are the right labels. |

## Not verified

- Any import or cache operation. The entry says none was run.

## Must fix before canonical use

None.

## Follow-ups

- The finding is another observation on `exllamav3-cache-detach-count-diagnostic`, not a new defect.

## Next

1. Record this approval.
2. Continue the walk at commit 78.
