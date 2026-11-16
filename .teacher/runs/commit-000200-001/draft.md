# f45eb4ce2090ca5db306cf863ee2f1826810e0ff


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/f45eb4ce2090ca5db306cf863ee2f1826810e0ff) · [Evidence ledger](draft.json)

Adds standalone Q/K LayerNorm before RoPE and broadcast affine weights, while introducing a suspected RMSNorm dispatch regression and leaving the alternative LayerNorm method unchanged.

- [Separate Q/K LayerNorm from RMSNorm fusion](#attention)

## Problem

Attention assumed Q/K normalization was RMSNorm, including RMS-specific attributes and fused RoPE weights. LayerNorm also restricted affine parameters to the final-axis shape. [source; call_81e120b6387d453895eed06ae1885fd5, call_61111e7c3fd74ad186a62e825d48343e]

## Reasoning

The edits are coupled: LayerNorm weights are excluded from RMS-only fusion, separate normalization moves before RoPE, and multidimensional affine weights are applied after final-axis normalization. [source; call_f9b28db36adf4c95b9ac6387ca01cda6, call_af9e1a3871fe46e482d3543ba852e6f7]

## Impact

Adds a reusable Q/K LayerNorm path to all three attention backends without wiring a model architecture to it. The new dispatch condition also introduces a suspected regression for loaded RMSNorm weights. [source; call_f9b28db36adf4c95b9ac6387ca01cda6, call_3536a727487c416d91b68f207772f3a7]

## Source Notes

Read the LayerNorm introduction, normalization-fusion entry and head-norm parameter repair. They establish the previous identical LayerNorm forward methods, fused RMSNorm interface and inherited native reduction/bounds concerns. [ancestor; call_a35331d04eb94171ac34860416c968d8, call_8bac54b53894451eb6549aff917ef0b8, call_1ea35df655064473987bd91797dac5a4]

Issue #16, “RuntimeError: CUDA error: invalid configuration argument,” reports conversion failure attributed in discussion to tokenizer truncation. Issue #7, “quantizing model: undefined symbol: __cxa_call_terminate,” concerns extension loading; #29, “Auto-YaRN for Qwen3? Maybe even set it dynamically?”, concerns scaling policy. Their relationship to this task is inferred solely from attention/rope source-path overlap, not evidence that QK LayerNorm addresses those reports. [inference; call_6e47bc917f364256a9bc44a2855930a5, call_a20cf0ee47264197ba8227b2ed78fe46, call_a040d7b6aefc455fad634514372c85c0]

<a id="attention"></a>

## Separate Q/K LayerNorm from RMSNorm fusion

Attention now accepts RMSNorm or LayerNorm for Q/K. It still requires K norm when Q norm is supplied. RMSNorm retains epsilon equality checking and constant weight bias; the LayerNorm branch copies Q's layernorm_eps and sets the fused weight offset to zero. Separate calls use each LayerNorm object's own epsilon, so they do not require equal Q/K epsilon. [source; call_f9b28db36adf4c95b9ac6387ca01cda6, call_61111e7c3fd74ad186a62e825d48343e]

load exposes normalization tensors to RoPE only for RMSNorm. For LayerNorm they remain None. Each decode route reshapes Q/K to batch × sequence × heads × head_dim, normalizes separately when RoPE is absent or no fused normalization tensor is available, then applies rotation. V is not normalized. Existing standalone calls without RoPE already supplied params and requested half output; the new calls retain that preparation. [source; call_f9b28db36adf4c95b9ac6387ca01cda6, call_81e120b6387d453895eed06ae1885fd5]

RoPE.apply forwards optional weights to a native kernel implementing RMS normalization, not centered LayerNorm. The wrapper requires half Q/K; native fused Q weights must be one-dimensional and head_dim long. Keeping LayerNorm outside this kernel avoids applying the wrong normalization formula and permits per-head affine weights, at the cost of separate operations; no speed comparison was measured. [source; call_49a9766d2979437bb0291834abf603d2, call_0c9644bbea9a4b6d84c07f5bf8a5caf7, call_f9b28db36adf4c95b9ac6387ca01cda6]

LayerNorm.forward preserves the existing F.layer_norm call for rank-one weights. Otherwise it normalizes only the final axis without affine parameters, multiplies by w and optionally adds b. Thus a heads × head_dim weight can broadcast across batch and sequence without normalizing across heads. Loading, optional bias, cached float32 copies and final dtype selection are unchanged. [source; call_af9e1a3871fe46e482d3543ba852e6f7, call_61111e7c3fd74ad186a62e825d48343e]

A scalar transcription with two heads [1,3] and [2,6], separate affine rows and epsilon 1e-5 produced approximately [-1,3] and [-1,7]. This illustrates final-axis normalization followed by head-specific affine transformation, not normalization across the combined head axes. [execution; call_8e18f1e5ce694e69bc5bde67e57eb8fc]

Explicit Q/K norm builders remain RMSNorm in Qwen3, Qwen3 MoE and Gemma3; Gemma3 retains its unit weight offset. Cohere and Cohere2 construct LayerNorm only for block input and final normalization, not Q/K. Their existing rank-one-weight path is unchanged. ParallelDecoderBlock consumes input_norm through forward; TransformerBlock likewise calls forward for its norms. No LayerNorm subclass or forward_torch caller appeared in the whole-tree searches. [source; call_3536a727487c416d91b68f207772f3a7, call_f0fc19cc0d5c4f23ace5061dccb93201, call_743b2a3aeed64a8081906b0ac41d10dc, call_b2e9a145dda74a84980b0515fe9ec5ab, call_f5ca95cd32eb4b87bb027c5fcf5ebcb3, call_6fb6c7d5cded4ba298947e3ef092ba4f, call_8553087c26864e0a8b54f152a017f173, call_2efb7a90b9104f37ae44ea1cd348a13a, call_dbbd38c976f94b62b073f7098bc8c10f]

The earlier parameter-overwrite defect remains removed: defaults are still confined to attention without head norms. Native reduction and padded-read concerns remain unchanged in rope.cu. LayerNorm bypasses native normalization, but still uses native rotation; the new RMSNorm truth-value failure can prevent ordinary Attention calls from reaching the fused kernel. [source; call_81e120b6387d453895eed06ae1885fd5, call_f9b28db36adf4c95b9ac6387ca01cda6, call_0c9644bbea9a4b6d84c07f5bf8a5caf7]

## Authoring-time findings — pending review

### tensor-truth-dispatch (suspected; defect)

The fallback condition tests an RMSNorm weight tensor's truth value rather than its presence.

Trigger: Loaded Attention with RoPE, Q/K RMSNorm and a weight tensor containing more than one element.

Expected: Skip standalone normalization and use the existing fused RMSNorm/RoPE path.

Actual: Each decode method evaluates not self.q_norm_tensor, which requests an ambiguous multi-element tensor truth value before RoPE. Attention.forward directly dispatches to these methods; Qwen3, Qwen3 MoE and Gemma3 supply the relevant norm objects. No-norm, no-RoPE and LayerNorm cases short-circuit differently.

Locations: f45eb4ce2090ca5db306cf863ee2f1826810e0ff:exllamav3/modules/attn.py — Attention.decode_sdpa_nc / decode_flash_attn_nc / decode_flash_attn

Source evidence: call_f9b28db36adf4c95b9ac6387ca01cda6, call_81e120b6387d453895eed06ae1885fd5, call_3536a727487c416d91b68f207772f3a7, call_de718a78310845569573d04f86eded4f, call_4a1e27c24e264f10ac44f1b090c22593

source_inspection: Traced load's tensor assignment, all three changed conditions, forward dispatch and explicit model norm builders. [call_f9b28db36adf4c95b9ac6387ca01cda6, call_f0fc19cc0d5c4f23ace5061dccb93201, call_743b2a3aeed64a8081906b0ac41d10dc, call_b2e9a145dda74a84980b0515fe9ec5ab]. Limits: No PyTorch execution reproduced the exception.

### layernorm-reference-shape (suspected; external_compatibility)

forward_torch retains the old affine-shape contract.

Trigger: Call LayerNorm.forward_torch with multidimensional weights newly supported by forward.

Expected: Provide the same final-axis normalization and broadcast affine transformation as forward.

Actual: forward_torch still passes the multidimensional weight directly to F.layer_norm with a one-axis normalized_shape. It lacks the new broadcast path. Whole-tree search found no repository caller, so the observed reach is the alternative method interface, not demonstrated production execution.

Locations: f45eb4ce2090ca5db306cf863ee2f1826810e0ff:exllamav3/modules/layernorm.py — LayerNorm.forward_torch

Source evidence: call_61111e7c3fd74ad186a62e825d48343e, call_af9e1a3871fe46e482d3543ba852e6f7, call_dbbd38c976f94b62b073f7098bc8c10f

source_inspection: Compared both methods with the complete LayerNorm diff and searched for alternative-method callers. [call_61111e7c3fd74ad186a62e825d48343e, call_af9e1a3871fe46e482d3543ba852e6f7, call_dbbd38c976f94b62b073f7098bc8c10f]. Limits: No external caller or Torch shape-error execution established.

### inherited-native-normalization-and-bounds (suspected; defect)

Inherited native reduction and padded-input-read concerns are carried over.

Trigger: Direct fused RoPE normalization with nonuniform lane values; or rotation with padded head width, such as 80, or shorter partial-rotary frequencies.

Expected: Store one complete sum per warp and avoid input reads beyond logical frequency/weight arrays.

Actual: Every lane writes its shuffle-down result to one shared sum slot. inv_freq[t] and normalization half2 weight loads lack padding guards. The existing test directly reaches this kernel with width 80 and normalization on/off, bypassing Attention's new dispatch failure. LayerNorm avoids the normalization-specific operations but not the frequency read.

Locations: f45eb4ce2090ca5db306cf863ee2f1826810e0ff:exllamav3/exllamav3_ext/rope.cu — rope_kernel

Source evidence: call_0c9644bbea9a4b6d84c07f5bf8a5caf7, call_a102f58c6b974a12b3462d2158a86192, call_16681d15cad341f4a0b6f1c220865264, call_f9b28db36adf4c95b9ac6387ca01cda6

source_inspection: Compared unchanged native code with its reduction helper, wrapper, direct test caller and task diff. [call_0c9644bbea9a4b6d84c07f5bf8a5caf7, call_a102f58c6b974a12b3462d2158a86192, call_16681d15cad341f4a0b6f1c220865264]. Limits: No GPU race detection or observed memory fault.

scalar_transcription: Computed 64 launched x lanes for width 80, versus 40 full-width frequency entries. [call_8e18f1e5ce694e69bc5bde67e57eb8fc, call_0c9644bbea9a4b6d84c07f5bf8a5caf7]. Limits: Integer launch arithmetic only, not kernel execution.

## Uncertainty and limits

No PyTorch, CUDA kernel, model inference or repository tests were executed. Tensor truth-value and shape failures are source-based observations, not reproduced exceptions.

The scalar calculation uses Python double precision, not the implementation's half-precision intermediate operations, broadcasting machinery or GPU scheduling.

Whole-tree literal searches identify explicit consumers, not dynamic or external callers. No checkpoint-level validation or performance measurement establishes model compatibility or overhead.
