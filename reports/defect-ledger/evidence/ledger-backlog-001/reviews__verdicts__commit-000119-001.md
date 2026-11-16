# Verdict: commit-000119-001

Reviewer: Fable (independent reviewer; file mailbox)
Run: `.teacher/runs/commit-000119-001`
Packet: `.teacher/retrieval/000119-001`
Upstream: `647bb7d549b8485ad052ac0650148bd35fcee6d4` "Add deferred loader"
Request: `reviews/requests/commit-000119-001.md`
Reviewed: 2026-11-14, working tree on top of `d0a2d08`, machine `exdev-314`

## Decision

**APPROVED for ancestor retrieval only.** Canonical and training remain false.

Every statement I checked is true, and the entry's one finding (`deferred-bf16-odd-tail`) is correct. As a description
of what the deferred loader is and how it is wired, the entry is accurate and useful to later readers.

It is not complete. The commit also moves transposition, padding and float-to-half conversion out of the modules and
into `get_tensor`, and that move breaks three eager paths the entry does not examine. The entry's limits say that
compatibility across "fused-weight paths, sliced loading and alternate collection implementations was not
established"; all three are in fact broken at this commit, by source. They are listed below as reviewer-only findings
and are required before canonical use.

## Artifacts reviewed (sha256)

All twelve hashes in the request match the files on disk.

## Run checks

| Check | Result |
|---|---|
| Run integrity | 13 of 13 ledger entries match the transcript, none uncited; final message equals the annotation; Markdown equals the render; full review; 41 of 41 implementation hashes; exactly 118 strict-ancestor entries; 1,738 blobs hash to their names; no evidence timestamp after the cutoff. |
| Replay | 13 of 13 recorded tool calls identical, including the `run` call and the ancestor search. |
| Unassisted | Standing instructions byte-identical to 118/001's. |
| No hindsight | No blob in the packet contains `reviews/verdicts` or a defect-ledger path. |
| Catalog | GitHub: open at the cutoff are 1, 4, 7, 10, 14, 22, 24, 25, 26, 27, 28, 29, 31. Matches the thirteen open rows. |
| Architecture trigger | Does not fire. |
| Task read | One `git_show` of 33,712 bytes, not truncated, covering all fourteen sections. |
| Lifecycle | `begin_deferred_load` / `end_deferred_load` / `abort_deferred_load` on `SafetensorsCollection`; only `mt_fread` switches to `defer`, and only when `deferred_mode and not no_defer`. The automatic-split loop brackets `module.load` when `module.can_defer_load()` and flushes before the dummy forward; the `except` calls `abort_deferred_load()` first. `_load_single` is not bracketed. Correct. |
| Deferred `get_tensor` | Final tensor allocated at once (`zeros` when padded, `empty` otherwise); a temporary when transposing, padding or converting float32; record appended with offset, size, flags and device. Correct. |
| Flush | Grouped by CPU/CUDA and filename, sorted by offset, cut into jobs of at most `8*1024**2` bytes; after the native call Python transposes the temporary and copies it into the unpadded region, which also performs the float-to-half conversion. `fp32_to_fp16` (and `cuda`) in the native job are never read. Correct. |
| Native workers | Strided job indices per worker with that worker's handle; CPU reads straight into the destination and converts BF16 in place; CUDA `malloc`s a host buffer per job, `cudaMemcpy`s, synchronises, then launches the conversion. `pread` on Linux, seek and `fread` otherwise. `STLOADER_THREADS` 5 to 8. Correct. |
| Eligibility | `Module.can_defer_load` is true for leaves and `all(...)` over `self.modules` otherwise; `Linear` refuses when `is_sliced`; `GatedMLP` when `num_slices > 1`. `Linear` now defaults omitted `full_*` to its padded sizes and omitted offsets to 0 before computing `is_sliced`. Correct. |
| Constructor safeguards | `LayerNorm` builds its float32 copies lazily; `su`/`sv` and the fused FP16 weight and bias pass `no_defer = True`. `LinearEXL3.__init__` otherwise reads only dtypes and shapes of what it is given. `Embedding` and `RMSNorm` wrap the tensor in a `Parameter` without copying. Correct. |
| FP16 linear | Ordinary weights are requested with `float2half`, `transpose` and `pad_to = (in_features, out_features)`; `LinearFP16` stores what it is given; `get_tensors` still returns `weight.T`; `forward` keeps the input's leading dimensions. Correct. |
| Execution | Recorded output: 8,388,608 bytes per chunk, 67,108,864 for eight; one element uncovered for 1, 3, 2,049 and 4,194,305 elements, none for 2; `0x3f80` read as binary16 is 1.875. Matches the prose. |
| Finding `deferred-bf16-odd-tail` | Correct. `inplace_bf16_to_fp16_cuda` launches `CEIL_DIVIDE(numel / 2, 1024)` blocks over `numel / 2` pairs and nothing handles a last odd element; a one-element final chunk asks for zero blocks. The CPU routine loops over every element, so only CUDA is affected. Chunks are 8 MiB, an even number of elements, so only a tensor's last chunk can be odd. Suspected is the right status. |

