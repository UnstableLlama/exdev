# 9bde46e775df21d54d78a0fbe78b1490bf311a5a


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/9bde46e775df21d54d78a0fbe78b1490bf311a5a) · [Evidence ledger](draft.json)

Adds an exported, unquantized 2D/3D convolution module that produces token-shaped outputs; its output-dtype options remain unused.

- [Convolution-backed patch projection](#modules)

## Problem

The change adds an exported convolution component with separate 2D and 3D forward paths, without integrating it into a model architecture. [source; call_1629b4592ada4822953f44b5eaefbcbb, call_b6150991f10d4f5bb9af12703e85dde8]

## Reasoning

The output reshaping suggests a patch-projection component for producing token sequences rather than a general-purpose convolution wrapper. This interpretation follows the channel-last 2D output and the patch-sized 3D input view. [inference; call_b6150991f10d4f5bb9af12703e85dde8]

## Impact

Consumers can import Conv from exllamav3.modules. Whole-parent-tree searches found no Conv constructor calls or F.conv calls; the task adds no model-side caller. [source; call_1629b4592ada4822953f44b5eaefbcbb, call_b0d7c997e28940c1a639e23c593836bd, call_15763d3591074442b8adfe98691b6218, call_b6150991f10d4f5bb9af12703e85dde8]

## Source Notes

The initial modules entry establishes the custom Module lifecycle and device boundary. The LayerNorm introduction entry documents the optional-bias loading and tensor-export pattern that Conv closely follows. [ancestor; call_f336016b5a314a579ce5e45356db56d0, call_eb0d0fec677d4426ac1226dd809bf72d]

Issue #33, “Error converting model,” reports a conversion-time file-opening failure, subsequently diagnosed as too many open files, and later discusses GLM4 generation problems. Its connection here is only an inferred shared loader dependency: its traceback names safetensors.get_tensor, which Conv.load now calls. It is not evidence of a convolution failure or motivation for this change. [inference; call_8cf8aa20185647c383eccf9c8da23329, call_ef9ef0c7ed724786aa3867716f50cda4, call_b6150991f10d4f5bb9af12703e85dde8]

<a id="modules"></a>

## Convolution-backed patch projection

Conv subclasses the custom Module base. Its constructor stores channel counts and kernel_size, rejects non-null qmap, and restricts len(kernel_size) to 2 or 3. These numbers select spatial dimensionality, not precision or performance tiers. [source; call_b6150991f10d4f5bb9af12703e85dde8, call_10264379a71f480c82d7e2cb3ecd62d3]

load requests <key>.weight and optional <key>.bias on the selected device with float2half=True, then caches their combined element count. This matches LayerNorm's loading pattern without its float32 working copies. get_tensors exports contiguous tensors under the original keys; unload clears tensors and device but retains the cached count. [source; call_b6150991f10d4f5bb9af12703e85dde8, call_4a629b63fde44d7c8a5bfe5e74dd452e]

The inspected file-backed loader paths convert float32 weights to float16 when float2half is enabled, and also convert bfloat16 unless allow_bf16 is enabled. Conv does not cast its input or create alternate parameter representations. [source; call_7c3314e57934413c95f6fcb6491dfab5, call_b6150991f10d4f5bb9af12703e85dde8]

The 2D path calls F.conv2d with kernel_size in the stride position, then flattens spatial dimensions and permutes channels last: [B,C,H',W'] becomes contiguous [B,H'W',C]. The loaded weight determines the actual filter shape; the constructor tuple supplies stride rather than constructing or validating that weight. [source; call_b6150991f10d4f5bb9af12703e85dde8]

The 3D path first views the input as [-1,in_channels,k0,k1,k2], calls F.conv3d with the same tuple as stride, and returns y.view(-1,out_channels).unsqueeze(0). With matching kernel-sized filters, each input patch produces one output vector and the result is [1,patch_count,out_channels]. Unlike the 2D path, it imposes a leading dimension of one and does not preserve a separate incoming batch dimension. [source; call_b6150991f10d4f5bb9af12703e85dde8]

A standard-library layout transcription checked the 2D permutation from [2,3,2,4] to [2,8,3], including channel ordering. A separate element-count check mapped 480 input elements to five [3,2,4,4] patches, yielding the conditional output shape [1,5,7] for seven output channels and one spatial result per patch. [execution; call_8e1661a487fa4e05b668f9dd51dc603a]

## Authoring-time findings — pending review

### conv-output-dtype-unused (suspected; defect)

Conv accepts output-dtype controls but neither forward branch applies them.

Trigger: A direct caller supplies constructor-level or forward-call out_dtype different from the convolution result dtype.

Expected: The returned tensor honors the requested output dtype, following the neighboring LayerNorm interface.

Actual: The constructor stores self.out_dtype, but forward reads neither dtype option and returns the reshaped convolution result unchanged.

Locations: 9bde46e775df21d54d78a0fbe78b1490bf311a5a:exllamav3/modules/conv.py — Conv.forward

Source evidence: call_b6150991f10d4f5bb9af12703e85dde8, call_4a629b63fde44d7c8a5bfe5e74dd452e, call_b0d7c997e28940c1a639e23c593836bd

source_inspection: Compared the new constructor and both forward branches with LayerNorm's explicit output conversion. The whole-parent-tree Conv( search found no callers, and the task adds only the class and package export, so the demonstrated reach is the newly exposed direct-call API, not an existing model workflow. [call_b6150991f10d4f5bb9af12703e85dde8, call_4a629b63fde44d7c8a5bfe5e74dd452e, call_b0d7c997e28940c1a639e23c593836bd, call_1629b4592ada4822953f44b5eaefbcbb]. Limits: No runtime dtype test was performed; external or dynamically constructed callers were not established.

## Uncertainty and limits

No PyTorch convolution, repository implementation, GPU test or model integration test was executed. The scalar check validates layout arithmetic only.

Checkpoint shape compatibility, input contiguity for the 3D view, and device/dtype compatibility are not validated by Conv itself; successful execution depends on suitable caller inputs and loaded tensors.

Existing get_tensor call sites were searched, but only the closely matching LayerNorm loading pattern and portions of the loader were inspected in detail; loader-wide compatibility is not established.
