# c2ec220c83d4a697f4726401aa8c7e6a5a551fa6


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/c2ec220c83d4a697f4726401aa8c7e6a5a551fa6) · [Evidence ledger](draft.json)

Reduces EXL3 host work through final-shaped output allocation, fewer native checks and cached kernel attributes. Performance is unmeasured; validation weakens and inherited dispatch hazards remain.

- [Reduce host work around EXL3 execution](#linear-exl3)

## Problem

The change targets CPU overhead in LinearEXL3: repeated kernel-attribute setup, native argument checks and Python output reshaping. [source; call_1ffdac360f33457e83458e5e2e713b83, call_bc52a350340f45c8aeacbcda1de97d7f]

## Reasoning

Allocating the final output shape and relaxing native output-shape checks are interdependent. The direct kernel receives multidimensional output storage but still computes flattened rows from A; checking C's last dimension replaces checking dimension 1. [source; call_bc52a350340f45c8aeacbcda1de97d7f, call_1ffdac360f33457e83458e5e2e713b83, call_598438ed20c6446a9eb7230f10660073]

Caching attribute setup and removing checks plausibly reduce host work, at the cost of weaker validation and additional persistent host state. No speedup is established. [inference; call_1ffdac360f33457e83458e5e2e713b83]

## Impact

Both single- and multi-GEMM now share a process-global set of kernel addresses. cudaFuncSetAttribute runs only for an address absent from that set; insertion does not check the call's return status. [source; call_1ffdac360f33457e83458e5e2e713b83]

The Python API still returns input leading dimensions followed by out_features, applies bias in place, and defaults to reconstruction above 32 flattened rows. The change does not eliminate output or input-transform scratch allocation. [source; call_996648dce5a54c0bbed944676d3ff216, call_bc52a350340f45c8aeacbcda1de97d7f]

## Source Notes

Read the cooperative-GEMM entry and subsequent tuning entry. They establish the fused transform interface, scratch-buffer precondition, reconstruction alternative and previously recorded selector and zero-block concerns. [ancestor; call_0f1bec96c7164e2b8f50a7292d0c5e0e, call_f91591e8477f48e7baaaf10102f1b14e]

Issue #11, “AssertionError: bias is wrong datatype,” reports a constructor failure; its reporter confirms an earlier fix. Issue #34, “torch._C._LinAlgError on last layer of quant,” reports Cholesky failure during conversion. Their relationship to this task is only inferred from shared LinearEXL3/Linear source paths, not evidence that this optimization fixes either report. [inference; call_fdf4c3a3ca0c4cde8724e73fe3294577, call_677f1a4a97ab4eb98e65bc8f4fabac00, call_64d73f6e70be41408ffc9d7735c8a8af, call_bc52a350340f45c8aeacbcda1de97d7f]

<a id="linear-exl3"></a>

## Reduce host work around EXL3 execution

forward allocates y directly with out_shape. Reconstruction creates a two-dimensional view y_ for dense GEMM and output Hadamard; direct quantized GEMM writes into y without a final view. Dtype selection becomes out_dtype or self.out_dtype or torch.half, and the unused input_dtype assignment disappears. [source; call_bc52a350340f45c8aeacbcda1de97d7f]

The native direct path derives m and k from A and n from packed B, then passes raw pointers to the kernel. Its outer kernel transforms input into A_had, processes 16-row GEMM chunks and transforms output in place. Thus output rank does not participate in kernel indexing. [source; call_598438ed20c6446a9eb7230f10660073, call_810c729fd1f44dc9bb8d0e21b5ea454e]

A standard-library shape calculation verified equal element counts between final-shaped and flattened outputs for leading shapes (), (1,), (2,3) and (2,2,8), with output width 128. This models allocation arithmetic rather than executing tensor operations. [execution; call_80795c4463284b068f55b568152c97b0]

Linear.forward remains compatible with the returned shape and continues optional softcap/post-scaling. The benchmark retains two-dimensional output and valid transform buffers; its calls remain compatible with the relaxed interface. test_qgemm explicitly compares both reconstruction settings on three-dimensional inputs, but was not run. [source; call_64d73f6e70be41408ffc9d7735c8a8af, call_ff5de9e58b7e473287e14a8b58269654, call_91c11b1818794cc6999b354fe50c2b44, call_bfa92a81a4804c4ca0d78f94cd257b15]

The removed checks previously enforced output row equality, input/output scale lengths and presence and shape of input-transform scratch. LinearEXL3 still allocates matching scratch and output, but its constructor checks scale dtypes rather than their lengths. The public native binding therefore loses protections not replaced universally by Python validation. [source; call_1ffdac360f33457e83458e5e2e713b83, call_996648dce5a54c0bbed944676d3ff216, call_bfa92a81a4804c4ca0d78f94cd257b15]

The previously recorded zero-block multi-GEMM arithmetic and Boolean selector expression are carried over unchanged. The five-argument select_gemm_shape header declaration also remains inconsistent with its six-argument definition; inspected internal selectors call the definition with six arguments. [source; call_be770d4353ba47f2b78abe1fc1855570, call_ea39001d98cb456eb61256bc765d15ea, call_598438ed20c6446a9eb7230f10660073, call_1ffdac360f33457e83458e5e2e713b83]

## Authoring-time findings — pending review

### removed-transform-validation (suspected; defect)

Removing transform-buffer validation permits malformed calls to reach raw-pointer kernel accesses.

Trigger: Call the exposed exl3_gemm binding with nonempty suh but A_had=None, or construct LinearEXL3 with undersized half-precision suh/svh and use the direct path.

Expected: Reject missing scratch or incorrect scale lengths before launch, as the previous checks did.

Actual: The wrapper forwards a null scratch pointer or undersized scale storage. The kernel uses these pointers without corresponding bounds checks. Normal forward allocation supplies scratch, and benchmark callers supply valid lengths; malformed scale lengths remain accepted by the inspected constructor.

Locations: c2ec220c83d4a697f4726401aa8c7e6a5a551fa6:exllamav3/exllamav3_ext/quant/exl3_gemm.cu — exl3_gemm

Source evidence: call_1ffdac360f33457e83458e5e2e713b83, call_810c729fd1f44dc9bb8d0e21b5ea454e, call_996648dce5a54c0bbed944676d3ff216, call_bfa92a81a4804c4ca0d78f94cd257b15

source_inspection: Compared removed checks with kernel pointer use, constructor validation and all discovered direct Python call sites. [call_ff5de9e58b7e473287e14a8b58269654, call_bc52a350340f45c8aeacbcda1de97d7f]. Limits: No malformed GPU call was executed; exact runtime failure is unmeasured.

### inherited-zero-multi-grid (suspected; defect)

Multi-GEMM retains a zero-block case before the new attribute cache is reached.

Trigger: Automatic Ampere multi-GEMM with reduction dimension 512, output width 128 and two-bit weights selects shape 2.

Expected: Use a positive block count or reject the dimensions before concurrency division.

Actual: Sixteen tiles divided by 24 produce num_sms=0; exl3_mgemm then computes total_sms/num_sms. Direct callers include fused attention K/V and expert gate/up/down projections, without a minimum-tile check at the inspected calls.

Locations: c2ec220c83d4a697f4726401aa8c7e6a5a551fa6:exllamav3/exllamav3_ext/quant/exl3_gemm.cu — exl3_mgemm

Source evidence: call_be770d4353ba47f2b78abe1fc1855570, call_ea39001d98cb456eb61256bc765d15ea, call_598438ed20c6446a9eb7230f10660073, call_c7414a6c213c46a08426cebac46faf3d, call_9692bdfa25674bd19040b878d9bb1b7c, call_204a46fbf1424ebcb273c84b42a156cd

scalar_transcription: Python calculated 16 tiles and a zero multi-GEMM cap. [call_80795c4463284b068f55b568152c97b0]. Limits: No native division or model execution; typical model dimensions were not established to trigger this case.

### inherited-boolean-selector (suspected; defect)

The inherited selector still compares a Boolean result with 8192.

Trigger: Hopper/Blackwell automatic selection with bits=3, reduction dimension 16384 and output width 4096.

Expected: A dimension threshold should compare a dimension; the intended exact rule is unestablished.

Actual: (size_k && bits >= 3) cannot exceed 8192, so this branch always selects shape 2. Both native selectors use it; positive forced shape indices bypass it.

Locations: c2ec220c83d4a697f4726401aa8c7e6a5a551fa6:exllamav3/exllamav3_ext/quant/exl3_kernel_map.cu — select_gemm_shape

Source evidence: call_be770d4353ba47f2b78abe1fc1855570, call_bfa92a81a4804c4ca0d78f94cd257b15, call_1ffdac360f33457e83458e5e2e713b83

scalar_transcription: Python modeled the representative Boolean comparison and obtained false. [call_80795c4463284b068f55b568152c97b0]. Limits: No GPU execution or measured performance consequence.

## Uncertainty and limits

No CUDA compilation, repository test, numerical comparison or timing benchmark was run.

Scalar checks establish shape and integer arithmetic only, not tensor layout behavior, GPU memory safety or floating-point equivalence.

The cache is keyed only by kernel address, not device or context. Correctness across devices, context recreation and concurrent calls is unestablished; eligible CUDA documentation was not inspected.

Caller searches establish literal repository occurrences, not dynamic or external consumers.
