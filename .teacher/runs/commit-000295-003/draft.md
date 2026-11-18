# 69f8f9a07b95142878997f79e0053b1c1e08422f


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/69f8f9a07b95142878997f79e0053b1c1e08422f) · [Evidence ledger](draft.json)

Clamps FP32-input gated activation products after FP16 conversion. Only Ernie 4.5 MoE routed experts select this path among inspected shipped builders; half-input activations and inherited caller/tail limitations remain unchanged.

- [Saturate narrowed FP32 gated activations](#runtime)

## Problem

FP32-input gated activations previously converted their products directly to FP16 without saturation. This change adds a clamp at that narrowing boundary, rather than clamping every activation implementation. [source; call_95c8a3e34cd04a39b9905b1bab39d6d0, call_cad4197b43824f4aa84059afc112ae9e]

## Reasoning

The immediate parent enabled FP32 routed-expert intermediates in Ernie 4.5 MoE. Together, the two changes retain wider gate/up results through activation multiplication and then bound the narrowed activation supplied to down projection. Their complementary numerical purpose is inference, not a measured accuracy result. [inference; call_929a8a04da8a4dad858841e24c4eaedb, call_79db9a744512496f976bd3ea6e5ff121, call_dd6e44356ad74741bbbaadf005fbb4d9, call_95c8a3e34cd04a39b9905b1bab39d6d0]

## Impact

Among the inspected shipped constructors, only Ernie4_5MoEModel's routed experts select the changed FP32-input kernel. Its ordinary and fused expert paths can both reach it. Dense Ernie, Ernie MoE's dense/shared experts, and every other located gated-MLP builder retain half inputs and therefore do not gain this saturation. [source; call_83b59a5f5b98411ebd64f5a8140e9c96, call_508f0ef43f564d80b9250131fb63ba70, call_dd6e44356ad74741bbbaadf005fbb4d9, call_cad4197b43824f4aa84059afc112ae9e]

## Source Notes

Read the FP32 activation introduction entry d97bfdf, the FP32 linear-output entry e9a3b6a, the padding-control entry 3637103, and immediate-parent entry 6f9928b. They record the reused precision boundary, incompatible in-place FP32 destination, odd-element tail, and conditional fused-expert contracts. [ancestor; call_f51890cfc6d94715ade04ad124d68704, call_ce1b50886c8b43d193b46a3ad0126dd8, call_58cc16e98cf24dc7b792214460180384, call_b7c19991cd3344368c512b5d071e1b0c]

Issue #34, “torch._C._LinAlgError on last layer of quant,” reports Command-A conversion failure; turboderp suggests activation clamping as a possible remedy. Its connection to this task is inference from that explicit suggestion and the saturation diff. It is not evidence this patch fixes Command-A: the inspected Cohere2 builder still selects half-input activation. [inference; call_33d3868d1a6048c2b7edd1841aacd784, call_83b59a5f5b98411ebd64f5a8140e9c96, call_95c8a3e34cd04a39b9905b1bab39d6d0]

Other numerical reports are background, not established fixes: #42, “converting to 3.0 bpw causes error; block state has 0 inf values and 34 NaN values,” concerns Midnight-Miqu and Command-R+; #52, “Error converting moonshotai/Kimi-Dev-72B,” discusses widening MLP down outputs; #53, “Command A support,” starts as a support request and later reports conversion failures; #58, “linalg.cholesky error converting OpenBuddy (Qwen3) 32B QAT,” reports NaNs. Their inferred association is shared Linear/GatedMLP conversion paths and overflow themes, not demonstrated reach of this FP32-only clamp. [inference; call_1ea932d748794649b7e36f723956f477, call_e78256c32e824bb2b61be2d4adac620c, call_74953df2ecd341acbafc479b2c7a748a, call_721ae6020bba47b4aa2b8dc94dd31965, call_24c03a0b488b4cb0957e5682fad9fa11, call_83b59a5f5b98411ebd64f5a8140e9c96]

The other inspected reports concern different failures: #55, “Possible GLM4 32B regression,” reports a LinearFP16 loading TypeError; #48, “`RuntimeError` when requesting logprobs with Gemma 3 models,” reports mismatched vocabulary dimensions; #31, “TypeError with presence penalty,” concerns sampler arguments; #7, “quantizing model: undefined symbol: __cxa_call_terminate,” concerns extension loading. None identifies activation saturation as its established remedy. [source; call_883e8fd7dbd14075b4531978a061eb41, call_df718b12bd9741ed88fe472fa6511751, call_bab993f66109402a986d03dc8b8b3135, call_9a9d685696ac4804b667d402d676aad1]

<a id="runtime"></a>

## Saturate narrowed FP32 gated activations

act_mul_kernel_f computes SiLU or tanh-approximate GELU on each FP32 gate value, multiplies by the FP32 up value, and converts the pair using __float22half2_rn. The new helper then applies __hmin2 with +65504 and __hmax2 with −65504 before storing half2. Thus the clamp operates after conversion, not on FP32 inputs or before their product. [source; call_cad4197b43824f4aa84059afc112ae9e, call_95c8a3e34cd04a39b9905b1bab39d6d0]

The bounds are binary16's largest finite magnitudes: (2−2^-10)×2^15 = 65504. A bounded scalar model preserved a product of 100, changed modeled positive overflow from infinity to 65504, and negative overflow to −65504. This illustrates saturation rather than recovery of the original magnitude. [execution; call_d818028825df4b4bb568f6cacc2435b6]

Both silu_mul and gelu_mul dispatch from x.dtype(): float requires float y and selects act_mul_kernel_f; otherwise both inputs must be half and select act_mul_kernel_h. Both require half z. Only the float kernel changes. Half-input activation/multiply, standalone activation helpers, and the non-gated MLP's PyTorch activations receive no clamp. [source; call_cad4197b43824f4aa84059afc112ae9e, call_95c8a3e34cd04a39b9905b1bab39d6d0, call_b5fcde59f83040a1ad9f1b7dadfdd13e]

The controlling module argument is interm_dtype, passed as out_dtype to gate/up Linear projections; the MLP's out_dtype instead controls down outputs. LinearFP16 and LinearEXL3 resolve unspecified projection output dtype to torch.half, so an FP32 down output alone does not select the changed activation kernel. [source; call_b5fcde59f83040a1ad9f1b7dadfdd13e, call_dd6e44356ad74741bbbaadf005fbb4d9, call_3836a6c670b34b46a2d4a47684eebadf, call_508f0ef43f564d80b9250131fb63ba70, call_412e704766f04decb022af926bfbf985]

Constructor audit: Qwen3Model, Glm4Model and Ernie4_5Model explicitly pass half to GatedMLP. Dots1Model passes half to its dense, routed and shared modules. MixtralModel and Qwen3MoEModel pass half to BlockSparseMLP. Ernie4_5MoEModel passes half to dense-prefix and optional shared GatedMLPs but float to routed BlockSparseMLP. CohereModel, Cohere2Model, DeciLMModel, Gemma2Model, Gemma3Model, LlamaModel, Phi3Model, and both Mistral3 text/vision construction sites omit interm_dtype, retaining None and the backend half default. Each of these half/default sites is outside the changed kernel. [source; call_7a99094ccde447a5bd1b0b212f290e0d, call_2a2620c1dd414cdc9e8f0e48e9076e89, call_a9d51c5f8ba24dbf9d28893d9c3eacda, call_83b59a5f5b98411ebd64f5a8140e9c96, call_508f0ef43f564d80b9250131fb63ba70]

Every GatedMLP forward path, including slicing, supplies up tensor u as activation destination. Located shipped constructors produce half u, agreeing with the wrapper. A hypothetical float-intermediate GatedMLP still supplies float u as z and is rejected before kernel launch. The earlier entry's ordinary BlockSparseMLP mismatch has already been removed: its current ordinary expert path allocates separate half a whenever interm_dtype is not half. [source; call_b5fcde59f83040a1ad9f1b7dadfdd13e, call_dd6e44356ad74741bbbaadf005fbb4d9, call_cad4197b43824f4aa84059afc112ae9e, call_95c8a3e34cd04a39b9905b1bab39d6d0]

Ernie4_5MoEModel selects routed experts after its dense-prefix boundary. For multiple flattened tokens or experts not fully EXL3-quantized, ordinary evaluation passes float g/u and separate half a. For one flattened token with fully EXL3 experts, fusion writes float cfg.interm_g/interm_u and supplies separately allocated half cfg.interm_a. Both paths therefore meet the changed activation's dtype contract; half-configured sparse builders instead reuse up storage as activation output. [source; call_ed1d5179e9a449c8a807244fc2ab90a0, call_dd6e44356ad74741bbbaadf005fbb4d9, call_cad4197b43824f4aa84059afc112ae9e]

The widened Ernie argument was introduced by 6f9928b, this task's immediate parent, with no intervening commit. Its entry explains the separate half activation destinations and notes that widening alone cannot guarantee a representable half product. This clamp addresses that remaining narrowing boundary without changing routing, workspace precision or expert dispatch. [ancestor; call_b7c19991cd3344368c512b5d071e1b0c]

The immediate-parent diff and task metadata independently establish that adjacency. Source reach is therefore narrower than the commit message: Ernie 4.5 MoE routed activations can differ when narrowing reaches the bounds; other located builders cannot differ through this edit. This does not establish that any checkpoint actually produces such values. [source; call_929a8a04da8a4dad858841e24c4eaedb, call_79db9a744512496f976bd3ea6e5ff121, call_83b59a5f5b98411ebd64f5a8140e9c96, call_95c8a3e34cd04a39b9905b1bab39d6d0]

The inherited pair-processing condition remains: 256 threads each handle two elements, with ceil(numel/512) blocks and a numel/2 guard. No scalar tail or evenness check is added. Scalar enumeration leaves the final element unwritten at lengths 1, 3, 129 and 513, while covering 128 and 512 completely. [execution; call_d818028825df4b4bb568f6cacc2435b6, call_cad4197b43824f4aa84059afc112ae9e, call_95c8a3e34cd04a39b9905b1bab39d6d0]

Fusion still depends on native GEMM preconditions: exl3_mgemm accepts half input and half/float output, checks selected-index count against output expert planes, and rejects unavailable kernel shapes. The clamp does not remove these checks or repair the inherited all-expert capacity and workspace-backed return conditions. TransformerBlock directly forwards params and immediately adds the MLP result without an output-dtype override. [source; call_508f0ef43f564d80b9250131fb63ba70, call_dd6e44356ad74741bbbaadf005fbb4d9, call_2307a285e1db4d5983642e393857ac60, call_95c8a3e34cd04a39b9905b1bab39d6d0]

## Authoring-time findings — pending review

### inherited-fp32-gated-destination (suspected; defect)

GatedMLP's opt-in FP32 intermediate path remains incompatible with the activation destination contract.

Trigger: Construct GatedMLP with interm_dtype=torch.float and execute forward with otherwise valid inputs.

Expected: Supply a half activation destination before the down projection.

Actual: GatedMLP passes float u as both up input and destination; silu_mul or gelu_mul rejects z's dtype before reaching the clamp. No located shipped GatedMLP constructor enables this setting. BlockSparseMLP's ordinary path now uses a separate half destination and does not retain this mismatch.

Locations: 69f8f9a07b95142878997f79e0053b1c1e08422f:exllamav3/modules/mlp.py — GatedMLP.forward

Source evidence: call_b5fcde59f83040a1ad9f1b7dadfdd13e, call_cad4197b43824f4aa84059afc112ae9e, call_83b59a5f5b98411ebd64f5a8140e9c96, call_dd6e44356ad74741bbbaadf005fbb4d9, call_95c8a3e34cd04a39b9905b1bab39d6d0

source_inspection: Compared whole-tree constructor/caller searches, destination arguments and native dtype checks. [call_061b8d3de7e04883bde6a2dff8233a7b, call_d004e439fccd4fb281ce8cc9715b62e5, call_2307a285e1db4d5983642e393857ac60]. Limits: Conditional external or opt-in configuration; no CUDA execution.

### inherited-odd-activation-tail (suspected; defect)

Both activation kernels still omit an odd final element.

Trigger: Call either activation wrapper with an odd total element count; an unpadded odd-width GatedMLP can expose it.

Expected: Write activation(x)*y to every destination element.

Actual: Only complete pairs are processed. An in-place destination retains its final ungated up value; a separate destination's final element is unwritten. The new clamp cannot affect that element.

Locations: 69f8f9a07b95142878997f79e0053b1c1e08422f:exllamav3/exllamav3_ext/activation.cu — act_mul_kernel_h / act_mul_kernel_f

Source evidence: call_cad4197b43824f4aa84059afc112ae9e, call_95c8a3e34cd04a39b9905b1bab39d6d0, call_b5fcde59f83040a1ad9f1b7dadfdd13e

scalar_transcription: Enumerated the inspected launch and pair-index arithmetic for odd and even lengths. [call_d818028825df4b4bb568f6cacc2435b6]. Limits: Integer coverage model only; no GPU kernel execution or claim of failure for padded model dimensions.

### inherited-all-expert-fused-capacity (suspected; defect)

The immediate parent's conditional fused all-expert buffer mismatch persists.

Trigger: One flattened token, fully EXL3 experts, activate_all_experts=True, and num_experts greater than num_experts_per_tok.

Expected: Allocate capacity for all selected experts or use ordinary evaluation.

Actual: Routing returns all expert indices, but fused buffers retain num_experts_per_tok planes. Dispatch still selects fusion and the native index-count/output-plane check rejects the call before activation. TransformerBlock forwards params directly; this does not establish that every conversion workflow reaches the condition.

Locations: 69f8f9a07b95142878997f79e0053b1c1e08422f:exllamav3/modules/block_sparse_mlp.py — BlockSparseMLP.forward

Source evidence: call_dd6e44356ad74741bbbaadf005fbb4d9, call_508f0ef43f564d80b9250131fb63ba70, call_2307a285e1db4d5983642e393857ac60, call_95c8a3e34cd04a39b9905b1bab39d6d0

source_inspection: Compared routing count, allocation, dispatch and native shape check with the unchanged module caller. [call_d004e439fccd4fb281ce8cc9715b62e5, call_dd6e44356ad74741bbbaadf005fbb4d9, call_508f0ef43f564d80b9250131fb63ba70]. Limits: Conditional source path, not an executed conversion failure.

### inherited-fused-return-contract (suspected; behavior_change)

The fused sparse result remains workspace-backed and bypasses the ordinary path's output conversion.

Trigger: Retain a fused result across another fused call, or request a per-call output dtype different from the workspace dtype.

Expected: An independent result honoring the override, consistent with ordinary evaluation.

Actual: Fusion returns a view of cfg.out_d without to2; subsequent calls reuse that workspace. The inspected TransformerBlock immediately adds the result and supplies no override, so it does not demonstrate problematic retention or conversion.

Locations: 69f8f9a07b95142878997f79e0053b1c1e08422f:exllamav3/modules/block_sparse_mlp.py — BlockSparseMLP.forward

Source evidence: call_dd6e44356ad74741bbbaadf005fbb4d9, call_2307a285e1db4d5983642e393857ac60, call_95c8a3e34cd04a39b9905b1bab39d6d0

source_inspection: Compared both return branches and located decoder consumption. [call_dd6e44356ad74741bbbaadf005fbb4d9, call_d004e439fccd4fb281ce8cc9715b62e5, call_2307a285e1db4d5983642e393857ac60]. Limits: No tensor-lifetime execution test; inspected decoder callers do not exercise the incompatible usage.

## Uncertainty and limits

No CUDA kernel, extension build, checkpoint load, conversion, generation or benchmark was executed. Actual activation distributions, accuracy benefits and performance costs remain unmeasured.

The scalar illustration uses Python arithmetic and explicit half-storage modeling, not CUDA FP32 arithmetic, approximate transcendental instructions or half2 intrinsics. CUDA-version-specific NaN and signed-zero behavior of the min/max sequence is not established by the supplied documentation.

Whole-tree literal searches and AST inspection establish the located repository constructors, not dynamic aliases or external callers. Fused expert reach remains conditional on successful loading and compatible GEMM kernels.
