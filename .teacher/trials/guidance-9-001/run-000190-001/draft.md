# c94905bf794f3b3bee00cd1f6645e624cc33cd12


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/c94905bf794f3b3bee00cd1f6645e624cc33cd12) · [Evidence ledger](draft.json)

RMSNorm moves flattening metadata work into C++ and returns its output directly. CUDA arithmetic is unchanged; speedup is unmeasured, and unsupported layouts lose an incidental view-time rejection.

- [Move RMSNorm shape handling into the native wrapper](#rmsnorm)

## Problem

RMSNorm.forward flattened its input and restored its output shape on every call. The change removes that Python-side shape handling. [source; call_b5903412a51c4016b63172c59c223861]

## Reasoning

The edits are interdependent: accepting unflattened tensors requires native RMSNorm to use the final dimension as width and multiply all leading dimensions into its row count. [source; call_87a9f5453a4847a9a1fb8823ddbab963, call_b5903412a51c4016b63172c59c223861]

## Impact

The wrapper returns its allocated output directly, preserving input shape and existing output-dtype selection. Reduced host overhead is plausible, but no speedup was measured. [inference; call_b5903412a51c4016b63172c59c223861]

## Source Notes

The root modules entry was read. It describes the original flatten/restore implementation, four-element vector accesses, and float-intermediate normalization. [ancestor; call_8cb855281afc48d6b2f2641570adf7c2]

Issue #39, “Gemma 3 architecture not in list?”, concerns branch availability and subsequently discusses frontend behavior and memory allocation. It provides no explicit connection to this RMSNorm change. [source; call_b1ff194215854b1c9f15bf18e4c656c3]

<a id="rmsnorm"></a>

## Move RMSNorm shape handling into the native wrapper

Python now allocates empty_like(x) without first creating a two-dimensional view, passes x and y directly to ext.rms_norm, and returns y. Removing the params annotation does not change argument order or its unused status. [source; call_a4fa560c784a43b5b808eb6018814aec, call_b5903412a51c4016b63172c59c223861]

Native validation moves width divisibility and weight-length checks from dimension 1 to dimension -1. Full shape equality replaces two individual input/output dimension checks; the macro compares sizes, not strides. Rows become the product of leading dimensions, initialized to one, so a vector has one row. [source; call_87a9f5453a4847a9a1fb8823ddbab963, call_9be022419b5c4a82b8ed216fcd298f3e]

The CUDA calculation is unchanged: each block normalizes one packed row using float square accumulation and reciprocal square root, then multiplies by weight plus constant_bias. Width must remain divisible by four because reads and writes process four elements. The 1024-thread block size is unchanged, not a new dispatch threshold. [source; call_391df4c0b77b4672944332358ab087cf, call_87a9f5453a4847a9a1fb8823ddbab963]

A standard-library indexing transcription verified complete contiguous coverage for shapes (8), (2,8), (2,3,8), and (2,3,4,8), yielding respectively 1, 2, 6, and 24 rows. This supports the flattening identity, not GPU correctness. [execution; call_d16b648cae2a442c9d101ca719798bc3]

Inspected callers retain compatible shape expectations: TransformerBlock and ParallelDecoderBlock consume shape-preserving normalization; all three attention implementations normalize four-dimensional Q/K only in their no-RoPE fallback; science/kv_quant_exp.py uses normalized three-dimensional activations for projection; test_qgemm.py supplies (1,batch_size,width). None needs a new argument for this change. [source; call_7edd1053f5004cdf98fd362c0441923d, call_5df24e1a94724af69dd7fc27d3bc9c86, call_29695d0764964d439be46997094a9ec2, call_1c591648530d4a9fae87a22130f10145, call_153c3642c0b54f42bad5f7713aba9104]

The existing forward_torch alternative explicitly reduces the last axis and retains its own dtype conversions. The optimized native path still uses packed pointer arithmetic; eliminating views does not make its kernel stride-aware. [source; call_a4fa560c784a43b5b808eb6018814aec, call_391df4c0b77b4672944332358ab087cf, call_b5903412a51c4016b63172c59c223861]

## Authoring-time findings — pending review

### strided-input (suspected; defect)

Removing the flattening view removes its incidental rejection of incompatible layouts without adding stride validation or contiguous conversion.

Trigger: Call RMSNorm.forward with a CUDA float/half tensor shaped (2,8,4), with strides (32,1,8), and a four-element half weight.

Expected: Normalize each logical final-axis row, or reject the unsupported layout before launching.

Actual: The changed shape checks accept this shape, while the kernel reads packed groups at row*dim. For the first logical row it reads offsets 0,1,2,3 instead of 0,8,16,24. The former flattening view could not merge these leading dimensions without copying.

Locations: c94905bf794f3b3bee00cd1f6645e624cc33cd12:exllamav3/modules/rmsnorm.py — RMSNorm.forward, c94905bf794f3b3bee00cd1f6645e624cc33cd12:exllamav3/exllamav3_ext/norm.cu — rms_norm_kernel

Source evidence: call_b5903412a51c4016b63172c59c223861, call_391df4c0b77b4672944332358ab087cf, call_9be022419b5c4a82b8ed216fcd298f3e, call_7edd1053f5004cdf98fd362c0441923d

scalar_transcription: Compared logical strided offsets against the kernel's packed indexing. [call_d16b648cae2a442c9d101ca719798bc3]. Limits: No tensor library or GPU execution; reach is an explicitly supplied public-wrapper input, not a demonstrated model-generated layout.

### existing-test-arity (suspected; defect)

The existing native normalization tests remain on a four-argument call form.

Trigger: Run test_rms_norm or test_rms_norm_benchmark against the inspected extension binding.

Expected: Calls reach normalization and its correctness or timing checks.

Actual: All three test call sites omit required constant_bias; the declaration takes five arguments and the binding supplies no default. The task leaves this mismatch unchanged.

Locations: d54648bfaba4ab016fc3345938cc9c0f1b02be48:tests/test_ext_norm.py — test_rms_norm, d54648bfaba4ab016fc3345938cc9c0f1b02be48:tests/test_ext_norm.py — test_rms_norm_benchmark

Source evidence: call_7361cadbd66d49cd9285548a61d950c6, call_5b3297f241064a9db40a3467e7ad8011, call_487ac09b7828456cb8258ebe80325fe3, call_61bb6e1a7f4f4f479a30b09d07efd170

source_inspection: Compared every literal ext.rms_norm caller found by whole-tree search with its declaration and binding. RMSNorm.forward supplies all five arguments; the test calls do not. [call_7361cadbd66d49cd9285548a61d950c6, call_a4fa560c784a43b5b808eb6018814aec, call_5b3297f241064a9db40a3467e7ad8011, call_61bb6e1a7f4f4f479a30b09d07efd170]. Limits: Tests were not executed; this is an inherited test-interface mismatch, not a newly introduced inference-path failure.

## Uncertainty and limits

No PyTorch, CUDA kernel, model execution or performance benchmark was run. The scalar check covers indexing only, not floating-point precision, allocation behavior or native integer overflow.

Caller inspection covered literal native RMSNorm calls and named normalization forward calls; it does not establish every dynamically dispatched module caller or external user's input layout.

No inspected internal producer was established to generate the transposed input used in the layout finding.
