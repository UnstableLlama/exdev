# d5c48a647bed87ade58919b147a8ed2b461c9bde


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/d5c48a647bed87ade58919b147a8ed2b461c9bde) · [Evidence ledger](draft.json)

Adds optional shared experts and combined quantization allocation, but fused execution skips their contribution and plain MLP allocation is incompatible with the declared interface.

- [Shared experts alongside routed experts](#block-sparse-mlp)

## Problem

BlockSparseMLP previously represented only routed experts. This change adds an optional always-evaluated shared MLP and includes its projections in TransformerBlock quantization allocation. [source; call_cce47444b97b4ea083da488434dd8d9a, call_880b1309672c4ecc8c36f68e23e69b11]

## Reasoning

Shared execution and allocation are complementary: registering the shared module makes its linears visible to recursive loading and conversion, while extending allocation supplies strategies for those additional quantization targets. [source; call_cce47444b97b4ea083da488434dd8d9a, call_880b1309672c4ecc8c36f68e23e69b11, call_7522bf55e9054f8ca5188c171bbfc95b, call_df8e8127fe0a430da3c4c89d33cc364e]

## Impact

The existing MixtralModel and Qwen3MoeModel constructors remain compatible because neither supplies the new optional argument. Neither enables shared experts through this change. [source; call_4d6694dcb04244a6a75fea1111e1094a, call_b7da23714b854505977f5d1e3000cf3a, call_93e5fff47f6a4821b7ad900c56029f45, call_cce47444b97b4ea083da488434dd8d9a]

Support is incomplete: the fused single-token branch returns before the new addition, and allocation assumes shared experts expose GatedMLP-style projection lists despite also accepting MLP. [source; call_cce47444b97b4ea083da488434dd8d9a, call_880b1309672c4ecc8c36f68e23e69b11, call_9f5f015c952d4eb689a9fab26b8f07a7]

## Source Notes

The earlier BlockSparseMLP introduction entry was read. It establishes the routed/fused execution and allocation background and records an all-expert-routing versus fused-buffer cardinality defect. [ancestor; call_88c7ecf885ab479281d7b3eaad4d6c64]

Issue #16, “RuntimeError: CUDA error: invalid configuration argument,” concerns tokenizer truncation; #43, “Error converting abliterated Qwen3 mlabonne/Qwen3-30B-A3B-abliterated,” concerns invalid inference states and Cholesky failure. Their relationship to this task is only inferred shared-source context: #16 includes transformer.py in its traceback and #43 lists BlockSparseMLP in its model log. Neither establishes motivation for shared experts. [inference; call_323dafd169cd4a00ba2bf71b6643d308, call_e49b8d21990d4796bc37ff20093750cc, call_9b179bca70df46cba6ec7254beb8c3bc]

Other inspected discussions have different framing: #39, “Gemma 3 architecture not in list?”, discusses branch availability and frontend behavior; #33, “Error converting model,” reports file-opening failures and later GLM sampling problems; #34, “torch._C._LinAlgError on last layer of quant,” and #42, “converting to 3.0 bpw causes error; block state has 0 inf values and 34 NaN values,” discuss numerical conversion failures. PR #26, “Superior 3INST parameters,” proposes codebook multiplier changes. Shared conversion-file context is an inferred association, not evidence these discussions prompted this task. [inference; call_124204ab3bfd4ce9823866bcdbff2edc, call_84160bb846624e6d973fd1ca17c9d805, call_d155351661564e18b4abbdc958e37a4f, call_08688b987b1e434880192bd23b6ea1cf, call_16a4ccb02dc64098a616595756018ebe]

<a id="block-sparse-mlp"></a>

## Shared experts alongside routed experts

BlockSparseMLP.__init__ adds shared_experts: MLP | GatedMLP | None, defaulting to None. A supplied object is stored and registered as a submodule. Module's recursive iteration, load, unload, weight counting and calibration-map collection therefore include it without adding it to the routed expert lists. [source; call_cce47444b97b4ea083da488434dd8d9a, call_7522bf55e9054f8ca5188c171bbfc95b]

In the ordinary branch, forward first accumulates routing-weighted expert outputs, restores x.shape, then adds shared_experts.forward(x, params) before output-dtype conversion. The shared branch sees every input token, the original input tensor and the same params; it receives no routing weight. Its output must be compatible with the routed output's shape and in-place addition. [source; call_71afa2539c81434181171a859cd8f311, call_cce47444b97b4ea083da488434dd8d9a]

MLP.forward computes down(activation(up(x))); GatedMLP.forward sums sliced down(activation(gate(x)) × up(x)) results. Existing decoder calls optionally normalize their input before invoking the MLP and pass params unchanged. The new shared call reuses BlockSparseMLP's input directly rather than introducing another normalization, routing step or output-dtype override. [source; call_9f5f015c952d4eb689a9fab26b8f07a7, call_d4174192e4bf45918cef1be1dc581928, call_8857147cc8984f24a7ebfdcbc5d32f89, call_cce47444b97b4ea083da488434dd8d9a]

The unchanged branch threshold counts flattened tokens, not merely the leading batch dimension: y = x.view(-1, hidden_size). More than one token, or non-EXL3/mixed routed storage, selects the ordinary branch. Exactly one token with all routed projections EXL3 selects fusion. Shared storage does not participate in that fusion eligibility test. [source; call_71afa2539c81434181171a859cd8f311, call_cce47444b97b4ea083da488434dd8d9a]

TransformerBlock.allocate_q appends shared gates, ups and downs to the corresponding routed lists. allocate_transformer sums each combined list's weight counts and expands a common group allocation back to individual keys. Shared projections consequently affect the budget and share each projection group's bit-width decision; this does not give them independent allocation choices. ParallelDecoderBlock.allocate_q is unchanged. [source; call_880b1309672c4ecc8c36f68e23e69b11, call_5b5b86813b18411dbb7d08aaf7ec70ee, call_d4174192e4bf45918cef1be1dc581928]

Whole-parent searches identify MixtralModel and Qwen3MoeModel as BlockSparseMLP construction sites, both leaving shared experts absent. TransformerBlock.forward directly dispatches to its supplied MLP; ParallelDecoderBlock has another generic MLP dispatch but its declared constructor type excludes BlockSparseMLP. Conversion main is the located allocate_q caller and requires every loaded quantization-target linear to have a strategy. [source; call_4d6694dcb04244a6a75fea1111e1094a, call_b7da23714b854505977f5d1e3000cf3a, call_93e5fff47f6a4821b7ad900c56029f45, call_d4174192e4bf45918cef1be1dc581928, call_f17da2020e954944a2515dcbfd27a06a, call_df8e8127fe0a430da3c4c89d33cc364e]

A bounded Python AST check of the reconstructed fused tail reports Assign, Return, Assign, If, Return: the first return precedes shared evaluation. Integer shape modeling also finds eight all-expert indices incompatible with a fused buffer allocated for two selected experts. [execution; call_098972fe482e454495ff136bd93edb6a]

## Authoring-time findings — pending review

### fused-shared-unreachable (suspected; defect)

The new shared-expert addition is unreachable in the fused branch.

Trigger: Supply shared_experts and forward exactly one flattened token with all routed expert projections stored as EXL3.

Expected: Return the routed result plus the shared MLP result, as the ordinary branch does.

Actual: The existing return final_hidden_states.view(x.shape) executes before the newly appended shared call. Only routed output is returned. TransformerBlock.forward can dispatch to this branch, but the inspected built-in constructors do not supply shared experts, limiting demonstrated reach to callers using the new API.

Locations: d5c48a647bed87ade58919b147a8ed2b461c9bde:exllamav3/modules/block_sparse_mlp.py — BlockSparseMLP.forward

Source evidence: call_cce47444b97b4ea083da488434dd8d9a, call_71afa2539c81434181171a859cd8f311, call_8857147cc8984f24a7ebfdcbc5d32f89, call_d4174192e4bf45918cef1be1dc581928, call_4d6694dcb04244a6a75fea1111e1094a

source_inspection: Compared both changed return paths and inspected decoder dispatch and construction sites. [call_cce47444b97b4ea083da488434dd8d9a, call_d4174192e4bf45918cef1be1dc581928]. Limits: No tensor or CUDA execution.

scalar_transcription: Reconstructed the task's fused tail in parent source and inspected its AST statement order. [call_098972fe482e454495ff136bd93edb6a]. Limits: Static Python reconstruction, not execution of BlockSparseMLP.forward.

### shared-mlp-allocation-interface (suspected; defect)

Allocation does not support the plain MLP type admitted by shared_experts.

Trigger: Construct a TransformerBlock containing BlockSparseMLP(shared_experts=<MLP instance>) and call allocate_q with a valid quantization budget.

Expected: Allocate strategies for the shared MLP's up and down projections.

Actual: TransformerBlock.allocate_q first accesses shared_experts.gates, which MLP does not define; it stores singular up and down instead. GatedMLP agrees with the new list-based accesses. Conversion main calls allocate_q before loading the module, so this API combination fails at allocation; neither inspected built-in sparse-model constructor supplies it.

Locations: d5c48a647bed87ade58919b147a8ed2b461c9bde:exllamav3/modules/transformer.py — TransformerBlock.allocate_q

Source evidence: call_880b1309672c4ecc8c36f68e23e69b11, call_cce47444b97b4ea083da488434dd8d9a, call_9f5f015c952d4eb689a9fab26b8f07a7, call_f17da2020e954944a2515dcbfd27a06a, call_df8e8127fe0a430da3c4c89d33cc364e

source_inspection: Compared both admitted shared-module implementations with the new attribute reads and the located conversion caller. [call_9f5f015c952d4eb689a9fab26b8f07a7, call_880b1309672c4ecc8c36f68e23e69b11, call_df8e8127fe0a430da3c4c89d33cc364e]. Limits: Attribute failure inferred from source; no repository execution.

### inherited-all-expert-fusion-cardinality (suspected; defect)

The ancestor-recorded all-expert fused-buffer mismatch is carried over unchanged.

Trigger: Forward one flattened token with fully EXL3 routed experts, activate_all_experts=True, and num_experts different from num_experts_per_tok.

Expected: Evaluate all experts using compatible buffers or select the ordinary branch.

Actual: Native routing returns num_experts indices, while fused intermediate buffers retain num_experts_per_tok entries. exl3_mgemm checks indices dimension 1 against output dimension 0, so the first fused call encounters a shape-check failure. The task does not change this dispatch or allocation. Decoder forwarding passes params through; conversion can supply the flag, but a default conversion reaching this fully quantized single-token case was not established.

Locations: d5c48a647bed87ade58919b147a8ed2b461c9bde:exllamav3/modules/block_sparse_mlp.py — BlockSparseMLP.forward

Source evidence: call_71afa2539c81434181171a859cd8f311, call_e7fc9554541b46dd8f608865c1235a82, call_099a4490da8a4e0793237e2ffd116bce, call_cce47444b97b4ea083da488434dd8d9a, call_df8e8127fe0a430da3c4c89d33cc364e

source_inspection: Rechecked current parent routing, fused allocations and native shape validation against the task diff. [call_e7fc9554541b46dd8f608865c1235a82, call_71afa2539c81434181171a859cd8f311, call_099a4490da8a4e0793237e2ffd116bce, call_cce47444b97b4ea083da488434dd8d9a]. Limits: Conditional source path, not a reproduced CUDA failure.

scalar_transcription: Modeled eight all-expert indices against a two-expert fused buffer and measured unequal cardinalities. [call_098972fe482e454495ff136bd93edb6a]. Limits: Integer shape arithmetic only.

## Uncertainty and limits

No repository inference, CUDA kernel, end-to-end conversion or performance test was run.

The Python check reconstructs the changed fused tail for AST inspection and models integer buffer dimensions; it does not execute tensor operations.

No supplied model constructor exercises shared experts, so checkpoint-specific shared-module shapes, calibration-map choices and numerical accuracy remain unverified.
