# c3049627ea2cdbe7f0c8e62e2491e4eed8d37072


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/c3049627ea2cdbe7f0c8e62e2491e4eed8d37072) · [Evidence ledger](draft.json)

Llama and its constructor-sharing subclasses now keep gate and up results in FP32 through SiLU multiplication. The activation still narrows to a clamped FP16 buffer before the already-FP32 down output; GPU accuracy and performance were not measured.

- [Keep Llama gate and up results in FP32 through the SiLU product](#llama-mlp-precision)

## Problem

Llama already requested FP32 down-projection output, but its gate and up projections still defaulted to FP16. That left two earlier points where large values could overflow: when the projection results were stored and when the half-precision activation kernel multiplied them. Widening the down result cannot recover information lost at either point. [inference; call_e907cc92edd04f99a4e4c314ec8f82ca, call_5b327eb2c1214630bf4c89e508ed6d64, call_23714e7b39634627b82817999a30fe42, call_9256c7f2aaee4211908f1e80574479e5, call_33b6a619704a4d7b9ead0f34eb946152]

## Reasoning

The one-line change sets interm_dtype=torch.float on every GatedMLP built by LlamaModel. That setting controls both gate and up result buffers. Their FP32 outputs select the existing float SiLU-multiply kernel, which computes the product in float, converts it to half, and clamps the converted result. The down projection still consumes half and produces float. The earlier change that gave GatedMLP a separate half activation destination is a precondition for this path: writing into the float up buffer would fail the wrapper's output-dtype check. [source; call_58019fda08954b92a5adaafcffd33f5e, call_5b327eb2c1214630bf4c89e508ed6d64, call_33b6a619704a4d7b9ead0f34eb946152]

## Impact

The change also reaches MiMoModel, MistralModel and Qwen2Model: each registered subclass calls LlamaModel.__init__ without replacing its MLP construction. It does not change GatedMLP's default or other models' independent constructor calls. [source; call_58019fda08954b92a5adaafcffd33f5e, call_23f9af2cd8024772a99fdb09f7259900, call_ec31d1d50bb8442099330473284e7ff2, call_2aec31f72d384458956c8e13c9b361a8, call_84cb45660be24a7eb65c020fdcdcc272, call_4823308473114af1a83c859792483f55, call_5b327eb2c1214630bf4c89e508ed6d64, call_98da4dadbdaa440c950fd7b088b1ed8e]

The tradeoff is wider gate and up temporaries and a different arithmetic path, not larger checkpoint weights or an FP32 down-projection input. Saturation bounds the half result at the activation boundary; it does not preserve products beyond half range exactly or establish that every source of nonfinite values is removed. [inference; call_58019fda08954b92a5adaafcffd33f5e, call_5b327eb2c1214630bf4c89e508ed6d64, call_6922c997f0f14fecac0066b4cc7ebddd, call_33b6a619704a4d7b9ead0f34eb946152]

## Source Notes

The initial architecture entry describes the shared Llama constructor and the Mistral window-mapping gap. The earlier Llama down-overflow entry explains why out_dtype was set to float independently of interm_dtype. The FP32 activation introduction and GatedMLP destination-fix entries document the half-output requirement, the earlier incompatible in-place destination, and the inherited odd-element tail. [ancestor; call_77e81bbc18e6499fa696d92a11099929, call_560b8ace448744d3bace9f709a54729a, call_37609bae414e4033bc5110c70c667e2b, call_961dff6c966a4414961e31a86a95fc37]

In #52, “Error converting moonshotai/Kimi-Dev-72B,” artus-dev reported Qwen2 conversion failures and a NaN at head calibration. Task author turboderp suggested setting out_dtype=torch.float on this same Llama GatedMLP call, and artus-dev reported that the suggestion worked. The concrete connection is the shared constructor and its separate precision settings: that report concerns out_dtype, which is already present in this task's parent, not the new interm_dtype setting. It is not a test of this change. [inference; call_17cddb3dd6944a6cb897319bbe0b2783, call_e907cc92edd04f99a4e4c314ec8f82ca, call_4823308473114af1a83c859792483f55, call_58019fda08954b92a5adaafcffd33f5e]

#34, “torch._C._LinAlgError on last layer of quant,” reports Command-A conversion with infinities at the input to the MLP down projection and discusses activation clamping. #53, “Command A support,” starts as a support request and later reports similar infinities and factorization errors. These are relevant by analogy to the activation-to-down boundary changed here, not evidence about Llama or about why this commit was made. #42, “converting to 3.0 bpw causes error; block state has 0 inf values and 34 NaN values,” reports a Midnight-Miqu failure at head calibration and includes a separate Command-R+ report; the shared calibration symptoms do not locate the first nonfinite value at gate/up. [inference; call_2a83f02b626c4318a4aff7008a8d5b58, call_6d1cf1f38e5a442ba56eb68475462e4a, call_b329c33faec44073967fe864f4f0fe4f, call_8fcdadf5bd88494d80fca7eb202de947, call_610646c3ff634ded97ccaa0ef84c306c, call_6922c997f0f14fecac0066b4cc7ebddd, call_5b327eb2c1214630bf4c89e508ed6d64]

Closed #16, “RuntimeError: CUDA error: invalid configuration argument,” shares the Llama architecture and Linear capture code, but its reported traceback is in attention Q projection before the MLP, and the discussion attributes it to tokenizer truncation. Closed #57, “Batch process interrupted,” names a Qwen2.5 model but reports Windows job creation and virtual-memory pressure before generation. #33, “Error converting model,” reports a Qwen3 conversion failure opening a file during checkpoint compilation. Neither the model-family overlap nor the shared conversion context identifies an FP32-intermediate fix for these reports. [inference; call_825192cf22f44e02b1184580291d2373, call_c0acc57648d74312aaad717f14a49be9, call_218043c676df46c7bfa6f3bb136c7474, call_b4cdd1d0793743d2882cdcf8fb2a4178, call_eb4b52270f88469e95e0e0e43397ebac, call_66f4a3870a6e414bbab06a519e0c21d8, call_58019fda08954b92a5adaafcffd33f5e]

The whole-parent-tree search for LlamaForCausalLM found the repository architecture declaration and references to the Transformers class embedded in a calibration corpus. Those corpus references are not calls to ExLlamaV3's LlamaModel constructor. [source; call_3f67b6da11e5433aafb02fdd5e574bc0, call_e907cc92edd04f99a4e4c314ec8f82ca]

<a id="llama-mlp-precision"></a>

## Keep Llama gate and up results in FP32 through the SiLU product

TransformerBlock supplies half-normalized input to the MLP. GatedMLP passes interm_dtype to the gate and up Linear modules for each slice, but passes its separate out_dtype to the down Linear. The activation result goes to the down projection, slice results are summed if needed, and the block adds the MLP result to its residual. Neither the normalization dtype nor that residual interface is edited. [source; call_58019fda08954b92a5adaafcffd33f5e, call_5b327eb2c1214630bf4c89e508ed6d64, call_66f4a3870a6e414bbab06a519e0c21d8]

Linear passes the requested result type to its ordinary-weight and EXL3 backends, including when conversion replaces the former with the latter. With half input, LinearFP16 used the same-dtype torch.matmul branch for the old half result; it now selects hgemm, whose float-output branch requests FP32 compute and output from cuBLAS with two half operands. LinearEXL3 allocates the requested result in both routes: reconstruction uses hgemm and an output transform, while direct EXL3 GEMM passes a float-output flag to its kernel selector. The existing EXL3 rule to reconstruct above 32 flattened rows unless overridden is unchanged. [source; call_6922c997f0f14fecac0066b4cc7ebddd, call_23714e7b39634627b82817999a30fe42, call_02daf8b5ac5b4a05ae3dfdadf18c088c, call_9256c7f2aaee4211908f1e80574479e5, call_800de2e29fa144daa666249b65651920]

Before and after the edit, Llama allocates a separate half destination: the old None setting and the new float setting both differ from torch.half. Only an explicitly half configuration can reuse the up buffer in place. The old SiLU kernel uses half2 arithmetic; the float-input kernel computes g/(1+exp(-g)) times u in float, then narrows and clamps to ±65,504, the largest finite binary16 magnitude. This moves the half-storage boundary without promoting the down projection's input. [source; call_58019fda08954b92a5adaafcffd33f5e, call_5b327eb2c1214630bf4c89e508ed6d64, call_33b6a619704a4d7b9ead0f34eb946152]

For TinyLlama-1.1B-Chat-v1.0, the pinned config declares LlamaForCausalLM, SiLU, 22 layers, hidden width 2,048 and intermediate width 5,632. This is below the 55,296-channel default slicing threshold and already aligned to the 128-channel padding unit. In all 22 layers the header contains model.layers.<i>.mlp.gate_proj.weight and up_proj.weight as [5632,2048] and down_proj.weight as [2048,5632], all BF16. No MLP bias, inverse scale or EXL3 tensor group is present, so Linear takes the ordinary-weight branch, with neither optional bias nor scaling. The unsliced constructor supplies no alternate or fused MLP key, and there are no extra MLP tensors in this header. The patch adds no tensor lookup and does not derive the runtime result dtype from the checkpoint's BF16 declaration. [source; call_b1c74e7dcd364b43b0676a34b4bd9c0d, call_ad6bad18f0b94d0980e0d6b80e807a83, call_36c45f06102a4064a7cac2edd63a393d, call_5b327eb2c1214630bf4c89e508ed6d64, call_6922c997f0f14fecac0066b4cc7ebddd, call_58019fda08954b92a5adaafcffd33f5e]

The inspected Mistral-7B-v0.1 and Qwen2.5-0.5B configs also select SiLU and fit a single MLP slice: hidden/intermediate widths are 4,096/14,336 and 896/4,864 respectively. Their subclass constructors inherit the same runtime dtype settings. Unlike the initial architecture entry's historical factory description, the inspected parent configs explicitly supply their respective model subclasses; the change reaches them through their super calls. [source; call_bce8f22ff25d465eb35fdd6126a5d5bb, call_0ca3f54c14bb42a28d3a7cb137bb6804, call_84cb45660be24a7eb65c020fdcdcc272, call_4823308473114af1a83c859792483f55, call_e907cc92edd04f99a4e4c314ec8f82ca, call_36c45f06102a4064a7cac2edd63a393d, call_58019fda08954b92a5adaafcffd33f5e]

A standard-library check computed gate + up + activation storage per TinyLlama token as 33,792 bytes before and 56,320 bytes after, using two projection buffers and one half destination. It decoded the half finite limit as 65,504 and illustrated saturation with gate=up=400: the idealized product was 160,000, outside finite half range. These are storage arithmetic and a scalar illustration, not GPU measurements. [execution; call_e7fc11ba1cea4170a5c8b6064cec5dc3, call_b1c74e7dcd364b43b0676a34b4bd9c0d, call_5b327eb2c1214630bf4c89e508ed6d64, call_33b6a619704a4d7b9ead0f34eb946152]

## Authoring-time findings — pending review

### inherited-odd-activation-tail (suspected; defect)

The half-destination mismatch was already removed before this change, but the activation kernels still have no scalar tail. The new Llama dtype selection changes which kernel runs, not how many elements it covers.

Trigger: Call silu_mul or gelu_mul with otherwise suitable odd-length buffers, or reach that call through a custom GatedMLP with an odd total intermediate element count and padding disabled, for example with pad_to=1.

Expected: Every destination element receives its gated product.

Actual: Both kernels stop at numel/2 complete pairs. The last element of a separate destination is unwritten; an aliased half up buffer retains its ungated final element.

Locations: c8ed45c6152fd6050a2a3f2f9035120fac35cb94:exllamav3/exllamav3_ext/activation.cu — act_mul_kernel_f / act_mul_kernel_h, c8ed45c6152fd6050a2a3f2f9035120fac35cb94:exllamav3/modules/mlp.py — GatedMLP.forward

Source evidence: call_58019fda08954b92a5adaafcffd33f5e, call_33b6a619704a4d7b9ead0f34eb946152, call_5b327eb2c1214630bf4c89e508ed6d64, call_720b06e6ce0548c89de0922b568a6d00

source_inspection: The direct Python activation consumers found are GatedMLP and BlockSparseMLP. TransformerBlock and ParallelDecoderBlock are broader callers through self.mlp.forward; the default Llama constructor retains 128-channel padding, so its normal path does not exercise the odd tail. [call_720b06e6ce0548c89de0922b568a6d00, call_31fe72e34cc84f039f9f92098ee9d10d, call_66f4a3870a6e414bbab06a519e0c21d8, call_5b327eb2c1214630bf4c89e508ed6d64, call_6922c997f0f14fecac0066b4cc7ebddd]. Limits: No inspected checkpoint is shown to trigger the odd-length path.

scalar_transcription: Enumerated two elements per thread, 256 threads per block and the integer pair guard. Sizes 1, 3, 129 and 513 lost exactly the last element; 128, 512 and 5,632 were fully covered. [call_6b2a58c7d09b4123bddf20a58e3bf6be, call_33b6a619704a4d7b9ead0f34eb946152]. Limits: Integer indexing model only; no CUDA launch or memory access.

### inherited-mistral-window-omission (suspected; defect)

The shared constructor still does not propagate Mistral's configured sliding window. The edit to MLP precision leaves this earlier observation unchanged.

Trigger: Construct MistralModel with the inspected Mistral-7B-v0.1 config, which declares sliding_window=4096.

Expected: Attention receives the configured window of 4,096.

Actual: Mistral delegates to LlamaModel, whose Attention constructor omits the argument, leaving the -1 default.

Locations: c3049627ea2cdbe7f0c8e62e2491e4eed8d37072:exllamav3/models/llama.py — LlamaModel.__init__, c8ed45c6152fd6050a2a3f2f9035120fac35cb94:exllamav3/models/mistral.py — MistralModel.__init__

Source evidence: call_bce8f22ff25d465eb35fdd6126a5d5bb, call_84cb45660be24a7eb65c020fdcdcc272, call_e907cc92edd04f99a4e4c314ec8f82ca, call_e6f0ffdceb88470fabd901d9a64dead7, call_58019fda08954b92a5adaafcffd33f5e

source_inspection: Checked the parent-tree LlamaModel references, the Mistral subclass's direct super call, the pinned config and Attention's default against the one-line task diff. [call_23f9af2cd8024772a99fdb09f7259900, call_84cb45660be24a7eb65c020fdcdcc272, call_bce8f22ff25d465eb35fdd6126a5d5bb, call_e907cc92edd04f99a4e4c314ec8f82ca, call_e6f0ffdceb88470fabd901d9a64dead7, call_58019fda08954b92a5adaafcffd33f5e]. Limits: Configuration propagation only; no attention output or runtime comparison was measured.

## Uncertainty and limits

No repository model, CUDA kernel, conversion job or generation workload was run. The evidence establishes which buffers and code paths change, not a specific author's failure case, a quality or speed improvement, or a measured peak-memory cost.

The scalar checks model buffer sizes, an idealized SiLU product and pair indexing. They do not reproduce CUDA's approximate exponent and division, half intrinsics, GEMM arithmetic or allocator behavior.

Checkpoint-header validation was limited to the directly edited Llama architecture's TinyLlama reference. The reach to other architectures follows from source inheritance, not fresh checkpoint validation of every subclass.

Literal caller searches cover named repository sites, not dynamic dispatch aliases or external callers.
