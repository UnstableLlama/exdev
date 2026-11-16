# 966762a32d1eb2c0aa5e01b02451676bca6ca7fd


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/966762a32d1eb2c0aa5e01b02451676bca6ca7fd) · [Evidence ledger](draft.json)

Adds Gemma3 text-model dispatch and assembly with separate local/global RoPE settings; vision remains a stub with an additional-tensor hook.

- [Gemma3 text assembly and separate positional settings](#models)

## Problem

Gemma3ForConditionalGeneration was not registered. Its nested text configuration and alternating local/global attention require architecture-specific assembly. [source; call_d7be3529fb7044769f9d5c2cdb41fb37, call_a308eb9de1684b5b9773c3cc7fcace34, call_fc0157278e8c4f0a9d731cd00d27d144]

## Reasoning

The change reuses existing transformer modules and extends the RoPE configuration helper to accept a separate dictionary and caller-specific defaults. This permits globally scaled RoPE and independent, unscaled local RoPE without changing the previous helper defaults. [source; call_4a342866b5dd4a02906ef2cc832c1149, call_a308eb9de1684b5b9773c3cc7fcace34, call_1ba8c576e4244387bde5150872b02799]

## Impact

Directory-based dispatch can now select Gemma3's text model. Vision is represented separately, but its load and unload methods explicitly raise NotImplementedError; this is not multimodal inference support. [source; call_562ade57beef4a6f953d5fac5033c368, call_db35e6b199614f8ea7d3333427b22e58, call_d7be3529fb7044769f9d5c2cdb41fb37, call_a308eb9de1684b5b9773c3cc7fcace34]

## Source Notes

The preceding entry describes the component dictionary and additional-tensor compilation hook that this adapter uses. [ancestor; call_a7a30ffe1a2d402f8464a76fc7d2a910]

PR #4, “chore: update config.py,” proposes a spelling correction. Issue #7, “quantizing model: undefined symbol: __cxa_call_terminate,” reports extension loading failure; issue #6, “No ROCm runtime is found, using ROCM_HOME='/usr',” reports a build-time assertion. Their connection to this change is inferred only from the shared config.py path and matching RoPE import traceback, not evidence that this architecture addition fixes them. [inference; call_96b66b0a197944e1a03f5837d2ef0bbf, call_8b7d7c4324ff4daf950b304a9e8640b9, call_ad3377f5a8c243b295503940e9952f56, call_562ade57beef4a6f953d5fac5033c368]

Issue #29, “Auto-YaRN for Qwen3? Maybe even set it dynamically?”, discusses request-dependent scaling and its cache/batching complications. Its relationship here is inferred from shared RopeSettings and rope.py references; Gemma3's two fixed settings do not implement that proposal. [inference; call_75594ade985c4279b3c2bbf1d591e3e9, call_a308eb9de1684b5b9773c3cc7fcace34]

<a id="models"></a>

## Gemma3 text assembly and separate positional settings

Gemma3Config registers Gemma3ForConditionalGeneration and supplies text and vision component classes. The existing factory defaults to text. Configuration reads dimensions from text_config, requires num_hidden_layers, and supplies vocabulary size 262208 when the base configuration finds neither top-level nor nested vocab_size. [source; call_a308eb9de1684b5b9773c3cc7fcace34, call_562ade57beef4a6f953d5fac5033c368, call_db35e6b199614f8ea7d3333427b22e58]

read_rope_settings_default now distinguishes an omitted dictionary from an explicitly empty one. Global settings read text_config with theta defaulting to 1,000,000; local settings read {}, yielding theta 10,000, full rotary dimensions and no scaling. Both use NEOX layout. Existing calls that supply only rope_style retain top-level configuration and the previous defaults. [source; call_4a342866b5dd4a02906ef2cc832c1149, call_a308eb9de1684b5b9773c3cc7fcace34, call_edf1a0b2c34e4d6d9ac284d82b92c461]

Layer locality is bool((idx + 1) % sliding_window_pattern): with the default period 6, every sixth layer is global. Local layers receive the configured sliding_window, while global layers receive -1. The adapter's fallback window is 4096, but every inspected model explicitly supplies 1024. FlashAttention consumers forward the window and query_pre_attn_scalar**(-0.5); the SDPA path explicitly rejects sliding-window attention. [source; call_a308eb9de1684b5b9773c3cc7fcace34, call_f8357c9e9daf4439afda25ce234c453f, call_251ef966e09540a9ba0a600bc2eafe72]

The inspected RoPE implementation computes inverse frequencies from theta and rotary dimension. Linear scaling divides them by the configured factor. Consequently the inspected checkpoints' factor 8 applies to global attention only; the empty local dictionary deliberately bypasses it. [source; call_1ba8c576e4244387bde5150872b02799, call_a308eb9de1684b5b9773c3cc7fcace34, call_ecb6693a84564e20b0b235f545bd8667]

Text tensor keys retain the language_model prefix. Assembly comprises a normalized embedding, sequential attention and GELU-gated MLP residual branches with pre/post RMSNorm, a final half-precision norm, and a vocabulary projection with the embedding key as an alternative. Q and K receive RMSNorm before RoPE. Norms use constant_bias=1; branch post-norms request float output. [source; call_a308eb9de1684b5b9773c3cc7fcace34, call_2b1721e94dc84799b91750c1d1cfc3b7, call_f8357c9e9daf4439afda25ce234c453f]

google/gemma-3-4b-it and google/gemma-3-4b-pt each map to hidden/intermediate widths 2560/10240 and 34 layers, overriding the adapter's width defaults. Both omit head counts and head_dim, so the adapter supplies 8 query heads, 4 KV heads and dimension 256. google/gemma-3-4b-it-qat-int4-unquantized and google/gemma-3-4b-it-qat-q4_0-unquantized explicitly supply those same dimensions, counts and query scalar 256. [source; call_ecb6693a84564e20b0b235f545bd8667, call_bda781bf93704452a8f796745c57ac17, call_1ebe29c11667467a97b76e4908137c57, call_d8c518950237414da8a906815134dbbc, call_a308eb9de1684b5b9773c3cc7fcace34]

google/gemma-3-12b-it and google/gemma-3-12b-pt each supply widths 3840/15360, 48 layers and 16/8 query/KV heads; the adapter supplies omitted head_dim and query scalar as 256. google/gemma-3-12b-it-qat-int4-unquantized and google/gemma-3-12b-it-qat-q4_0-unquantized explicitly confirm those dimensions and scalar. Thus none of these four uses the adapter's default widths or head counts. [source; call_645d5d5f1f3642338809235d6a27712d, call_7c26c059040c4785b91a3e9bae0f67eb, call_92052473970a4ffba44b75b92fa0e7e2, call_3647a2df32f84e6aaac7b29490a2b4e9, call_a308eb9de1684b5b9773c3cc7fcace34]

google/gemma-3-27b-it, google/gemma-3-27b-pt and google/gemma-3-27b-it-qat-q4_0-unquantized each supply widths 5376/21504, 62 layers, 32/16 query/KV heads, head_dim 128 and query scalar 168. The adapter reads these overrides rather than deriving the attention scale from head_dim. [source; call_6e714ddc05184d71a0a2f519fb24ff2d, call_2ce5fa2a843447a4b824017e7437432d, call_46fe15e33a254bbbaae9e7098d7e5e24, call_a308eb9de1684b5b9773c3cc7fcace34]

All eleven inspected configurations use the registered architecture and nested text_config, with linear RoPE factor 8 and window 1024. The five QAT configurations explicitly specify period 6, theta 1,000,000, local base frequency 10,000 and vocabulary 262208. Their null attention/output softcaps fall through read_dict to the adapter's 0.0 defaults. Local base frequency is not read by this adapter, but its fixed 10,000 agrees with those files. [source; call_a308eb9de1684b5b9773c3cc7fcace34, call_51da57dbe0e54d518eb83754702729cf, call_1ebe29c11667467a97b76e4908137c57, call_d8c518950237414da8a906815134dbbc, call_92052473970a4ffba44b75b92fa0e7e2, call_3647a2df32f84e6aaac7b29490a2b4e9, call_46fe15e33a254bbbaae9e7098d7e5e24, call_ecb6693a84564e20b0b235f545bd8667, call_bda781bf93704452a8f796745c57ac17, call_645d5d5f1f3642338809235d6a27712d, call_7c26c059040c4785b91a3e9bae0f67eb, call_6e714ddc05184d71a0a2f519fb24ff2d, call_2ce5fa2a843447a4b824017e7437432d]

A bounded Python transcription produced local/global layer counts of 29/5, 40/8 and 52/10 for 34, 48 and 62 layers. The corresponding query scales are 0.0625 for scalar 256 and approximately 0.077151675 for scalar 168. These are schedule and scalar checks, not model execution. [execution; call_2483a2d4a92f4a0f97880f7f6cd435ee]

The vision class's additional-tensor hook returns the union of source entries under vision_tower and multi_modal_projector. This preserves a separation between text execution and additional checkpoint tensors without implementing a vision forward path. [source; call_a308eb9de1684b5b9773c3cc7fcace34]

## Uncertainty and limits

No model loading, generation, conversion or GPU execution was performed. Configuration agreement does not establish tensor-layout compatibility or numerical correctness.

The Python computation transcribed layer scheduling and attention-scale arithmetic; it did not execute the model or attention kernels.

Model configurations were supplied as hash-verified historical mirror files. Omitted configuration values establish which adapter defaults apply, not independent validation of those defaults.
