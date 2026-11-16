# ce58d99c710900b0fe78229e8b193ab50b60234a


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/ce58d99c710900b0fe78229e8b193ab50b60234a) · [Evidence ledger](draft.json)

Disables routing-gate padding so expert selection receives exactly num_experts scores; expert projection padding and the inherited all-expert fused-shape mismatch remain unchanged.

- [Keep routing dimensions equal to the expert count](#block-sparse-mlp)

## Problem

The routing projection inherited Linear's 128-feature padding, although its output is interpreted directly as expert scores without trimming to num_experts. [source; call_999508332534471e827e25bbb0f22c06, call_eedd372e2f084e73805a9b505e1ef4dd]

## Reasoning

Setting pad_to=1 preserves the router's exact hidden-size input and num_experts output dimensions. It fixes the projection boundary rather than adding a slice before softmax. [source; call_3e6719f08eda4ad886acf8fd10a60d1b, call_999508332534471e827e25bbb0f22c06]

## Impact

Expert projections retain their existing padding. Router dtype, top-k selection, weight renormalization and execution-path selection are unchanged. [source; call_3e6719f08eda4ad886acf8fd10a60d1b, call_eedd372e2f084e73805a9b505e1ef4dd]

## Source Notes

Issue #34, “torch._C._LinAlgError on last layer of quant,” reports Cholesky failure; issue #38, “Error converting nvidia/Llama-3_1-Nemotron-Ultra-253B-v1,” reports a sliced-weight loading size mismatch. Their relevance is only inferred shared-file context through linear.py; neither report establishes motivation for this router change. [inference; call_ba38dae416b94fd69f720d54ca85d569, call_61548de4b3924f3d9b8b0586e1a1d88a, call_3e6719f08eda4ad886acf8fd10a60d1b]

<a id="block-sparse-mlp"></a>

## Keep routing dimensions equal to the expert count

Linear rounds each dimension using (dimension + pad_to - 1) // pad_to * pad_to. The default 128 is an alignment multiple, not an expert-count limit; 1 makes this rounding an identity. [source; call_999508332534471e827e25bbb0f22c06, call_3e6719f08eda4ad886acf8fd10a60d1b]

The FP16 loading path passes the rounded dimensions to tensor loading, and LinearFP16.forward allocates and returns out_features columns without removing padding. BlockSparseMLP then applies softmax and top-k across every returned column, using the resulting indices for expert dispatch. [source; call_999508332534471e827e25bbb0f22c06, call_b0eae653417141f8bd7b3a06cf7834c6, call_eedd372e2f084e73805a9b505e1ef4dd]

The likely correctness rationale is to exclude artificial routing candidates at their source. Exact router dimensions avoid both unnecessary projection columns and the need to mask or slice them downstream. [inference; call_3e6719f08eda4ad886acf8fd10a60d1b, call_eedd372e2f084e73805a9b505e1ef4dd]

A standard-library transcription gives old/new output widths of 128/8, 128/64, 128/128 and 256/129 for illustrative expert counts 8, 64, 128 and 129. Counts already divisible by 128 have unchanged output width. [execution; call_b0f38acbded741acb65233def17da6a9]

The earlier BlockSparseMLP entry records an all-expert fused-buffer cardinality mismatch. [ancestor; call_7824008344b6457a9d71d687795f4b87]

That mismatch is carried over: the patch changes only router construction, while all-expert routing and fused allocations still use different expert counts under the recorded trigger. [source; call_3e6719f08eda4ad886acf8fd10a60d1b, call_eedd372e2f084e73805a9b505e1ef4dd]

## Authoring-time findings — pending review

### inherited-all-expert-fused-shape (suspected; defect)

The router-padding fix leaves the inherited all-expert fused-path shape mismatch intact.

Trigger: One flattened token, fully EXL3 expert projections, activate_all_experts=True, and num_experts different from num_experts_per_tok.

Expected: Allocate for every selected expert or use the ordinary execution path.

Actual: Routing selects num_experts indices, but fused intermediates and outputs retain num_experts_per_tok entries. Whole-tree searches found Qwen3 MoE construction and decoder self.mlp.forward calls; inspected decoder calls pass params through. This establishes conditional reach, not that ordinary conversion triggers the single-token fused case.

Locations: ce58d99c710900b0fe78229e8b193ab50b60234a:exllamav3/modules/block_sparse_mlp.py — BlockSparseMLP.forward

Source evidence: call_eedd372e2f084e73805a9b505e1ef4dd, call_3e6719f08eda4ad886acf8fd10a60d1b, call_29c76e44b47c4846a2b4a38b6559ff2b, call_11fb12255ac64e6bb8af85a8a4e53f04, call_0b36b9726d8b4c898cc3bd61d4f314e9, call_fa9d96a259994fe5bae544fdfc8f5acc

source_inspection: Compared routing cardinality with unchanged fused allocations and inspected decoder forwarding and Qwen3 MoE construction. [call_eedd372e2f084e73805a9b505e1ef4dd, call_0b36b9726d8b4c898cc3bd61d4f314e9, call_fa9d96a259994fe5bae544fdfc8f5acc]. Limits: No native kernel execution or end-to-end reproduction.

scalar_transcription: Modeled eight all-expert indices against a fused output expert dimension of two. [call_b0f38acbded741acb65233def17da6a9]. Limits: Integer shape arithmetic, not repository execution.

## Uncertainty and limits

No repository tensor operations, GPU kernels or end-to-end model workflows were executed; the computation checks integer dimensions only.

No model-specific accuracy or performance improvement is established.
