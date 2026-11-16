# 830b6a018070a327d6d261628dff496f1303cf93


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/830b6a018070a327d6d261628dff496f1303cf93) · [Evidence ledger](draft.json)

Prepares component-based model construction and preserves hook-selected original tensors during compilation, while retaining text as the default component.

- [Component selection and preservation of additional tensors](#models)

## Problem

Model construction previously selected one config.model_class, while compilation collected only tensors belonging to the selected model's modules. These interfaces lacked explicit component selection and an additional-tensor preservation hook. [source; call_6ff37ba3b83546bfb2d40d1f5ebfc788, call_975ff533d1af497d8013c0b17e91d71b]

## Reasoning

The change separates component construction from checkpoint preservation: callers select one component, but compilation queries every registered component class for additional tensors. [source; call_6ff37ba3b83546bfb2d40d1f5ebfc788]

This is consistent with preparation for multimodal checkpoints rather than completed multimodal inference: all supplied registrations remain text components, and Model.from_config explicitly retains a multimodal TODO. [inference; call_6ff37ba3b83546bfb2d40d1f5ebfc788]

## Impact

Model.from_config defaults to component='text', asserts that the component exists, and instantiates its mapped class. The config attribute changes from model_class to model_classes, so external integrations using the old attribute require adaptation. [source; call_6ff37ba3b83546bfb2d40d1f5ebfc788]

## Source Notes

PR #25, “Language layers for Mistral Small 3.1 and InternVL3,” contains turboderp's concern that language-only support could produce checkpoints incompatible with future component models. Its relationship to this task is inferred from the shared component-model design; the discussion does not explicitly identify this commit. [inference; call_1ec37664549342eeb07aee0c2a51b819, call_6ff37ba3b83546bfb2d40d1f5ebfc788]

Other matching discussions concern different changes: PR #4, “chore: update config.py,” proposes a spelling correction; issue #7, “quantizing model: undefined symbol: __cxa_call_terminate,” reports extension loading; issue #6, “No ROCm runtime is found, using ROCM_HOME='/usr',” reports installation/JIT failure. Their connection here is inferred only from shared config/model paths, not a demonstrated fix. [inference; call_3bd20169df63466387328a0b371340d8, call_3a4242e04d9e4d57bbc72a59fb7ca293, call_f588e4dee13f4a6586e252575affcb80, call_6ff37ba3b83546bfb2d40d1f5ebfc788]

Issue #33, “Error converting model,” includes a traceback through compile_model's get_tensors call, later identifies too many open files, and subsequently discusses GLM4 output. Issue #34, “torch._C._LinAlgError on last layer of quant,” concerns Cholesky failure during quantization. Shared compilation/conversion paths establish contextual overlap only; attributing either issue's resolution to this refactor would be unsupported. [inference; call_422669c498c549c1afde61035c7f7c5d, call_d9204e5d9ebc4ee9b66991b7d73dba40, call_65c1e93902be462aa9a52588b3723c7b, call_6ff37ba3b83546bfb2d40d1f5ebfc788]

<a id="models"></a>

## Component selection and preservation of additional tensors

Config now stores a component-name-to-class dictionary. Existing architecture constructors supply a text mapping. LlamaConfig accepts an optional derived_model mapping, using the ordinary Llama text mapping when that argument is falsey. [source; call_6ff37ba3b83546bfb2d40d1f5ebfc788]

MistralConfig and Qwen2Config explicitly supply their respective model subclasses through derived_model. Previously their inherited LlamaConfig constructor selected LlamaModel. Both selected subclasses delegate construction to LlamaModel, so the inspected change distinguishes class identity without introducing a separate layer implementation. [source; call_6ff37ba3b83546bfb2d40d1f5ebfc788, call_53943f2cd71b4698a0c5056345ccb491, call_906ac06f96db449c8063bd38e982910c, call_d190dc7f6d794a459403bf94b69319ac]

Model.get_additional_compiled_tensors defaults to an empty dictionary. compile_model merges each registered class's result, expects an n_bytes entry for each tensor, and appends tensor-name strings after the ordinary module entries in its shard plan. Duplicate extra-tensor keys are resolved by dictionary update order. [source; call_6ff37ba3b83546bfb2d40d1f5ebfc788]

Writing dispatches on plan-entry type: Module entries load quantized working-directory tensors by prefix and close that collection; string entries load an individual original tensor from config.stc. Both paths request BF16 preservation and contiguous tensors before the existing shard writer and weight-map construction. [source; call_6ff37ba3b83546bfb2d40d1f5ebfc788, call_975ff533d1af497d8013c0b17e91d71b, call_cfbd5cf8c0414ba0a7bbcae3664d4e6b]

Additional tensors use the existing soft shard limit: shard_size is multiplied by 1024² bytes, exact fits stay in the current shard, and an oversized item is not split. Reported n_bytes values contribute to total_size and therefore to multi-shard index metadata. [source; call_6ff37ba3b83546bfb2d40d1f5ebfc788, call_975ff533d1af497d8013c0b17e91d71b]

A bounded Python transcription verified the allocation boundaries with capacity 10: [6,4] stays together, [6,5] separates, and [11] remains one oversized shard. One shard_size unit evaluates to 1,048,576 bytes. [execution; call_88499189d23a4246876b3c7bbaf6aee2]

## Authoring-time findings — pending review

### extra-tensor-warning-name (suspected; defect)

The additional-tensor oversize warning references the preceding module variable instead of the current tensor key.

Trigger: An additional tensor reports n_bytes greater than max_shard_bytes.

Expected: Identify the oversized additional tensor and continue allocating its shard.

Actual: With ordinary modules present, the warning identifies the last module instead. If model.modules is empty, evaluating module.key raises UnboundLocalError before allocation continues.

Locations: 830b6a018070a327d6d261628dff496f1303cf93:exllamav3/conversion/compile.py — compile_model

Source evidence: call_6ff37ba3b83546bfb2d40d1f5ebfc788, call_975ff533d1af497d8013c0b17e91d71b

source_inspection: Inspected the new extra-tensor loop and the preceding module loop. Whole-parent literal caller search found conversion main calling compile_model after its conversion loop. The supplied default hook returns no additional tensors, so this observation concerns nonempty hook implementations rather than demonstrated failures of current text conversions. [call_6ff37ba3b83546bfb2d40d1f5ebfc788, call_8a19b679c9d74f0b8d20e567885deb37, call_dcb27dee28604e9db803495c3e75131a]. Limits: No repository execution; literal search does not establish external or dynamic caller coverage.

## Uncertainty and limits

No model loading, GPU inference, safetensors serialization, or filesystem round trip was executed.

The scalar check models shard allocation only; it does not execute compile_model.

Pinned model configurations were not inspected, so model-by-model checkpoint compatibility and dimensions remain unestablished.

External callers and dynamically constructed component mappings were not exhaustively validated.
