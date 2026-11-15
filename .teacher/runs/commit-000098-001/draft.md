# 875e503e84ddf27441f551a2c7dc50982c8cd48c


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/875e503e84ddf27441f551a2c7dc50982c8cd48c) · [Evidence ledger](draft.json)

Adds Cohere architecture dispatch and shared-input parallel decoder assembly with configurable logit scaling; Command R Plus Q/K-normalization requirements remain unhandled.

- [Cohere configuration and parallel decoder assembly](#models)

## Problem

CohereForCausalLM lacked an architecture registration. The change connects that identifier to new CohereConfig and CohereModel classes. [source; call_e559e37aba314bb687df499b91828fa5]

## Reasoning

The implementation composes existing LayerNorm, parallel decoder, attention, gated MLP and output-scaling components rather than adding a separate execution backend. [source; call_6adb6eef7f674a6e9db3503ee5dc59e3]

## Impact

Config.from_directory can now select CohereConfig through the architecture registry. This establishes dispatch support, not verified compatibility with every checkpoint carrying that identifier. [source; call_e559e37aba314bb687df499b91828fa5, call_6dd8b68f3e5840fe83c5dab9ec3f8405]

## Source Notes

The earlier parallel-decoder entry records optional-component and plain-MLP allocation inconsistencies. [ancestor; call_d5f9204827cb4f3080d34bf520eb284a]

Those generic implementations remain unchanged, but the new Cohere constructor supplies all three components and uses GatedMLP, whose plural projection collections satisfy the allocator's interface. These particular inherited triggers are therefore not exercised by this construction. [source; call_f4f59f8ab13e4375bb49d0259a3f8945, call_2cabdb7c8865433e819ab1e0c4f21c8b, call_6adb6eef7f674a6e9db3503ee5dc59e3]

Parent-tree Cohere occurrences include a README roadmap item and a chat template; neither is an architecture implementation. [source; call_de6cdfc4ca2241168e42cd3f4da329ba]

The inspected discussions concern “quantizing model: undefined symbol: __cxa_call_terminate,” “`cogito-v1-preview-qwen-32B` generates incoherent output for bpw <= 2.5,” and “Build Failure on Windows: CUDA 12.4 / PyTorch 2.7.0+cu126 / VS 2022.” Their framing is extension loading, quantization quality and compilation, respectively; none identifies this architecture addition as its remedy. [source; call_33591fec5ce54208aad73f8e885a11f1, call_0515fc8af0d74bddabca79816ec44222, call_79e37a5524234a408c11abbcc6c7dfae]

<a id="models"></a>

## Cohere configuration and parallel decoder assembly

CohereConfig reads hidden width, query and KV head counts, intermediate width and layer count. Missing KV head count defaults to the query count; a missing or false head_dim is derived by integer division of hidden width by query heads. hidden_act may be absent, but when present must be silu. [source; call_6adb6eef7f674a6e9db3503ee5dc59e3, call_6dd8b68f3e5840fe83c5dab9ec3f8405]

The external key layer_norm_eps becomes the internal layernorm_eps argument, defaulting to 1e-5 and reaching F.layer_norm. logit_scale defaults to 0.0625, or one sixteenth, and reaches Linear.post_scale: it multiplies projected logits in place, after any softcap, rather than scaling the head's captured input statistics. [source; call_6adb6eef7f674a6e9db3503ee5dc59e3, call_0885de7eedb74d68b80a82ea56c916c2, call_d1b66b47e0254c80829c6088bdf6330d, call_eb4fb4058a9f48e18018d644fc606384, call_817164ea6edf4a4fb3ed766e7e425fd2, call_8b5ffadf3ea742f28cabe92af19c0a10, call_12c0b2407b0746a1b484b312706276e8]

Each layer computes a shared normalized input y, then adds Attention(y) and GatedMLP(y) to the residual. The MLP does not consume the attention-updated residual. Calls remain sequential in Python: “parallel” describes branch dependencies, not concurrent scheduling. The block's prefill branch returns after the attention residual addition and skips the MLP. [source; call_6adb6eef7f674a6e9db3503ee5dc59e3, call_f4f59f8ab13e4375bb49d0259a3f8945]

Checkpoint prefixes are model.embed_tokens, model.layers.<idx>.input_layernorm, self_attn.{q,k,v,o}_proj, mlp.{up,gate,down}_proj, model.norm and lm_head. The final normalization requests half precision. With tie_word_embeddings enabled, the constructor can provide model.embed_tokens as the head's alternative key; Linear searches its primary and alternative loading keys. [source; call_6adb6eef7f674a6e9db3503ee5dc59e3, call_d1b66b47e0254c80829c6088bdf6330d]

RoPE settings use the GPTJ style and the existing configuration helper. prepare_inputs records input_ids and delegates attention preparation. The unchanged dispatcher defaults to uncached Flash Attention; uncached modes reject a cache, while cached batch preparation checks page alignment, cache capacity and an exclusive choice of past_len or cache_seqlens. [source; call_6adb6eef7f674a6e9db3503ee5dc59e3, call_6dd8b68f3e5840fe83c5dab9ec3f8405, call_8391363c36dd44d0a2a18a0ee948db64]

All ten inspected CohereLabs configurations select CohereForCausalLM, specify silu, vocabulary size 256000 and layer_norm_eps=1e-5. aya-23-35B has hidden/intermediate widths 8192/22528, 40 layers, Q/KV heads 64/64 and logit_scale=0.0625. aya-23-8B has 4096/14336, 32 layers, 32/8 heads and the same scale. Both explicitly disable Q/K normalization. [source; call_7069668e4d7743d19f36051870af05da, call_fcec6fed60a34797a8df59351cdde2b5, call_54609a6bfa9d417faaac2444a6714d61, call_71399b418044455bab2b225ddacafc18, call_3bc4f765930148628bbc7c2caa4edd6a, call_b639267fd3a2461696ba3f058e3e60fa, call_7fd0e4076f724cf687cb32b1dc9ad44c, call_8fa1f4c382844862a30c859f7ecf158d, call_47f72d8ddfdf4ae2a53a58c121781c9e, call_456a57652aec400499128364558ca884]

aya-expanse-32b and c4ai-command-r-08-2024 each use 8192/24576 widths, 40 layers, 64/8 heads and scale 0.0625. aya-expanse-8b uses 4096/14336, 32 layers and 32/8 heads, but overrides the scale with 0.125. All three explicitly disable Q/K normalization; the new configuration mapping preserves these dimensional and scaling differences. [source; call_54609a6bfa9d417faaac2444a6714d61, call_3bc4f765930148628bbc7c2caa4edd6a, call_71399b418044455bab2b225ddacafc18, call_6adb6eef7f674a6e9db3503ee5dc59e3]

c4ai-command-r-v01 and c4ai-command-r-v01-4bit each specify 8192/22528 widths, 40 layers, 64/64 heads and scale 0.0625. The former explicitly enables tied embeddings; the latter omits that key and therefore takes the new True default. Both omit use_qk_norm. Dimensional agreement for the 4bit variant is not a storage-format compatibility result. [source; call_47f72d8ddfdf4ae2a53a58c121781c9e, call_456a57652aec400499128364558ca884, call_6adb6eef7f674a6e9db3503ee5dc59e3]

c4ai-command-r-plus, c4ai-command-r-plus-08-2024 and c4ai-command-r-plus-4bit each specify 12288/33792 widths, 64 layers, 96/8 heads and scale 0.8333333333333334. Those values are read by the new mapping, but all three also require use_qk_norm=true, which this implementation does not consume. [source; call_b639267fd3a2461696ba3f058e3e60fa, call_7fd0e4076f724cf687cb32b1dc9ad44c, call_8fa1f4c382844862a30c859f7ecf158d, call_6adb6eef7f674a6e9db3503ee5dc59e3, call_8391363c36dd44d0a2a18a0ee948db64]

A standard-library calculation of the inspected hidden-width/query-head pairs—4096/32, 8192/64 and 12288/96—produced head_dim=128 in every case. This checks the fallback shape arithmetic only. [execution; call_0913ebd48a1c48eba8fe6fe72386edf2]

## Authoring-time findings — pending review

### cohere-qk-normalization (suspected; external_compatibility)

The architecture registration includes configurations requiring Q/K normalization, but the new assembly neither implements it nor rejects that requirement.

Trigger: Select a CohereForCausalLM checkpoint with use_qk_norm=true, including the three inspected Command R Plus configurations, and reach attention execution.

Expected: Honor the configured Q/K normalization or reject unsupported configurations explicitly.

Actual: CohereConfig ignores use_qk_norm. CohereModel constructs ordinary Attention, whose three decode paths project and reshape Q/K, then apply RoPE without normalization; each retains a TODO for Q/K norms.

Locations: 875e503e84ddf27441f551a2c7dc50982c8cd48c:exllamav3/models/cohere.py — CohereModel.__init__, 2bc4822f61e3fce361ba56df0ef413c7a16061d1:exllamav3/modules/attn.py — Attention

Source evidence: call_6adb6eef7f674a6e9db3503ee5dc59e3, call_8391363c36dd44d0a2a18a0ee948db64, call_b639267fd3a2461696ba3f058e3e60fa, call_7fd0e4076f724cf687cb32b1dc9ad44c, call_8fa1f4c382844862a30c859f7ecf158d

source_inspection: Compared all three attention decode paths with the new constructor and checkpoint flags. Whole-parent-tree searches found no use_qk_norm consumer and located existing Attention construction sites; the task adds a direct Cohere construction site reached through registry-based configuration selection. The observation is limited to the newly admitted normalization-requiring configurations, not every existing Attention caller. [call_9cd8582f657f426d8e6826a1e16b1b18, call_c878454c4520446fbf4a77a64cb354a5, call_6dd8b68f3e5840fe83c5dab9ec3f8405, call_e559e37aba314bb687df499b91828fa5, call_8391363c36dd44d0a2a18a0ee948db64]. Limits: No checkpoint was loaded or evaluated; output degradation and the precise reference normalization formula were not measured.

## Uncertainty and limits

No model loading, conversion, generation, PyTorch operation or GPU kernel was executed. The scalar calculation checks only integer head-dimension arithmetic.

Configuration agreement does not establish checkpoint tensor compatibility or numerical equivalence. The two 4bit configurations explicitly describe bitsandbytes storage; this change does not demonstrate support for that format.

Model configuration bytes came from the supplied hash-verified mirrors; their revision identifiers describe verified file sets rather than official Git commits.
