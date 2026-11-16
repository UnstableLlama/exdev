# 30c7386b7c6a8f6899729975ef5da13cbf7b34f3


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/30c7386b7c6a8f6899729975ef5da13cbf7b34f3) · [Evidence ledger](draft.json)

Moves expert selection before softmax, eliminating redundant normalization while preserving exact-arithmetic routing weights; GPU speed and FP16 equivalence remain unmeasured.

- [Normalize only selected routing logits](#block-sparse-mlp)

## Problem

Routing previously computed softmax over every expert, selected top-k probabilities, then renormalized the selected weights. [source; call_04ac0a65709e44baa5bc8705fe29086d]

## Reasoning

For finite logits in exact arithmetic, softmax preserves ordering and its full-expert denominator cancels during selected-weight renormalization. Selecting logits first therefore permits a single softmax over only the selected experts. [inference; call_04ac0a65709e44baa5bc8705fe29086d, call_ee915d7244324f1eb23cf3289b2219e5]

## Impact

The change removes explicit selected-weight summation and division, and reduces softmax width from the expert count to the selected count during ordinary routing. Expert evaluation and output accumulation remain unchanged. [source; call_04ac0a65709e44baa5bc8705fe29086d, call_472645478ab74da5af32537480179a01]

## Source Notes

The introducing entry 6fc153d7 describes routed expert execution, single-token EXL3 fusion, and all-expert calibration; it also records the conditional fused-buffer cardinality mismatch. [ancestor; call_ddbfe4db2ca94acca688f690d2fc0607]

PR #26, “Superior 3INST parameters,” discusses decoder multipliers; issue #33, “Error converting model,” reports file-opening failure; issue #34, “torch._C._LinAlgError on last layer of quant,” reports Cholesky failure. Their inferred relevance is only shared conversion-file context, not evidence motivating this routing optimization. [inference; call_62080a2bda474707a8eb6977bbdce3bd, call_890482559b3744799268fdc9e0e09f5b, call_c8e12ad3b7774aad9cb46614d7231fdb, call_04ac0a65709e44baa5bc8705fe29086d]

<a id="block-sparse-mlp"></a>

## Normalize only selected routing logits

BlockSparseMLP.forward now passes router_logits directly to torch.topk and applies torch.softmax to its returned values along the expert dimension. The two edits work together: removing the full softmax without changing normalization would incorrectly normalize raw logits by their sum. [source; call_04ac0a65709e44baa5bc8705fe29086d]

The selected count remains num_experts_per_tok, or num_experts when activate_all_experts is true. Ordinary execution multiplies expert outputs by routing_weights before index_add_; fused execution supplies those weights to the down-projection multi-GEMM and sums its expert outputs. Neither consumer changes. [source; call_472645478ab74da5af32537480179a01, call_04ac0a65709e44baa5bc8705fe29086d]

A standard-library scalar transcription compared both normalization formulas on 900 finite-logit cases with 2, 8 and 64 experts and several selected counts. Maximum absolute weight difference was 2.220446049250313e-16; this checks the algebra numerically, not repository or CUDA execution. [execution; call_ee915d7244324f1eb23cf3289b2219e5]

The inherited all-expert fused-path mismatch is carried over: the diff changes normalization but neither the fused-path guard nor buffers sized by num_experts_per_tok. [source; call_472645478ab74da5af32537480179a01, call_04ac0a65709e44baa5bc8705fe29086d, call_732af8b9404740cb8d76bac49561d41c]

## Authoring-time findings — pending review

### inherited-all-expert-fused-shape (suspected; defect)

All-expert routing still conflicts with fixed selected-expert fused buffers.

Trigger: One flattened token, fully EXL3 expert projections, activate_all_experts=True, and num_experts != num_experts_per_tok.

Expected: Evaluate all experts or use the ordinary path supporting that cardinality.

Actual: The first fused multi-GEMM receives num_experts indices but an output with num_experts_per_tok expert slots, violating its shape check. Inspected direct MLP callers in TransformerBlock and ParallelDecoderBlock forward params unchanged. Conversion supplies the flag during unquantized calibration; that does not establish that normal conversion reaches this fully quantized trigger.

Locations: 30c7386b7c6a8f6899729975ef5da13cbf7b34f3:exllamav3/modules/block_sparse_mlp.py — BlockSparseMLP.forward

Source evidence: call_472645478ab74da5af32537480179a01, call_04ac0a65709e44baa5bc8705fe29086d, call_732af8b9404740cb8d76bac49561d41c, call_3090db4763f84af1a199300265150945, call_777927f40766494195a67aa717c91dab, call_f13c8d2377c64d049e0c02e9ae264e6f, call_a9df4390e0cc478d8e8d54d5d4cb9c6a

source_inspection: Compared unchanged fused allocations and routing cardinality against the native index/output shape check, then inspected decoder forwarding and calibration flag construction. [call_472645478ab74da5af32537480179a01, call_732af8b9404740cb8d76bac49561d41c, call_777927f40766494195a67aa717c91dab, call_a9df4390e0cc478d8e8d54d5d4cb9c6a]. Limits: Conditional source-level observation; no end-to-end or GPU reproduction.

## Uncertainty and limits

No GPU execution or latency measurement was performed. The scalar check uses Python double precision, not the router's FP16 tensor arithmetic.

Exact-arithmetic equivalence does not establish bitwise equality, identical tie handling after rounding, or behavior for nonfinite logits.
