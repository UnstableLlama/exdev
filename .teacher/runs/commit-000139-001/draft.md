# 6fc153d7a062aa7f53fe13b27d008c2d90d8d62f


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/6fc153d7a062aa7f53fe13b27d008c2d90d8d62f) · [Evidence ledger](draft.json)

Adds routed expert MLP execution, single-token EXL3 fusion and calibration/allocation integration; source inspection identifies an all-expert fused-path shape mismatch.

- [Routed experts and calibration integration](#block-sparse-mlp)

## Problem

The change adds a routed mixture of gated MLP experts, together with allocation and calibration integration. [source; call_2d6d78c0c0b142599da5afe93963d874, call_5306b9ac721949eeb0ef900da33435ef, call_76ea411489c04be09eb4173a389e2823]

## Reasoning

Calibration can activate every expert to collect down-projection inputs, then recompute reference outputs with ordinary routing. This separates calibration coverage from the behavior used to measure conversion error. [source; call_76ea411489c04be09eb4173a389e2823, call_fc9f0d422688480985e6b6f8b1ed7262]

## Impact

BlockSparseMLP becomes a public module and is recognized by both decoder allocation methods. The diff does not register a model architecture or enable all-expert calibration by default. [source; call_f83e9da09e56414aa172277b83b4858c, call_5306b9ac721949eeb0ef900da33435ef, call_266aa4a25d2e466182fe1a4c6d356158]

## Source Notes

Issue #7, “quantizing model: undefined symbol: __cxa_call_terminate,” reports an extension-loading problem; issue #34, “torch._C._LinAlgError on last layer of quant,” reports Cholesky failure during conversion. Their connection here is only inferred shared-file context: model.py and convert_model.py appear in their tracebacks. Neither establishes motivation for this feature. [inference; call_e00ea7d4d98848fc9c22824ef717a01f, call_9db17f6ea6fc46d7acfcbe5d5a8d82a3, call_76ea411489c04be09eb4173a389e2823, call_266aa4a25d2e466182fe1a4c6d356158]

<a id="block-sparse-mlp"></a>

## Routed experts and calibration integration

The router projects flattened tokens to expert scores, applies softmax, selects the configured number of experts and renormalizes their weights. Each selected expert computes activation(gate(x)) × up(x), followed by its down projection; weighted outputs are accumulated back into token order. [source; call_2d6d78c0c0b142599da5afe93963d874]

The ordinary path groups tokens by expert and invokes Linear.forward. Despite its “Torch path” label, activation remains a native CUDA call: silu_mul or gelu_mul. Those callees process FP16 pairs, with GELU using a tanh approximation. [source; call_2d6d78c0c0b142599da5afe93963d874, call_fc9f0d422688480985e6b6f8b1ed7262, call_725804d23b744b8ea5cd74ad5c07e367]

The fused path is selected only for one flattened token with every expert projection stored as EXL3. MultiLinear requires equal dimensions and bit widths within each projection group, no biases or softcaps, and unit post-scaling. Mixed storage emits a warning and uses the ordinary path. [source; call_2d6d78c0c0b142599da5afe93963d874]

Fusion builds device pointer tables and performs separate indexed multi-GEMMs for gate, up and down projections. Only the down call receives routing weights; its expert outputs are summed afterward. The native entry point requires FP16 inputs, allows FP16 or FP32 outputs and checks that the index count equals the output's expert dimension. The -1 argument leaves kernel-shape selection automatic. [source; call_2d6d78c0c0b142599da5afe93963d874, call_abf022fec54d41e89bb45a8b3b35a916]

The single-token restriction appears intended to exploit indexed multi-GEMM without solving multi-token dispatch; the source explicitly leaves 1 < batch size < 32 as future work. That comment is not a measured crossover threshold. [inference; call_2d6d78c0c0b142599da5afe93963d874]

Expert gate/up projections share an input calibration map, while each down projection has its own map. Linear.capture_H accumulates XᵀX only for the first key sharing a map. Enabling activate_all_experts makes the ordinary path supply every expert with input rows; reference outputs are separately recomputed without that flag. [source; call_2d6d78c0c0b142599da5afe93963d874, call_fc9f0d422688480985e6b6f8b1ed7262, call_76ea411489c04be09eb4173a389e2823]

Allocation groups each expert projection list into one bit-width decision, summing its weight counts and expanding the result back to individual keys. The added .experts.0. wildcard normalization complements existing slice normalization. The model-level calibration_all_experts switch defaults to false. [source; call_da31012628b04a19b43bb05bc1e0018a, call_7fb8d9fa7ae340f39caa8b8576ed1a29, call_5306b9ac721949eeb0ef900da33435ef, call_266aa4a25d2e466182fe1a4c6d356158]

## Authoring-time findings — pending review

### all-expert-fused-shape (suspected; defect)

All-expert routing conflicts with the fused path's fixed selected-expert buffer count.

Trigger: Call BlockSparseMLP.forward with one flattened token, fully EXL3 experts, activate_all_experts=True, and num_experts different from num_experts_per_tok.

Expected: Evaluate every expert, or select the ordinary path that supports all-expert evaluation.

Actual: Routing produces num_experts indices, but fused buffers retain num_experts_per_tok entries. The first exl3_mgemm call encounters its index-count/output-dimension check. Parent-tree searches found no pre-existing BlockSparseMLP construction; inspected decoder methods forward params to their supplied MLP, and conversion introduces the flag. This establishes a conditional API failure, not that default conversion reaches it.

Locations: 6fc153d7a062aa7f53fe13b27d008c2d90d8d62f:exllamav3/modules/block_sparse_mlp.py — BlockSparseMLP.forward

Source evidence: call_2d6d78c0c0b142599da5afe93963d874, call_abf022fec54d41e89bb45a8b3b35a916, call_5e5bd2e097814e77837348e7010fc188, call_e0a3c58a735b48ccba320ea85af10631, call_a5c8a45dc9194e3798f3756e373bd4d4, call_76ea411489c04be09eb4173a389e2823

source_inspection: Compared routing cardinality, fused allocations and the native shape check, and inspected decoder forwarding sites. [call_2d6d78c0c0b142599da5afe93963d874, call_abf022fec54d41e89bb45a8b3b35a916, call_a5c8a45dc9194e3798f3756e373bd4d4]. Limits: No repository or CUDA execution.

scalar_transcription: For eight experts and two selected experts, modeled indices as (1,8) against fused output expert dimension 2; ordinary routing's corresponding equality holds and all-expert routing's fails. [call_0dc5ace0cc2949b881e5e0d290e1143c]. Limits: Standard-library integer shape arithmetic, not tensor allocation or a kernel test.

## Uncertainty and limits

No GPU execution, numerical-equivalence test or performance measurement was performed. The scalar check models buffer dimensions only.

Model-specific construction and end-to-end conversion with the new module are not demonstrated by this change.

The inspected activation kernels reinterpret buffers as FP16; broader intermediate-dtype compatibility is not established.
