# 1db3dce033981fe2d1825165a9389b3fdcd21b67


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/1db3dce033981fe2d1825165a9389b3fdcd21b67) · [Evidence ledger](draft.json)

Adds Qwen3ForCausalLM dispatch and model assembly using existing transformer modules, per-head Q/K RMSNorm, explicit head dimensions and conditional tied-head weights.

- [Qwen3 registration and normalized attention assembly](#models)

## Problem

The parent registry does not recognize Qwen3ForCausalLM, so Config.from_directory rejects that architecture before model construction. [source; call_e4ac242afd14444291820d6f2e843515, call_dc8a9a7252df4999a767e37a9134390c]

## Reasoning

The change adds a dedicated Qwen3 configuration and model builder, reusing existing transformer modules while supplying Q/K normalization and independently configured attention-head dimensions. [source; call_719b4343aa5d495cac49eee49ce9abf9, call_f3e01fd7da824c7c9c084bfdb500ac00]

## Impact

Registry dispatch now maps Qwen3ForCausalLM to Qwen3Config and Qwen3Model. No attention kernel or existing architecture mapping is changed. [source; call_f683c92addb041809ab86cf7ebc770ec, call_e4ac242afd14444291820d6f2e843515, call_719b4343aa5d495cac49eee49ce9abf9]

## Source Notes

Issue #29, “Auto-YaRN for Qwen3? Maybe even set it dynamically?”, requests automatic or per-request scaling. Its connection to this change is inferred from Qwen3 and RoPE configuration, not an explicit commit reference. The patch delegates to existing RoPE configuration rather than implementing that request. [inference; call_dec14834a34d4134b6610b4f555714f9, call_719b4343aa5d495cac49eee49ce9abf9, call_dc8a9a7252df4999a767e37a9134390c]

Other inspected discussions concern different changes: PR #4, “chore: update config.py”, proposes a spelling correction; issue #7, “quantizing model: undefined symbol: __cxa_call_terminate”, reports a native-extension import failure and the reporter’s toolchain workaround. Neither supplies evidence of Qwen3 execution. [source; call_8a7beb340a6c4b83b42913f2758d046e, call_72f02de8e60a482aa598ea05d7280c60]

<a id="models"></a>

## Qwen3 registration and normalized attention assembly

Qwen3Config declares Qwen3ForCausalLM and passes Qwen3Model to the base configuration. Adding Qwen3Model to the registry comprehension makes the existing directory-based architecture lookup select these classes. [source; call_f683c92addb041809ab86cf7ebc770ec, call_719b4343aa5d495cac49eee49ce9abf9, call_e4ac242afd14444291820d6f2e843515, call_dc8a9a7252df4999a767e37a9134390c]

Configuration preserves an explicit head_dim, falling back to hidden_size // num_attention_heads only when it is absent or falsy. KV-head count defaults to query-head count, tied embeddings default to false, and a supplied hidden_act must be silu. Required dimensions and RMS epsilon are read from the model configuration. [source; call_719b4343aa5d495cac49eee49ce9abf9, call_dc8a9a7252df4999a767e37a9134390c, call_b9f3f32663504918b1cbac40bd51e323]

The model consists of token embedding, sequential pre-normalized attention/MLP blocks, final RMSNorm producing half precision, and a vocabulary projection. Each normal block adds attention to its residual, then normalizes that updated residual for the MLP. Checkpoint keys follow model.layers.{idx}, including self_attn.q_norm and self_attn.k_norm. [source; call_719b4343aa5d495cac49eee49ce9abf9, call_4f5484a7d2ca4e2a921fd4789d7c20b4]

Attention projects hidden_size to query_heads × head_dim for Q and KV_heads × head_dim for K/V. All three existing backends reshape into heads and apply the supplied Q/K RMSNorms before RoPE; V is not normalized. RMSNorm.forward flattens all leading dimensions, invokes the native operation over the final dimension, then restores shape. Thus Q/K normalization is per head, not across the concatenated projection. [source; call_719b4343aa5d495cac49eee49ce9abf9, call_f3e01fd7da824c7c9c084bfdb500ac00, call_91a90bfeda5c413c9e9ce46633f3d9cd]

The builder leaves attention scaling unspecified and uses existing full-attention defaults. prepare_inputs stores input_ids and delegates to prepare_for_attn: absent an explicit mode, this selects uncached FlashAttention; cached FlashAttention requires its existing cache parameters, while the uncached preparation paths reject a cache. [source; call_719b4343aa5d495cac49eee49ce9abf9, call_f3e01fd7da824c7c9c084bfdb500ac00]

For tied embeddings, model.embed_tokens becomes the head’s alternate key only when tie_word_embeddings is true and the collection reports no lm_head. The builder also retains calibration mappings block.attn, block.mlp and block, rather than introducing Qwen3-specific quantization machinery. [source; call_719b4343aa5d495cac49eee49ce9abf9]

Qwen/Qwen3-0.6B, Qwen/Qwen3-0.6B-Base and Qwen/Qwen3-0.6B-FP8 each match the new architecture string and specify hidden size 1024, intermediate size 3072, 28 layers, 16 query heads, 8 KV heads, head dimension 128 and tied embeddings. Their explicit values override the builder’s dimensional and tying defaults. [source; call_adb85501d6214731a0719d30844405e5, call_ecfbd56d13de47f885a63337a5cbe7a2, call_32388148db834fcb961680f29c3b4a3a, call_719b4343aa5d495cac49eee49ce9abf9]

Qwen/Qwen3-1.7B, Qwen/Qwen3-1.7B-Base and Qwen/Qwen3-1.7B-FP8 each match the registration and specify hidden/intermediate sizes 2048/6144, 28 layers, 16 query heads, 8 KV heads, head dimension 128 and tied embeddings. [source; call_1b8085b511554fbbbfa827de23778661, call_4aea54b9fdf04376b618ce53d5ee4105, call_d23349c377904d17acdf13bac31f5c37, call_719b4343aa5d495cac49eee49ce9abf9]

Qwen/Qwen3-4B, Qwen/Qwen3-4B-Base and Qwen/Qwen3-4B-FP8 each match the registration and specify hidden/intermediate sizes 2560/9728, 36 layers, 32 query heads, 8 KV heads, head dimension 128 and tied embeddings. [source; call_50574e0db3ca45b7bd3475cb2ba48c1b, call_44601e77898745c0ba9d727bd5d20bcf, call_f22b7e267cdb4e1a80e2e8324e029235, call_719b4343aa5d495cac49eee49ce9abf9]

Qwen/Qwen3-8B, Qwen/Qwen3-8B-Base and Qwen/Qwen3-8B-FP8 each match the registration and specify hidden/intermediate sizes 4096/12288, 36 layers, 32 query heads, 8 KV heads, head dimension 128 and untied embeddings. [source; call_feaea1f230dd41118badaa5927039540, call_c542bac6d4884b949a493c8d35dbe57e, call_43a00f58b62142898bb11610d73b83ad, call_719b4343aa5d495cac49eee49ce9abf9]

Qwen/Qwen3-14B, Qwen/Qwen3-14B-Base and Qwen/Qwen3-14B-FP8 each match the registration and specify hidden/intermediate sizes 5120/17408, 40 layers, 40 query heads, 8 KV heads, head dimension 128 and untied embeddings. [source; call_54e40a52cbbd492f8d31f4b78a7812e8, call_51047b8606ff48b49d04dda7c891fa41, call_9fed277031434e479c3200e6c2a5bba5, call_719b4343aa5d495cac49eee49ce9abf9]

Qwen/Qwen3-32B and Qwen/Qwen3-32B-FP8 each match the registration and specify hidden/intermediate sizes 5120/25600, 64 layers, 64 query heads, 8 KV heads, head dimension 128 and untied embeddings. [source; call_3ea41f164a174134b17a4af7d6d4a727, call_e467d449ab2340c6807803065c2fd215, call_719b4343aa5d495cac49eee49ce9abf9]

A standard-library arithmetic check of these dimensions gives Q widths 2048, 2048, 4096, 4096, 5120 and 8192 for 0.6B through 32B, respectively; every KV width is 1024. The fallback head dimension would instead be 64 for 0.6B and 80 for 4B and 32B, demonstrating why retaining explicit head_dim matters. This is scalar shape arithmetic, not repository or GPU execution. [execution; call_7e1fe7f2a1a441618414d9eadd1cd8ba]

Reusing the normalized-attention interface avoids a separate Qwen3 kernel implementation, while explicit head dimensions accommodate attention widths unequal to the residual width. This is a design interpretation of the assembly and shape calculations, not a measured performance benefit. [inference; call_719b4343aa5d495cac49eee49ce9abf9, call_f3e01fd7da824c7c9c084bfdb500ac00, call_7e1fe7f2a1a441618414d9eadd1cd8ba]

## Uncertainty and limits

No model loading, conversion, generation, or GPU kernel execution was performed. The Python check measures only transcribed dimension arithmetic.

Configuration compatibility does not establish checkpoint compatibility: tensor headers were not inspected, and the FP8 variants’ quantization metadata was not validated against the loader.

Long-context accuracy, automatic YaRN scaling, and performance are not established by this change.
