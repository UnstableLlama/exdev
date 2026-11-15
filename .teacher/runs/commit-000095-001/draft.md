# 39e400d16aa506a98f6da102176b3310b95022f0


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/39e400d16aa506a98f6da102176b3310b95022f0) · [Evidence ledger](draft.json)

Adds an exported LayerNorm component with optional bias, cached float32 parameter copies and PyTorch-backed forward paths, without changing model architecture assembly.

- [LayerNorm lifecycle and precision handling](#modules)

## Problem

The module package provides RMSNorm but lacks a LayerNorm class. This change adds and exports that reusable component without changing model constructors. [source; call_b3ceeeec537e44b4a9c433af5c90c814, call_c274b94d3d1747fb967f06a35b1a2b81, call_b395654445be4d2fb03cb4b31eb60a22]

## Reasoning

LayerNorm follows the custom Module lifecycle while delegating normalization to PyTorch rather than adding a native kernel. [source; call_86ef0dcdffa84b1485c60d1563c26e8c, call_b395654445be4d2fb03cb4b31eb60a22]

## Impact

Consumers can import LayerNorm from exllamav3.modules; the diff does not wire it into an architecture or replace existing RMSNorm calls. [source; call_c274b94d3d1747fb967f06a35b1a2b81, call_b395654445be4d2fb03cb4b31eb60a22]

## Source Notes

The inspected discussions concern “quantizing model: undefined symbol: __cxa_call_terminate,” “`cogito-v1-preview-qwen-32B` generates incoherent output for bpw <= 2.5,” and “Build Failure on Windows: CUDA 12.4 / PyTorch 2.7.0+cu126 / VS 2022.” They report extension-loading, quantization-quality and compilation problems respectively, not a LayerNorm request. [source; call_a08da0ab16f34dc9b4e5e8ab4466ed8e, call_904154adb8f241b1844cce3218c5453c, call_3fa1758e9acd40a8990d8a32718c47ed]

<a id="modules"></a>

## LayerNorm lifecycle and precision handling

The constructor requires an epsilon argument, accepts an optional output dtype, and rejects non-null qmap values. Epsilon is forwarded directly to F.layer_norm; this module supplies no numerical default or configuration-key lookup. [source; call_b395654445be4d2fb03cb4b31eb60a22]

load retrieves <key>.weight and optional <key>.bias on the requested device. Float32 checkpoint tensors are converted to half before float32 working copies are created. Other checkpoint dtypes are retained in the primary copies. Thus the float32 copies do not preserve the original precision of float32 checkpoint values. [source; call_b395654445be4d2fb03cb4b31eb60a22]

A bounded scalar conversion illustrates that precision consequence: float32 1.000100016593933 becomes 1.0 after half conversion and float32 expansion, losing approximately 0.0001000166. [execution; call_23a5094d8cd746d6aec56efd7ed94430]

forward and forward_torch are identical: float32 inputs select float32 parameter copies; all other inputs select the primary copies. Both call F.layer_norm with normalized_shape=x.shape[-1:], restricting normalization to the final axis, then apply the call-level output dtype or the constructor-level dtype. Neither method uses params or invokes the imported native extension. [source; call_b395654445be4d2fb03cb4b31eb60a22]

This differs from the existing RMSNorm implementation, whose ordinary forward calls ext.rms_norm and whose Torch alternative explicitly computes a mean-square normalization without centering. LayerNorm instead has a single delegated implementation shared by both entry points. [source; call_ea0fdbb746f24cfe98bc9519d9f576a3, call_b395654445be4d2fb03cb4b31eb60a22]

weights_numel counts logical weight and optional bias elements, not the additional float32 copies. get_tensors exports contiguous primary tensors only. unload clears the device and all tensor references but retains the cached element count. [source; call_b395654445be4d2fb03cb4b31eb60a22]

Keeping both parameter representations trades additional storage for avoiding parameter conversion inside each forward call. Delegating both entry points to PyTorch also avoids maintaining separate native and reference implementations; no measured speed advantage is established. [inference; call_b395654445be4d2fb03cb4b31eb60a22]

## Uncertainty and limits

No repository implementation, PyTorch operation or GPU kernel was executed; dtype compatibility and numerical behavior remain untested.

The scalar precision check models IEEE half rounding with Python struct, not PyTorch device conversion.

No performance measurements or architecture integration tests establish the cost or model-level effect of this component.
