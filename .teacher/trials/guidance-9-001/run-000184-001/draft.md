# 8357593c39b444f9e7e46bd90d385b6dcd7e1c62


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/8357593c39b444f9e7e46bd90d385b6dcd7e1c62) · [Evidence ledger](draft.json)

Moves MoE routing into the extension, caches single-token workspaces and folds weighted expert reduction into multi-GEMM; performance remains unmeasured, with conditional compatibility changes and an inherited shape mismatch.

- [Native routing and reusable single-token expert execution](#block-sparse-mlp)

## Problem

BlockSparseMLP previously performed routing through Python tensor calls, allocated fused-path workspaces on each forward, and launched a separate output sum. [source; call_809723051f4d414d909e89b8a5d77b28]

## Reasoning

The change combines native routing, reusable buffers and an in-kernel expert reduction. The reduction is a prerequisite for replacing out_d.sum(dim=0) with a view of its first expert slot; those edits are not independent. [source; call_b804fe012a314f45bba3d09ccca5f9fd]

## Impact

This removes repeated Python orchestration and workspace allocation from single-token fused execution, at the cost of retaining workspaces for the loaded layer. CPU overhead reduction is plausible but was not measured. [inference; call_b804fe012a314f45bba3d09ccca5f9fd]

## Source Notes

The read introduction entry establishes the original routed-expert implementation, MultiLinear preconditions and an all-expert fused-buffer mismatch. Inspection of the parent and task diff shows that mismatch is carried over. [ancestor; call_7ee27a00703e4870b6696c5df320109e]

Both setup.py and the JIT loader recursively collect C++ sources, so the new libtorch source requires no explicit source-list edit. [source; call_1f25def32b3a427e87a0ae08defd8aa0]

Related-file discussions concern different problems: #7, “quantizing model: undefined symbol: __cxa_call_terminate,” reports extension loading; #21, “Build Failure on Windows: CUDA 12.4 / PyTorch 2.7.0+cu126 / VS 2022,” reports compilation; #38, “Error converting nvidia/Llama-3_1-Nemotron-Ultra-253B-v1,” concerns padding during loading; #34, “torch._C._LinAlgError on last layer of quant,” concerns Cholesky failure. Any connection to this task is inferred only from shared ext.py, setup.py, linear.py or convert_model.py paths, not evidence of its motivation. [inference; call_ebf25646a195403cb98c674713394e2b, call_170e1e55006a4feba280401d40e2490d, call_df2563b757b648d1a563aff842eb0d1e, call_5855f96f39c245c8bafb746f4d72855e]

<a id="block-sparse-mlp"></a>

## Native routing and reusable single-token expert execution

Forward flattens tokens and calls blocksparse_mlp_routing through the new binding. The native helper computes y @ gate_tensor, selects top-k logits and normalizes only those logits with softmax. It returns indices first and weights second, matching the Python unpacking. A Python equivalent remains present but its call is commented out. [source; call_b804fe012a314f45bba3d09ccca5f9fd]

For exactly one flattened token and ordinary routing, load-time FP16 logit/weight buffers and int64 index buffers are reused; top-k is unsorted. Larger inputs or activate_all_experts use allocating ATen operations, selecting either num_experts_per_tok or all experts. Conversion supplies the exact activate_all_experts key and separately recomputes ordinary-routing reference states. [source; call_b804fe012a314f45bba3d09ccca5f9fd, call_593c78ddb74e4dc5aa74baf29ff1d215, call_1f25def32b3a427e87a0ae08defd8aa0]

ExpertsCFG retains input-transform, gate, up, activation and down-output buffers with num_experts_per_tok expert slots and one token per slot. Activation aliases the up buffer when its dtype is already FP16. These buffers are allocated even for nonquantized layers and released by clearing the configuration on unload. [source; call_b804fe012a314f45bba3d09ccca5f9fd]

Expert dispatch remains unchanged: multiple tokens or nonuniformly EXL3 storage use the ordinary expert loop; single-token fully EXL3 layers use three multi-GEMMs. MultiLinear still requires matching dimensions, bit widths and codebook multipliers, no expert biases or softcaps, and unit post-scale. [source; call_809723051f4d414d909e89b8a5d77b28, call_b804fe012a314f45bba3d09ccca5f9fd, call_8a2e638f8b9446e4a7614a9c82dd337d]

The kernel already applies routing weights during each expert's output transform. After its existing grid synchronization, the new reduction lets only z=0 blocks sum expert planes into plane zero. The 32-element division and lane arithmetic distribute one output element per warp lane. FP32 outputs accumulate as float; FP16 outputs use sequential half additions. [source; call_ab60bc4a4c2b4f7495e95a073319207f, call_b804fe012a314f45bba3d09ccca5f9fd]

Only calls supplying weights receive the new reduction. The inspected gate/up calls and attention K/V call pass None, preserving separate outputs; the expert down call supplies routing weights and now consumes plane zero. The native entry point still requires FP16 inputs and FP16 or FP32 outputs. [source; call_f7dc2b0fc7de4c9c9edf3482bcb32010, call_1f25def32b3a427e87a0ae08defd8aa0, call_e439c416a67a4bcd90e55cfa80a6cb94, call_b804fe012a314f45bba3d09ccca5f9fd]

A scalar transcription covered every output exactly once for nine tested width/grid combinations. Sequential half rounding of [2048, 1, -2048] produced 0 versus 1 for wide accumulation followed by half rounding, demonstrating why the new reduction should not be assumed numerically identical to another reduction implementation. [execution; call_3cc0f35c170645f18f22ac398dfa3afe]

The inspected decoder callers normalize inputs to FP16, pass params without a per-call MLP dtype override, and immediately add the result into the residual. Mixtral constructs FP16 MLP outputs; Qwen3 MoE requests FP32 outputs. Both agree with the cached constructor-selected dtype, although the public per-call override no longer works on the fused path. [source; call_7403577d1ca94eee80d1b7414c8d9def, call_ad0ccd3204df434f9a14b69bf8361287, call_b804fe012a314f45bba3d09ccca5f9fd]

## Authoring-time findings — pending review

### routing-bias-bypass (suspected; defect)

Direct router matmul drops the optional bias previously applied by LinearFP16.forward.

Trigger: Load a routing-gate weight with a nonzero optional bias and execute BlockSparseMLP.forward.

Expected: Route using y @ weight + bias, as before.

Actual: RoutingCFG stores only weight and the native helper computes matmul without bias. Linear.load_fp16 still accepts the bias, and no inspected router guard forbids it. This affects both routing branches conditionally; no supplied checkpoint demonstrates such a bias.

Locations: 8357593c39b444f9e7e46bd90d385b6dcd7e1c62:exllamav3/exllamav3_ext/libtorch/blocksparse_mlp.cpp — blocksparse_mlp_routing

Source evidence: call_b804fe012a314f45bba3d09ccca5f9fd, call_4f479d22cb5d4af1b191c9ddb6249c34, call_1f25def32b3a427e87a0ae08defd8aa0

source_inspection: Compared the bypassed Linear/LinearFP16 path with the new helper and inspected decoder callers and model construction sites. [call_7403577d1ca94eee80d1b7414c8d9def, call_e43329dd3f3446d48a1e0aa54e304393]. Limits: Conditional supported-loader input, not an observed model failure.

### fused-output-dtype (suspected; behavior_change)

The fused path ignores the forward call's out_dtype argument.

Trigger: Call a single-token fully EXL3 BlockSparseMLP with out_dtype different from its constructor-selected output dtype.

Expected: Honor the per-call override as the previous allocation did.

Actual: The output buffer is allocated during load using only self.out_dtype or FP16; forward returns its view without conversion. The ordinary path still honors the override. Inspected decoder callers do not supply this override.

Locations: 8357593c39b444f9e7e46bd90d385b6dcd7e1c62:exllamav3/modules/block_sparse_mlp.py — BlockSparseMLP.forward

Source evidence: call_b804fe012a314f45bba3d09ccca5f9fd, call_809723051f4d414d909e89b8a5d77b28, call_7403577d1ca94eee80d1b7414c8d9def

source_inspection: Compared old per-call allocation with cached allocation and inspected the two decoder forwarding sites. [call_2f8761b6e44f483995268341fc3da34e, call_b804fe012a314f45bba3d09ccca5f9fd]. Limits: No tensor execution or demonstrated in-tree caller requesting a conflicting dtype.

### all-expert-fused-shape (suspected; defect)

The inherited all-expert routing mismatch persists with cached workspaces.

Trigger: One flattened token, fully EXL3 experts, activate_all_experts=True, and num_experts unequal to num_experts_per_tok.

Expected: Evaluate all experts or use the ordinary expert path.

Actual: Routing returns num_experts indices while cached fused buffers contain num_experts_per_tok slots. The first multi-GEMM rejects the index/output dimension mismatch. Conversion supplies the flag, but default conversion reaching this fully quantized single-token condition is not established.

Locations: 8357593c39b444f9e7e46bd90d385b6dcd7e1c62:exllamav3/modules/block_sparse_mlp.py — BlockSparseMLP.forward

Source evidence: call_b804fe012a314f45bba3d09ccca5f9fd, call_e439c416a67a4bcd90e55cfa80a6cb94, call_1f25def32b3a427e87a0ae08defd8aa0

source_inspection: Checked routing cardinality, unchanged fused dispatch, cached dimensions, native shape check and decoder params forwarding. [call_b804fe012a314f45bba3d09ccca5f9fd, call_e439c416a67a4bcd90e55cfa80a6cb94, call_7403577d1ca94eee80d1b7414c8d9def]. Limits: No CUDA execution.

## Uncertainty and limits

No extension compilation, CUDA execution, end-to-end model test or timing measurement was performed.

Scalar checks model indexing and arithmetic only, not cooperative synchronization, ATen out-buffer behavior or GPU floating-point equivalence.

External checkpoint coverage, concurrent forwards and downstream consumers retaining module outputs were not established.
