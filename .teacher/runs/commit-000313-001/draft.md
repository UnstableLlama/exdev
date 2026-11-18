# 2957e20cad48ba6c8768f6dc82a49ff786e84e76


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/2957e20cad48ba6c8768f6dc82a49ff786e84e76) · [Evidence ledger](draft.json)

Removes two README roadmap items now backed by an existing model registry and Formatron-based constrained sampling. The edit changes documentation only and retains the preview warning and remaining roadmap items.

- [Update the README roadmap to reflect existing capabilities](#docs)

## Problem

The README's “What's missing?” list still presented constrained sampling as future work, although the parent tree already contained a Formatron-based JSON generation example and the runtime code to apply its constraints. The list also carried the open-ended item “Support for more architectures” despite an existing registry with multiple model implementations. [source; call_500274b68d3d4012b85b2ffe6cb1abb3, call_8cfe6b4a176e49a5ad1dced0a7ea66db, call_538799728e70480abb2f276509181690, call_013d3eac8c534bd09d3905e80cb1a707]

## Reasoning

The strongest reading is that the README is catching up with existing code, not announcing new features. Removing the constrained-sampling item reflects a concrete implementation. Removing the architecture item narrows the list of broad gaps; it does not imply that every model is supported. The commit message gives no more specific rationale. [inference; call_fd709c6f0c3d476fb12b3804d2eeb5c6, call_8cfe6b4a176e49a5ad1dced0a7ea66db, call_dce7c6c554d8440895d30d9e784cd2c0, call_013d3eac8c534bd09d3905e80cb1a707]

## Impact

Only README.md changes: two to-do bullets disappear and a stray leading space is removed from the paragraph introducing V3. The preview warning and the remaining items—LoRA, ROCm, tensor-parallel inference, and optimization—stay in place. No runtime behavior, dependency declaration, model registration, or CLI instruction changes. [source; call_fd709c6f0c3d476fb12b3804d2eeb5c6, call_500274b68d3d4012b85b2ffe6cb1abb3]

## Source Notes

The initial usage and evaluation entry establishes that the README introduced V3 as a preview, not a production-ready V2 replacement. The later Formatron entry documents the existing per-job filter interface and additive logit masks, and records caveats around speculative sampling, prefix reset, and vocabulary caching. [ancestor; call_73ec9d08fede4bd5b7a7cd4eb483554e, call_cbe473231310470bb47b36bf50550f98]

Closed issue #12, “Qwen2.5 Coder 0.5B Instruct | ValueError: Unsupported type in stop_conditions,” reports a successful conversion followed by a chat failure using `-mode llama3`. A reply recommended `-mode chatml` for Qwen, and the reporter acknowledged omitting it. The inferred connection is the README's manual chat-mode example and the matching exception text in Job; this is stop-condition handling, not JSON grammar filtering, and the diff changes neither. [inference; call_479552a6d7184881b312f39b100a97ce, call_86cfa2d88fff4cdfac5322f4f331465c, call_b61a93d91f5c4c379aa9942a08d127fb, call_53a4bb5158fb4270a58fda87f01f6cdd, call_500274b68d3d4012b85b2ffe6cb1abb3, call_fd709c6f0c3d476fb12b3804d2eeb5c6]

Three other matches are to files inspected for context, not to the README edits. Issue #7, “quantizing model: undefined symbol: __cxa_call_terminate,” traces an extension import failure through the same `RopeSettings`/`RopeStyle` import in `models/config.py`; the reporter says a fresh Conda toolchain resolved it. PR #4, “chore: update config.py,” proposes correcting the `containg` typo still visible in the inspected docstring. Issue #48, “`RuntimeError` when requesting logprobs with Gemma 3 models,” reports a width mismatch on the `held_logits.append` line still present in Job. These source matches are inferred connections only; none is addressed by deleting either bullet. [inference; call_fa501d309acd4e8da803d4f99c763091, call_0eb0e76d444a48d3b47d58cad0ef54c9, call_dce7c6c554d8440895d30d9e784cd2c0, call_45b4786871c247ff86d174d5d2115c3c, call_fba1b459e5354cc49b862875aa52c5fd, call_fd709c6f0c3d476fb12b3804d2eeb5c6]

The model discussions are related by names in the inspected registry, not by an upstream link to this edit. Issue #51, “dots.llm1 support,” requests support and includes a reply reporting that it was added; the registry lists Dots1Model. Issue #29, “Auto-YaRN for Qwen3? Maybe even set it dynamically?”, asks about long-context scaling, a separate question from Qwen3Model registration. Issue #55, “Possible GLM4 32B regression,” shows Glm4Model being selected before conversion fails in FP16 loading; a reply reports a separate dev-branch fix. Registration and reliable operation are different claims. [inference; call_5a298ddb0d754659a3b5e82b91b8df68, call_2fc1eb6b0c94447fa68077ab1a4fd43f, call_50d797e25aa344aa8554cef4b4b4771b, call_013d3eac8c534bd09d3905e80cb1a707]

Other discussion matches concern unchanged wording. “Possible ETA for AMD compatibility?” (#41) asks about AMD support and suggests Vulkan; “Please Switch to Flash-Infer” (#44) reports a Turing/FlashAttention obstacle and requests an alternative. Their inferred connections are the README's unchanged ROCm caveat and FlashInfer note. [inference; call_f15d3b126be34a618f7becdabe7c866c, call_2dd423429c234b829733d8c44ed80c78, call_500274b68d3d4012b85b2ffe6cb1abb3, call_fd709c6f0c3d476fb12b3804d2eeb5c6]

“running the QTIP inference code” (#49) offers setup advice for upstream QTIP and discusses differences from EXL3; “Another improved quantization method from QTIP team?” (#56) asks how YAQA relates to EXL3. The shared QTIP name is the inferred link to the paragraph whose indentation changes, not evidence of a quantizer change. “VRAM usage vs. EXL2” (#60) reports higher Mistral Large loading memory in EXL3, while “Soooo Cool !!! Thanks a lot for the new version ! I loved the v2” (#10) expresses appreciation. Their overlap is the V2/EXL2 comparison, not either removed item. [inference; call_b61329c2bd8d41a088503b11ba0d58df, call_595400453de24f07b48e9c694b678476, call_badaff3d3ee64d06a40ada389f322ad6, call_308861e506174639b905d06d9aaa7dc4, call_fd709c6f0c3d476fb12b3804d2eeb5c6]

<a id="docs"></a>

## Update the README roadmap to reflect existing capabilities

Architecture selection already uses a registry rather than assuming every model is a Llama variant. `Config.from_directory` reads the single `architectures` entry in `config.json`, rejects an unregistered value, and constructs the matching configuration class. The registry derives its keys from the model classes' `config_class.arch_string` values and carries both the config and model class. [source; call_dce7c6c554d8440895d30d9e784cd2c0, call_013d3eac8c534bd09d3905e80cb1a707]

A standard-library AST check of the parent registry counted 20 entries and 20 distinct class identifiers, including separate Gemma 3 text and full-model classes and separate dense and MoE Qwen3 classes. This counts declared inputs to registration, not models successfully loaded. [execution; call_454deef1e998456ea149c9ce1591fc03, call_013d3eac8c534bd09d3905e80cb1a707]

Constrained sampling already had an opt-in path. The example builds a JSON-schema formatter and passes a `FormatronFilter` to `Job`, or supplies one filter list per prompt through `Generator.generate`. The adapter asks Formatron for the allowed next tokens and builds a logit mask. `Job.prepare_logit_mask` combines active masks, `receive_logits` passes the result to the sampler, and `receive_sample` advances the filter state. This constrains token choice during generation rather than checking finished JSON afterward. The example uses separate filter instances for concurrent jobs because the state changes as tokens are accepted. [source; call_8cfe6b4a176e49a5ad1dced0a7ea66db, call_0785a6daae4242ccbdf08dd36d1c4aa4, call_538799728e70480abb2f276509181690]

## Uncertainty and limits

The standard-library check counted class identifiers in source without importing the registry. It does not establish unique runtime architecture keys, checkpoint compatibility, or successful conversion or inference.

No model, GPU kernel, or Formatron engine was run. The examples and filter code establish an available interface, not grammar compliance across all generation modes.
