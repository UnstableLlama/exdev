# 830b6a018070a327d6d261628dff496f1303cf93


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/830b6a018070a327d6d261628dff496f1303cf93) · [Evidence ledger](draft.json)

Introduces named model components and preservation of additional source tensors during compilation, but leaves Qwen3 MoE on the incompatible single-class configuration contract.

- [Component-aware construction and compilation](#models)

## Problem

Configuration previously selected one model class, while compilation only collected tensors belonging to the instantiated model's modules. These interfaces lacked explicit component selection and a way to preserve additional component tensors. [source; call_0ce7a553da124005b3c0dd86a69b5a42, call_b4861443b21642b79e00ebda31a283e6]

## Reasoning

The component mapping and additional-tensor hook are complementary preparation: the mapping identifies component classes, and compilation asks every registered component class which extra source tensors to retain. This does not itself implement multimodal inference. [source; call_0ce7a553da124005b3c0dd86a69b5a42]

## Impact

Existing factory calls continue to select 'text' by default, but Qwen3MoeConfig is left supplying a class instead of the newly required mapping, creating an incompatible registered architecture. [source; call_0ce7a553da124005b3c0dd86a69b5a42, call_9086762c92f6460a9d824d461dcafda9, call_7551d688571e4829a8b50dba31ba4746, call_b4d052d014be4378bed162df240ef54d]

## Source Notes

The root models entry was read. It establishes the original single-class factory and explains that MistralConfig and Qwen2Config previously caused the factory to construct LlamaModel despite their registered subclasses. [ancestor; call_5e4a18d5be044d248cfa3ea32192905f]

PR #25, 'Language layers for Mistral Small 3.1 and InternVL3', discusses component models and avoiding language-only quantizations incompatible with future multimodal support. Its relationship to this task is inferred from those matching interface concerns, not an explicit commit reference. [inference; call_61bfc4f614504319b5beacd5fcb99ac0, call_0ce7a553da124005b3c0dd86a69b5a42]

Other inspected discussions have narrower, distinct framing: PR #4 corrects 'containg'; issue #7 reports an undefined native symbol; issue #6 reports a ROCm notification and installation traceback. Issue #33, 'Error converting model', initially reports file-opening failures, later identifies too many open files, and subsequently discusses GLM4 output problems. Their overlap with this task is inferred from shared files or traceback calls, not evidence that this refactor fixes them. [inference; call_c942e3ea980c4976a1e7079f25184173, call_83519ec680f34694bb975f56c601f31d, call_a16ac1c2319e47d787dacb869f4ef33a, call_db397af870fd4c6993f57846b8d462a3, call_a516748c7d5c4ee894845238da3cbec8, call_0ce7a553da124005b3c0dd86a69b5a42]

<a id="models"></a>

## Component-aware construction and compilation

Config now stores model_classes rather than model_class. Model.from_config accepts component='text', asserts that the component exists, then invokes the selected class with config and remaining keyword arguments. The architecture registry still contains a singular 'model_class' entry, but Config.from_directory consumes its 'config_class' entry instead; that registry field is not the renamed Config attribute. [source; call_0ce7a553da124005b3c0dd86a69b5a42, call_d77c275f553e443ab6e33dd0f1d02d06, call_7551d688571e4829a8b50dba31ba4746, call_3816560fb6b541018d64c268f40ec599]

Cohere, Cohere2, DeciLM, Gemma2, GLM4, Llama, Mixtral, Phi3 and Qwen3 configurations wrap their existing class in a 'text' mapping. LlamaConfig additionally accepts derived_model, using its default mapping when that argument is falsy. MistralConfig and Qwen2Config supply their own mappings through this argument, so the factory now selects their named subclasses. Both inspected subclasses delegate construction to LlamaModel; this is not a new attention implementation. [source; call_0ce7a553da124005b3c0dd86a69b5a42, call_ed89c462bf81457b9ef2d4338de740f0, call_c760e06032a140e9a3c141e0c9e7ac9f]

Whole-parent searches and AST inspection found factory calls in evaluation, examples, model_init, conversion, science utilities and tests. Every located Model.from_config call supplies only its configuration argument, so none needs an explicit component argument. Their success nevertheless depends on the configuration supplying the new mapping; the unchanged Qwen3MoeConfig violates that precondition. [source; call_b4d052d014be4378bed162df240ef54d, call_9158b3a823694f00aa02f5fcc1cfaa59, call_9086762c92f6460a9d824d461dcafda9, call_0ce7a553da124005b3c0dd86a69b5a42]

Model.get_additional_compiled_tensors defaults to an empty dictionary. compile_model merges each component's returned dictionary, reads each entry's n_bytes for shard accounting, and appends its tensor-name string after the ordinary module entries. Repeated extra names use dictionary-update replacement semantics. The hook must therefore return names loadable from config.stc and suitable byte counts; it does not return tensor payloads. [source; call_0ce7a553da124005b3c0dd86a69b5a42]

Shard writing distinguishes Module objects from strings. Modules retain prefix-based reads from work_dir/qtensors and close that collection after each module. String entries read an individual original tensor through config.stc. Both paths request BF16 preservation and contiguous tensors, then join the same output dictionary and weight map. The new branch does not close config.stc here. [source; call_0ce7a553da124005b3c0dd86a69b5a42, call_b4861443b21642b79e00ebda31a283e6, call_915728163ebe46dda2aa731c33a7de4c]

The existing shard-size conversion multiplies the configured value by 1024², making the limit binary megabytes despite the 'MB' message. Additional tensors use the same greedy packing rule: equality fits, an overflow starts another shard only when the current shard is nonempty, and an oversized item is warned about rather than split. Thus the limit is a packing target, not a hard maximum. [source; call_b4861443b21642b79e00ebda31a283e6, call_0ce7a553da124005b3c0dd86a69b5a42]

## Authoring-time findings — pending review

### qwen3-moe-component-migration (suspected; defect)

The registered Qwen3 MoE configuration is not migrated to the component mapping contract.

Trigger: Construct a valid Qwen3MoeConfig and pass it to Model.from_config.

Expected: The default text component constructs Qwen3MoeModel.

Actual: The unchanged constructor passes Qwen3MoeModel directly to Config. After this diff it is stored as model_classes, so the factory's membership test operates on a class rather than a dictionary and raises TypeError. If compilation is invoked with a separately constructed model, model_classes.items() instead raises AttributeError. Direct factory callers include model_init.init, conversion get_base_model, evaluation, examples and tests; the failure is conditional on selecting this architecture, not universal.

Locations: 830b6a018070a327d6d261628dff496f1303cf93:exllamav3/models/qwen3_moe.py — Qwen3MoeConfig.__init__, 830b6a018070a327d6d261628dff496f1303cf93:exllamav3/models/model.py — Model.from_config

Source evidence: call_9086762c92f6460a9d824d461dcafda9, call_0ce7a553da124005b3c0dd86a69b5a42, call_7551d688571e4829a8b50dba31ba4746, call_b4d052d014be4378bed162df240ef54d, call_915728163ebe46dda2aa731c33a7de4c

scalar_transcription: A standard-library Python check applied membership and .items() to a dummy model class and to its corresponding text mapping. The class produced TypeError and AttributeError; the mapping supported both operations. [call_9158b3a823694f00aa02f5fcc1cfaa59]. Limits: This models the inspected contract mismatch; it does not import or execute the repository factory or load a checkpoint.

## Uncertainty and limits

No model loading, conversion, tensor serialization or GPU execution was performed. The Python check used a dummy class to model the changed container operations.

Checkpoint configurations were not inspected model by model; this annotation does not establish compatibility across the indexed model variants.

Task-tree searches were unavailable under the strict-ancestor restriction. Post-change conclusions combine the complete supplied diff with parent source; dynamic and external callers remain unexamined.

Additional-tensor copying, filesystem behavior and peak host-memory usage remain untested.
