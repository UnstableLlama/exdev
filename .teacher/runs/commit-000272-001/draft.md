# 39ded1b7b83ccb63a7893e2c25160225ffd3a7b3


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/39ded1b7b83ccb63a7893e2c25160225ffd3a7b3) · [Evidence ledger](draft.json)

Removes an extra argument from BlockSparseMLP's native routing call, restoring its four-parameter interface for Mixtral and Qwen3 MoE without changing routing algorithms or inherited conditional limitations.

- [Restore the native routing call contract](#block-sparse-mlp)

## Problem

The default BlockSparseMLP route supplied five arguments to a native function declared, implemented and bound with four parameters. [source; call_4fe7f9c7606741fbb0abae986c908a1b, call_1ce9fed7d73246388a9a6cc3e21f1645, call_d0d382ff63034220bf89a3197c9b85b1, call_7a3f6621e1fd434ca79b4947736c868f]

## Reasoning

Removing the trailing False restores the existing native interface rather than introducing a new routing option. The native implementation reads activate_all_experts from params. [source; call_4fe7f9c7606741fbb0abae986c908a1b, call_d0d382ff63034220bf89a3197c9b85b1]

## Impact

Mixtral and Qwen3 MoE use the default native route and therefore benefit from the repaired call. Dots1 explicitly selects the separate single-group Dots router, so this edit does not change its routing call. [source; call_9c8c59743f5b4bf797cf149d6b5c4b38, call_db7d0d84c39c433caa6b47c2121c56cd, call_fdb5e32bb15d4f47b8dd5bf27b31f20d, call_e5b969b808f247e38d3cf80adfea8878, call_4fe7f9c7606741fbb0abae986c908a1b]

## Source Notes

Read the BlockSparseMLP introduction, native-routing optimization and correction-biased-routing entries. They establish the fusion preconditions, four-argument native interface and previously recorded argument mismatch. [ancestor; call_1ad9d4eedc714d7cbe67c8893f8628c6, call_33a2395a1305486daa293943b378e412, call_94c3541cd9194f598f4ceecf7f51dcef]

<a id="block-sparse-mlp"></a>

## Restore the native routing call contract

The entire edit removes one positional False from BlockSparseMLP.forward. Whole-parent search finds this as the sole Python call to blocksparse_mlp_routing; its declaration and binding remain unchanged. [source; call_4fe7f9c7606741fbb0abae986c908a1b, call_aadac5dbd51f47e093fcd87ea5b0aae0, call_1ce9fed7d73246388a9a6cc3e21f1645, call_7a3f6621e1fd434ca79b4947736c868f]

The native router multiplies flattened token rows by the gate matrix, selects expert logits and softmax-normalizes the selected values. One token without all-expert activation reuses configured output buffers; other cases allocate results and select either the configured expert count or every expert. It returns indices followed by weights. [source; call_d0d382ff63034220bf89a3197c9b85b1]

Routing occurs before the ordinary-versus-fused expert dispatch, so the argument repair applies to both paths. The ordinary path handles multiple flattened tokens or non-fully-EXL3 experts; the fused path handles one token with fully EXL3 experts. The threshold 1 is a token-count dispatch condition, not a newly tuned performance threshold. [source; call_e5b969b808f247e38d3cf80adfea8878, call_4fe7f9c7606741fbb0abae986c908a1b]

Repository construction sites are Mixtral, Qwen3 MoE and Dots1. TransformerBlock forwards params to its MLP and immediately consumes the result in residual addition. ParallelDecoderBlock has another generic MLP call, but its declared constructor types exclude BlockSparseMLP; this is not evidence of a registered sparse-model workflow there. [source; call_630a4b1e94f14d0e9e8574a13c508db5, call_9c8c59743f5b4bf797cf149d6b5c4b38, call_db7d0d84c39c433caa6b47c2121c56cd, call_fdb5e32bb15d4f47b8dd5bf27b31f20d, call_8bf8287596514c09b56db8bd6d102d26]

The author's “Fix regression” description is consistent with restoring the previously documented native interface. It does not imply that all conditional BlockSparseMLP paths now succeed: grouped routing, optional Dots inputs and fused-output contracts remain unchanged. [inference; call_4fe7f9c7606741fbb0abae986c908a1b, call_33a2395a1305486daa293943b378e412, call_e5b969b808f247e38d3cf80adfea8878]

## Authoring-time findings — pending review

### inherited-all-expert-fusion-count (suspected; defect)

The repair removes the argument mismatch but carries over the all-expert fused-buffer mismatch.

Trigger: One flattened token, fully EXL3 experts, activate_all_experts=True and num_experts different from num_experts_per_tok.

Expected: Evaluate all experts with compatible storage or select the ordinary path.

Actual: Routing produces num_experts indices while fused buffers retain num_experts_per_tok planes. The first multi-GEMM checks index count against output planes and rejects the mismatch. TransformerBlock forwards params, establishing conditional API reach, not that ordinary conversion reaches this combination.

Locations: 39ded1b7b83ccb63a7893e2c25160225ffd3a7b3:exllamav3/modules/block_sparse_mlp.py — BlockSparseMLP.forward

Source evidence: call_e5b969b808f247e38d3cf80adfea8878, call_d0d382ff63034220bf89a3197c9b85b1, call_7ffa9b1b807c418ca95fbf4b3448dda6, call_8bf8287596514c09b56db8bd6d102d26, call_4fe7f9c7606741fbb0abae986c908a1b

source_inspection: Compared router cardinality, persistent allocation, dispatch and native shape validation. [call_e5b969b808f247e38d3cf80adfea8878, call_d0d382ff63034220bf89a3197c9b85b1, call_7ffa9b1b807c418ca95fbf4b3448dda6]. Limits: No CUDA execution.

### inherited-grouped-routing-unassigned (suspected; defect)

Grouped routing remains disabled without rejecting unsupported configurations.

Trigger: Enable deepseekv3_routing with n_group or topk_group different from 1.

Expected: Compute routing results or explicitly reject the configuration.

Actual: The grouped call remains commented out, leaving selected_experts and routing_weights unassigned before expert evaluation. None of the three located model constructors selects this unsupported combination.

Locations: 39ded1b7b83ccb63a7893e2c25160225ffd3a7b3:exllamav3/modules/block_sparse_mlp.py — BlockSparseMLP.forward

Source evidence: call_e5b969b808f247e38d3cf80adfea8878, call_4fe7f9c7606741fbb0abae986c908a1b, call_630a4b1e94f14d0e9e8574a13c508db5, call_fdb5e32bb15d4f47b8dd5bf27b31f20d

source_inspection: Traced routing assignments and inspected all located sparse-model constructors. [call_e5b969b808f247e38d3cf80adfea8878, call_9c8c59743f5b4bf797cf149d6b5c4b38, call_db7d0d84c39c433caa6b47c2121c56cd, call_fdb5e32bb15d4f47b8dd5bf27b31f20d]. Limits: Conditional API path; not executed.

### inherited-dots-required-inputs (suspected; new_requirement)

The Dots router still requires values that the enclosing API permits to be absent.

Trigger: Select single-group Dots routing with missing correction bias or routed_scaling_factor=None.

Expected: Validate required routing inputs or supply supported defaults.

Actual: routing_dots unconditionally performs arithmetic with both values. Its sole located caller is BlockSparseMLP.forward. Dots1 supplies a scaling value, but loading the correction bias remains optional.

Locations: 39ded1b7b83ccb63a7893e2c25160225ffd3a7b3:exllamav3/modules/block_sparse_mlp.py — routing_dots

Source evidence: call_e5b969b808f247e38d3cf80adfea8878, call_fdb5e32bb15d4f47b8dd5bf27b31f20d, call_4fe7f9c7606741fbb0abae986c908a1b

source_inspection: Compared constructor defaults and optional loading with unconditional router arithmetic. [call_e5b969b808f247e38d3cf80adfea8878]. Limits: No tensor operations executed.

### inherited-fused-output-contract (suspected; behavior_change)

The fused path retains its workspace-backed output and ignored per-call dtype override.

Trigger: Retain a fused result across another fused call, or request out_dtype different from the load-time output dtype.

Expected: An independent result honoring the per-call dtype, as recorded for the earlier implementation.

Actual: The returned view shares cfg.out_d and uses its load-time dtype; subsequent fused calls overwrite that workspace. Inspected decoder callers omit the override and consume results immediately, so they do not demonstrate either incompatibility.

Locations: 39ded1b7b83ccb63a7893e2c25160225ffd3a7b3:exllamav3/modules/block_sparse_mlp.py — BlockSparseMLP.forward

Source evidence: call_e5b969b808f247e38d3cf80adfea8878, call_8bf8287596514c09b56db8bd6d102d26, call_33a2395a1305486daa293943b378e412, call_4fe7f9c7606741fbb0abae986c908a1b

source_inspection: Traced the returned view to persistent allocation and compared immediate decoder consumers. [call_e5b969b808f247e38d3cf80adfea8878, call_8bf8287596514c09b56db8bd6d102d26]. Limits: No output-lifetime or dtype test.

## Uncertainty and limits

No extension invocation, GPU inference or performance measurement was performed. Interface agreement is established by source inspection, not a successful runtime test.

The change is an argument-count repair with no numerical algorithm change; a scalar computation would not validate native argument binding.

Caller searches cover literal occurrences in the parent repository, not external callers or dynamic dispatch.
