# c2ec220c83d4a697f4726401aa8c7e6a5a551fa6


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/c2ec220c83d4a697f4726401aa8c7e6a5a551fa6) · [Evidence ledger](draft.json)

Reduces repeated Python and CUDA host work by allocating final-shaped outputs and caching kernel attribute setup. Speedup is unmeasured; removed native buffer checks expose malformed direct calls.

- [Reduce host work around EXL3 multiplication](#linear-exl3)

## Problem

The existing forward path reshaped its output after computation, and both native GEMM wrappers called cudaFuncSetAttribute on every launch. [source; call_d930d7a5939b4277835567f923968c1d, call_662669092f7e4eb2b6a5e2b2bf61fae1]

## Reasoning

Allocating the final output shape directly and remembering configured kernel pointers plausibly reduces repeated host-side work, consistent with the commit's stated CPU-overhead goal. This is not a measured speedup. [inference; call_bea8e0259b134b7c8ccbcd0a1b5109da, call_8773cdf479854d40bcd331a835b498cc]

## Impact

The Python output shape remains unchanged, but direct GEMM now accepts that multidimensional allocation without an intermediate output view. Several native argument checks are also removed, weakening protection for malformed direct calls. [source; call_bea8e0259b134b7c8ccbcd0a1b5109da, call_8773cdf479854d40bcd331a835b498cc]

## Source Notes

The root quantized-inference entry was read for provenance. It establishes the original direct-versus-reconstructed execution paths and records historical packed-sign and launch-sizing limitations. [ancestor; call_9867e277e7674933b5ed6006cfb465c4]

Those historical limitations are not all current: the inspected parent constructor unpacks supplied su/sv and stores self.su/self.sv as None, while single-GEMM launch sizing clamps the block count to at least one. The task leaves both mechanisms unchanged. [source; call_662669092f7e4eb2b6a5e2b2bf61fae1, call_a7af802f81ac4dd787e17497245012db, call_8773cdf479854d40bcd331a835b498cc, call_bea8e0259b134b7c8ccbcd0a1b5109da]

Issue #11, “AssertionError: bias is wrong datatype,” reports a constructor assertion and a subsequently acknowledged fix. Issue #34, “torch._C._LinAlgError on last layer of quant,” reports Cholesky failure during conversion. Their relationship to this task is only inferred from shared exl3.py or linear.py paths; neither discussion establishes motivation for this overhead change. [inference; call_2dc54674e8aa425788db251732450e5b, call_439028d6a74a4f8183818a9f7bf37999, call_8773cdf479854d40bcd331a835b498cc]

<a id="linear-exl3"></a>

## Reduce host work around EXL3 multiplication

LinearEXL3.forward still flattens input leading dimensions and defaults to reconstruction only above 32 rows; params['reconstruct'] remains an override. The threshold is unchanged, not a newly demonstrated crossover. Output dtype selection becomes out_dtype or self.out_dtype or torch.half, replacing first_not_none. [source; call_8773cdf479854d40bcd331a835b498cc, call_662669092f7e4eb2b6a5e2b2bf61fae1]

Both branches now allocate y with the final leading dimensions and out_features. Reconstruction creates a two-dimensional y_ view for hgemm and the output Hadamard; direct GEMM receives y itself. Bias is added to y and y is returned. Thus the direct branch eliminates the final output view, whereas reconstruction still needs one for its existing callees. [source; call_8773cdf479854d40bcd331a835b498cc]

The Python and native shape edits are coupled. Native GEMM checks C's last dimension rather than dimension 1 and removes the A/C first-dimension equality check. Its launch dimensions still come from flattened A and packed B, and the kernel addresses C as flat storage. The factor 16 in the width check converts B's packed tile count into output channels. [source; call_bea8e0259b134b7c8ccbcd0a1b5109da, call_d930d7a5939b4277835567f923968c1d, call_b2c43f628ba44440b4ef856401875235, call_3928fcb93eae4dfbb7734d7f7d648c15]

A standard-library scalar check confirmed that final shapes with zero, one or two leading dimensions retain m*n elements after flattening, including the 32/33-row branch boundary. This checks allocation arithmetic, not PyTorch views or GPU writes. [execution; call_08d8e754228a46d4b4cc9f753883805e]

Whole-tree search found direct exl3_gemm calls in LinearEXL3.forward and science/qgemm_benchmark.py, plus the public native binding. The benchmark retains compatible two-dimensional outputs, full-length scale vectors and A itself as transform workspace. The header retains tensor-reference arguments, and the kernel already consumes raw pointers, so neither requires a signature change. [source; call_970d6f50e1964a22b17993d647d480e7, call_4eb77bebdb7b4a5c871c783ae593c7f1, call_3c5b6bda637f4d7b831180d6b6e29a8c, call_b2c43f628ba44440b4ef856401875235]

Linear.forward continues to consume the returned tensor for optional softcap and post-scaling. Its loading and conversion constructors remain unchanged. The existing test_qgemm exercises both reconstruction overrides using three-dimensional inputs and compares outputs with rtol=atol=0.05; it was not executed. [source; call_67dd796926334b62b373107237838a4c, call_7d4832e5b406487d832c3e9b458cc33e]

A shared std::set<void*> now records kernel pointers encountered by single- and multi-GEMM. Each wrapper calls cudaFuncSetAttribute with the unchanged SMEM_MAX only when the pointer is absent, then inserts it. Launch geometry and kernel arguments are unchanged. The insertion is unconditional on the attribute call's result, and the set contains no device identifier. [source; call_bea8e0259b134b7c8ccbcd0a1b5109da, call_d930d7a5939b4277835567f923968c1d]

Removing output-row equality enables final-shaped allocations, but dropping scale-length and workspace checks is not necessary for that shape change. A capacity check on C and retained transform-buffer checks would preserve malformed-call protection while accepting multidimensional outputs. [inference; call_bea8e0259b134b7c8ccbcd0a1b5109da, call_b2c43f628ba44440b4ef856401875235]

## Authoring-time findings — pending review

### unchecked-native-buffers (suspected; defect)

Removed native checks allow malformed direct calls to reach kernels with insufficient output or transform storage.

Trigger: Call the exported exl3_gemm with otherwise compatible A/B but C=(1,n) for A with two rows; alternatively supply suh while omitting A_had, or supply undersized suh, svh or A_had.

Expected: Reject incompatible buffer capacities and require a correctly sized transform workspace when suh is present.

Actual: The remaining checks validate output width but not total capacity. OPTPTR permits a null A_had, and the kernel uses it whenever suh is present. Kernel addressing follows A/B-derived dimensions rather than the supplied buffer capacities, exposing out-of-bounds or null accesses.

Locations: c2ec220c83d4a697f4726401aa8c7e6a5a551fa6:exllamav3/exllamav3_ext/quant/exl3_gemm.cu — exl3_gemm

Source evidence: call_bea8e0259b134b7c8ccbcd0a1b5109da, call_d930d7a5939b4277835567f923968c1d, call_b2c43f628ba44440b4ef856401875235, call_3928fcb93eae4dfbb7734d7f7d648c15, call_970d6f50e1964a22b17993d647d480e7

source_inspection: Compared removed guards with raw-pointer kernel addressing and searched direct callers. LinearEXL3 allocates matching output/workspace storage; the benchmark also prepares matching buffers. Reach is established through the exported native binding, not every ordinary model invocation. Constructor checks validate scale dtype but not length. [call_970d6f50e1964a22b17993d647d480e7, call_662669092f7e4eb2b6a5e2b2bf61fae1, call_4eb77bebdb7b4a5c871c783ae593c7f1, call_8773cdf479854d40bcd331a835b498cc]. Limits: No malformed GPU call was executed; the precise runtime failure is unmeasured.

## Uncertainty and limits

No CUDA execution, numerical comparison or performance benchmark was run. The scalar check validates shape arithmetic only.

The kernel-attribute cache is keyed only by function pointer. Correctness across CUDA devices, contexts, concurrent native callers and failed attribute-setting calls was not established.

The existing GPU comparison test requires a local model and explicitly selected CUDA device; inspecting it does not establish that this change passes it.
