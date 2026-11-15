# 0b2dba5ac5aab77fb9d9aabdda72ceb5befa8b11


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/0b2dba5ac5aab77fb9d9aabdda72ceb5befa8b11) · [Evidence ledger](draft.json)

Adds optional JPEG diagnostics for original and regularized linear weights, using per-tensor clipped color normalization.

- [Optional weight visualization during conversion](#image-dump)

## Problem

Quantization lacked the image-dump hooks added here for inspecting original and regularized weight matrices. [source; call_d27a072e16ad46fdb87ad63789512ef9, call_c0a09fa0c7d54efc8abf5db35a74aaf1]

## Reasoning

The implementation makes visualization opt-in and copies tensors before modifying their display values, separating diagnostic normalization from quantization data. [source; call_d27a072e16ad46fdb87ad63789512ef9, call_fc73f96fd5814137b431daefef80461f]

## Impact

Image dumping introduces CPU copies, color-array construction and synchronous image writes. These support the documentation's qualitative memory, disk-space and latency warnings; their magnitude is not measured. [inference; call_fc73f96fd5814137b431daefef80461f, call_27244c56ff9348ad8b2678644b593a7e]

## Source Notes

Issue #7, “quantizing model: undefined symbol: __cxa_call_terminate,” reports a native-extension import failure and the reporter's environment workaround. Its connection here is only inferred from the matching convert.py import line, not evidence that image dumping addresses that failure. [inference; call_2ee456a33d1443c6bbb717693f7b3184, call_edcd1d6ce2004a21b7885a8ded34f20a]

<a id="image-dump"></a>

## Optional weight visualization during conversion

The parser accepts -img and --image_dump. prepare copies the current invocation's flag into image_dump for both new and resumed jobs; prepare_env creates work_dir/images even when dumping is disabled. [source; call_d27a072e16ad46fdb87ad63789512ef9, call_719c3441403b482b9936a877c2991f72]

main dumps loaded Linear quantization targets selected by a truthy qmap and non-null device, before swapping their original weights to CPU. Original images use images/<linear.key>.jpg. A second path, images/<linear.key>.reg.jpg, passes through Linear.convert_exl3 to quantize_exl3, where weight_r is saved after regularize and before ldlq. These are pre-quantization diagnostics, not pictures of reconstructed quantized weights. [source; call_719c3441403b482b9936a877c2991f72, call_d27a072e16ad46fdb87ad63789512ef9, call_fd09eac8f7e34d3ea828517071ea61ed, call_c0a09fa0c7d54efc8abf5db35a74aaf1, call_15e58427e80d410ba8d2349233cb704c]

Both conversion APIs append optional save_reg=None parameters. save_tensor_image imports matplotlib.cm and PIL.Image only when called, detaches and copies its input to CPU float32, clamps to mean ± 3 standard deviations, and normalizes by the resulting six-standard-deviation span plus 1e-8. It applies gnuplot2, drops alpha, multiplies RGB by 255, converts to uint8 and saves the image. [source; call_fd09eac8f7e34d3ea828517071ea61ed, call_c0a09fa0c7d54efc8abf5db35a74aaf1, call_fc73f96fd5814137b431daefef80461f]

A scalar transcription with mean 0 and standard deviation 1 mapped values at or below -3 to 0, the mean to approximately 0.5, and values at or above 3 to approximately 1. A finite constant input with zero standard deviation mapped to 0 because of the denominator epsilon. [execution; call_8240f9545d0a4ff5b11032d26d479b30]

Independent normalization emphasizes each matrix's internal pattern rather than preserving a shared absolute color scale between original and regularized weights. Clipping also deliberately discards outlier magnitude in the visualization. [inference; call_fc73f96fd5814137b431daefef80461f]

## Authoring-time findings — pending review

### documentation-dump-scope (suspected; defect)

The added documentation overstates coverage as “all tensors” and omits the leading -- from the long option.

Trigger: Following the new image-dump option description.

Expected: Documentation names --image_dump and describes images of selected linear weights and their regularized forms.

Actual: The text says “-img / image_dump” and “all tensors,” whereas the parser registers --image_dump and main only dumps its selected Linear quantization targets.

Locations: 0b2dba5ac5aab77fb9d9aabdda72ceb5befa8b11:doc/convert.md — image_dump option description

Source evidence: call_27244c56ff9348ad8b2678644b593a7e, call_d27a072e16ad46fdb87ad63789512ef9, call_719c3441403b482b9936a877c2991f72

source_inspection: Compared the added documentation with the parser registration and the linear-target selection surrounding the image writes. [call_27244c56ff9348ad8b2678644b593a7e, call_d27a072e16ad46fdb87ad63789512ef9, call_719c3441403b482b9936a877c2991f72]. Limits: No CLI invocation or image generation was executed.

## Uncertainty and limits

No repository conversion, GPU operation, matplotlib colormap or Pillow image save was executed. Installed-library compatibility and filesystem behavior remain unverified.

The scalar check uses Python floating-point arithmetic and supplied statistics, not PyTorch float32 reductions or image encoding.
