# 42afcd7e6cd361b2be9aef1072f26ffccffb92db


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/42afcd7e6cd361b2be9aef1072f26ffccffb92db) · [Evidence ledger](draft.json)

Adds Gemma3ForCausalLM registration and top-level configuration parsing, reusing the existing Gemma3 decoder with unprefixed tensor keys.

- [Standalone Gemma3 dispatch with shared decoder assembly](#models)

## Problem

The existing Gemma3 adapter recognized Gemma3ForConditionalGeneration, read nested text_config values and used language_model-prefixed tensor names. Standalone Gemma3ForCausalLM checkpoints require a different architecture registration, configuration layout and tensor namespace. [source; call_eb7f8d532d2c4a819f713586040c0cee, call_c3de6c38489f4d4b9a9ead03fae4b289, call_1b26dfb33b3743a1abc22c306a8efc4d]

## Reasoning

The three edits cooperate: registration enables dispatch, Gemma3TextConfig supplies top-level settings, and an empty key prefix lets the existing decoder address standalone weights. Registration alone would not resolve the configuration and weight-name differences. [inference; call_a7e24e887f76464b87f6144cee40ec9a, call_c3de6c38489f4d4b9a9ead03fae4b289, call_9cd0d9efdf4e409c82fd24f38c57ca50]

## Impact

Gemma3ForCausalLM gains a text-only component mapping. Existing conditional-generation construction retains the default language_model. prefix; the vision stub is unchanged. [source; call_c3de6c38489f4d4b9a9ead03fae4b289, call_eb7f8d532d2c4a819f713586040c0cee]

## Source Notes

The earlier Gemma3 entry describes the decoder assembly and separate local/global RoPE settings reused here, and explicitly records that vision loading remains unimplemented. [ancestor; call_961e885bf8c84629a8130a3cad5a8e1b]

PR #25, “Language layers for Mistral Small 3.1 and InternVL3,” contains gakada's later report that gemma-3-1b cannot run because it uses Gemma3ForCausalLM. Its relationship to this fix is inferred from that exact architecture identifier, not an explicit commit reference. Gakada opened the PR and reported the problem; the supplied fix attribution is turboderp. [inference; call_6dd27a0654a141c9b68bbce9cdc5b391, call_c3de6c38489f4d4b9a9ead03fae4b289]

PR #4, “chore: update config.py,” concerns a spelling correction. Issue #7, “quantizing model: undefined symbol: __cxa_call_terminate,” concerns extension loading. Their connection to this inspection is only the shared config.py path; neither establishes a Gemma3 architecture defect. [inference; call_21324f567cf740f3a28c952f62407023, call_b1a1ffd645de452ab049496aac1758c0, call_9cd0d9efdf4e409c82fd24f38c57ca50]

<a id="models"></a>

## Standalone Gemma3 dispatch with shared decoder assembly

Config.from_directory selects a configuration class through the architecture registry. The added Gemma3TextConfig identifies Gemma3ForCausalLM and maps only the text component to Gemma3TextModel; Model.from_config defaults to that text component. [source; call_a7e24e887f76464b87f6144cee40ec9a, call_c3de6c38489f4d4b9a9ead03fae4b289, call_9cd0d9efdf4e409c82fd24f38c57ca50, call_fe9cdaffbf4f4fc991061b579dc2941e]

Gemma3TextModel delegates to Gemma3Model with key_prefix=''. All changed decoder keys—including embedding, block norms, attention, MLP, final norm, output projection and its embedding alternative—use that prefix. Existing construction keeps key_prefix='language_model.', preserving its prior names. [source; call_c3de6c38489f4d4b9a9ead03fae4b289, call_c8b01242d201459d9d97613295895425]

The new configuration copies the existing Gemma3 defaults while removing text_config nesting. It requires num_hidden_layers, falls back to vocabulary size 262208 only when the base configuration supplies none, and uses hidden/intermediate defaults 2304/9216, head dimension 256 and query/KV head defaults 8/4. [source; call_c3de6c38489f4d4b9a9ead03fae4b289, call_9cd0d9efdf4e409c82fd24f38c57ca50]

Global NEOX RoPE reads top-level settings with theta default 1,000,000. Local RoPE receives an empty dictionary, retaining theta 10,000 without checkpoint scaling. The shared decoder makes every sixth layer global by default, supplies local layers the configured window, and computes attention scale as query_pre_attn_scalar**(-0.5). [source; call_c3de6c38489f4d4b9a9ead03fae4b289, call_9cd0d9efdf4e409c82fd24f38c57ca50, call_eb7f8d532d2c4a819f713586040c0cee]

google/gemma-3-1b-it, google/gemma-3-1b-pt, google/gemma-3-1b-it-qat-int4-unquantized and google/gemma-3-1b-it-qat-q4_0-unquantized each match the new architecture and top-level layout. Each explicitly supplies widths 1152/6912, 26 layers, query/KV heads 4/1, head dimension and query scalar 256, window 512, period 6 and vocabulary 262144. Thus each overrides the width, head-count, window and vocabulary fallbacks; each supplies no RoPE scaling. [source; call_1b26dfb33b3743a1abc22c306a8efc4d, call_33ed7c3608ac4572a3de5a15eb292774, call_fbda41ade0db41eeb282a668219db8d7, call_6e7b447b48264308b170cf0ca3d30b92, call_c3de6c38489f4d4b9a9ead03fae4b289]

google/medgemma-27b-text-it also matches the new architecture and layout, but supplies widths 5376/21504, 62 layers, query/KV heads 32/16, head dimension 128, query scalar 168, window 1024 and vocabulary 262144. Its global settings include linear RoPE factor 8; the separately constructed local settings do not inherit that scaling. [source; call_4474ac445344475fb397461f8bcbe613, call_c3de6c38489f4d4b9a9ead03fae4b289, call_9cd0d9efdf4e409c82fd24f38c57ca50]

A bounded Python transcription produced 22 local/4 global layers for 26 layers and 52 local/10 global layers for 62 layers. Query scalars 256 and 168 yielded scales 0.0625 and approximately 0.077151675 respectively. [execution; call_21298f6a810244de8d0c8cf69238f83a]

## Uncertainty and limits

No checkpoint loading, conversion, generation or GPU execution was performed. Configuration agreement does not establish numerical or tensor-layout compatibility.

The scalar check transcribed layer scheduling and attention-scale arithmetic; it did not execute repository model code.

The five indexed causal-language-model configurations were read, but the eleven indexed conditional-generation configurations were not independently reread for this change.

Whole-tree Gemma3-name search found the adapter and registry references; exhaustive searches of every configuration-key consumer and generic constructor caller were not completed.