## Reviewer-only findings (never to a teacher)

All three are from source inspection at the task commit. Nothing was executed.

1. **Variant collection no longer usable.** `VariantSafetensorsCollection.get_tensor` still has the four-argument
   signature (`key, device, optional, allow_bf16`) and the class has no `begin_deferred_load`, `end_deferred_load` or
   `abort_deferred_load`. `Embedding`, `RMSNorm`, `LayerNorm` and `Linear` now pass `float2half = True` (and more), so
   any load through a config built with `st_variants` raises `TypeError`; on the automatic-split path
   `self.config.stc.begin_deferred_load()` raises `AttributeError` first. No caller inside the repository passes
   `st_variants`; it is a public `Config` keyword.
2. **Sliced FP16 load: padding target smaller than the tensor.** A truly sliced `Linear` (a `GatedMLP` with
   `intermediate_size > MAX_MLP_INTERMEDIATE`, 55,296) loads the full checkpoint tensor through its `alt_key` with
   `pad_to = (self.in_features, self.out_features)`, the slice's sizes. The eager path does
   `padded = zeros(pad_to); padded[slices of tensor.shape].copy_(tensor)`: the destination view is clamped to the
   slice size and the source is the full tensor, so `copy_` cannot broadcast. `LinearFP16`'s own slicing (which
   expects the full tensor) is never reached. Affects loading an unquantized model with such an MLP, that is,
   converting it; quantized slices load through `load_exl3` and are unaffected. No supported checkpoint with an MLP
   that wide was identified.
3. **Fused FP32 weights are no longer converted to half.** `LinearFP16.__init__` lost
   `if weight.dtype == torch.float: weight = weight.to(torch.half)`. The ordinary path compensates with
   `float2half = True`; the fused path (`fkey`, used for fused q/k/v and fused gate/up) calls `get_tensor` without
   it. A float32 fused checkpoint therefore reaches `ext.hgemm`, which requires `kHalf` for the weight. BF16 fused
   checkpoints are converted by the loader's default and are unaffected.

Smaller, same area: `Linear.pad_out` now builds a `(in, out)` target, but its only remaining 2-D caller is the fused
path, which still holds the weight as `(out, in)` at that point. It returns early when no padding is needed, so this
matters only for a fused layer whose sizes are not multiples of 128. And `load_exl3` still loads `bias` deferred
while `LinearEXL3.__init__` converts a float32 bias at once; EXL3 biases are written as half, so this is latent.

## Not verified

- Any compilation or execution, including the three findings above.
- Stream ordering between the BF16 kernel launched on the worker thread and later PyTorch work.
- That raising through `TORCH_CHECK` inside `Py_BEGIN_ALLOW_THREADS` is safe on I/O failure; the eager reader at the
  parent has the same pattern.

## Must fix before canonical use

1. A canonical entry must cover the eager-path consequences of moving the transforms into `get_tensor`: the variant
   collection, sliced FP16 loading and fused FP32 weights (findings 1 to 3).

## Follow-ups

1. Ledger: file three reviewer-origin candidates from findings 1 to 3 (suspected, source inspection, introduced at
   `647bb7d5`), excluded from historical context and training like the top-p record. Send them with the next request.
2. Ledger: `deferred-bf16-odd-tail` is approved as drafted.

## Next

1. Record this approval.
2. Continue the walk at commit 120.
