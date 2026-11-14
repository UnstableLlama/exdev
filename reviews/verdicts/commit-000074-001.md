# Verdict: commit-000074-001

Reviewer: Fable (independent reviewer; file mailbox)
Run: `.teacher/runs/commit-000074-001`
Packet: `.teacher/retrieval/000074-001`
Upstream: `cf848114852240a51fb6b9e77c686051c39302b2` "Add cache quantization"
Request: `reviews/requests/commit-000074-001.md`
Reviewed: 2026-11-13, working tree on top of `41010aa`

## Decision

**APPROVED for ancestor retrieval only.** Unassisted. The walk may continue from commit 75 (after 39/006, per the
commit 39 decision).

Canonical and training remain false.

Not thin. A 1,156-line feature, and the entry gives the design (compress around the unchanged FP16 attention call), the
storage format with its real cost, the paging rules, the limits of the new test, and the point a reader would otherwise
get wrong: every quantized `get_kv` allocates full-capacity FP16 temporaries, so stored size and peak memory are
different things. It read issue 1 and linked it as inference.

## Artifacts reviewed (sha256)

- draft.json: `e23f7e20dcf7784059a426882303c3ae2dfcf51dc52d9a432817ebf103c79686`
- draft.md: `c796687b35dacd18ac0a4c7309f5ba5d74994bf4b7ae7994598022012b10fca6`
- raw-transcript.json: `522056bd30ce9b733f7b75e811448cf4f5d9bb1d13eed908567ccdfa2c30275b`
- provenance.json: `d6dbf296c10717a233ad8659d4b222637b15915cfb2b5c39b9f72f8858bac163`
- coverage.json: `dd4adeeb8de7a3b4ec8b839a26d88c36befcdd5205ecb998525283f4153b0f4f`
- packet manifest (on disk): `00bf9e8f96c3a0de3b744ee36a42176092c41104f9576b8ef9fe0d97a7ba0174`
- unreferenced bundle: `38411298127aaa2f9d5b264f4d2e5ddea0d8e84c0f386170bbe24e8f3f2eb8fa`

All match the request.

## Run checks

| Check | Result |
|---|---|
| Run integrity | 27 of 27 ledger entries match the transcript, none uncited; final message equals the annotation; Markdown equals the render; assessment is full review; 39 of 39 implementation hashes match; exactly 73 strict-ancestor entries; all 1073 blobs hash to their names; no content timestamp after the cutoff. |
| Diff coverage | 13 of 14 sections read. The one unread section is `doc/cq_humaneval.png`, a binary. The entry says it did not interpret the image and infers nothing from it. Accepted: there is nothing a text tool could have read. |
| Unassisted | No coverage, no assistance flag. Standing instructions byte-identical to 73/001. |
| Opening context | Message, author, parent `fc5b39c2` (commit 73) and task SHA match Git. Cutoff 2025-04-22T21:52:33+02:00, five minutes after commit 73. |
| Catalogs | Open: seven rows as at 73, including issue 1 "Cache Quantization Strategy", which was read. Closed: one row, issue 16, matched on many generic terms; read and correctly reported as unrelated. |
| Python layer | Verified. `Cache` forwards keyword arguments to each layer; `get_layer` and the new `update_layer` pass sequence lengths and the block table; the FP16 layer returns its tensors and `update_kv` does nothing; the quantized layer allocates two `torch.empty` FP16 tensors of the full cache shape on every `get_kv`, decodes into them, and encodes `length` new tokens in `update_kv`. `attn.py` calls `update_layer` right after `flash_attn_with_kvcache`. `copy_page` copies codes and both scale arrays and asserts only the code shapes. |
| Kernels | Verified. 32-value warp Hadamard, factor 0.17678, block maximum stored as a half scale, `lrintf` then clamp to `[0, 2^b - 1]` after the offset (so the signed range is `[-2^(b-1), 2^(b-1) - 1]`), one `__ballot_sync` word per bit; decode reverses it. Paged encode starts at `cache_seqlens` and covers `seq_len` tokens through the block table; paged decode returns early for positions at or beyond `cache_seqlens`. Divisibility checks as stated. |
| Storage arithmetic | `b` int32 words and one half per 32 values is `b + 0.5` bits per value. Correct. |
| CLI | Verified. `-cq` takes one number or `k,v`; three or more raises; without it the cache is built with `CacheLayer_fp16` explicitly. The 2 to 8 assertion is in the layer constructor. |
| Test scope | Verified. `tests/test_kv_quant.py` lists `cuda:1`, 8-bit only (its own comment says it tests paging, not accuracy), permutes the block table, appends five tokens, tolerances 0.08 and 0.01. |
| Execution claim | Replayed the `run` call: identical output. Arithmetic and `struct` only. |
| Inherited finding | `inherited-detach-diagnostic` is carried from the entry for `4fa0e686`, which the run read; the line is untouched here. Existing defect, no new identity. |

## Finding `zero-block-scale`

The source facts are right: `1e-10` is added to the block maximum, the sum is rounded to half, half cannot hold it, and
an all-zero block then divides zero by zero.

What the entry leaves "not established" can be settled from the same file. The stored scale is that same half zero, and
`dequant_block` multiplies every decoded level by it before the rotation. Whatever integer the undefined conversion
yields, it is clamped to a valid code, and a valid code times a zero scale is zero. So an all-zero block decodes to
zeros. The floor does not do its job, and the result is still correct.

Keep the status at suspected. If it goes to the ledger, record it as an ineffective guard with no wrong output shown,
not as data loss.

## Not verified

- Nothing compiled or run on a GPU. Accuracy at any bitrate, peak memory and speed are unmeasured, as the entry says.

## Must fix before canonical use

Reviewer-only.

1. The figure is the only quality evidence the commit carries and no entry can describe it. A canonical entry needs a
   human or an image-capable pass to say what `cq_humaneval.png` shows.
2. The README hunk (cache quantization removed from the two to-do lists) is read and not mentioned.
3. The launch geometry of the paged encoder uses `ceil(warps / ceil(warps / 32))` warps per block. When the number of
   32-value groups per token is above 32 and not a multiple of the block count, the last block of a token runs one or
   more warps past the token. I did not work out whether any supported model has such a width; the test's dimensions
   would show it only if one of them does. Worth a look by whoever next reads this file.

## Follow-ups

- Validation marks a run incomplete when a binary section is unread. A binary section should be recorded as unreadable
  so that "incomplete" keeps its meaning.

## Next

Record this approval. Then 39/006 per `commit-000039-deci-references.decision.md`, then continue from commit 75.
