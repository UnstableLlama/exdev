# e9a3b6a9256fc59f888b80a7d4a58883954b39de


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/e9a3b6a9256fc59f888b80a7d4a58883954b39de) · [Evidence ledger](draft.json)

Adds selectable FP32 linear outputs and FP32 Hadamard transforms, unifies EXL3 scales, and disables fused output Hadamard in GEMM. Shipped models retain FP16 linear outputs; the new FP32 MLP-intermediate setting is not supported end-to-end.

- [Selectable linear output precision and scale-fused Hadamard transforms](#modules)

## Problem

Both linear implementations previously allocated FP16 GEMM outputs and converted afterward. Requesting FP32 therefore did not preserve an FP32 GEMM result. [source; call_13eb6635fde84fd19b6ad2cec9ff06ad, call_ff68f6a124b0488eb9dc569d2c81d60b]

## Reasoning

The change moves output-dtype selection before GEMM, supports FP32 output storage and reduction, and supplies a matching FP32 Hadamard path. It also normalizes packed sign fields into half-precision scale vectors so output transforms use one scale-based interface. [source; call_13eb6635fde84fd19b6ad2cec9ff06ad]

## Impact

This adds opt-in FP32 linear outputs, not general FP32-input linear support. Existing model definitions do not enable the new intermediate or linear output settings. [source; call_295c9c13dc3b471ca2138e11c2fb7ae2, call_82216054571e4367893b3e0c1cd438b0, call_ff68f6a124b0488eb9dc569d2c81d60b, call_13eb6635fde84fd19b6ad2cec9ff06ad]

## Source Notes

Issue #5, “Will exl3 quants need requanting later?”, asks about format stability and subsequently Ampere support. Turboderp promises backward compatibility if storage changes and distinguishes Ampere performance from functionality. [source; call_4894c3a44de54117a5e61fe4d4c9f6c6]

The discussion bears on this change's packed-scale loading compatibility: unpacking old sign fields is consistent with the stated compatibility policy. That connection is inference; the discussion does not identify this commit or promise FP32 kernels. [inference; call_4894c3a44de54117a5e61fe4d4c9f6c6, call_13eb6635fde84fd19b6ad2cec9ff06ad]

Issue #7 reports “quantizing model: undefined symbol: __cxa_call_terminate” and a reporter-supplied toolchain workaround. Issue #15 reports incoherent cogito-v1-preview-qwen-32B output at bpw <= 2.5; its response discusses quantization regularization and reconversion. Neither discussion establishes this dtype change as its remedy. [source; call_18f66cc45a504b8788f405d7fef2e6c4, call_4bf8bcb14ba44c619c262098f02b39d6]

<a id="modules"></a>

## Selectable linear output precision and scale-fused Hadamard transforms

Linear now passes its optional out_dtype through ordinary, sliced, loaded-quantized and newly quantized inner-layer construction. LinearFP16.forward and LinearEXL3.forward allocate using call-level out_dtype, then constructor out_dtype, then torch.half. They return that allocation rather than applying to2 afterward; EXL3 bias addition no longer first casts the output to the bias dtype. [source; call_13eb6635fde84fd19b6ad2cec9ff06ad]

The old to2 helper honors dtype1 when supplied, otherwise dtype2. Thus explicit FP32 requests already returned FP32 tensors, but only after FP16 computation/storage. With FP16 input and no request, both implementations return FP16 before and after this change. With an explicit FP16 request they likewise remain FP16; with an explicit FP32 request the new allocation is genuinely FP32. EXL3's former input-dtype fallback must not be read as FP32-input support: its parent Hadamard wrapper rejected FP32 input, and both task GEMM entry points still require FP16 input. [source; call_ff68f6a124b0488eb9dc569d2c81d60b, call_7d8236c3c9ad4239a7b1b55672b8b604, call_0ebf505228384f21b317396223f9bb2c, call_13eb6635fde84fd19b6ad2cec9ff06ad]

In the shipped Llama, Mistral, Qwen2, Phi3, Gemma2 and DeciLM definitions, attention Q/K/V/O projections, gated-MLP gate/up/down projections, and lm_head retain FP16 outputs in ordinary execution. No model sets Linear.out_dtype or GatedMLP.interm_dtype, and none sets GatedMLP.out_dtype. TransformerBlock supplies FP16 normalized inputs and final model norms request FP16. Gemma2's explicit FP32 settings belong to post-attention and post-MLP norms, not linear layers. DeciLM no-op blocks instantiate no corresponding projections. These output dtypes do not change from the parent. [source; call_295c9c13dc3b471ca2138e11c2fb7ae2, call_82216054571e4367893b3e0c1cd438b0, call_ff68f6a124b0488eb9dc569d2c81d60b, call_df251a3a6eb9427bbba3741bfa7d812c, call_13eb6635fde84fd19b6ad2cec9ff06ad]

hgemm retains two-dimensional shape checks and FP16 A/B checks. FP16 C selects cublasHgemm; FP32 C selects cublasGemmEx with CUDA_R_16F inputs, CUDA_R_32F output and CUBLAS_COMPUTE_32F. Both use alpha=1 and beta=0. exl3_gemm retains its packed-weight shape relationships and int16 B requirement, accepts half or float C, and rejects non-null sv. Kernel specialization's 0x10 bit now selects output precision rather than output Hadamard fusion; partial-result reloads and stores use float pointers for FP32 C. [source; call_82216054571e4367893b3e0c1cd438b0, call_13eb6635fde84fd19b6ad2cec9ff06ad]

had_r_128 requires equal input/output shapes, two-dimensional input and width divisible by 128. It now accepts matching half/half or float/float tensors. Both paths apply optional half-precision pre/post scale vectors; those vectors are pointer-cast without explicit dtype or length checks in the wrapper. The half path multiplies scales in half precision and rounds the float transform before post-scaling; the float path keeps transform values and scale multiplication in float. [source; call_0ebf505228384f21b317396223f9bb2c, call_13eb6635fde84fd19b6ad2cec9ff06ad]

The 128-wide transform combines four values per thread with a 32-lane butterfly. The factor 0.088388347648 normalizes by 1/sqrt(128); a standard-library calculation found relative discrepancy about 3.60e-12 before conversion to the CUDA float literal. An exhaustive scalar check of all 65,536 packed words verified that the inspected unpacking convention maps set bits to -1 and clear bits to +1 reversibly. [execution; call_0842549a05094f8daeae42df3bc215da, call_0ebf505228384f21b317396223f9bb2c, call_7d8236c3c9ad4239a7b1b55672b8b604]

For packed-only storage, the parent constructor retained su/sv int16 tensors and left suh/svh absent. The task sets su=sv=None and expands both into half sign vectors. For unpacked-only storage, both versions retain suh/svh and absent su/sv. get_tensors therefore preserves packed keys in the parent but emits unpacked scale keys after task construction. get_weight_tensor is unchanged: it conditionally unpacks su/sv using tensor truth tests, otherwise uses suh/svh, then applies left/right Hadamards and scales. Task construction makes the packed truth-test branches unreachable for normally constructed objects. [source; call_7d8236c3c9ad4239a7b1b55672b8b604, call_13eb6635fde84fd19b6ad2cec9ff06ad]

Parent forward passed only suh to the input transform, including when packed su was retained. Its packed-sv direct-GEMM route selected the in-kernel output Hadamard/sign path; unpacked svh instead used a separate Hadamard followed by Python multiplication. The task always applies input scales from suh, calls exl3_gemm with sv=None, then applies an in-place output Hadamard with svh fused into that call. The reconstruction route similarly uses hgemm followed by the scale-fused output Hadamard. Its existing default remains reconstruction above 32 flattened input rows, overridable through reconstruct. [source; call_7d8236c3c9ad4239a7b1b55672b8b604, call_82216054571e4367893b3e0c1cd438b0, call_13eb6635fde84fd19b6ad2cec9ff06ad]

This trades the packed layer's fused output-transform path for a uniform separate transform, while removing the unpacked layer's separate Python output-scale multiplication. FP32 avoids FP16 intermediate output storage but uses twice the output-buffer bytes. Accuracy or speed improvements are plausible motivations, not measured results. [inference; call_13eb6635fde84fd19b6ad2cec9ff06ad, call_7d8236c3c9ad4239a7b1b55672b8b604]

Whole-parent source searches plus the task diff identify had_r_128 calls only in LinearEXL3.forward, hgemm calls in the two linear implementations, and exl3_gemm calls in LinearEXL3.forward and four locations in science/qgemm_benchmark.py. The benchmark already supplies half A/C, short B and sv=None, so its argument contract remains compatible. Task linear calls use the new scale semantics and null GEMM sv. Their normal FP16 inputs remain compatible; the FP32-intermediate exception is recorded separately. [source; call_295c9c13dc3b471ca2138e11c2fb7ae2, call_010881a1ec624dd881c6e5bd4206bbee, call_ff68f6a124b0488eb9dc569d2c81d60b, call_13eb6635fde84fd19b6ad2cec9ff06ad]

## Authoring-time findings — pending review

### fp32-mlp-intermediate-contract (suspected; defect)

The new FP32 intermediate option is not supported end-to-end by GatedMLP.forward.

Trigger: Construct GatedMLP with interm_dtype=torch.float32 and run forward with otherwise valid FP16 inputs.

Expected: Gate/up outputs should be activated and consumed by the down projection with a compatible dtype, or the unsupported setting should be rejected before computation.

Actual: Gate and up projections allocate FP32 outputs. silu_mul and gelu_mul perform no dtype checks and reinterpret their buffers as half pointers. Their kernel processes numel/2 half2 values, not numel FP32 values. The tensor remains tagged FP32 afterward. A dense down projection then fails hgemm's FP16 input check; an EXL3 down projection first performs a supported float Hadamard but subsequently fails the same FP16-input requirement in either GEMM route. No shipped model constructor enables interm_dtype, so this concerns the new opt-in setting rather than every model workflow.

Locations: e9a3b6a9256fc59f888b80a7d4a58883954b39de:exllamav3/modules/mlp.py — GatedMLP.forward, e9a3b6a9256fc59f888b80a7d4a58883954b39de:exllamav3/exllamav3_ext/activation.cu — act_mul_kernel

Source evidence: call_13eb6635fde84fd19b6ad2cec9ff06ad, call_ff68f6a124b0488eb9dc569d2c81d60b, call_82216054571e4367893b3e0c1cd438b0, call_73f3ee3c7f08478c90a284078b93d9ce

source_inspection: Traced gate/up dtype propagation, activation pointer casts, down projection forwarding and both GEMM input checks; inspected all model GatedMLP construction sites located by the parent-tree search. [call_13eb6635fde84fd19b6ad2cec9ff06ad, call_ff68f6a124b0488eb9dc569d2c81d60b, call_82216054571e4367893b3e0c1cd438b0, call_73f3ee3c7f08478c90a284078b93d9ce]. Limits: No native execution; external callers were not enumerated.

scalar_transcription: Computed activation write coverage for 128 FP32 elements: the half2 loop writes 256 bytes of a 512-byte tensor. [call_0842549a05094f8daeae42df3bc215da, call_ff68f6a124b0488eb9dc569d2c81d60b]. Limits: Byte-count arithmetic only, not a CUDA execution or numerical simulation.

## Uncertainty and limits

No CUDA kernels, PyTorch inference, numerical accuracy tests or performance benchmarks were executed. Scalar checks do not reproduce GPU rounding, concurrency or cuBLAS behavior.

Task behavior was reconstructed from the complete supplied diff and parent source; no solved-tree checkout was available.

Caller searches establish literal in-repository uses, not dynamic calls or external extension consumers.
