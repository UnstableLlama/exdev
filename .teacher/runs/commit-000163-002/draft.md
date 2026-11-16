# 830b6a018070a327d6d261628dff496f1303cf93


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/830b6a018070a327d6d261628dff496f1303cf93) · [Evidence ledger](draft.json)

Introduces named model components and an additional-tensor compilation hook, but leaves registered Qwen3 MoE on the incompatible single-class interface.

- [Component selection and compilation](#models)

## Problem

Configuration previously selected one model class, and compilation collected only the instantiated model's modules. Neither interface represented separately selectable components or additional source tensors. [source; call_633c3ace0f444ebc864f9e28a0dd248e, call_55654da583e240909c4dc4eccf58dacc]

## Reasoning

A component-name dictionary replaces the single class reference. A default text component preserves existing factory call signatures, while a class-level hook allows compilation to collect tensors without instantiating every component. [source; call_633c3ace0f444ebc864f9e28a0dd248e]

## Impact

This is preparation, not implemented multimodal inference: the factory explicitly retains a multimodal TODO, and the added tensor hook returns an empty dictionary by default. Qwen3 MoE is omitted from the configuration migration. [source; call_633c3ace0f444ebc864f9e28a0dd248e, call_8cf6485cdd8648f894d58e9ed7c8e3c3]

## Source Notes

The earlier Qwen3 MoE entry describes Qwen3MoeConfig supplying Qwen3MoeModel directly to Config and registering both through directory-based dispatch. [ancestor; call_836a495611b14dc0abd161f215cb67c6]

PR #25, “Language layers for Mistral Small 3.1 and InternVL3,” contains turboderp's stated preference for deliberate component support over language-only patches producing incompatible future multimodal checkpoints. Its connection to this change is inferred from the component-model interface, not an explicit commit reference. [inference; call_a9c51c805e534786b5004117db3cf542, call_633c3ace0f444ebc864f9e28a0dd248e]

PR #4, “chore: update config.py,” concerns a spelling correction. Issue #7, “quantizing model: undefined symbol: __cxa_call_terminate,” concerns extension loading; issue #6, “No ROCm runtime is found, using ROCM_HOME='/usr',” reports an installation/build failure. Their relationship here is only inferred from shared config.py/model.py paths, not evidence that this refactor fixes those reports. [inference; call_abaaa74061094957817cb22697ebbd84, call_76b0fe83d9214f10b28c74adc842a655, call_73842155e48a4cdeaeb26393c625a9b6, call_633c3ace0f444ebc864f9e28a0dd248e]

Issue #33, “Error converting model,” initially reports failure at compile_model's qtensors_stc.get_tensors call, later identified in the discussion as too many open files and reported resolved. The thread subsequently tracks GLM4 generation producing exclamation marks. Association with this task is inferred from the matching compiler call and later discussion of separated vision components; it does not establish a fix by this commit. [inference; call_ce52eaa724bd4ec2801a5f01cdeb7538, call_9f7418aeea434af7a30cf4d2b6df87cc, call_633c3ace0f444ebc864f9e28a0dd248e]

<a id="models"></a>

## Component selection and compilation

The complete configuration-subclass inventory contains twelve classes. At the task commit, direct Config subclasses pass these second arguments: CohereConfig → {"text": CohereModel}; Cohere2Config → {"text": Cohere2Model}; DeciLMConfig → {"text": DeciLMModel}; Gemma2Config → {"text": Gemma2Model}; Glm4Config → {"text": Glm4Model}; MixtralConfig → {"text": MixtralModel}; Phi3Config → {"text": Phi3Model}; Qwen3Config → {"text": Qwen3Model}. LlamaConfig passes derived_model when truthy, otherwise {"text": LlamaModel}. MistralConfig and Qwen2Config call LlamaConfig with derived_model set to {"text": MistralModel} and {"text": Qwen2Model}, respectively. Unchanged Qwen3MoeConfig still passes the bare Qwen3MoeModel class. [source; call_8cf6485cdd8648f894d58e9ed7c8e3c3, call_633c3ace0f444ebc864f9e28a0dd248e]

Config stores that argument verbatim as model_classes. For each of the eleven migrated configurations under its ordinary construction, Model.from_config checks membership of the requested component, defaults to "text", and invokes the corresponding class with config and forwarded kwargs. Llama's explicit nonempty override instead determines the available components. The same factory cannot consume Qwen3MoeConfig's bare class. [source; call_633c3ace0f444ebc864f9e28a0dd248e, call_fc97279a3f824567b1697808e133fbf1]

Mistral and Qwen2 now select their named model subclasses rather than LlamaModel. Both selected constructors simply delegate to LlamaModel; their configuration-class identity changes without introducing a different constructor computation. [source; call_ac4c8633508f45d1a6d351dfcce195c5, call_cfd72f06d58b4238b463dafaef4fd96d, call_fc97279a3f824567b1697808e133fbf1, call_633c3ace0f444ebc864f9e28a0dd248e]

The registry contains twelve architecture files, but the diff changes eleven of them: qwen3_moe.py is the sole omitted registered architecture file. Conversely, config.py and model.py are changed infrastructure files, not registered architecture implementations. architectures.py itself is unchanged. [source; call_8cf6485cdd8648f894d58e9ed7c8e3c3, call_633c3ace0f444ebc864f9e28a0dd248e]

The introducing ancestor entry for that omitted architecture is a5caa423bbd9d8a61266a88fb237c18fb77ec0b8, whose chapter is “Qwen3 MoE assembly and calibration.” It describes a direct Config subclass supplying Qwen3MoeModel, rather than inheritance through LlamaConfig. [ancestor; call_836a495611b14dc0abd161f215cb67c6]

At the Additional tensors block, compile_model iterates model_classes.items() and merges each class's get_additional_compiled_tensors(config) result. All eleven migrated default mappings reach the newly inherited empty hook and add nothing. A custom Llama mapping can provide other hooks. Qwen3MoeConfig instead fails at .items() if execution reaches this block. [source; call_633c3ace0f444ebc864f9e28a0dd248e, call_8cf6485cdd8648f894d58e9ed7c8e3c3]

Hook results describe tensors by key with n_bytes metadata. Compilation appends those keys after module allocations, using the existing shard budget of shard_size × 1024² bytes. An oversized tensor is warned about but not split. Module entries load from work_dir/qtensors; string entries load by exact key from config.stc, retain BF16 permission, become contiguous, and join the same output shard and weight map. Dictionary updates merge duplicate keys rather than preserving separate component namespaces. [source; call_55654da583e240909c4dc4eccf58dacc, call_633c3ace0f444ebc864f9e28a0dd248e]

Whole-tree caller search and inspected call-site context found direct Model.from_config calls in conversion/convert_model.py:get_base_model, conversion/quant_config.py:create_quantization_config_json, model_init.py:init, eval/compare_q_exllamav3.py, eval/model_diff.py (both models), examples/{async_generator,banned_strings,dynamic_gen,generation_loop,generator,loading}.py, science/kv_quant_exp.py, and tests/{generator_stresstest,test_qgemm,test_quant_fn}.py. None supplies component. These sites are unchanged by the task. [source; call_2548ed8318374a0e9d2527fab36e7654, call_8635d467bec444d7bb701815971f81df, call_633c3ace0f444ebc864f9e28a0dd248e]

Chat, perplexity evaluation and HumanEval reach the factory indirectly through model_init.init. Conversion reaches it before quantization through get_base_model and again when constructing output quantization metadata. Consequently the omitted Qwen3 MoE migration is not confined to an optional multimodal path. [source; call_8635d467bec444d7bb701815971f81df, call_55654da583e240909c4dc4eccf58dacc]

## Authoring-time findings — pending review

### qwen3-moe-component-migration (suspected; defect)

The shared configuration interface changes to a dictionary, but registered Qwen3MoeConfig still supplies a model class.

Trigger: Construct a valid Qwen3MoeConfig and pass it to Model.from_config; alternatively call compile_model with that config and reach its Additional tensors block.

Expected: Select Qwen3MoeModel as the text component and allow compilation to enumerate component hooks.

Actual: Config stores Qwen3MoeModel as model_classes. The normal factory membership test raises TypeError rather than constructing the model; compilation's .items() raises AttributeError if reached independently. All inspected factory callers omit component, including conversion, examples and evaluation entry points. Ordinary conversion fails before reaching the compiler hook.

Locations: 830b6a018070a327d6d261628dff496f1303cf93:exllamav3/models/qwen3_moe.py — Qwen3MoeConfig.__init__, 830b6a018070a327d6d261628dff496f1303cf93:exllamav3/models/model.py — Model.from_config, 830b6a018070a327d6d261628dff496f1303cf93:exllamav3/conversion/compile.py — compile_model

Source evidence: call_633c3ace0f444ebc864f9e28a0dd248e, call_8cf6485cdd8648f894d58e9ed7c8e3c3, call_2548ed8318374a0e9d2527fab36e7654, call_8635d467bec444d7bb701815971f81df

source_inspection: Compared every parent configuration constructor and registry entry with the task diff, then inspected whole-tree factory callers. [call_8cf6485cdd8648f894d58e9ed7c8e3c3, call_633c3ace0f444ebc864f9e28a0dd248e, call_8635d467bec444d7bb701815971f81df]. Limits: No repository model was instantiated.

scalar_transcription: Applied the new membership and .items() operations to a plain stand-in model class and to its text-component dictionary. The dictionary operations succeeded; the class operations raised TypeError and AttributeError. [call_fc97279a3f824567b1697808e133fbf1]. Limits: Standard-library Python stand-in, not execution of Model.from_config or compile_model.

## Uncertainty and limits

Task-state conclusions combine inspected parent source with the complete task diff; direct solved-tree reads were unavailable.

No model loading, conversion, filesystem-library behavior or GPU execution was tested. The Python check models dictionary operations only.

Checkpoint configurations and tensor headers were not validated; this annotation establishes interface changes, not model-by-model checkpoint compatibility.
