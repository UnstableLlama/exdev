# 544ba423bf9c58c940dca6cb36a1aa93f6cda41a


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/544ba423bf9c58c940dca6cb36a1aa93f6cda41a) · [Evidence ledger](draft.json)

Registers EXAONE4 using shared post-norm blocks and selective local RoPE. The dense 32B reference matches the inspected layout; all four pinned 1.2B variants stop at the null window pattern, and registration does not add native AWQ, GPTQ, or FP8 loading.

- [EXAONE4 dispatch, post-norm blocks, and checkpoint compatibility](#models)

## Problem

The parent registry cannot dispatch a checkpoint declaring Exaone4ForCausalLM. The change adds the registry entry and a text-model adapter that maps EXAONE4 configuration and checkpoint keys onto the existing decoder modules. [source; call_6afdbdba6e694e01a1d8bc3e50067bf0, call_6de0b1550c6247a2b4281f4e0be10b29, call_b97ba25f22a44e04b4cd4215ab5fbd62]

## Reasoning

Registration and implementation are complementary. ARCHITECTURES derives the lookup key from Exaone4Model.config_class.arch_string. Config.from_directory selects Exaone4Config from the single architectures entry, not model_type; Model.from_config then constructs the config's text component. The adapter also depends on the immediately preceding TransformerBlock change: both branches are present but neither has an input norm, so each needs the new FP16 input fallback. [source; call_6de0b1550c6247a2b4281f4e0be10b29, call_b97ba25f22a44e04b4cd4215ab5fbd62, call_aac72dc442054204ac0e9630112c1167, call_bdce74478f6a42d9be5f535ede3992bc]

The 32B schedule gives three layers per group a bounded attention window and leaves every fourth layer able to attend across the available causal prefix. That combines local and global attention without introducing a new kernel. This is a consequence of the construction, not evidence of the author's rationale or of reduced KV allocation: all layers still advertise KV-cache support. [inference; call_b97ba25f22a44e04b4cd4215ab5fbd62, call_4e8bb0a1e1fc4e47a5c8bd46fa0a7c00, call_bbd2b851836c4ce590d77a12a0ed281b, call_720c8597b17943b98e22000de99fc999]

## Impact

The dense 32B reference supplies the schedule and the inspected decoder tensor layout. All four inspected 1.2B variants reach the same null-pattern construction failure, regardless of their weight format. At the separate storage boundary, the 32B AWQ and GPTQ projections do not match a native Linear loading route, and the 32B FP8 projections use a file dtype the loader rejects. Recognizing the architecture is not the same as supporting every checkpoint that declares it. [source; call_b97ba25f22a44e04b4cd4215ab5fbd62, call_72b903ab3ebe4fdf8090a748c92df662, call_56cf4816bd824bf3a55a720711523ab3, call_e2733f47b7f448f09cf8b98304647e54, call_76199f824572452781745e0f16f88473, call_20bb0e4442b24154993aa4994378ab81, call_bdce74478f6a42d9be5f535ede3992bc, call_b61046349ff442bf8c8db2828c44e0ff]

## Source Notes

Read the initial models and modules chapters for the shared checkpoint and decoder contracts, Qwen3 for per-head normalization and the tied-head fallback, SmolLM3 for selective RoPE, and language-only Gemma3 for local/global attention and post-norm composition. The immediate parent entry documents the normless sequential fallback and the separate research sampler; the EXAONE chat entry documents the independent example-side formatter; the scaled-FP8 entry documents the ordinary Linear scale hook and its loader preconditions. [ancestor; call_071236595bf04656a9a8ad08a3a84e2c, call_d2a649469d744e27a7764159ae36ca0a, call_8ce14bfe96f24b1789ddcac1445c97b3, call_fd0c2a9213244455adcb77cd26b0ce97, call_afad1eb5a26248fdb5d1cb634cdbc4b0, call_d9e583006f9f4c78acd4fb8926a7c777, call_b0b01ce7b3e74b70ab3d4c7f6e00e3ec, call_d574acdd54eb4a229aae2425aecb5340]

The undefined expect_arch diagnostic reported by the Qwen3 entry does not carry over: 'Fix assertion' (04dc5571) replaced it with self.arch_string, and the parent source still uses that expression. The old missing-input-norm failure was removed from sequential forward by the immediate parent, not by this patch. ParallelDecoderBlock still dereferences its components unconditionally, but EXAONE4 does not instantiate it. The plural-projection allocator still assumes .ups/.downs; EXAONE4 supplies GatedMLP, which has those lists, not plain MLP. SmolLM3 Base's missing no_rope_layers is specific to that adapter; EXAONE4 has its own, distinct null-pattern failure. [source; call_47d4e7001e184cea812e024277a2ef86, call_bdce74478f6a42d9be5f535ede3992bc, call_bbd2b851836c4ce590d77a12a0ed281b, call_b97ba25f22a44e04b4cd4215ab5fbd62, call_aa2c79f06b3c4f82a9fe2b27eb8c8d20]

The checked history and current source show no intervening repair of the sampler's direct norm access or the mutable prefill flag. The sampler file history has only its introduction; Model.prefill still leaves the flag set, and the task changes neither model dispatch loop nor block forward. The separate EXAONE chat mode also still passes an exact-token lookup result unchecked to Job; an absent marker ID yields None, which Job rejects even though a literal string stop is supplied. The task's string helper neither calls that mode nor uses its stop list. [source; call_bd9837992742484c96abcba3bcc9fb68, call_65e6ba18bf93462d894c72b4b1acf2d4, call_cff13878f330421aa95a40e2c8907dbe, call_bdce74478f6a42d9be5f535ede3992bc, call_c9257d3b590a440fa685118310b136b1, call_720c8597b17943b98e22000de99fc999, call_7cbb1f759b0443c3b7aef777ac4db9b0, call_b97ba25f22a44e04b4cd4215ab5fbd62]

The later 'Keep original torch.dtype' edit affects metadata reporting, and the #55 regression fix affects the fused-weight fallback; neither supplies F8_E4M3 decoding or changes the ordinary scale sequence. The parent still scales deferred placeholders before end_deferred_load populates them, and still transposes ordinary weights without transposing the scale grid. Neither secondary issue is the failure reached with the pinned FP8 files: their file dtype is rejected first. The dense BF16 examples do not supply scale grids on the inspected projections. [source; call_fc70f9329f614f28a5305beaf66f7def, call_0dd2f77c008f4f0c9938a7a30ec6f6f0, call_b61046349ff442bf8c8db2828c44e0ff, call_bbd2b851836c4ce590d77a12a0ed281b, call_e60a185bc7064044a6f29f623b26715d, call_720c8597b17943b98e22000de99fc999, call_56cf4816bd824bf3a55a720711523ab3, call_9e3e95e8f8f847819a07d9bc1a767108]

The discussion connections are inferred, not upstream links. PR #4, “chore: update config.py,” proposes a spelling correction in the shared config file. Issue #7, “quantizing model: undefined symbol: __cxa_call_terminate,” traces through the same Config/RoPE imports to an extension import failure. Issue #29, “Auto-YaRN for Qwen3? Maybe even set it dynamically?”, discusses the shared RopeSettings mechanism, but EXAONE4's pinned scaling is Llama3-style, not request-dependent YaRN. Issue #33, “Error converting model,” reaches the inspected safetensors file-open call during compilation, not the architecture dispatch or dtype checks. [inference; call_0315ecddf5164d3d9c8abad6ec02a0c1, call_4856997ec3154f0faf53f1e26ca63614, call_01dd780b9db04753a8b42b0e7559d585, call_86e98823a42c43ca97dad6aa176d5c3e, call_e60a185bc7064044a6f29f623b26715d, call_c9257d3b590a440fa685118310b136b1]

Other inferred overlaps are through the shared conversion or generation code. PR #26, “Superior 3INST parameters,” proposes a decoder multiplier, not model registration. Issue #34, “torch._C._LinAlgError on last layer of quant,” and #52, “Error converting moonshotai/Kimi-Dev-72B,” trace into Linear.convert_exl3 and Cholesky; #42, “converting to 3.0 bpw causes error; block state has 0 inf values and 34 NaN values,” logs the same projection families during conversion of another model. Issue #53, “Command A support,” asks about Command A and availability of EXL3 quants, and points to the separate Cohere2 adapter. Issue #48, “`RuntimeError` when requesting logprobs with Gemma 3 models,” traces a Gemma logits-width mismatch in Job, not an EXAONE4 failure; the reference EXAONE4 vocabulary width is already 128-aligned. None establishes that this change fixes the reported behavior. [inference; call_56f3018a1f744c9a87e2920c7f11fe89, call_2862daabce3940b88ea91501bb3173bc, call_88bc713da28647d98f7634439b1deb8f, call_3bb3eafdeebf42129037226871cf96ed, call_ca899816a78b4133a07580c72e357269, call_a874fc7e03854d80b8ebd1a95fcff058, call_e60a185bc7064044a6f29f623b26715d, call_4e8bb0a1e1fc4e47a5c8bd46fa0a7c00]

<a id="models"></a>

## EXAONE4 dispatch, post-norm blocks, and checkpoint compatibility

The adapter requires hidden width, query-head count, intermediate width, RMS epsilon and layer count. KV heads default to query heads; a missing, null or zero head_dim falls back to hidden_size // num_attention_heads. The optional activation must be SiLU when supplied. Tying defaults false, window width defaults to -1 (unrestricted), and pattern defaults to None. The typed reader treats JSON null as missing. The parent Cohere2 and Gemma3 adapters read the same pattern key as an integer period, while Gemma2 reads sliding_window_size; EXAONE4 reads the exact sliding_window key and its own string pattern. No existing adapter's interpretation changes. [source; call_b97ba25f22a44e04b4cd4215ab5fbd62, call_ce70fc294b554e0f9d3e1301d34f1ea8, call_bbd2b851836c4ce590d77a12a0ed281b]

LGAI-EXAONE/EXAONE-4.0-1.2B, EXAONE-4.0-1.2B-AWQ, EXAONE-4.0-1.2B-FP8 and EXAONE-4.0-1.2B-GPTQ-Int8 each declare the registered architecture and explicitly provide hidden/intermediate widths 2048/4096, 32/8 query/KV heads, head width 64, 30 layers, tied embeddings and a 65,536-position setting. Each supplies null for both window fields. Width resolves to -1, but pattern resolves to None and layer 0 attempts len(None); this source does not produce an all-global, all-rotary, or any other usable 1.2B schedule. [source; call_25e1ba13fc8a4fbf8857c1a7a6860635, call_4ddd06b28f3643c39df7461bf3865eb6, call_2eac2e5e8723476b99b2543d9f125a9d, call_8f05fc237b0643168e38aeb22da597c3, call_b97ba25f22a44e04b4cd4215ab5fbd62, call_bbd2b851836c4ce590d77a12a0ed281b]

LGAI-EXAONE/EXAONE-4.0-32B, EXAONE-4.0-32B-AWQ, EXAONE-4.0-32B-FP8 and EXAONE-4.0-32B-GPTQ each explicitly supply 5120/27392 widths, 40/8 heads, head width 128, 64 layers, untied embeddings, 131,072 positions, window 4096 and pattern LLLG. For each non-final layer the code repeats the string and tests for uppercase L; it forces the final layer global. Local layers receive both the window and NEOX RoPE; global layers receive -1 and no RoPE, but still run attention and Q/K normalization. Both sizes supply vocabulary 102400, SiLU, RMS epsilon 1e-5, theta 1,000,000 and Llama3 scaling with factor 16, original context 8192, and low/high factors 1/4. [source; call_4e8bb0a1e1fc4e47a5c8bd46fa0a7c00, call_35e93bd0f06a4fde9f23a73a61065793, call_40908de89a97435ca8d25c73ec02d6d8, call_8d8d713380ca49c4903d19ebece663e1, call_25e1ba13fc8a4fbf8857c1a7a6860635, call_b97ba25f22a44e04b4cd4215ab5fbd62, call_720c8597b17943b98e22000de99fc999, call_c9257d3b590a440fa685118310b136b1]

The block starts from the embedding's default FP32 residual. Attention receives an FP16 copy, reshapes projected Q/K/V by head, and applies per-head RMSNorm to Q and K, not V. The rotary path supplies those weights to RoPE; the nonrotary path calls the norms directly. The O projection defaults to FP16, and its post-norm preserves that dtype before addition to the FP32 residual. The MLP takes a fresh FP16 copy of the updated residual, applies SiLU(gate) times up in FP16, and requests FP32 down output; its post-norm preserves FP32 before the second addition. These are ordinary weight-multiplying RMSNorms, not Gemma's weight-plus-one variant. The final model.norm explicitly emits FP16 into lm_head. [source; call_b97ba25f22a44e04b4cd4215ab5fbd62, call_bdce74478f6a42d9be5f535ede3992bc, call_c9257d3b590a440fa685118310b136b1, call_720c8597b17943b98e22000de99fc999, call_7cbb1f759b0443c3b7aef777ac4db9b0, call_edb9c6dcecee4cea9b0e00f1ff709735]

prepare_inputs saves the original IDs in params and returns prepare_for_attn's result, matching all 16 parent architecture call sites without omitting a caller-side guard. Cache checks and page/position preparation remain in the helper. Cached and uncached FlashAttention receive the window tuple; sdpa_nc rejects a nonnegative window. Model.prefill stops at the last block, after its attention but before its post-norm, residual addition or MLP. The model's separate default_chat_prompt emits a truthy optional system turn, one user turn, and an open assistant prefix, using [|system|], [|user|], [|assistant|] and [|endofturn|] with newlines. It supplies no default system text, explicit BOS, history, or stop handling. [source; call_b97ba25f22a44e04b4cd4215ab5fbd62, call_5987c806add04822af6cc31423538a3e, call_aac72dc442054204ac0e9630112c1167, call_bbd2b851836c4ce590d77a12a0ed281b, call_c9257d3b590a440fa685118310b136b1, call_bdce74478f6a42d9be5f535ede3992bc]

Dense first-layer headers match the requested .weight keys: self_attn.{q,o}_proj are [2048,2048] or [5120,5120]; {k,v}_proj are [512,2048] or [1024,5120]; mlp.{gate,up}_proj are [4096,2048] or [27392,5120]; down_proj reverses those axes. self_attn.{q,k}_norm have width 64 or 128; post_attention_layernorm, post_feedforward_layernorm and model.norm have hidden width. model.embed_tokens.weight is [102400,H]. The 1.2B dense header starts with the embedding, without a separate lm_head at the start of its sorted keys; all four 32B headers inspected contain a separate BF16 lm_head.weight [102400,5120]. The tied branch offers the embedding as an alternate, not forced shared storage: has_tensor('lm_head') is an exact bare-key check and does not detect lm_head.weight, but Linear tries the primary key before the alternate within each format. [source; call_9e3e95e8f8f847819a07d9bc1a767108, call_84f58840e62c41709be7ae977d115ed4, call_56cf4816bd824bf3a55a720711523ab3, call_8fc319b7d03c44b4bb77c868bdda13ec, call_bc23b38786c345e7b528280a0a9615c0, call_ff4943f7cc084a37bd9bc1f13375a971, call_1543b909c3684bfa85cc11d1a6b643a7, call_eba47e760e884baea208609b778d0e89, call_bdce74478f6a42d9be5f535ede3992bc, call_b97ba25f22a44e04b4cd4215ab5fbd62]

No fused projection or sliced MLP keys are selected: the adapter supplies separate projections and both intermediate widths are below the shared split threshold 55,296. In the checked layer-0 headers no projection bias or EXL3 group is present. Linear probes EXL3 using trellis plus su/suh and sv/svh; without that group it does not read the EXL3 auxiliaries scale, mcg or mul1. Ordinary loads ask for .weight and optional .bias and .weight_scale_inv. AWQ instead stores I32 qweight [in,out/8] and qzeros [in/128,out/8], with F16 scales [in/128,out]. GPTQ stores I32 qweight [in/p,out], qzeros [in/128,out/p], and g_idx [in], plus F16 scales [in/128,out], where p is four at 8 bits or eight at 4 bits. The native Linear loader never reads those packed AWQ/GPTQ tensors. FP8 uses ordinary matrix names with F8_E4M3 and a BF16 weight_scale_inv grid [out/128,in/128]; the dtype rejection happens before reading that grid. [source; call_b97ba25f22a44e04b4cd4215ab5fbd62, call_4297db15f4594f569934bbfce0663601, call_bbd2b851836c4ce590d77a12a0ed281b, call_d76added98b74481bc8fa787c2284f88, call_a2413d3bc9004d1d96e981d38c926dc4, call_e2733f47b7f448f09cf8b98304647e54, call_76199f824572452781745e0f16f88473, call_f783f82f36a74dcc8e53c2175059de55, call_20bb0e4442b24154993aa4994378ab81, call_9fbed0ed7d1e4ab7bfdcbac746b0b8ef, call_b61046349ff442bf8c8db2828c44e0ff]

The bounded Python check executed the extracted typed reader and transcribed the layer expression: 1.2B gave -1/None and TypeError; an empty string gave division by zero; 32B gave 48 local layers and 16 global layers at zero-based indices 3,7,…,63. Integer arithmetic reproduced the dense matrix dimensions and four versus five query heads per KV head. It also reproduced the FP8 scale-grid mismatch after default weight transposition (K projection: stored 4×16 or 8×40, required 16×4 or 40×8) and the 2,048/8,192 wavelength boundaries of the Llama3 scaling blend. The extracted dtype switch raised 'Unknown dtype F8_E4M3'. [execution; call_72b903ab3ebe4fdf8090a748c92df662, call_385eaf17634d4760b708440721aeebb5]

## Authoring-time findings — pending review

### null-window-pattern-blocks-1p2b (suspected; external_compatibility)

The new adapter cannot construct any of the four inspected 1.2B variants unchanged.

Trigger: Build a model from any inspected 1.2B configuration, where sliding_window_pattern is null and there is more than one layer. Omitting the key has the same effect; explicitly supplying an empty string instead reaches modulo zero.

Expected: Handle the absent schedule explicitly, or reject it with an architecture-specific configuration diagnostic.

Actual: The pattern defaults to None and the layer-0 expression calls len(None), before any decoder blocks or the head are built. An empty string reaches idx % 0. Model.from_config is the generic constructor dispatch; conversion's get_base_model is one higher-level caller.

Locations: 544ba423bf9c58c940dca6cb36a1aa93f6cda41a:exllamav3/models/exaone4.py — Exaone4Model.__init__

Source evidence: call_b97ba25f22a44e04b4cd4215ab5fbd62, call_25e1ba13fc8a4fbf8857c1a7a6860635, call_4ddd06b28f3643c39df7461bf3865eb6, call_2eac2e5e8723476b99b2543d9f125a9d, call_8f05fc237b0643168e38aeb22da597c3, call_e60a185bc7064044a6f29f623b26715d

scalar_transcription: Ran the extracted reader and the scalar layer predicate with the pinned values and an empty-pattern case. [call_72b903ab3ebe4fdf8090a748c92df662]. Limits: No model construction or tensor loading was run.

### packed-awq-gptq-projections-not-loadable (suspected; external_compatibility)

The registered architecture does not add a loader for the packed AWQ and GPTQ checkpoint variants.

Trigger: Load a layer-0 packed projection from the pinned 32B AWQ or GPTQ checkpoint. The 1.2B variants have the same storage mismatch but are blocked earlier by the pattern.

Expected: Packed-format support would require a matching decoder or an explicit format rejection.

Actual: Linear.load finds neither an EXL3 group nor a dense .weight for the projection and raises its generic unsupported-quantization-format ValueError.

Locations: ff21ee46edb9ba74d709257f482c809a7bd406d0:exllamav3/modules/linear.py — Linear.load

Source evidence: call_e2733f47b7f448f09cf8b98304647e54, call_76199f824572452781745e0f16f88473, call_bdce74478f6a42d9be5f535ede3992bc, call_c983ddb28daa48d69309051cfc24528e

source_inspection: Compared the keys requested by the new projection builders and Linear's two storage routes with both header layouts. [call_b97ba25f22a44e04b4cd4215ab5fbd62, call_bbd2b851836c4ce590d77a12a0ed281b, call_e2733f47b7f448f09cf8b98304647e54, call_76199f824572452781745e0f16f88473, call_c983ddb28daa48d69309051cfc24528e]. Limits: No full load; no claim about external unpackers or converted checkpoint formats.

### fp8-dtype-rejected-before-scales (suspected; external_compatibility)

The inherited FP8 dtype restriction remains at the task revision.

Trigger: Load an F8_E4M3 projection from the pinned 32B FP8 checkpoint. The 1.2B FP8 header has the same dtype, but model construction stops earlier.

Expected: Support for the checkpoint would require decoding the file dtype and applying the corresponding scales.

Actual: The sole direct load_fp16 caller is Linear.load. Its weight request reaches SafetensorsCollection.get_tensor and convert_dtype raises ValueError before the companion scale lookup.

Locations: ff21ee46edb9ba74d709257f482c809a7bd406d0:exllamav3/loader/safetensors.py — convert_dtype

Source evidence: call_f05030d93a0d4683afd49058ecb5605e, call_e60a185bc7064044a6f29f623b26715d, call_b61046349ff442bf8c8db2828c44e0ff, call_20bb0e4442b24154993aa4994378ab81

repository_execution: Executed the extracted parent dtype switch with the exact header dtype string. [call_385eaf17634d4760b708440721aeebb5]. Limits: Only the string-to-dtype helper ran, not checkpoint loading or PyTorch.

### sdpa-rejects-local-attention (suspected; external_compatibility)

The selectable no-cache SDPA route is not equivalent to FlashAttention for the 32B schedule.

Trigger: Forward a loaded 32B model with attn_mode='sdpa_nc', without a cache, and reach the first local layer.

Expected: A compatible alternative would implement the local mask or reject the backend choice before projection.

Actual: Attention.forward dispatches to decode_sdpa_nc, which projects Q/K/V and then asserts that sliding_window is negative. Layer 0 supplies 4096.

Locations: ff21ee46edb9ba74d709257f482c809a7bd406d0:exllamav3/modules/attn.py — Attention.decode_sdpa_nc

Source evidence: call_85e8a68e510247f1beb78b51ac8e4512, call_c9257d3b590a440fa685118310b136b1, call_b97ba25f22a44e04b4cd4215ab5fbd62, call_070cd7809b274c9a9af7bc9a32a255a2

source_inspection: Traced the explicit mode through shared dispatch to its window assertion. [call_720c8597b17943b98e22000de99fc999, call_c9257d3b590a440fa685118310b136b1, call_070cd7809b274c9a9af7bc9a32a255a2]. Limits: This is an explicit backend limit, not a measured failure of the default FlashAttention path.

### research-sampler-bypasses-normless-fallback (suspected; external_compatibility)

The inherited sampler precondition now excludes the normless EXAONE4 blocks.

Trigger: Point sample_qkv at an otherwise loadable EXAONE4 model and reach an uncached target layer.

Expected: A compatible sampler would use the same FP16 branch input as the block, apply Q/K normalization, and handle the absence of global-layer RoPE.

Actual: The sampler dereferences module.attn_norm.forward on None before it can call block.forward. Its later direct RoPE call is also unconditional, so adding only the input cast would not handle a global target.

Locations: ff21ee46edb9ba74d709257f482c809a7bd406d0:science/kv_quant_exp.py — sample_qkv

Source evidence: call_9d330832d9044f5d8db6d47c65c7ff9e, call_c9257d3b590a440fa685118310b136b1, call_b97ba25f22a44e04b4cd4215ab5fbd62, call_052d48f063e347c8b28dc172ea7250d1, call_9172d703da83492b9a87f74f06244e80

source_inspection: Compared the sampler's direct projection setup with the task builder and shared forward; the only literal caller is the research script itself. [call_9d330832d9044f5d8db6d47c65c7ff9e, call_c9257d3b590a440fa685118310b136b1, call_bdce74478f6a42d9be5f535ede3992bc, call_052d48f063e347c8b28dc172ea7250d1, call_9172d703da83492b9a87f74f06244e80, call_b97ba25f22a44e04b4cd4215ab5fbd62]. Limits: The script defaults to Llama; this does not affect ordinary EXAONE4 forward or generation.

### reused-prefill-params-skip-residual-updates (suspected; defect)

The inherited mutable prefill flag still affects the newly registered decoder.

Trigger: Reuse the same params dictionary for ordinary forward after prefill reaches the last KV block, without clearing prefill, and reach the attention call.

Expected: An ordinary forward should apply the attention post-norm and residual update, then run the MLP branch.

Actual: Model.prefill leaves prefill true; neither forward nor the new prepare_inputs clears it. TransformerBlock returns after attention without updating the residual or running the MLP.

Locations: ff21ee46edb9ba74d709257f482c809a7bd406d0:exllamav3/models/model.py — Model.prefill, ff21ee46edb9ba74d709257f482c809a7bd406d0:exllamav3/modules/transformer.py — TransformerBlock.forward

Source evidence: call_bdce74478f6a42d9be5f535ede3992bc, call_b97ba25f22a44e04b4cd4215ab5fbd62, call_41802e68da05491d81439bd9482df94e, call_f1d761c99f2944a0a7610f0e35504e49, call_9172d703da83492b9a87f74f06244e80

source_inspection: Traced dictionary mutation and block dispatch; the inspected generation example uses fresh dictionaries, and Job passes a literal prefill dictionary. [call_bdce74478f6a42d9be5f535ede3992bc, call_7cbb1f759b0443c3b7aef777ac4db9b0, call_c9257d3b590a440fa685118310b136b1, call_f1d761c99f2944a0a7610f0e35504e49, call_9172d703da83492b9a87f74f06244e80]. Limits: Conditional direct-API reuse, not an observed bundled-generation failure.

## Uncertainty and limits

No full configuration or model was instantiated, and no weight payload, native loader, CUDA kernel, generation, EXL3 conversion, or performance or reference-output comparison was exercised. Execution evidence is limited to isolated Python helpers and scalar metadata checks.

Header checks cover the first-layer tensor families at all eight pins, plus selected final norm and head entries. They are not an exhaustive inventory of all tensors in all shards. Storage metadata does not establish scale values, numerical equivalence, tokenizer behavior, or usable context length.

The rationale for the forced-global final layer and precision choices is not stated in the inspected change. The pinned 32B pattern already ends in G, so the forced-final rule does not alter that particular schedule.
