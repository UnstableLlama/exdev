# 08cf8e91ce7b145c20700a055214fa23b6c0b2d9


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/08cf8e91ce7b145c20700a055214fa23b6c0b2d9) · [Evidence ledger](draft.json)

Centralizes CUDA thread sizing, initializes candidate minima explicitly, and adds optional non-CUDA tensor listing alongside comments and a README wording correction.

- [Quantizer cleanup and broader tensor diagnostics](#cleanup)

## Problem

The change combines cleanup with two behavioral edits: optional non-CUDA tensor inspection and explicit initialization of the quantizer's candidate minimum. [source; call_dca7034063eb441b93267758e32a038a, call_99ce30326c154496a089f55780a59fb1]

## Reasoning

A shared NUM_THREADS constant replaces three occurrences of 1024, keeping kernel iteration strides and launch sizing tied to the same value. [source; call_99ce30326c154496a089f55780a59fb1]

## Impact

list_gpu_tensors retains CUDA-only filtering by default; cuda_only=False permits other torch.Tensor devices through the existing size filter. [source; call_dca7034063eb441b93267758e32a038a]

## Source Notes

The README edit only inserts “the” before “EXL3 format”; it does not revise or validate the surrounding performance claims. [source; call_7b8985f4090143d684269698addfe7df]

<a id="cleanup"></a>

## Quantizer cleanup and broader tensor diagnostics

quantize_tiles_kernel processes 256-value tiles. For bit width K, its candidate loop examines 2^K states per outgoing edge, with 65536 >> K edges. The patch initializes min_err to INFINITY and min_in_edge to zero, then updates only on strictly smaller error, replacing unconditional acceptance of candidate zero. [source; call_61d9f810fa1744f796972e8f0780bfd8, call_99ce30326c154496a089f55780a59fb1]

For finite candidate errors, the strict comparison preserves the first minimum on ties. It is not universally equivalent for exceptional values: a scalar transcription selected the later finite value from [NaN, 2] under the new rule, whereas the old rule retained NaN. [execution; call_4a29649c19aa466cb42eaf3f27e9920c, call_99ce30326c154496a089f55780a59fb1]

NUM_THREADS remains 1024. A scalar enumeration verified complete, nonduplicated edge coverage for all dispatched K values 1–8: launches use 1024 threads for K=1–6, 512 for K=7 and 256 for K=8. This checks indexing, not GPU execution. [execution; call_4a29649c19aa466cb42eaf3f27e9920c, call_61d9f810fa1744f796972e8f0780bfd8]

The diagnostic helper searches module globals and thread-frame locals, then follows object attributes, dictionary entries and sequence members. Its new comments explain this existing traversal; the functional extension is the optional device filter. Tensor sizes remain integer byte counts divided by 1024², so the documented megabytes are whole MiB, with a default minimum of one. [source; call_d73fba9ed812460c9ba65abbe3911d41, call_dca7034063eb441b93267758e32a038a]

Collected records remain sorted by descending size and printed in per-device tables. The tabulate import moves from after traversal to the beginning of the helper, rather than becoming a module-level import or a newly declared dependency. [source; call_d73fba9ed812460c9ba65abbe3911d41, call_dca7034063eb441b93267758e32a038a]

## Uncertainty and limits

No CUDA compilation, kernel execution, performance measurement or live tensor traversal was performed.

The scalar comparison check uses Python floating-point values, not CUDA float32 arithmetic; it establishes illustrative selection behavior rather than end-to-end quantizer correctness.
