# e9a3b6a9256fc59f888b80a7d4a58883954b39de


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/e9a3b6a9256fc59f888b80a7d4a58883954b39de) · [Evidence ledger](draft.json)

Adds native FP32 GEMM outputs and FP32 Hadamard processing, fuses output scales into Hadamard, and propagates output dtype preferences through linear and gated-MLP construction.

- [Selectable GEMM output precision and fused Hadamard scales](#modules)

## Problem

Linear outputs previously passed through FP16 GEMM storage before any requested output conversion. EXL3 output-channel scaling also required a separate multiplication when unpacked scales were used. [source; call_4d54b1ef030f4ff1bfa2fd369c707130, call_439deead9ba643e5936176dd3628e156]

## Reasoning

The change selects output precision before GEMM, carries FP32 through EXL3 reduction and output Hadamard, and folds output-channel multiplication into that Hadamard kernel rather than into GEMM. [source; call_ba7578106be44284803c00cdd2391d16, call_d99e4c7393a84d179f22f1284462da03, call_439deead9ba643e5936176dd3628e156]

## Impact

FP32 output avoids the explicit half conversion at GEMM output and EXL3 partial-result stores, at the cost of larger output storage. This does not introduce FP32 GEMM inputs or establish measured accuracy or speed improvements. [inference; call_656f40f8a97e459cb2839a26b0f64a36, call_e5eb0f24de284ba8bf85a6f669d8e7da, call_ba7578106be44284803c00cdd2391d16]

## Source Notes

Issue #7, “quantizing model: undefined symbol: __cxa_call_terminate,” reports an extension import failure and a reporter-supplied environment workaround. Issue #15, “`cogito-v1-preview-qwen-32B` generates incoherent output for bpw <= 2.5,” discusses quantization regularization. Neither discussion explicitly identifies this change as its fix. [source; call_a684c827cd424a8b9e6862f0c26c5c82, call_ca2bb4bf554143ae913624739d5503ec]

<a id="modules"></a>

## Selectable GEMM output precision and fused Hadamard scales

hgemm retains half inputs and dispatches on the destination dtype. Half output uses cublasHgemm; float output uses cublasGemmEx with CUDA_R_16F inputs, CUDA_R_32F output and CUBLAS_COMPUTE_32F. Both branches reverse operands and use dimensions (n, m, k) for row-major multiplication, with alpha=1 and beta=0. [source; call_656f40f8a97e459cb2839a26b0f64a36]

EXL3 kernel specialization repurposes bit 0x10 from output-Hadamard selection to output precision; the low four bits still select quantization bits. Float output receives float partial-result loads and stores, while half output retains half2 conversion. Fused output Hadamard is disabled, and the native wrapper explicitly rejects non-null sv. [source; call_e5eb0f24de284ba8bf85a6f669d8e7da, call_ba7578106be44284803c00cdd2391d16]

had_r_128 now accepts matching FP16 or FP32 input/output tensors, checking two-dimensional input, matching shapes and a column count divisible by 128. Each 32-thread block handles 128 values: a four-value transform per thread followed by five XOR-shuffle stages across the warp. The multiplier 0.088388347648 approximates 1/sqrt(128), normalizing the transform. [source; call_d99e4c7393a84d179f22f1284462da03, call_210d3dfa337841c49d217cb77b45c0dc]

A scalar transcription of the four-value transform and five shuffle stages recovered a 128-element test vector with maximum error 1.78e-15 after two normalized transforms. The normalization literal differs from 1/sqrt(128) by approximately 3.18e-13. [execution; call_eeaf61cbb70242bc9e34afdfcc5586e2]

Both Hadamard paths consume half pre/post scale vectors. The half path multiplies pre-scales in half, performs the transform in float, rounds back to half and then multiplies post-scales in half. The float path converts scales to float and retains float values throughout. Thus fused scales do not imply identical arithmetic precision between paths. [source; call_d99e4c7393a84d179f22f1284462da03, call_2f4c3663465640a4b4e93c46f766a2ba]

LinearEXL3 normalizes legacy packed signs into unpacked half scales at construction and clears su/sv. Both reconstructed-weight hgemm and direct exl3_gemm now feed a separate in-place output Hadamard with svh post-scaling. The existing default reconstruction threshold remains more than 32 flattened input rows; get_inner_weight_tensor still reconstructs a half matrix. [source; call_439deead9ba643e5936176dd3628e156, call_8b26bb61c2a7402b8aacee41ce520be8]

Linear forwards its optional output dtype through loading and quantization. Both inner implementations allocate the GEMM destination using call-level override, then constructor preference, then torch.half. They return this result directly rather than casting afterward; EXL3 also stops casting the result to the bias dtype before addition. [source; call_9ba8faefcc194483b4b7bd0fc772ab9a, call_439deead9ba643e5936176dd3628e156, call_4d54b1ef030f4ff1bfa2fd369c707130, call_38fbaf0477be472393e5368770ed880e]

GatedMLP adds interm_dtype for gate/up projections and passes its existing out_dtype to down projections. Its unchanged forward loop still applies the selected activation to gate/up outputs before invoking down, so these constructor controls affect intermediate computation rather than merely the final return conversion. [source; call_759d2d99fdda438dbea221bb48da87f1, call_c22214349c7a476cbd470dbaee4f8a76]

## Uncertainty and limits

No CUDA compilation, repository execution, GPU numerical comparison or performance measurement was performed.

The scalar Hadamard check uses Python double precision; it does not reproduce CUDA float rounding, half multiplication, warp execution or memory behavior.

End-to-end compatibility of the new GatedMLP intermediate dtype option with activation kernels and subsequent projections was not established.
