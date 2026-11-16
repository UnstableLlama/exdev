# c2b8516f17487d060163f841cf83340e007ced4f


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/c2b8516f17487d060163f841cf83340e007ced4f) · [Evidence ledger](draft.json)

Removes references to an absent GEMV header from all eight EXL3 compilation units, leaving GEMM code and dispatch unchanged.

- [Remove the stale GEMV header dependency](#quantized-inference)

## Problem

All eight EXL3 compilation units included ../exl3_gemv_kernel.cuh, but that header is absent from the parent quant directory. [source; call_caba958e06714184894e4dddf9bd22ee, call_053aee6e5f63486e8c51ed7ac9c0a7bf]

## Reasoning

Removing the stale include addresses the missing-header dependency rather than supplying a GEMV implementation. The existing GEMM header and per-unit declarations remain included. [source; call_9b8cdc13c5444cc2a08e9d7ef06a0c35, call_7065fa7b9d5547918a252c4c5f14d208]

## Impact

This removes a source-level compilation obstacle from the extension build: setup.py recursively collects .cu files, including these units. Successful compilation of the complete extension is not established. [inference; call_c7ee56d7813a4543a7afc1770f1085a5, call_caba958e06714184894e4dddf9bd22ee, call_053aee6e5f63486e8c51ed7ac9c0a7bf]

## Source Notes

Issue #21, “Build Failure on Windows: CUDA 12.4 / PyTorch 2.7.0+cu126 / VS 2022,” reports errors in PyTorch/CUDA headers and was closed without a solution. It does not report this missing GEMV header; it is not evidence that this change resolves that issue. [source; call_6cfaf23d3b6b4fd1a725496263c5f2ae]

<a id="quantized-inference"></a>

## Remove the stale GEMV header dependency

The complete change deletes the same include from exl3_comp_unit_1.cu through exl3_comp_unit_8.cu; it changes no kernel bodies, dispatch entries or numerical constants. [source; call_9b8cdc13c5444cc2a08e9d7ef06a0c35, call_bc70cc60713e4213a005419a153360f4, call_909a84a6fc5a44c3931511a9e5edb023, call_954af5adbb5443c2b74096dcc5d22b68, call_e72b87e50354431fae4b387fd2c966a4, call_1b6b3758cefc425282ff002865d0b4ea, call_43cd65fa19144fd28ae41ff8fff27be1, call_5c2966b07ace4290b956cd9161912730]

The inspected first unit defines FP32 and FP16 GEMM function-pointer arrays using EXL3_GEMM_KERNEL_INSTANCES. Its GEMM implementation include remains intact. Whole-parent search finds exl3_gemv only in the eight removed include directives, supporting deletion rather than replacement as the narrowly scoped repair. [source; call_7065fa7b9d5547918a252c4c5f14d208, call_caba958e06714184894e4dddf9bd22ee, call_9b8cdc13c5444cc2a08e9d7ef06a0c35]

## Uncertainty and limits

No CUDA compilation or runtime test was performed. This include-only change offers no useful numerical computation to validate with a scalar Python model.
