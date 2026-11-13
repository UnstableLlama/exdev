# 1d3e3b9dcc3f102a3720fd28d1b38095d44b1d30


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/1d3e3b9dcc3f102a3720fd28d1b38095d44b1d30) · [Evidence ledger](draft.json)

Replace full-result Hessian Hadamard transforms with float32 blockwise overwrites, reducing temporary size while retaining out-of-place weight transforms.

- [Blockwise in-place Hessian Hadamard transforms](#quantizer)

## Problem

Hessian finalization previously materialized full-matrix results for both Hadamard transforms before LDL decomposition. [source; call_e17cda7aec5e48abad888cb47045c8a6]

## Reasoning

The change replaces those two calls with blockwise helpers that overwrite the original tensor, trading batched matrix multiplication for sequential block multiplication and slice assignment. [source; call_afc19eb777474021bc4ed9142c28831d]

## Impact

This reduces the size of individual transform-result temporaries from a whole Hessian to a 128-row or 128-column slab. Actual peak VRAM savings and runtime costs remain unmeasured. [inference; call_afc19eb777474021bc4ed9142c28831d, call_e17cda7aec5e48abad888cb47045c8a6]

## Source Notes

Issue #7, “quantizing model: undefined symbol: __cxa_call_terminate,” reports a native-extension import failure and a reporter-supplied environment workaround, not Hadamard memory pressure. It does not establish motivation for this change. [source; call_5fdf18f2553242ee93e131f435c0d04b]

<a id="quantizer"></a>

## Blockwise in-place Hessian Hadamard transforms

blockwise_preapply_had_r_ multiplies each column slab by the normalized Hadamard matrix; blockwise_preapply_had_l_ multiplies each row slab from the left. Each computes a separate block_transformed tensor before copying it into the corresponding input slice. These are mutating Python helpers, not allocation-free custom kernels, and they return no transformed tensor. [source; call_afc19eb777474021bc4ed9142c28831d]

Both helpers require torch.float input and divisibility of the transformed dimension by had_dim. finalize_capture_H supplies had_k = 128. The factor 1/sqrt(had_dim) normalizes the Hadamard matrix; get_hadamard_dt caches the device-and-dtype-specific scaled matrix. [source; call_afc19eb777474021bc4ed9142c28831d, call_e17cda7aec5e48abad888cb47045c8a6, call_6048fdf9b3bf4852b46a4c0d0588cba1]

The surrounding data flow is preserved: average and regularize H, apply column signs, transform columns, apply row signs, transform rows, then call block_ldl(H, 16). That callee uses Cholesky factorization and 16-wide diagonal blocks; the patch does not eliminate its allocations or positive-definiteness requirement. Finalized H is still moved to CPU for later proxy-error evaluation, while L and sign data are cached for reuse. [source; call_e17cda7aec5e48abad888cb47045c8a6, call_afc19eb777474021bc4ed9142c28831d]

The original out-of-place helpers remain available, with only a local variable rename. quantize_exl3 still uses them for weight preprocessing and reconstruction; the memory optimization is confined to Hessian finalization. [source; call_afc19eb777474021bc4ed9142c28831d, call_e17cda7aec5e48abad888cb47045c8a6]

A standard-library scalar transcription verified that overwriting independent slabs matches out-of-place left and right transforms on an 8×12 matrix with block size 4. It also verified order-128 Sylvester orthogonality. For a square float32 Hessian of width d, one result slab contains 128d elements rather than d²; the 128×128 transform itself occupies 65,536 bytes. [execution; call_e82a7a0f3885434daaece0a4e873aabc]

The smaller temporaries support the stated VRAM objective, but sequential Python iterations and additional slice writes may cost throughput. Temporary lifetimes, matrix-multiplication workspaces, and allocator caching prevent treating the slab-size calculation as a measured peak-memory reduction. [inference; call_afc19eb777474021bc4ed9142c28831d, call_e82a7a0f3885434daaece0a4e873aabc]

## Uncertainty and limits

No PyTorch or CUDA execution, allocator measurements, throughput benchmarks, or end-to-end quantization tests were performed.

The scalar check uses Python arithmetic and a smaller block size for overwrite equivalence; it does not establish float32 rounding equivalence or GPU workspace requirements.
