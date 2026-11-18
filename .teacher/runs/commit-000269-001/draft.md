# 13fa9ca2cf41d1383e00ff2775cb4683d6db15ea


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/13fa9ca2cf41d1383e00ff2775cb4683d6db15ea) · [Evidence ledger](draft.json)

Honors configured expert down-output precision and repairs BlockSparseMLP's FP32 activation destination, while leaving an ordinary-path accumulation dtype mismatch and inherited fused-path limitations.

- [Separate intermediate, activation and down-output precision](#block-sparse-mlp)

## Problem

Expert down projections hard-coded half output despite BlockSparseMLP accepting out_dtype. The ordinary expert path also reused FP32 intermediates as the activation destination, although the native activation requires a half destination. [source; call_3d66b702a6ee480bbd95944ec4cd6e93, call_f441f743f32d49d6b3d6bcbf6dc94e70, call_aa48198966f0407d8f03be22a2931208]

## Reasoning

The edits establish separate precision boundaries: gate/up results may be FP32, the activated product must be FP16 for the down projection, and the down projection may produce the configured output dtype. Changing down output alone would not repair the incompatible activation destination. [source; call_3d66b702a6ee480bbd95944ec4cd6e93, call_aa48198966f0407d8f03be22a2931208, call_8626b9c13b1c4c7abe0308c601fdf79d]

## Impact

Mixtral explicitly requests half intermediates and half output, so its configured precision remains unchanged. Qwen3Moe requests half intermediates and float output; its ordinary down projections now honor that float setting. Neither constructor supplies shared experts. [source; call_acea9b63efe545bcbaa9fc51dd8662b6, call_350694fd7450481fbb844b87a49e055c, call_3d66b702a6ee480bbd95944ec4cd6e93]

The ordinary path still accumulates into zeros_like(input), without adapting that buffer to the down-output dtype. Successful FP32-output execution through that path is therefore not established by this change. [source; call_f441f743f32d49d6b3d6bcbf6dc94e70, call_3d66b702a6ee480bbd95944ec4cd6e93]

## Source Notes

The original BlockSparseMLP entry records the all-expert fused-buffer mismatch. The shared-expert entry records an unreachable fused shared contribution. The mixed-mode activation entry records the incompatible FP32 in-place activation caller. [ancestor; call_3419605fe6ee4d05a28c1c5cf0400aae, call_f72aac4358fa43fbb2d64e6843b2c75a, call_0283eb6ad0a34184ad7ebda737e91ffd]

Issue #43, “Error converting abliterated Qwen3 mlabonne/Qwen3-30B-A3B-abliterated,” reports invalid calibration states and Cholesky failure. Its association here is inference from the Qwen3 sparse model and BlockSparseMLP log, not evidence that this commit addresses that report. [inference; call_2d412db67dc94eb89f013032fc771e46, call_3ea6598891054f10993a4a95d3f44752, call_350694fd7450481fbb844b87a49e055c]

Issue #34, “torch._C._LinAlgError on last layer of quant,” and #42, “converting to 3.0 bpw causes error; block state has 0 inf values and 34 NaN values,” concern numerical conversion failures. Their association is only inferred shared Linear conversion-source context; neither establishes this change's motivation or successful remediation. [inference; call_8ddc89ebe2fd4ed3be9b3f1d0687270e, call_05440f583b114fc49a60a035442deb10, call_f21342d1b1d04f528ec17def3fd09afc]

<a id="block-sparse-mlp"></a>

## Separate intermediate, activation and down-output precision

Each expert's down Linear now stores self.out_dtype rather than torch.half. Linear passes that setting into LinearFP16 and LinearEXL3. Both forward methods prioritize a per-call override, then the stored dtype, then half; the expert call supplies no override. [source; call_3d66b702a6ee480bbd95944ec4cd6e93, call_f21342d1b1d04f528ec17def3fd09afc, call_1190cdadead44f5da8348d3ef9125100, call_9777c3b7293944b0a188ec90b795493a]

For half gate/up intermediates, the ordinary expert helper continues overwriting u. Otherwise it allocates a half tensor a, calls activation(g,u,a), then feeds a to down. Both native activations accept matching half or float inputs but require half output. Their float kernel computes the activation-product in float before converting each pair to half. [source; call_3d66b702a6ee480bbd95944ec4cd6e93, call_aa48198966f0407d8f03be22a2931208]

The new preparation follows the existing fused path, whose load method already creates a separate half interm_a for non-half intermediates. GatedMLP's other located activation caller remains activation(g,u,u), so this repair is local to BlockSparseMLP. [source; call_f441f743f32d49d6b3d6bcbf6dc94e70, call_4b93f3b0ce17435bb4d1e82a2d4fb75d, call_3d66b702a6ee480bbd95944ec4cd6e93]

For unquantized down projections, half input with float output selects ext.hgemm rather than torch.matmul. The native callee requires half operands and supports float output through cublasGemmEx with FP32 compute. This does not preserve FP32 activations through the entire expert. [source; call_1190cdadead44f5da8348d3ef9125100, call_8626b9c13b1c4c7abe0308c601fdf79d, call_3d66b702a6ee480bbd95944ec4cd6e93]

Dispatch is unchanged: bsz counts flattened tokens; more than one token or any non-EXL3 expert projection selects ordinary execution. One token with fully EXL3 projections selects fusion. MultiLinear reads dimensions and tensor pointers, not stored out_dtype; fused output already uses cfg.out_d allocated with self.out_dtype or half. [source; call_f441f743f32d49d6b3d6bcbf6dc94e70, call_f22d9367a9c24eba8edb6bb45ccd749c, call_3d66b702a6ee480bbd95944ec4cd6e93]

TransformerBlock allocation continues consuming the unchanged projection lists. Its forward method requests half output from mlp_norm and passes that tensor to the MLP. Combined with Qwen3Moe's float down-output setting, this exposes the ordinary path's input-typed accumulator to differently typed expert results. [source; call_6e174d2c562744e389dc5e28bf5dad2f, call_350694fd7450481fbb844b87a49e055c, call_f441f743f32d49d6b3d6bcbf6dc94e70, call_3d66b702a6ee480bbd95944ec4cd6e93]

A standard-library reconstruction confirmed that the fused tail's first return still precedes the shared-expert addition. The scalar allocation model reports no extra activation destination for half intermediates and two additional destination bytes per element for float intermediates, excluding allocator overhead. [execution; call_df5478919f644df8bf59a332f372151e]

## Authoring-time findings — pending review

### ordinary-output-accumulator-dtype (suspected; defect)

FP32 expert results reach an input-typed accumulation buffer without conversion.

Trigger: Use half input, out_dtype=torch.float, and ordinary execution. Qwen3Moe supplies that output setting, TransformerBlock supplies half normalized input, and multiple flattened tokens select ordinary execution.

Expected: Accumulate routed float results into a compatible buffer and return the requested output dtype.

Actual: The changed down projection produces float current_state, while zeros_like(y) leaves final_hidden_states half for this caller. These are passed directly to index_add_ without reconciling dtypes. Runtime rejection is suspected but was not executed.

Locations: 13fa9ca2cf41d1383e00ff2775cb4683d6db15ea:exllamav3/modules/block_sparse_mlp.py — BlockSparseMLP.forward

Source evidence: call_3d66b702a6ee480bbd95944ec4cd6e93, call_f441f743f32d49d6b3d6bcbf6dc94e70, call_350694fd7450481fbb844b87a49e055c, call_6e174d2c562744e389dc5e28bf5dad2f, call_1190cdadead44f5da8348d3ef9125100

source_inspection: Compared the task's down-output change with the unchanged accumulator, inspected both sparse-model constructors, and traced TransformerBlock's normalized input into the MLP. [call_3d66b702a6ee480bbd95944ec4cd6e93, call_f441f743f32d49d6b3d6bcbf6dc94e70, call_acea9b63efe545bcbaa9fc51dd8662b6, call_350694fd7450481fbb844b87a49e055c, call_6e174d2c562744e389dc5e28bf5dad2f, call_1190cdadead44f5da8348d3ef9125100]. Limits: No PyTorch execution or eligible library documentation establishes the exact runtime diagnostic.

### carried-fused-shared-return (suspected; defect)

The ancestor-recorded unreachable fused shared-expert addition persists unchanged.

Trigger: Supply shared_experts and forward one flattened token with fully EXL3 routed projections.

Expected: Include the shared contribution as ordinary execution does.

Actual: The fused branch returns final_hidden_states.view(x.shape) before its shared call. Neither inspected built-in constructor supplies shared experts, so demonstrated reach is conditional API use through the generic decoder dispatch.

Locations: 13fa9ca2cf41d1383e00ff2775cb4683d6db15ea:exllamav3/modules/block_sparse_mlp.py — BlockSparseMLP.forward

Source evidence: call_f441f743f32d49d6b3d6bcbf6dc94e70, call_3d66b702a6ee480bbd95944ec4cd6e93, call_acea9b63efe545bcbaa9fc51dd8662b6, call_350694fd7450481fbb844b87a49e055c, call_6e174d2c562744e389dc5e28bf5dad2f

source_inspection: Inspected the early return, subsequent shared call, branch condition, decoder dispatch and both built-in construction sites; the task diff changes none of those statements. [call_f441f743f32d49d6b3d6bcbf6dc94e70, call_3d66b702a6ee480bbd95944ec4cd6e93, call_6e174d2c562744e389dc5e28bf5dad2f, call_acea9b63efe545bcbaa9fc51dd8662b6, call_350694fd7450481fbb844b87a49e055c]. Limits: No tensor or CUDA execution.

scalar_transcription: Reconstructed the changed source and checked fused-tail AST statement order. [call_df5478919f644df8bf59a332f372151e]. Limits: Static reconstruction, not execution of forward.

### carried-all-expert-fused-cardinality (suspected; defect)

The inherited all-expert routing versus fused-buffer cardinality mismatch remains.

Trigger: One flattened token, fully EXL3 projections, activate_all_experts=True, and num_experts different from num_experts_per_tok.

Expected: Allocate compatible all-expert buffers or choose ordinary execution.

Actual: Native routing returns num_experts indices, but fused outputs retain num_experts_per_tok entries. exl3_mgemm checks these dimensions for equality. Decoder forwarding permits the parameter; default conversion reaching this combination was not established.

Locations: 13fa9ca2cf41d1383e00ff2775cb4683d6db15ea:exllamav3/modules/block_sparse_mlp.py — BlockSparseMLP.forward

Source evidence: call_f441f743f32d49d6b3d6bcbf6dc94e70, call_3d66b702a6ee480bbd95944ec4cd6e93, call_a758e23a9d8b45218f1d41294271a427, call_894137de06164d2d90b7cab6f19f3cfd, call_6e174d2c562744e389dc5e28bf5dad2f

source_inspection: Compared native routing cardinality with Python buffer allocation and dispatch, native multi-GEMM shape validation, and decoder parameter forwarding; checked that the task diff leaves these unchanged. [call_a758e23a9d8b45218f1d41294271a427, call_f441f743f32d49d6b3d6bcbf6dc94e70, call_894137de06164d2d90b7cab6f19f3cfd, call_6e174d2c562744e389dc5e28bf5dad2f, call_3d66b702a6ee480bbd95944ec4cd6e93]. Limits: Conditional source failure path; no CUDA reproduction.

## Uncertainty and limits

No repository tensor operation, extension build, CUDA kernel, model inference, accuracy test or benchmark was executed.

The standard-library check reconstructed changed statements and modeled allocation and cardinality arithmetic; it does not establish GPU behavior or index_add_ runtime acceptance.

Literal whole-tree searches establish the inspected built-in constructors and consumers, not dynamic or external callers.
