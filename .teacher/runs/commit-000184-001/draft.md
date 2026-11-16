# 8357593c39b444f9e7e46bd90d385b6dcd7e1c62


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/8357593c39b444f9e7e46bd90d385b6dcd7e1c62) · [Evidence ledger](draft.json)

Moves MoE routing into ATen, reuses single-token workspaces and reduces weighted experts inside multi-GEMM. Speedup is unmeasured; output ownership and dtype behavior change, while an inherited all-expert shape mismatch persists.

- [Native routing and persistent expert workspaces](#block-sparse-mlp)

## Problem

BlockSparseMLP performed routing through Python, allocated single-token expert workspaces on every call, and launched a separate tensor reduction over expert outputs. [source; call_4b2ce8682ddc4aafa64ece154d775325]

## Reasoning

The change combines native ATen routing, load-time workspace allocation and an in-kernel weighted-output reduction. These remove repeated Python-side work; the kernel reduction is also a correctness precondition for replacing out_d.sum(dim=0) with its first slice. [source; call_4717b600aab34fb7bca9ae16422891f9, call_4878c88c5a8b4e52bde0f87ded17c62a, call_925a7137209846c6ae6473833ffd9360]

These mechanisms support the author's CPU-overhead motivation, but do not establish a measured speedup. [inference; call_4878c88c5a8b4e52bde0f87ded17c62a, call_4717b600aab34fb7bca9ae16422891f9]

## Impact

Routing moves into the extension for both execution paths. Expert execution still uses the ordinary path for multiple flattened tokens or non-fully-EXL3 experts; the fused path remains single-token only. [source; call_4878c88c5a8b4e52bde0f87ded17c62a, call_4b2ce8682ddc4aafa64ece154d775325]

## Source Notes

Read the introducing BlockSparseMLP entry, which documents fusion preconditions and an all-expert routing/buffer-count mismatch. That observation remains relevant to this change. [ancestor; call_b4d8c39b478e47b9a9ce161764d830f4]

Issue #34, “torch._C._LinAlgError on last layer of quant,” concerns Cholesky failure; #38, “Error converting nvidia/Llama-3_1-Nemotron-Ultra-253B-v1,” concerns loading/padding dimensions. Their connection here is only inferred shared-source context through linear.py, not evidence that this optimization addresses either report. Issue #21, “Build Failure on Windows: CUDA 12.4 / PyTorch 2.7.0+cu126 / VS 2022,” reports compilation failures and was closed without a solution; it does not validate this extension change. [inference; call_29e49fa9d13e4db1be3d7f98616861b5, call_21ac5eb2400d4442864cb849bb537183, call_d8dcd621bc52450c939da1d12b54f55a, call_461a191ae7784f9eac4ea32ed42c807f]

<a id="block-sparse-mlp"></a>

## Native routing and persistent expert workspaces

The binding exposes blocksparse_mlp_routing(bsz, cfg, y, params), returning expert indices followed by weights. RoutingCFG supplies the gate matrix, expert counts and reusable single-token buffers. The Python routing helper remains as an inactive alternative beside the extension call. [source; call_f96344f666d741f592ff29310009019c, call_49aaa0d0515f4b6ea0b65cd00bd548f3, call_4878c88c5a8b4e52bde0f87ded17c62a]

For one token without activate_all_experts, ATen matmul_out, topk_out and softmax_out reuse preallocated buffers; top-k sorting is disabled. Otherwise routing allocates results and selects either num_experts_per_tok or every expert. Both branches normalize only selected logits. This is native orchestration of ATen operations, not a newly fused routing CUDA kernel. [source; call_4717b600aab34fb7bca9ae16422891f9]

load allocates expert input-transform, gate, up, activation and output buffers with dimensions based on num_experts_per_tok and one token. Activation aliases the up buffer when intermediates are FP16; otherwise it has a separate FP16 buffer. unload clears both configuration objects. Allocation occurs even when the ordinary expert path will be used. [source; call_4878c88c5a8b4e52bde0f87ded17c62a]

The existing multi-GEMM already applies routing weights during its output Hadamard/scaling stage. After the final grid synchronization, the added reduction runs only when B_weights is present and blockIdx.z is zero. It sums corresponding elements across expert planes into plane zero. The constant 32 partitions elements into warp-sized groups; each expert-plane stride is size_m × size_n. [source; call_46f207f7030f49ed927a584f24bee1a5, call_925a7137209846c6ae6473833ffd9360]

Whole-tree multi-GEMM search finds Python calls in BlockSparseMLP and attention. Gate/up calls and attention's K/V call pass no weights, so they do not acquire the new reduction. Only the MLP down call supplies routing weights and consumes the reduced first plane. [source; call_e73eea6031fc4f09b1b6eecd51adacdb, call_4b2ce8682ddc4aafa64ece154d775325, call_a2c42eebb10b46b8a435cad33a209c00, call_4878c88c5a8b4e52bde0f87ded17c62a]

Reduction accumulates in float for FP32 output but uses sequential __hadd for FP16 output. A standard-library binary16 transcription produced 0 for [2048, 1, -2048], whose exact sum is 1, illustrating rounding sensitivity rather than proving disagreement with the previous implementation. The same check verified complete scalar indexing for example plane sizes 128 and 4096. [execution; call_99a9821a14e54b7dbee7065c55c68e5f, call_925a7137209846c6ae6473833ffd9360]

The inspected model constructors remain compatible with load-time output dtype selection: Mixtral requests FP16 and Qwen3 MoE requests FP32. TransformerBlock and ParallelDecoderBlock invoke their MLP without a per-call dtype override and immediately add its result into the residual. The latter is a generic accepting call site, not evidence that a registered model installs BlockSparseMLP there. [source; call_a4ad1c98f73a4cc29e8fba8401561042, call_3ae4981ad3444af487df0a34885b320c, call_6c4d2be7adad42ff9dae070afc5c3574, call_fe63c6f9973844ae96e42fa59f69fa34]

## Authoring-time findings — pending review

### inherited-all-expert-buffer-count (suspected; defect)

The previously recorded all-expert fused-path mismatch is carried over, not repaired by native routing.

Trigger: One flattened token, fully EXL3 experts, activate_all_experts=True, and num_experts different from num_experts_per_tok.

Expected: Evaluate all experts or choose the ordinary path.

Actual: Routing returns num_experts indices while persistent expert buffers retain num_experts_per_tok planes. The first multi-GEMM encounters its index-count/output-plane check. Decoder callers forward params; this is a conditional API failure, not proof that default conversion reaches the combination.

Locations: 8357593c39b444f9e7e46bd90d385b6dcd7e1c62:exllamav3/modules/block_sparse_mlp.py — BlockSparseMLP.forward

Source evidence: call_4717b600aab34fb7bca9ae16422891f9, call_4878c88c5a8b4e52bde0f87ded17c62a, call_599c22d7c0a64b918a067a89652ffd79, call_133602b38a39477b8c33bb2d1a8fdf24, call_fe63c6f9973844ae96e42fa59f69fa34, call_6c4d2be7adad42ff9dae070afc5c3574

source_inspection: Compared native routing cardinality, persistent allocations, unchanged dispatch and native shape checks. [call_4717b600aab34fb7bca9ae16422891f9, call_4878c88c5a8b4e52bde0f87ded17c62a, call_599c22d7c0a64b918a067a89652ffd79]. Limits: No CUDA execution.

### fused-output-dtype-override (suspected; behavior_change)

The fused path no longer honors the forward call's out_dtype override.

Trigger: Call the single-token fused path with out_dtype different from the load-time output dtype.

Expected: Preserve the former precedence of per-call out_dtype over self.out_dtype.

Actual: The returned view uses cfg.out_d, allocated using only self.out_dtype and the FP16 fallback. Inspected decoder callers omit the override, so they do not demonstrate this incompatibility.

Locations: 8357593c39b444f9e7e46bd90d385b6dcd7e1c62:exllamav3/modules/block_sparse_mlp.py — BlockSparseMLP.forward

Source evidence: call_4878c88c5a8b4e52bde0f87ded17c62a, call_fe63c6f9973844ae96e42fa59f69fa34, call_6c4d2be7adad42ff9dae070afc5c3574

source_inspection: Compared removed per-call allocation with load-time allocation and inspected decoder call sites. [call_4878c88c5a8b4e52bde0f87ded17c62a, call_6c4d2be7adad42ff9dae070afc5c3574]. Limits: External callers were not available.

### persistent-output-alias (suspected; behavior_change)

Fused forward returns reusable workspace storage instead of a separate reduction result.

Trigger: Retain a fused forward result across another fused call on the same module.

Expected: Previously returned values remain independent of later forward calls.

Actual: The first-plane view shares cfg.out_d, which the next down projection overwrites. Inspected decoder callers consume the result immediately in residual addition; no retained-output failure was demonstrated there.

Locations: 8357593c39b444f9e7e46bd90d385b6dcd7e1c62:exllamav3/modules/block_sparse_mlp.py — BlockSparseMLP.forward

Source evidence: call_4878c88c5a8b4e52bde0f87ded17c62a, call_fe63c6f9973844ae96e42fa59f69fa34, call_6c4d2be7adad42ff9dae070afc5c3574

source_inspection: Traced the returned slice to persistent output storage and inspected immediate consumers. [call_4878c88c5a8b4e52bde0f87ded17c62a, call_6c4d2be7adad42ff9dae070afc5c3574]. Limits: No tensor-lifetime or concurrent-call execution test.

## Uncertainty and limits

No extension build, repository execution, GPU correctness test or performance measurement was performed.

The scalar check models indexing and binary16 rounding, not CUDA scheduling, ATen behavior or equivalence to the previous torch.sum implementation.

Routing now directly consumes routing_gate.inner.weight rather than invoking Linear.forward. General compatibility with alternative router storage and optional bias was not established.
