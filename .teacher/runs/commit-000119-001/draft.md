# 647bb7d549b8485ad052ac0650148bd35fcee6d4


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/647bb7d549b8485ad052ac0650148bd35fcee6d4) · [Evidence ledger](draft.json)

Adds module-scoped deferred loading with batched native reads, loader-side transformations and constructor safeguards. Automatic splitting adopts the lifecycle; an odd-element CUDA BF16 conversion tail remains a suspected defect.

- [Deferred tensor population and module loading](#loading)

## Problem

The existing loader completes each tensor read before returning. Module construction therefore interleaves allocation, individual reads and transformations rather than scheduling a module's tensor reads together. [source; call_c0b96fbd3ac4439caf7386c42aa66048, call_cd17ae4c512a418080fb688927c033f4]

## Reasoning

Deferred loading separates allocation from population: module constructors receive destination tensors immediately, while a subsequent flush reads their contents and performs required transformations. This requires constructors to avoid consuming unfinished tensor values. [source; call_224f301938ae469187458cff3877948c]

Batching reads, sorting them by file offset and moving conversion into the loader plausibly reduce per-tensor overhead. This is an inferred performance rationale, not a measured speedup. [inference; call_224f301938ae469187458cff3877948c, call_cd17ae4c512a418080fb688927c033f4]

## Impact

Automatic device splitting now brackets eligible module loads with begin_deferred_load and end_deferred_load, completing the flush before the dummy forward used for memory sizing. Exceptions clear pending loads before the existing out-of-memory handling. Explicit single-device loading is not similarly bracketed. [source; call_224f301938ae469187458cff3877948c, call_6630d3e98d2e43369ae27dc16b6c877d]

The change also moves ordinary FP16 linear-weight transposition and padding into the loader, and generalizes LinearFP16.forward's output shape from exactly three dimensions to the input's leading dimensions plus out_features. [source; call_224f301938ae469187458cff3877948c, call_ad00af6d0d6c42c8b041aac26dc80cf9]

## Source Notes

Issue #7, “quantizing model: undefined symbol: __cxa_call_terminate,” reports extension import failure; its reporter later describes resolving it by installing a compatible compiler in the Conda environment. Its relationship to this task is only an inferred file overlap: the traceback includes models/model.py. It does not establish a deferred-loader motivation or validation. [inference; call_2b9e83cbacc44ca29cdc7ed1a6f30ad0, call_224f301938ae469187458cff3877948c]

<a id="loading"></a>

## Deferred tensor population and module loading

SafetensorsCollection defaults to immediate loading. While deferred_mode is active, only the mt_fread backend switches to the new defer path, unless no_defer is requested. The Python backend remains immediate. Existing callers can therefore retain eager reads without adopting the new lifecycle. [source; call_c0b96fbd3ac4439caf7386c42aa66048, call_224f301938ae469187458cff3877948c]

A deferred get_tensor allocates the final shape and dtype and retains a record containing file offset, byte count, destination, optional temporary tensor, conversion flags and device. Padding uses a zero-filled final tensor. Transposition, padding or FP32-to-FP16 conversion require a temporary; otherwise the file bytes can target the final allocation directly. [source; call_224f301938ae469187458cff3877948c]

end_deferred_load groups requests by CPU/CUDA and filename, sorts each file's requests by offset, and splits them into jobs of at most 8 MiB. Native workers take strided job indices. After native reads, Python transposes temporary tensors when requested and copies their unpadded region into the final destination; that copy also provides FP32-to-FP16 conversion. The native job's fp32_to_fp16 field is not itself acted on. [source; call_224f301938ae469187458cff3877948c]

The CPU worker reads directly into the supplied pointer and optionally converts BF16 in place. The CUDA worker allocates a host buffer per job, reads into it, selects the target device, copies to the destination, synchronizes and optionally launches BF16 conversion. This is host-staged loading, not GPUDirect. Linux uses pread; the alternative branch uses a worker-specific file handle with seek and fread. [source; call_224f301938ae469187458cff3877948c, call_cd17ae4c512a418080fb688927c033f4]

STLOADER_THREADS increases from five to eight and also governs the existing eager reader and file-handle count. MAX_DEFERRED_LOAD_CHUNK bounds each deferred job at 8 MiB, whereas the existing eager reader retains 512 KiB blocks. The conversion kernel uses 1,024 threads per block, with each thread handling two elements. [source; call_224f301938ae469187458cff3877948c, call_cd17ae4c512a418080fb688927c033f4]

A scalar arithmetic check gives 8,388,608 bytes per deferred chunk and 67,108,864 bytes for eight simultaneous maximum-size host staging buffers. This bounds those worker buffers only, not total process or device memory. [execution; call_2f06887d239a406ebdfa34a455e54be0]

Deferral eligibility propagates recursively through Module.children stored in modules: leaves permit it, while composites require every child to permit it. Linear rejects sliced instances, and GatedMLP rejects multiple slices. Linear now resolves omitted full dimensions to its padded dimensions and omitted slice offsets to zero before determining whether it is sliced. [source; call_224f301938ae469187458cff3877948c, call_c7161dfd51564781bfe6da3bc94b2427]

Constructor-time consumers receive special treatment. LayerNorm creates float32 weight and bias caches lazily during forward instead of copying unfinished values during load. Packed EXL3 su/sv tensors explicitly bypass deferral because LinearEXL3 immediately unpacks their bits. Fused FP16 weights also bypass deferral before slicing. [source; call_224f301938ae469187458cff3877948c, call_628907f1de6b4e7eaca62b0061497e4e, call_c7161dfd51564781bfe6da3bc94b2427]

Embedding, RMSNorm and LayerNorm delegate float32-to-half conversion to get_tensor. Ordinary FP16 linears request transposed, padded weights from the loader; LinearFP16 consequently stores the supplied orientation rather than transposing it again. Its export path still transposes back to checkpoint orientation. [source; call_224f301938ae469187458cff3877948c, call_ad00af6d0d6c42c8b041aac26dc80cf9]

## Authoring-time findings — pending review

### deferred-bf16-odd-tail (suspected; defect)

The new CUDA BF16 conversion covers pairs only and has no scalar tail, leaving the final element of an odd-length deferred BF16 tensor unconverted.

Trigger: A file-backed BF16 tensor with an odd element count is loaded to CUDA through the deferred path with allow_bf16 false.

Expected: Every BF16 element should be converted to FP16 before the destination is consumed.

Actual: inplace_bf16_to_fp16_cuda passes numel / 2 to a kernel that converts two elements per thread. An odd final element retains BF16 bits in storage treated as FP16. A one-element final chunk also computes zero launch blocks; its runtime handling was not tested.

Locations: 647bb7d549b8485ad052ac0650148bd35fcee6d4:exllamav3/exllamav3_ext/stloader.cu — inplace_bf16_to_fp16_cuda, 647bb7d549b8485ad052ac0650148bd35fcee6d4:exllamav3/exllamav3_ext/stloader.cpp — stloader_deferred_cuda

Source evidence: call_224f301938ae469187458cff3877948c, call_166786c681a8427990778ecae94733af, call_c177abcc1f4a4b86a007970300fcb5bb, call_6630d3e98d2e43369ae27dc16b6c877d

source_inspection: The parent-tree search finds no pre-existing conversion helper. The task introduces its direct caller in stloader_deferred_cuda, reached through end_deferred_load. Parent get_tensor call sites include embedding, normalization and linear loading; automatic splitting supplies the new broader lifecycle. The finding is conditional on odd-sized BF16 CUDA data, not a claim that every model reaches it. [call_166786c681a8427990778ecae94733af, call_c177abcc1f4a4b86a007970300fcb5bb, call_224f301938ae469187458cff3877948c, call_6630d3e98d2e43369ae27dc16b6c877d]. Limits: No affected model checkpoint or GPU execution was demonstrated.

scalar_transcription: Python modeled the inspected chunking and pair-count expressions. Counts 1, 3, 2049 and 4194305 each leave one element uncovered, while 2 leaves none. Interpreting the illustrative BF16-one bit pattern 0x3f80 as binary16 yields 1.875 instead of 1.0. [call_224f301938ae469187458cff3877948c, call_2f06887d239a406ebdfa34a455e54be0]. Limits: This checks finite integer indexing and bit interpretation, not the repository kernel, CUDA launch behavior or floating-point conversion implementation.

## Uncertainty and limits

No repository implementation, native extension or GPU kernel was executed. The Python check models chunk arithmetic and pair coverage only; it does not establish CUDA stream ordering, conversion rounding, error handling or runtime correctness.

Loading throughput and peak device memory were not measured. Temporary tensors for transposition, padding and FP32 conversion can coexist with final destinations.

Compatibility across all model shapes, fused-weight paths, sliced loading and alternate collection implementations was not established.
