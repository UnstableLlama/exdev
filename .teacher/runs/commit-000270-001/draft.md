# b8c830c17f53cf0d4caf7b774fe458b2f31cb85c


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/b8c830c17f53cf0d4caf7b774fe458b2f31cb85c) · [Evidence ledger](draft.json)

Adds Dots routing and a disabled grouped DS3 helper, exports correction bias, aligns ordinary accumulation dtype and restores fused shared-expert addition. Routing dispatch remains incomplete, and the default native call has a signature mismatch.

- [Correction-biased routing and expert-output integration](#block-sparse-mlp)

## Problem

The change adds correction-biased sigmoid routing, but enables only the single-group Dots route in forward; grouped DS3 dispatch remains commented out. [source; call_e2521972ad6047289b91ea7f082e2254]

## Reasoning

The new routers supply expert indices and weights to the existing expert-evaluation paths. Loading and exporting correction bias preserves the additional routing state. [source; call_e2521972ad6047289b91ea7f082e2254, call_e07f37d372fd4e54aa9ba7e6e54b1162]

## Impact

MixtralModel and Qwen3MoeModel use compatible keyword constructor calls and leave the new routing flag false. Their default routing path nevertheless encounters the native-call signature mismatch recorded in findings. [source; call_c6cc662d6aac46f6b46631251636dba9, call_be277a7f41e049c08bfd291fcf9b5b47, call_e2521972ad6047289b91ea7f082e2254, call_cba2aa43d7d244858167faf2b3c97340]

## Source Notes

Read the BlockSparseMLP introduction and shared-expert entries. They establish the earlier fusion design and record shared-output, shared-allocation and all-expert buffer observations. [ancestor; call_f08d14ccb0cd4dc49b31b4e3bc7b0119, call_30db9eae685548ba8fa3ecf94899fe46]

Issue #51, “dots.llm1 support,” is louiehelm's architecture-support request. Its connection to this task is inferred from the Dots name and discussion of Deepseek-style MoE modules, not an established upstream link. [inference; call_74c18aed9b8f4001ba3f6333378e99c4, call_e2521972ad6047289b91ea7f082e2254]

Issue #43, “Error converting abliterated Qwen3 mlabonne/Qwen3-30B-A3B-abliterated,” reports NaN states and Cholesky failure. Its inferred association is the BlockSparseMLP conversion-log occurrence and Qwen3-MoE context; it does not establish motivation for this routing change. [inference; call_caa359dc66bd4b45b69b096ed41a36d8, call_55d1da195f064b35b668ad23eaa41e35, call_be277a7f41e049c08bfd291fcf9b5b47]

<a id="block-sparse-mlp"></a>

## Correction-biased routing and expert-output integration

BlockSparseMLP adds deepseekv3_routing=False and optional routed_scaling_factor, n_group and topk_group values. load places these in RoutingCFG alongside an optional tensor named <module key>.gate.e_score_correction_bias. unload clears the bias reference; get_tensors exports a present bias contiguously under the same name. This name is hard-coded rather than derived from key_routing_gate. [source; call_e2521972ad6047289b91ea7f082e2254]

Whole-parent searches locate one RoutingCFG builder, updated by the diff, and two BlockSparseMLP construction sites: MixtralModel and Qwen3MoeModel. Both use keyword arguments and omit the new options. TransformerBlock.forward passes params unchanged to its MLP. ParallelDecoderBlock has another generic MLP dispatch, although its declared constructor types exclude BlockSparseMLP. [source; call_e635eb141cd64aabaadc58b683091e2e, call_2f37efdc4fd9498e91f69f0db2606261, call_c6cc662d6aac46f6b46631251636dba9, call_be277a7f41e049c08bfd291fcf9b5b47, call_e7ea57d517c44d6aa8978a4cd3e67c41]

routing_dots projects flattened token rows through gate_tensor, adds correction bias to logits, selects top-k experts, applies sigmoid to the selected biased logits, then normalizes and scales their weights. activate_all_experts selects every expert. Exactly one flattened token without that flag uses preallocated outputs; the general branch allocates results. [source; call_e2521972ad6047289b91ea7f082e2254, call_e07f37d372fd4e54aa9ba7e6e54b1162]

routing_ds3 instead computes sigmoid before adding correction bias for selection. It divides experts into n_group equal-sized groups, scores each group by its best two corrected scores, retains topk_group groups and then selects experts. Weights gather the original uncorrected sigmoid scores. The reshape requires divisible group sizes, and topk(2) requires at least two experts per group. This helper is not enabled by forward. [source; call_e2521972ad6047289b91ea7f082e2254]

Both new helpers add 1e-20 to the selected-weight sum before normalization and multiply by routed_scaling_factor. The constant is a denominator stabilizer, not an expert-selection threshold; its effective behavior depends on tensor precision. [source; call_e2521972ad6047289b91ea7f082e2254]

A scalar transcription using logits [0,1,2], bias [2,0,0], two selected experts and scale 2 produced Dots weights [1,1] for selected experts {0,2}. Gathering uncorrected sigmoid scores for that same set produced approximately [0.724219,1.275781]. Thus the modeled Dots bias affects mixture weights as well as selection. [execution; call_156933a76c9f42ffb49e4d1d95071e20]

The existing native router selects top-k logits and applies softmax, reusing buffers for one token and allowing all-expert selection in its general branch. The task keeps it for deepseekv3_routing=False but adds a fifth argument without updating its four-argument declaration, definition or binding. [source; call_cba2aa43d7d244858167faf2b3c97340, call_a060fc950eb94072a1861c26e22a1ba4, call_aea22adac183443eaa6e50796068406d, call_e2521972ad6047289b91ea7f082e2254]

The ordinary accumulator now uses self.out_dtype rather than necessarily inheriting the input dtype. This agrees with Qwen3MoeModel's FP32 down-projection outputs; Mixtral requests FP16. The fused tail removes the early return that previously bypassed shared experts, making their addition reachable. [source; call_e2521972ad6047289b91ea7f082e2254, call_be277a7f41e049c08bfd291fcf9b5b47, call_c6cc662d6aac46f6b46631251636dba9, call_e07f37d372fd4e54aa9ba7e6e54b1162]

The shared-output observation is removed by the task, but the inherited plain-MLP allocation mismatch and all-expert fused-buffer mismatch remain. Neither buffer allocation nor TransformerBlock's shared-projection attribute accesses is repaired. [source; call_e2521972ad6047289b91ea7f082e2254, call_e7ea57d517c44d6aa8978a4cd3e67c41, call_11b8b2eb33d147798cc1f552f480df05, call_e07f37d372fd4e54aa9ba7e6e54b1162, call_1788690c627249e8877bcac204f5bf1a]

## Authoring-time findings — pending review

### native-router-argument-mismatch (suspected; defect)

The default route passes five arguments to a four-argument native binding.

Trigger: Call BlockSparseMLP.forward with deepseekv3_routing=False, its default.

Expected: Obtain expert indices and softmax routing weights.

Actual: The appended False has no matching native parameter, implying argument rejection before expert evaluation. Both inspected built-in sparse-model constructors retain this default, and TransformerBlock.forward dispatches to their MLP.

Locations: b8c830c17f53cf0d4caf7b774fe458b2f31cb85c:exllamav3/modules/block_sparse_mlp.py — BlockSparseMLP.forward

Source evidence: call_e2521972ad6047289b91ea7f082e2254, call_cba2aa43d7d244858167faf2b3c97340, call_aea22adac183443eaa6e50796068406d, call_b4b3378b98754090a9337dcd556211f3, call_e7ea57d517c44d6aa8978a4cd3e67c41

source_inspection: Compared the changed call with the declaration, implementation, binding and both located constructors. [call_a060fc950eb94072a1861c26e22a1ba4, call_c6cc662d6aac46f6b46631251636dba9, call_be277a7f41e049c08bfd291fcf9b5b47]. Limits: The extension was not invoked.

### grouped-routing-unassigned (suspected; defect)

DS3-enabled dispatch leaves routing results unassigned outside the single-group configuration.

Trigger: Set deepseekv3_routing=True with n_group or topk_group different from 1, including default None values.

Expected: Perform grouped routing or explicitly reject the unsupported configuration.

Actual: The routing_ds3 call is commented out. selected_experts remains unbound when consumed by either expert-mask construction or fused GEMM. Built-in constructors do not enable this flag, limiting established reach to the new API.

Locations: b8c830c17f53cf0d4caf7b774fe458b2f31cb85c:exllamav3/modules/block_sparse_mlp.py — BlockSparseMLP.forward

Source evidence: call_e2521972ad6047289b91ea7f082e2254, call_e07f37d372fd4e54aa9ba7e6e54b1162, call_2f37efdc4fd9498e91f69f0db2606261

source_inspection: Traced dispatch assignments and inspected both located constructors. [call_e2521972ad6047289b91ea7f082e2254, call_c6cc662d6aac46f6b46631251636dba9, call_be277a7f41e049c08bfd291fcf9b5b47]. Limits: Conditional API path; no repository execution.

### optional-inputs-required-by-dots (suspected; new_requirement)

Dots routing requires bias and scaling values that construction permits to be absent.

Trigger: Enable deepseekv3_routing with n_group=topk_group=1 but leave correction bias or routed_scaling_factor as None.

Expected: Validate required inputs or provide supported defaults.

Actual: routing_dots unconditionally adds the bias and uses the scaling factor in tensor arithmetic, without a guard or fallback. Neither inspected built-in constructor enables this route.

Locations: b8c830c17f53cf0d4caf7b774fe458b2f31cb85c:exllamav3/modules/block_sparse_mlp.py — routing_dots

Source evidence: call_e2521972ad6047289b91ea7f082e2254, call_c6cc662d6aac46f6b46631251636dba9, call_be277a7f41e049c08bfd291fcf9b5b47

source_inspection: Compared optional constructor values with unconditional router operations and the new forward call site. [call_e2521972ad6047289b91ea7f082e2254]. Limits: No tensor-operation execution.

### inherited-all-expert-fusion-cardinality (suspected; defect)

All-expert routing still conflicts with fixed selected-expert fused buffers.

Trigger: Use valid Dots routing inputs, one flattened token, fully EXL3 experts, activate_all_experts=True and num_experts different from num_experts_per_tok.

Expected: Evaluate every expert with compatible buffers or choose the ordinary path.

Actual: Routing returns num_experts indices, but fused buffers have num_experts_per_tok entries. The first exl3_mgemm checks index dimension 1 against output dimension 0. This inherited mismatch persists; default native routing encounters the separate argument mismatch first.

Locations: b8c830c17f53cf0d4caf7b774fe458b2f31cb85c:exllamav3/modules/block_sparse_mlp.py — BlockSparseMLP.forward

Source evidence: call_e2521972ad6047289b91ea7f082e2254, call_e07f37d372fd4e54aa9ba7e6e54b1162, call_1788690c627249e8877bcac204f5bf1a, call_e7ea57d517c44d6aa8978a4cd3e67c41

source_inspection: Compared routing cardinality, fused allocation, dispatch and native shape validation. [call_e2521972ad6047289b91ea7f082e2254, call_1788690c627249e8877bcac204f5bf1a]. Limits: Conditional API reach, not a demonstrated default workflow.

### inherited-plain-shared-allocation (suspected; defect)

Shared-expert allocation still assumes GatedMLP attributes despite admitting plain MLP.

Trigger: Supply an MLP as shared_experts and invoke TransformerBlock.allocate_q.

Expected: Allocate the shared up and down projections.

Actual: Allocation accesses gates, ups and downs; plain MLP stores singular up and down and has no gates. GatedMLP supplies the list interface. The task leaves allocation unchanged, and neither inspected built-in sparse constructor supplies shared experts.

Locations: b8c830c17f53cf0d4caf7b774fe458b2f31cb85c:exllamav3/modules/transformer.py — TransformerBlock.allocate_q

Source evidence: call_e7ea57d517c44d6aa8978a4cd3e67c41, call_11b8b2eb33d147798cc1f552f480df05, call_e2521972ad6047289b91ea7f082e2254, call_c6cc662d6aac46f6b46631251636dba9, call_be277a7f41e049c08bfd291fcf9b5b47

source_inspection: Rechecked both admitted shared-module implementations against unchanged allocation accesses. [call_e7ea57d517c44d6aa8978a4cd3e67c41, call_11b8b2eb33d147798cc1f552f480df05]. Limits: No allocation execution.

## Uncertainty and limits

No repository inference, extension invocation, CUDA test or performance measurement was run.

The scalar transcription uses Python double precision and deterministic tie ordering; it does not establish PyTorch FP16 rounding, top-k tie ordering or preservation of the 1e-20 stabilizer.

No DS3/Dots reference checkpoint configuration or tensor header was listed in the inspected evidence index. Checkpoint-specific correction-bias names, shapes and dtypes were not validated.
