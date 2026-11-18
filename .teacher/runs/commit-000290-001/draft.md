# 6735462a21fc889267373011b5867868e57c14f8


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/6735462a21fc889267373011b5867868e57c14f8) · [Evidence ledger](draft.json)

Replaces boolean routing dispatch with explicit standard, DS3 and Dots policies and adds configurable bias lookup. Dots1 is migrated, but custom bias export remains inconsistent and new registry imports lack implementation files.

- [Explicit routing policy and configurable correction-bias lookup](#block-sparse-mlp)

## Problem

BlockSparseMLP selected routing through a boolean and group-count condition, leaving grouped routing disabled. The change replaces this with explicit router selection. [source; call_81e6e71f8d3148f6b87ff7237fcd5fe5]

## Reasoning

Selecting a routing function during construction separates routing policy from expert execution. Dots1's simultaneous keyword migration is necessary because deepseekv3_routing is removed. [source; call_81e6e71f8d3148f6b87ff7237fcd5fe5, call_39c773ea018d479d895c92eaead89ce2]

## Impact

Dots1 retains its existing Dots router; Mixtral and Qwen3 MoE now use the Python standard router instead of the native implementation. The added Ernie registry imports reference files absent from the parent and not supplied by this change. [source; call_39c773ea018d479d895c92eaead89ce2, call_b61e9be6b8004e7aba829c685a1e8936, call_c27e25a6216f48fe8dc7fd3488a69d32, call_81e6e71f8d3148f6b87ff7237fcd5fe5, call_1882289f9dbf4b838b79388678da59b1, call_250ae712feed420b826260ed8f24f363]

## Source Notes

Read the BlockSparseMLP introduction, correction-biased-routing entry and native-call repair entry. They establish the earlier fusion design, disabled grouped route and recorded conditional input/output limitations. [ancestor; call_0d626b78c6834d44adc0d844a66eac9b, call_fbc9a6d8f39d4d2bb922ebf02294b8b3, call_af2fe85d42e240cdb70502b194958d9f]

Issue #51, “dots.llm1 support,” is an architecture-support request with a later report of support and a first-layer quantization workaround. Its relationship here is inferred from Dots1 and the existing sigmoid router, not an explicit link to this refactor. [inference; call_707d06ee37a941e5b20a510c51dc9274, call_c9df1622cbd6435f948abc20717a258a]

Closed issue #43, “Error converting abliterated Qwen3 mlabonne/Qwen3-30B-A3B-abliterated,” concerns NaN states and Cholesky failure. Its inferred association is the BlockSparseMLP conversion log, not evidence that routing refactoring fixes that failure. [inference; call_afede01b0ee14571afc37954c1312ac8, call_26a34886c6a647d2916be301d4e750fe, call_81e6e71f8d3148f6b87ff7237fcd5fe5]

Issue #7, “quantizing model: undefined symbol: __cxa_call_terminate,” reports native-extension loading trouble. Its inferred connection is shared package-initialization traceback context; it is a different failure from the missing Ernie modules. [inference; call_821a922bdd02403884c518fdc98e5efa, call_1882289f9dbf4b838b79388678da59b1]

<a id="block-sparse-mlp"></a>

## Explicit routing policy and configurable correction-bias lookup

Construction accepts router_type='std', 'ds3' or 'dots', stores the corresponding function in routing_fn, and rejects other names. forward invokes that function before the unchanged ordinary-versus-fused expert dispatch. [source; call_81e6e71f8d3148f6b87ff7237fcd5fe5, call_ab4f548364dc435cbd9361ef76fa8da7]

Whole-parent searches locate three BlockSparseMLP builders. Dots1 migrates its explicit boolean to router_type='dots'; Mixtral and Qwen3 MoE omit both options and therefore accept the new standard default. All use keyword arguments. No other reader of the removed deepseekv3_routing attribute was found. [source; call_9bc97b31ff184145b852f24b1e44bd96, call_cbd4785778184157a6d51801f2539674, call_c9df1622cbd6435f948abc20717a258a, call_b61e9be6b8004e7aba829c685a1e8936, call_c27e25a6216f48fe8dc7fd3488a69d32, call_39c773ea018d479d895c92eaead89ce2]

routing_std is the renamed existing Python helper, previously only referenced by a commented call. Like the replaced native router, it projects token rows, selects top-k logits and softmax-normalizes selected values. One flattened token without activate_all_experts reuses output buffers; otherwise it allocates results and can select every expert. This removes a native boundary but establishes no speed improvement. [source; call_aceb8f60edb7432ea33f65216c1dd2a8, call_ab4f548364dc435cbd9361ef76fa8da7, call_5105d179a15240098c17a63380ab6ed9, call_81e6e71f8d3148f6b87ff7237fcd5fe5]

routing_dots adds correction bias to logits before top-k and sigmoid normalization. routing_ds3 instead adds bias to sigmoid scores for selection, scores each group by its best two corrected scores, masks unselected groups and gathers uncorrected sigmoid weights. DS3 therefore requires divisible group sizes and at least two experts per group. Both sigmoid routes normalize with a 1e-20 denominator stabilizer and multiply by routed_scaling_factor. [source; call_ab4f548364dc435cbd9361ef76fa8da7]

Explicit DS3 selection removes the earlier unassigned-routing-results branch, but does not validate DS3 inputs. Previously the sole active Dots call required n_group=topk_group=1; Dots1 already supplies those values. The new selector calls each helper directly, without adding argument preparation or missing-bias handling. [source; call_b49a425f23454025a9134f286ecc1a6d, call_ab4f548364dc435cbd9361ef76fa8da7, call_c9df1622cbd6435f948abc20717a258a, call_81e6e71f8d3148f6b87ff7237fcd5fe5]

key_e_score_bias changes the optional tensor lookup to <module key>.<configured suffix>, falling back to gate.e_score_correction_bias for a missing or empty suffix. RoutingCFG receives the loaded tensor as before. get_tensors remains on the hard-coded old suffix, so custom lookup and export naming disagree. [source; call_ca5acb4c60444928bb91b4f2159794d8, call_ab4f548364dc435cbd9361ef76fa8da7, call_81e6e71f8d3148f6b87ff7237fcd5fe5]

Both dots-studio/dots.llm1.base and dots-studio/dots.llm1.inst configurations specify 128 routed experts, six selected experts, hidden size 4096, expert width 1408 and scale 2.5. Both select one initial dense layer, overriding the source defaults of eight selected experts and three dense layers. Their routing configuration agrees with Dots1's unchanged single-group construction. [source; call_4da986062a544be4aae5fc7708581314, call_84bf18eb6abe4799aabb2c5362a41e90, call_c9df1622cbd6435f948abc20717a258a]

Representative base-checkpoint headers contain model.layers.1.mlp.gate.e_score_correction_bias [128] and gate.weight [128,4096], matching the unchanged default lookup and expert count. Expert gate/up weights are [1408,4096], down weights [4096,1408], and shared gate/up weights [2816,4096]. The unchanged default path needs no alternate bias name; custom suffix presence is caller-dependent. Attention and dense-layer tensors in these headers are not read by BlockSparseMLP itself. [source; call_fcf75cda289f422498937506fcab66a7, call_95c6481c099a4a8aa77a6d6b42a90309, call_ab4f548364dc435cbd9361ef76fa8da7, call_c9df1622cbd6435f948abc20717a258a]

A scalar transcription with logits [2,1,0] and two selected experts produced standard weights approximately [0.731059,0.268941], summing to 1, versus zero-bias Dots weights [1.366123,1.133877], summing to scale 2.5. Integer shape arithmetic also confirmed that 128 all-expert indices cannot satisfy a six-plane fused-output equality check. [execution; call_5a10fa49ae2941aeb17d2a5584be092b]

The all-expert fused-buffer mismatch and workspace-backed fused return recorded by earlier entries remain unchanged. The grouped unassigned-variable defect is removed by explicit dispatch, while optional Dots inputs remain unguarded. TransformerBlock forwards params and immediately consumes the MLP result; ParallelDecoderBlock has another generic call but does not declare BlockSparseMLP among its constructor types. [source; call_ab4f548364dc435cbd9361ef76fa8da7, call_81e6e71f8d3148f6b87ff7237fcd5fe5, call_4c733e3b50b0424d976290d20d714723, call_903aaa9f1efa43d485b1d94a18379f9a]

## Authoring-time findings — pending review

### missing-ernie-registry-modules (suspected; defect)

The registry adds imports without supplying their implementation modules.

Trigger: Import exllamav3.models.architectures, including through Config.from_directory.

Expected: Load the architecture registry and resolve supported configurations.

Actual: ernie4_5.py and ernie4_5_moe.py are absent from the parent model directory, and the complete task diff adds neither. The first new relative import consequently cannot resolve in this tree. Config.from_directory imports the registry before selecting any model, so reach is not limited to Ernie configurations; models/__init__.py does not itself import the registry.

Locations: 6735462a21fc889267373011b5867868e57c14f8:exllamav3/models/architectures.py — module imports

Source evidence: call_1882289f9dbf4b838b79388678da59b1, call_250ae712feed420b826260ed8f24f363, call_3424d69e85e54a37946124e3dc7823b1, call_7803a6d8ae7d4d26a093e1210fc40154, call_04542899467649f6bacedfb6c71906d8, call_5c20c6079fcf4dc5946930b9beb526c8

source_inspection: Compared the parent module listing, registry importer and all three task sections. [call_1882289f9dbf4b838b79388678da59b1, call_39c773ea018d479d895c92eaead89ce2, call_81e6e71f8d3148f6b87ff7237fcd5fe5, call_250ae712feed420b826260ed8f24f363]. Limits: No import was executed.

### custom-bias-export-name (suspected; defect)

Custom correction-bias lookup is not propagated to tensor export.

Trigger: Load a present bias using a nondefault key_e_score_bias, then call BlockSparseMLP.get_tensors.

Expected: Export the bias under the configured tensor name.

Actual: load requests the configured suffix, but get_tensors emits gate.e_score_correction_bias. No built-in construction site supplies a custom suffix, so established reach is the new API rather than an existing model workflow.

Locations: 6735462a21fc889267373011b5867868e57c14f8:exllamav3/modules/block_sparse_mlp.py — BlockSparseMLP.get_tensors

Source evidence: call_81e6e71f8d3148f6b87ff7237fcd5fe5, call_ab4f548364dc435cbd9361ef76fa8da7, call_ca5acb4c60444928bb91b4f2159794d8, call_9e2988f3adb5476a9727f94c5185deb9, call_9bc97b31ff184145b852f24b1e44bd96

source_inspection: Compared configured lookup with unchanged dictionary emission. [call_ab4f548364dc435cbd9361ef76fa8da7, call_81e6e71f8d3148f6b87ff7237fcd5fe5]. Limits: No export/reload round trip was executed.

### sigmoid-router-required-inputs (suspected; new_requirement)

Explicit router selection exposes helpers whose required inputs remain optional in the constructor.

Trigger: Select dots or ds3 with absent correction bias or scaling; alternatively select ds3 while leaving group counts None or using fewer than two experts per group.

Expected: Validate router-specific preconditions or provide supported defaults.

Actual: Both helpers unconditionally use bias and scale; DS3 also reshapes by group counts and calls topk(2). Dots1 supplies scale and single-group values, but bias loading remains optional. No located built-in constructor selects ds3.

Locations: 6735462a21fc889267373011b5867868e57c14f8:exllamav3/modules/block_sparse_mlp.py — routing_dots / routing_ds3

Source evidence: call_ab4f548364dc435cbd9361ef76fa8da7, call_81e6e71f8d3148f6b87ff7237fcd5fe5, call_b49a425f23454025a9134f286ecc1a6d, call_c9df1622cbd6435f948abc20717a258a, call_9bc97b31ff184145b852f24b1e44bd96

source_inspection: Compared constructor defaults and selector dispatch with helper arithmetic and all located model builders. [call_ab4f548364dc435cbd9361ef76fa8da7, call_81e6e71f8d3148f6b87ff7237fcd5fe5]. Limits: Conditional API failures; representative base-checkpoint bias is present.

### inherited-all-expert-fusion-count (suspected; defect)

All-expert routing still conflicts with fixed selected-expert fused buffers.

Trigger: One flattened token, fully EXL3 experts, activate_all_experts=True and num_experts != num_experts_per_tok.

Expected: Use compatible all-expert storage or dispatch to ordinary expert evaluation.

Actual: Routing returns num_experts indices while fused buffers retain num_experts_per_tok planes. The first exl3_mgemm checks indices dimension 1 against output dimension 0 and rejects the mismatch. TransformerBlock forwards params, establishing conditional reach, not that ordinary calibration necessarily uses this combination.

Locations: 6735462a21fc889267373011b5867868e57c14f8:exllamav3/modules/block_sparse_mlp.py — BlockSparseMLP.forward

Source evidence: call_ab4f548364dc435cbd9361ef76fa8da7, call_81e6e71f8d3148f6b87ff7237fcd5fe5, call_903aaa9f1efa43d485b1d94a18379f9a, call_810d56918ce646d68be1ffa46251f9f5, call_4c733e3b50b0424d976290d20d714723

scalar_transcription: Modeled 128 all-expert indices against six fused output planes. [call_5a10fa49ae2941aeb17d2a5584be092b]. Limits: Integer shape arithmetic, not repository or GPU execution.

### inherited-fused-output-contract (suspected; behavior_change)

The fused path retains workspace-backed results and ignores the per-call output-dtype override.

Trigger: Retain a fused result across another fused call, or request a dtype different from the load-time output dtype.

Expected: An independent result honoring out_dtype, consistent with the ordinary path.

Actual: The returned view shares cfg.out_d and retains its allocation dtype. A later fused call overwrites the workspace. Located decoder callers consume results immediately and omit the override, so they do not demonstrate either incompatibility.

Locations: 6735462a21fc889267373011b5867868e57c14f8:exllamav3/modules/block_sparse_mlp.py — BlockSparseMLP.forward

Source evidence: call_ab4f548364dc435cbd9361ef76fa8da7, call_81e6e71f8d3148f6b87ff7237fcd5fe5, call_810d56918ce646d68be1ffa46251f9f5, call_4c733e3b50b0424d976290d20d714723

source_inspection: Traced fused return storage and compared decoder consumers. [call_ab4f548364dc435cbd9361ef76fa8da7, call_4c733e3b50b0424d976290d20d714723]. Limits: No tensor lifetime or dtype test.

## Uncertainty and limits

No repository inference, import attempt, CUDA invocation or performance measurement was performed.

The scalar transcription uses Python double precision, not tensor precision; it does not test top-k ties, FP16 underflow of the 1e-20 stabilizer or native/Python runtime equivalence.

Checkpoint inspection covers representative base-model header entries, not every layer or shard, and does not establish instruction-checkpoint tensor identity.

Caller compatibility is established for literal repository construction sites, not dynamic or external callers. External positional callers may also be affected by inserting key_e_score_bias before qmap.
