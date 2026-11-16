# 6aa1449169a7076d61223fcf74b4e6ceb849327d


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/6aa1449169a7076d61223fcf74b4e6ceb849327d) · [Evidence ledger](draft.json)

Registers MiMoForCausalLM through thin Llama-derived classes, enabling ordinary decoder construction while deliberately leaving MTP unsupported.

- [MiMo dispatch through the Llama decoder](#models)

## Problem

MiMoForCausalLM was absent from architecture dispatch; the change adds a Llama-derived implementation explicitly excluding MTP layers. [source; call_09335d5eea16423b80edb6760e07e6df, call_479dc166d40c4b25a10b306b834c5d09, call_9fff3f3caefd4fc98c6e0f96de46e5ce]

## Reasoning

Registration and the derived-model mapping work together: Config.from_directory selects MiMoConfig, which supplies {'text': MiMoModel}; Model.from_config then constructs that subclass rather than the default LlamaModel. [source; call_815b6891af054b6e85c26dbae8b88d22, call_7efa4087e3ad4748940d32c2273a43d2, call_9fff3f3caefd4fc98c6e0f96de46e5ce]

## Impact

MiMo gains the existing Llama configuration and decoder construction without a new execution implementation. This establishes dispatch support, not measured checkpoint equivalence or MTP support. [source; call_9fff3f3caefd4fc98c6e0f96de46e5ce, call_41b01627d27b4225b77079349473e536]

## Source Notes

The initial models ancestor entry was read. It documents shared Llama construction, checkpoint naming and missing sliding-window propagation in related wrappers. [ancestor; call_b129e7c865634ddaa557f231146f11f8]

PR #4, 'chore: update config.py', concerns a spelling correction. Issue #7, 'quantizing model: undefined symbol: __cxa_call_terminate', reports an extension/toolchain problem. Issue #33, 'Error converting model', reports file-opening failures and later GLM4 sampling trouble. Their overlap with inspected configuration or compilation files is contextual; no causal connection to the MiMo change is established. [inference; call_325936f1dea74e83bc0f92cd774bb955, call_1e79e0e179ca4d148ead06eb7129ff7e, call_712b07f896244c8dab50d2b2991c12e0, call_674d068510974a4faf7f9896250cdef8]

<a id="models"></a>

## MiMo dispatch through the Llama decoder

MiMo follows the existing Mistral and Qwen2 wrapper pattern: an architecture-specific config supplies its text model class, and the model delegates construction to LlamaModel. Those existing wrappers apply no additional constructor guards that the new wrapper omits. [source; call_17da75d1c0854ac9b9d1dfdf426526d2, call_6ca4223f99d440a992698a61d932b330, call_07d706bbcf314f5facda339c7ecdafbe, call_9fff3f3caefd4fc98c6e0f96de46e5ce]

Inherited construction creates model.embed_tokens, num_hidden_layers transformer blocks, model.norm and lm_head. Blocks use input/post-attention RMSNorm, separate q_proj/k_proj/v_proj/o_proj attention projections and gate_proj/up_proj/down_proj MLP projections. The config accepts SiLU, defaults missing KV-head count to query-head count, and derives missing head width from hidden_size divided by query-head count. [source; call_41b01627d27b4225b77079349473e536]

All five inspected XiaomiMiMo configs match the new architecture identifier and inherited core dimensions: MiMo-7B-Base, MiMo-7B-RL, MiMo-7B-RL-0530, MiMo-7B-RL-Zero and MiMo-7B-SFT each specify 36 layers, hidden width 4096, intermediate width 11008, 32 query heads, eight KV heads and explicit head width 128. Each supplies SiLU, RMS epsilon 1e-5 and untied embeddings, so the corresponding inherited defaults are not needed. [source; call_5b720285f489452d9735101546d9b7f4, call_532adc31c1174ace89314a55bbfd3e8e, call_db0668b929d04004b62b2d815d328073, call_a3e97aa525d34a14adb3424f55792c30, call_6aa32bb89b664c7d96b6339b120652f6, call_41b01627d27b4225b77079349473e536]

The inherited RoPE reader consumes theta 640000 for each model. Base, RL, RL-Zero and SFT declare 32768 maximum positions; RL-0530 declares 65536 and null rope_scaling. All five disable sliding-window attention. The unchanged Llama constructor still does not propagate sliding-window settings, but these configurations do not request that behavior. [source; call_815b6891af054b6e85c26dbae8b88d22, call_41b01627d27b4225b77079349473e536, call_5b720285f489452d9735101546d9b7f4, call_532adc31c1174ace89314a55bbfd3e8e, call_db0668b929d04004b62b2d815d328073, call_a3e97aa525d34a14adb3424f55792c30, call_6aa32bb89b664c7d96b6339b120652f6]

Each inspected configuration declares one next-token-prediction layer, but MiMo adds no constructor logic for it: the inherited loop builds only decoder indices 0 through 35. This is the concrete boundary of the change's 'no MTP yet' scope. [source; call_9fff3f3caefd4fc98c6e0f96de46e5ce, call_41b01627d27b4225b77079349473e536, call_5b720285f489452d9735101546d9b7f4, call_532adc31c1174ace89314a55bbfd3e8e, call_db0668b929d04004b62b2d815d328073, call_a3e97aa525d34a14adb3424f55792c30, call_6aa32bb89b664c7d96b6339b120652f6]

A standard-library arithmetic check gives query width 4096, KV width 1024, four query heads per KV head and 39 top-level modules. It checks the transcribed dimensions and construction count, not repository execution. [execution; call_ccabf65822944a69a0a76be70d82f7bd]

## Uncertainty and limits

No model loading, conversion, generation or GPU tests were executed. The Python check used transcribed integer metadata only.

Checkpoint tensor headers and reference modeling implementations were not inspected; configuration agreement alone does not establish weight-name coverage, bias handling or numerical equivalence.

MTP is intentionally excluded. Compatibility beyond the five inspected configurations remains unestablished.
