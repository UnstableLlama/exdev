# 4d82aab28eb526fb387a12f1d190af6fd875b999


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/4d82aab28eb526fb387a12f1d190af6fd875b999) · [Evidence ledger](draft.json)

Adds optional weighted GPU tile splitting and skips empty-device work, while preserving the existing asynchronous transfer path. Independent rounding can produce a negative final share.

- [User-weighted multi-GPU tile allocation](#quantizer)

## Problem

Multi-GPU tile quantization previously divided work equally, apart from a remainder assigned to the last device; users could not specify relative shares. [source; call_45d0c7d750984088b7805e6ff191c1d9]

## Reasoning

The change threads optional integer device ratios from conversion arguments into the existing asynchronous tile distributor rather than changing the quantization kernel. [source; call_9e66790884f944c3b9b960961924a09f, call_45d0c7d750984088b7805e6ff191c1d9]

## Impact

Users can assign unequal tile shares while retaining equal splitting when ratios are omitted. Single-device execution still bypasses the multi-GPU splitter. [source; call_45d0c7d750984088b7805e6ff191c1d9, call_ae7dc3dcddc54416ba869c0bdc2a6e66]

<a id="quantizer"></a>

## User-weighted multi-GPU tile allocation

Conversion adds -dr/--device_ratios, defaulting to an empty string. main parses a supplied comma-separated list as integers, asserts that its length matches --devices, and passes it through quant_args; otherwise it passes None. Parent-tree searches found neither device_ratios nor the near spelling device_ratio. [source; call_9e66790884f944c3b9b960961924a09f, call_c335d6451a4b43629a13dd326d5163aa, call_ef968921332c4893a686e693a22c002e]

For N tiles and ratios r, quantize_tiles_multigpu computes N*r/sum(r), rounds each share to a multiple of 16 tiles, then assigns the entire rounding discrepancy to the last share. Each tile contains 256 values. This preserves the total tile count but neither exact proportions nor necessarily nonnegative shares. [source; call_45d0c7d750984088b7805e6ff191c1d9, call_ae7dc3dcddc54416ba869c0bdc2a6e66]

A scalar transcription produced shares [64, 64, 128] for 256 tiles with ratios [2, 2, 4], and [0, 256] with ratios [0, 1]. [execution; call_58f03df754cd48a785f29662e9dca6af]

Input, reconstructed tiles, and indices use matching pinned-host slices. Positive shares are copied to their selected GPUs, quantized with cached scratch buffers, and copied back. The new guard skips those operations for empty shares, but completion events remain outside the guard; gathering still returns results to the first device. [source; call_45d0c7d750984088b7805e6ff191c1d9, call_ae7dc3dcddc54416ba869c0bdc2a6e66]

The inspected direct callers are ldlq and the nested test_scale in g_scale_gss, so the same allocation policy applies to feedback quantization and scale-search trials. LDLQ feedback remains on the first device. The separate synchronous helper is unchanged and still splits equally. [source; call_0a3457b688c44d849e4f0cb00e0ea776, call_ae7dc3dcddc54416ba869c0bdc2a6e66]

## Authoring-time findings — pending review

### negative-final-share (suspected; defect)

Independent rounding can overallocate earlier devices and leave a negative final split even with positive ratios.

Trigger: A multi-GPU call with 32 tiles and device_ratios=[3,3,3,1]. LDLQ constructs 32 tiles per call when size_n is 512.

Expected: Produce nonnegative device shares totaling 32 tiles.

Actual: The allocation arithmetic produces [16,16,16,-16] and passes it to torch.split before the positive-share guard. The guard therefore does not repair the invalid partition.

Locations: 4d82aab28eb526fb387a12f1d190af6fd875b999:exllamav3/modules/quant/exl3_lib/quantize.py — quantize_tiles_multigpu

Source evidence: call_45d0c7d750984088b7805e6ff191c1d9, call_0a3457b688c44d849e4f0cb00e0ea776, call_ae7dc3dcddc54416ba869c0bdc2a6e66

scalar_transcription: Executed the new share formula with 32 tiles and four positive ratios, obtaining a negative final share. [call_58f03df754cd48a785f29662e9dca6af]. Limits: No PyTorch or GPU execution; the exact library exception was not observed.

source_inspection: Whole-parent-tree caller search identifies LDLQ and scale-search trials as direct consumers. LDLQ uses size_n/16 tiles; actual model availability for the illustrative width was not established. [call_0a3457b688c44d849e4f0cb00e0ea776, call_ae7dc3dcddc54416ba869c0bdc2a6e66]. Limits: Reach is conditional on tile count and ratios, not every conversion.

## Uncertainty and limits

No CUDA kernels, PyTorch splitting, or end-to-end conversion were executed; the computation checks only transcribed Python allocation arithmetic.

The source establishes 16-tile rounding granularity but does not explain why that granularity was chosen. Performance improvements are unmeasured.
