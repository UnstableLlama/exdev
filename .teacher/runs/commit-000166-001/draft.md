# 08858bc8e35b6350516507a4f01435bd4e76e25b


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/08858bc8e35b6350516507a4f01435bd4e76e25b) · [Evidence ledger](draft.json)

Repairs Qwen3 MoE's component-interface regression by registering its model class under the existing "text" key.

- [Restore Qwen3 MoE component registration](#models)

## Problem

Qwen3MoeConfig still supplied a bare model class, while Config stored it as model_classes and its consumers expected a component dictionary. [source; call_63b78b662a92465bae992a9684af6d96, call_9bb71336784143b6812caa9e0327327f, call_64b8f3a954b34fb6a8f8bc37c066d280, call_79f1d99ee304425cbf688ee62bdf7d7d]

## Reasoning

Wrapping Qwen3MoeModel in {"text": Qwen3MoeModel} satisfies both factory lookup and compilation's component enumeration without changing the model implementation. [source; call_39cd9b8a2dca4a6da47fa26e21f1dc3f, call_64b8f3a954b34fb6a8f8bc37c066d280, call_79f1d99ee304425cbf688ee62bdf7d7d]

## Impact

The default text factory can now select Qwen3MoeModel. Compilation can enumerate its inherited additional-tensor hook, which returns an empty dictionary; this fix adds no auxiliary tensors or vision component. [source; call_39cd9b8a2dca4a6da47fa26e21f1dc3f, call_64b8f3a954b34fb6a8f8bc37c066d280, call_63b78b662a92465bae992a9684af6d96, call_69e695dc25fa4c6e94f475ad4594257c]

## Source Notes

The earlier component-refactor entry recorded the omitted Qwen3 MoE migration and its factory/compiler failures. [ancestor; call_73d5591f804e4241bc973c2e6ab3661d]

Comparing the parent implementation with the complete patch shows that this specific inherited interface mismatch is removed. [source; call_39cd9b8a2dca4a6da47fa26e21f1dc3f, call_63b78b662a92465bae992a9684af6d96, call_64b8f3a954b34fb6a8f8bc37c066d280]

PR #4, “chore: update config.py,” concerns spelling; issue #7, “quantizing model: undefined symbol: __cxa_call_terminate,” concerns extension loading. Their association here is only an inference from shared inspected config.py/model.py paths, not evidence of this regression. [inference; call_5528d915b7a04221af8096fd51ebfa81, call_4e18c7768e5b445e98ca15e7867f5e11, call_39cd9b8a2dca4a6da47fa26e21f1dc3f]

Issue #33, “Error converting model,” reports a file-opening failure later identified as too many open files, then tracks GLM4 exclamation-mark output. Its association is inferred from the matching compile_model tensor-loading call, not from evidence that this dictionary fix addresses either report. [inference; call_bb2545ad1339429888a43ebbd9ecb7b1, call_002ceed65aaa4d04a1b9a54e6268f1f2, call_79f1d99ee304425cbf688ee62bdf7d7d, call_39cd9b8a2dca4a6da47fa26e21f1dc3f]

<a id="models"></a>

## Restore Qwen3 MoE component registration

Config retains its model_classes argument verbatim. Model.from_config defaults component to "text", checks membership, then invokes the selected class with config and forwarded kwargs. The patch repairs the producer rather than adding a bare-class compatibility branch to these consumers. [source; call_9bb71336784143b6812caa9e0327327f, call_64b8f3a954b34fb6a8f8bc37c066d280, call_39cd9b8a2dca4a6da47fa26e21f1dc3f]

The selected Qwen3MoeModel constructor remains unchanged: it assembles embeddings, attention and sparse-expert transformer blocks, final normalization and the output head, and enables all-expert calibration. The change repairs access to that constructor, not its numerical computation. [source; call_63b78b662a92465bae992a9684af6d96, call_39cd9b8a2dca4a6da47fa26e21f1dc3f]

A bounded Python transcription produced TypeError for bare-class membership and AttributeError for bare-class .items(); the text dictionary selected the stand-in constructor and collected an empty additional-tensor result. This checks the interface mechanism, not repository execution. [execution; call_0b70f52e1c144cf0b90fe4b68ea89ed8]

The inspected config.json files for Qwen/Qwen3-235B-A22B, Qwen/Qwen3-235B-A22B-FP8 and Qwen/Qwen3-235B-A22B-GPTQ-Int4 each declare Qwen3MoeForCausalLM, matching Qwen3MoeConfig.arch_string. The same repaired text-component mapping applies to each; the patch changes no dimensions or configuration defaults. [source; call_c34fd210765b447b89e48a29a425aac2, call_14911a94c7904b25baf1e2bd038e9672, call_8512db9f07214d13b9a1ec21b82b3363, call_63b78b662a92465bae992a9684af6d96, call_39cd9b8a2dca4a6da47fa26e21f1dc3f]

The inspected config.json files for Qwen/Qwen3-30B-A3B, Qwen/Qwen3-30B-A3B-Base, Qwen/Qwen3-30B-A3B-FP8 and Qwen/Qwen3-30B-A3B-GPTQ-Int4 also each declare Qwen3MoeForCausalLM. Each therefore matches the same repaired mapping, independently of its unchanged dimensions and checkpoint quantization metadata. [source; call_ae4407bc5cde44ab8904f13a2618b951, call_72229f9132414c6f9bf035637b66cd98, call_2d9796f8b3b743d19e618923f8063625, call_1070f62c4d2245dba506973d13d96fb1, call_63b78b662a92465bae992a9684af6d96, call_39cd9b8a2dca4a6da47fa26e21f1dc3f]

## Uncertainty and limits

No repository model loading, conversion or GPU inference was executed. The Python check used a stand-in class and transcribed dictionary operations.

Checkpoint configuration inspection establishes architecture identity, not weight-format compatibility or successful inference, particularly for FP8 and GPTQ variants.
