# 544ba423bf9c58c940dca6cb36a1aa93f6cda41a


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/544ba423bf9c58c940dca6cb36a1aa93f6cda41a) · [Evidence ledger](draft.json)

Registers EXAONE4 and builds post-normalized decoder blocks with local RoPE attention and global non-rotary attention. The pinned 32B configs fit that schedule, but all four 1.2B configs reach a constructor error because their layer pattern is null.

- [EXAONE4 dispatch, post-normalized blocks and hybrid attention](#models)

## Problem

The parent registry does not recognize `Exaone4ForCausalLM`. The commit message says “Add Exaone4 architecture,” and the diff adds both the registry entry and the configuration and model classes needed to construct it. Registration does not by itself establish compatibility with every checkpoint that declares the architecture. [source; call_0150d061ae2749c7bcb64c9caf323f0d, call_d70002e1cffa40c986c844e2916e15d4, call_1c25ab12bbea4cbc9d32f2f66d664846, call_5eaabcf92c094b00a446fce893b149ff]

## Reasoning

The registry and model builder supply different steps of the same path: `Config.from_directory` resolves the single architecture string to `Exaone4Config`, and `Model.from_config` uses that config's `text` component to construct `Exaone4Model`. The registry alone would not supply the EXAONE layer layout, and the builder alone would not make it discoverable through the factory. [source; call_d70002e1cffa40c986c844e2916e15d4, call_1c25ab12bbea4cbc9d32f2f66d664846, call_5eaabcf92c094b00a446fce893b149ff, call_aacdfe12203b4fe9beadfdc942db9fd3, call_23da5b887b58442caf766d02d2866364]

EXAONE reuses the Qwen3-style projection and per-head normalization layout, but moves the residual-branch norms to the outputs and couples rotary positioning to the local-attention schedule. Reusing `TransformerBlock` is possible because the immediate parent already supplies FP16 inputs when a branch has no pre-norm. This is a source-supported design fit, not evidence of why the author chose the implementation. [inference; call_5eaabcf92c094b00a446fce893b149ff, call_7f7d290c4ae749a6862901eef4bb884c, call_2c8af29868594cc7a5d2a597b6769958]

## Impact

The 32B configs supply the string pattern this builder expects. All four pinned 1.2B configs also match the architecture string, but supply a null pattern and reach an error during model construction, before decoder blocks or weights are loaded. The registry does not add AWQ or GPTQ decoding or extend the safetensors dtype table for FP8. [source; call_5eaabcf92c094b00a446fce893b149ff, call_3377d4ebd2ec4e5683ae2e23c7541681, call_2b8c103dbf634a81865bcbce530f9958, call_1456a551b75a44e5bc4fec734b39e28d, call_6811bfd0bb9f43eb8852d42a9aabcc81, call_74481648287e4b03a7a0f81289d32525, call_2c86362cd06a4b1c9f15a8847000c3d1, call_2b5d195740564322ac07eca2af4e10ea, call_74e7416fd19c434797451855cfb728c1, call_d21423e7ff434b2e8defedee0f58d851, call_7132326581ff46759be7728f1eecfb7b, call_4967aa3afc5e40a8815f9fbe83f5b31a]

## Source Notes

The class-owned registry entry explains the `config_class` and `arch_string` convention and records the inherited architecture-mismatch diagnostic. The Qwen3 entry documents the reused Q/K-normalization and head lookup pattern. The immediate-parent TransformerBlock entry explains the normless FP16 handoff and records the independent prefill and KV-sampler issues. The earlier EXAONE chat entry documents the manually selected history formatter and its stop-list behavior. [ancestor; call_cdbef282238f467aab05aeadc632c70a, call_ea851eab49164819bbdb1277935f495a, call_e65606eb629143618756601a66dd851f, call_f60bdcb4d32e49e0bfb074746ac8848a]

The earlier K-only Q/K-normalization issue remains in `Attention`'s constructor, but EXAONE supplies both norms with the same epsilon. The optional plain-MLP allocation issue does not follow this assembly: EXAONE supplies `GatedMLP`, not plain `MLP`, and does not choose `ParallelDecoderBlock`. [source; call_5eaabcf92c094b00a446fce893b149ff, call_4fa802e5dd18419195240a9fa2eb6b2f, call_2c8af29868594cc7a5d2a597b6769958, call_fa68c2d87ec14948a416ca0bfcd414ad]

PR #4, “chore: update config.py,” proposes a spelling correction in the shared config file. Issue #7, “quantizing model: undefined symbol: __cxa_call_terminate,” reports an extension import failure and a toolchain workaround; its traceback includes the same `RopeSettings` import in `config.py`. Issue #29, “Auto-YaRN for Qwen3? Maybe even set it dynamically?”, requests Qwen3 scaling changes in the shared RoPE code. These are inferred overlaps by file, import or mechanism, not evidence that the EXAONE patch addresses those reports. [inference; call_6526435930c84996ad8932bae0cc3274, call_0909d4c3a8864228b3026877c47fe6bb, call_9ab8547696834d6da1ca9c32a37d0cdb, call_aacdfe12203b4fe9beadfdc942db9fd3, call_d146e0da02ec49e2b0550203e2c67a67]

PR #26, “Superior 3INST parameters,” proposes a codebook multiplier in the shared conversion workflow. Issue #33, “Error converting model,” reports a Qwen3 file-open failure in `SafetensorsCollection.get_tensor` during compilation. Issues #34, “torch._C._LinAlgError on last layer of quant,” #42, “converting to 3.0 bpw causes error; block state has 0 inf values and 34 NaN values,” and #52, “Error converting moonshotai/Kimi-Dev-72B,” report quantization failures with `Linear.convert_exl3` in the trace. Their inferred overlap is shared conversion code, not an EXAONE constructor or tensor-format failure. [inference; call_3cd4a8b08edf4d53bca3b49d05b92a02, call_3a1fefab80ab46f086351685f71fe7d2, call_c097c915a14343ae9bfa78092386e048, call_c77e059d123541f3851d8a5f2f975432, call_0e2b062569634e3ab2d0bc7db53c7303, call_ddf15adea9064c329eada0e12067e89a, call_7132326581ff46759be7728f1eecfb7b]

Issue #48, “`RuntimeError` when requesting logprobs with Gemma 3 models,” reports a logits-buffer width mismatch for Gemma 3, an overlap by model source inspected for window scheduling, not by the failing operation. Issue #50, “RuntimeError: Insufficient VRAM in split for model and cache despite remaining 1GB VRAM (exllamav3 + tabbyAPI),” matches the shared autosplit error string but reports other models. Issue #53, “Command A support,” asks about availability of Command A quants and points to the inspected Cohere2 builder; its local/global arrangement is a comparison, not a link to EXAONE provenance. [inference; call_0becd97110694d0988169a27b1381fd1, call_c5635b8fb8434ff18205faca0542c817, call_a9145370aad84af58f5021384d0c161d, call_23da5b887b58442caf766d02d2866364, call_700349846d5e41e3a9406845ab1d167d]

<a id="models"></a>

## EXAONE4 dispatch, post-normalized blocks and hybrid attention

`Exaone4Config` requires residual width, query-head count, intermediate width, RMS epsilon and layer count. A missing KV-head count defaults to the query-head count; a falsy head width is derived by integer division of residual width by query heads. `hidden_act` can be absent but otherwise must be `silu`; tying defaults to false. The shared config reader treats null as missing, so `sliding_window: null` becomes −1 and `sliding_window_pattern: null` becomes `None`. The same exact pattern key is an integer period in Cohere2 and Gemma3, but this new class expects a string of layer codes; those other readers are unchanged. [source; call_5eaabcf92c094b00a446fce893b149ff, call_aacdfe12203b4fe9beadfdc942db9fd3, call_3377d4ebd2ec4e5683ae2e23c7541681, call_f77df612a84348d9ae157325b421f211, call_9bf6de37d73048ddaa2eb02798840258, call_bc0114cf1b804afb95051c1a5a0cdab6, call_700349846d5e41e3a9406845ab1d167d]

The four pinned 1.2B configs (`EXAONE-4.0-1.2B`, `EXAONE-4.0-1.2B-AWQ`, `EXAONE-4.0-1.2B-FP8`, and `EXAONE-4.0-1.2B-GPTQ-Int8`) each provide hidden/intermediate widths 2048/4096, 32 query and 8 KV heads of width 64, 30 layers, 65,536 maximum positions, tying enabled, and null window and pattern. Each matches dispatch and dimensional inputs, but the pattern default is not usable for its 30-layer construction. The variants declare different storage methods, not different layer schedules. [source; call_5eaabcf92c094b00a446fce893b149ff, call_2b8c103dbf634a81865bcbce530f9958, call_1456a551b75a44e5bc4fec734b39e28d, call_6811bfd0bb9f43eb8852d42a9aabcc81, call_74481648287e4b03a7a0f81289d32525]

The four pinned 32B configs (`EXAONE-4.0-32B`, `EXAONE-4.0-32B-AWQ`, `EXAONE-4.0-32B-FP8`, and `EXAONE-4.0-32B-GPTQ`) each provide hidden/intermediate widths 5120/27392, 40 query and 8 KV heads of width 128, 64 layers, 131,072 maximum positions, untied embeddings, window 4096 and pattern `LLLG`. Each matches the dispatch, dimension and window inputs without those fallbacks. Both sizes explicitly supply SiLU, RMS epsilon 1e-5, vocabulary 102400, theta 1,000,000 and Llama-3 frequency scaling. Neither size relies on deriving head width. The model builder does not select its runtime cache mode from `use_cache`. [source; call_5eaabcf92c094b00a446fce893b149ff, call_4fa802e5dd18419195240a9fa2eb6b2f, call_2c86362cd06a4b1c9f15a8847000c3d1, call_2b5d195740564322ac07eca2af4e10ea, call_74e7416fd19c434797451855cfb728c1, call_d21423e7ff434b2e8defedee0f58d851, call_2b8c103dbf634a81865bcbce530f9958, call_1456a551b75a44e5bc4fec734b39e28d, call_6811bfd0bb9f43eb8852d42a9aabcc81, call_74481648287e4b03a7a0f81289d32525]

The schedule repeats the pattern by zero-based modular indexing. Only uppercase `L` marks a local layer, and the final layer is global regardless of the character. Local layers get both the configured window and NEOX-style RoPE; global layers get −1 and no RoPE. For the 32B reference, shared Llama-3 scaling preserves frequencies with wavelengths shorter than 2048 positions, scales those longer than 8192 by dividing the inverse frequency by 16, and interpolates between those thresholds. Those thresholds come from the original 8192 positions divided by the configured high and low factors, 4 and 1; they are separate from the 4096 attention window. [source; call_5eaabcf92c094b00a446fce893b149ff, call_4fa802e5dd18419195240a9fa2eb6b2f, call_aacdfe12203b4fe9beadfdc942db9fd3, call_d146e0da02ec49e2b0550203e2c67a67, call_2c86362cd06a4b1c9f15a8847000c3d1]

The bounded Python check produced 48 local and 16 global layers for `LLLG`, with global indices 3, 7, …, 63. It calculated Q and KV projection widths of 5120/1024 at 32B and 2048/512 at 1.2B, corresponding to five and four query heads per KV head, respectively. The transcribed 1.2B schedule failed at `len(None)` after config defaulting, and a two-layer empty-string check failed at modulo by zero. [execution; call_a19506e98a684b8d89f1c4464021ef62]

Attention projects and reshapes Q/K/V into heads, and normalizes only Q and K. The local RMSNorm weights can be passed into `RoPE.apply`; without RoPE, attention runs the Q/K norms explicitly. Both FlashAttention paths receive the window pair; cached attention additionally consumes cache tensors and updates the cache. The inherited SDPA path rejects a nonnegative window instead of emulating it. A global layer therefore keeps Q/K normalization even though it skips rotation and does not request a finite window. [source; call_5eaabcf92c094b00a446fce893b149ff, call_4fa802e5dd18419195240a9fa2eb6b2f]

The module sequence is embedding, sequential decoder blocks, final RMSNorm with FP16 output, and vocabulary projection. Within a block, attention receives an FP16 view or cast of the incoming residual; `post_attention_layernorm` normalizes the attention result before it is added. The gated MLP receives a fresh FP16 handoff from that updated residual, combines gate and up activations before the down projection, requests FP32 output, then applies `post_feedforward_layernorm` before the second addition. No `input_layernorm` is requested. On last-cache-layer prefill, the shared block runs attention and returns the incoming residual before either addition or the MLP; `Model.prefill` stops there. [source; call_5eaabcf92c094b00a446fce893b149ff, call_2c8af29868594cc7a5d2a597b6769958, call_23da5b887b58442caf766d02d2866364, call_fa68c2d87ec14948a416ca0bfcd414ad]

The dense headers match the requested tensor families. In layer 0, `self_attn.{q,o}_proj.weight` are [2048,2048] at 1.2B and [5120,5120] at 32B; `{k,v}_proj.weight` are [512,2048] and [1024,5120]. Q/K norm weights are [64] and [128]. `mlp.{gate,up}_proj.weight` are [4096,2048] and [27392,5120], with the axes reversed for `down_proj.weight`. Both post-norm weights and `model.norm.weight` have residual width. `model.embed_tokens.weight` is [102400,2048] or [102400,5120]. Stored linear matrices are output-by-input; the ordinary loader requests the transpose for its internal representation. [source; call_5eaabcf92c094b00a446fce893b149ff, call_4fa802e5dd18419195240a9fa2eb6b2f, call_7132326581ff46759be7728f1eecfb7b, call_2c0cb40e941a4fecab28d8a8fd93e3eb, call_4c1c32577e7647ddaff2b69f40555e1b, call_ee8c868f725a41f2a1d94265985aefe9, call_16b319bf5d2943a3b5694ab77b5c1348]

The dense 32B has `lm_head.weight` [102400,5120] and disables the alternate key. The dense 1.2B header starts with the embedding and has no head entry at its sorted head position; if construction got past scheduling, its tied head would fall back to `model.embed_tokens.weight`. This is a loading fallback, not forced parameter sharing: `has_tensor("lm_head")` probes an exact name, and Linear tries EXL3 storage across the primary and alternate keys before trying ordinary weights across those keys. The inspected dense projection groups contain no optional `.bias` or `.weight_scale_inv`, and no EXL3 `trellis` or `su`/`suh`, `sv`/`svh` group, so they select the ordinary weight path without bias or inverse scales. The EXL3-only optional `.scale`, `.mcg` and `.mul1` are not requested on that path. This builder does not supply a fused QKV key. [source; call_5eaabcf92c094b00a446fce893b149ff, call_4967aa3afc5e40a8815f9fbe83f5b31a, call_7132326581ff46759be7728f1eecfb7b, call_2c0cb40e941a4fecab28d8a8fd93e3eb, call_ee8c868f725a41f2a1d94265985aefe9, call_cd0cbdb94f734b409d2e91f1775f3224]

The representative `mlp.down_proj` headers distinguish layout from loadability. The 1.2B and 32B AWQ headers store `.qweight` [4096,256] and [27392,640]; GPTQ stores [1024,2048] and [3424,5120]. Those groups also have `.qzeros` and `.scales`, and GPTQ adds `.g_idx`; the inspected Linear paths do not request these names. Both FP8 headers instead use the expected `.weight` name and dense shape, plus `.weight_scale_inv` [16,32] or [40,214] for 128-by-128 blocks. Linear has an optional inverse-scale read, but its preceding weight read encounters the unsupported `F8_E4M3` dtype first. [source; call_de061e98d6b04517b0f07ac764b77ada, call_06898615cf07468b9429630446460ca4, call_97bd7a141b1f463485abcd8b907fcef5, call_8254cf5c6fcc482c881f92bdcbc1755c, call_95ecaea1ca644b619da785f5e7302d75, call_1007a6c6961544ba999d2ed1f9898804, call_7132326581ff46759be7728f1eecfb7b, call_4967aa3afc5e40a8815f9fbe83f5b31a, call_ddf15adea9064c329eada0e12067e89a]

`prepare_inputs` saves the original IDs in `params`, calls `prepare_for_attn`, and returns the resulting tensor. All 16 existing hooks found by the parent search use the same three statements, with no extra local guards or exception handling. The shared helper defaults to uncached FlashAttention and retains its cached-mode argument preparation and checks. Separately, `default_chat_prompt` emits an optional system turn, one user turn and an open assistant prefix, with `[|endofturn|]` after each included message. It emits no BOS marker and does not set a tokenizer policy or stop list. It neither replaces nor repairs the manual chat template. The only literal in-tree call found, `imgsearch`, requires a vision component before it reaches that hook, whereas EXAONE registers text only. [source; call_5eaabcf92c094b00a446fce893b149ff, call_988cbd490ced4ebc926eb2cd1a314109, call_1818267fda174cc38d5011dab50bb09e, call_aef216d75a67471b871a6d0ea01e28fc, call_4fa802e5dd18419195240a9fa2eb6b2f, call_ddfb1468aed648f5990a2bfecf401002, call_700349846d5e41e3a9406845ab1d167d]

## Authoring-time findings — pending review

### null-or-empty-layer-pattern (suspected; defect)

The new builder indexes a pattern that its own config reader allows to be absent. `Model.from_config` directly calls the registered text constructor, so ordinary model initialization and conversion reach this check when given an affected config.

Trigger: Construct the model with two or more decoder layers and a null, missing or empty `sliding_window_pattern`. All four pinned 1.2B configs have 30 layers and a null pattern.

Expected: Handle the reference no-window configuration without indexing a missing pattern, or reject unsupported pattern values with a configuration error that identifies the field.

Actual: `len(None)` raises `TypeError` at layer index 0 for null or missing patterns; an empty string reaches `idx % 0` and raises `ZeroDivisionError`. The last-layer guard does not protect any earlier layer.

Locations: 544ba423bf9c58c940dca6cb36a1aa93f6cda41a:exllamav3/models/exaone4.py — Exaone4Model.__init__

Source evidence: call_5eaabcf92c094b00a446fce893b149ff, call_3377d4ebd2ec4e5683ae2e23c7541681, call_74bef46b87704f429824286fa08961a5, call_23da5b887b58442caf766d02d2866364, call_839411b6b5d14ac18b291f763413793d, call_700349846d5e41e3a9406845ab1d167d, call_2b8c103dbf634a81865bcbce530f9958, call_1456a551b75a44e5bc4fec734b39e28d, call_6811bfd0bb9f43eb8852d42a9aabcc81, call_74481648287e4b03a7a0f81289d32525

source_inspection: Traced typed defaulting, the registry-selected text constructor, and the model-init and converter entry points. [call_3377d4ebd2ec4e5683ae2e23c7541681, call_5eaabcf92c094b00a446fce893b149ff, call_700349846d5e41e3a9406845ab1d167d]. Limits: This does not establish a correct reference RoPE policy for the null case.

scalar_transcription: Used the parent `read_dict` helper with a transcription of the layer expression and observed both exceptions. [call_a19506e98a684b8d89f1c4464021ef62]. Limits: The EXAONE class and weight loader were not executed.

### inherited-architecture-mismatch-diagnostic (suspected; defect)

The new config subclass inherits the unchanged mismatch assertion from `Config.__init__`.

Trigger: With assertions enabled, construct `Exaone4Config` directly against a config with one different architecture string.

Expected: Reject the mismatch with an assertion that identifies the expected architecture.

Actual: The assertion message evaluates undefined `expect_arch`, so it raises `NameError`. The normal factory selects the matching class first for stable supported files.

Locations: 544ba423bf9c58c940dca6cb36a1aa93f6cda41a:exllamav3/models/exaone4.py — Exaone4Config.__init__, ff21ee46edb9ba74d709257f482c809a7bd406d0:exllamav3/models/config.py — Config.__init__

Source evidence: call_5eaabcf92c094b00a446fce893b149ff, call_aacdfe12203b4fe9beadfdc942db9fd3

source_inspection: Compared the new superclass call with the unchanged assertion and factory ordering. [call_5eaabcf92c094b00a446fce893b149ff, call_aacdfe12203b4fe9beadfdc942db9fd3]. Limits: No full config constructor was executed; this is the conditional mismatched-class path.

### local-layers-reject-sdpa (suspected; external_compatibility)

The hybrid schedule exposes an existing backend restriction. The literal parent search found the SDPA mode inside attention dispatch, not an in-tree client selecting it.

Trigger: Run a constructed model containing a nonnegative-window layer with `attn_mode="sdpa_nc"`, without a cache and with assertions enabled.

Expected: An SDPA-compatible path would preserve the requested local window, or an unsupported combination would be rejected before layer execution.

Actual: `Attention.decode_sdpa_nc` projects Q/K/V and then asserts that the window is negative. Either FlashAttention route instead passes the window to its backend.

Locations: ff21ee46edb9ba74d709257f482c809a7bd406d0:exllamav3/modules/attn.py — Attention.decode_sdpa_nc

Source evidence: call_5eaabcf92c094b00a446fce893b149ff, call_4fa802e5dd18419195240a9fa2eb6b2f, call_04b7111043e7476da9ec71b7dee1e59a

source_inspection: Compared the mode dispatch, window assertion and FlashAttention arguments. [call_04b7111043e7476da9ec71b7dee1e59a, call_4fa802e5dd18419195240a9fa2eb6b2f]. Limits: This is a nondefault mode restriction, not a measured FlashAttention failure.

### quantized-reference-storage-boundary (suspected; external_compatibility)

Config recognition does not imply support for the indexed AWQ, GPTQ or FP8 tensor formats.

Trigger: Reach shared Linear loading with one of the sampled packed AWQ/GPTQ projections or `F8_E4M3` projections. The pinned 1.2B variants have the earlier pattern-construction barrier; the 32B configs supply a usable pattern.

Expected: Loading these published formats would require matching storage decoding, or an explicit format rejection before projection loading.

Actual: The AWQ/GPTQ names do not match either the EXL3 tensor group or the ordinary `.weight` probe for the sampled packed projection. FP8 matches the ordinary name but `convert_dtype` rejects the stored dtype before the inverse-scale read.

Locations: ff21ee46edb9ba74d709257f482c809a7bd406d0:exllamav3/modules/linear.py — Linear.load, ff21ee46edb9ba74d709257f482c809a7bd406d0:exllamav3/loader/safetensors.py — convert_dtype

Source evidence: call_7132326581ff46759be7728f1eecfb7b, call_4967aa3afc5e40a8815f9fbe83f5b31a, call_ddf15adea9064c329eada0e12067e89a, call_360b5540e5474d3b95ab850c4b6c7c67, call_de061e98d6b04517b0f07ac764b77ada, call_06898615cf07468b9429630446460ca4, call_97bd7a141b1f463485abcd8b907fcef5, call_8254cf5c6fcc482c881f92bdcbc1755c, call_95ecaea1ca644b619da785f5e7302d75, call_1007a6c6961544ba999d2ed1f9898804

source_inspection: Compared representative headers for both sizes with the two Linear storage probes and checked that `get_tensor` dispatches dtype before selecting the loading method. [call_7132326581ff46759be7728f1eecfb7b, call_ddf15adea9064c329eada0e12067e89a, call_06898615cf07468b9429630446460ca4, call_8254cf5c6fcc482c881f92bdcbc1755c, call_1007a6c6961544ba999d2ed1f9898804]. Limits: Representative header inspection, not loading or validation of an entire checkpoint. The commit does not promise those formats.

### kv-sampler-does-not-handle-exaone-branch-input (suspected; external_compatibility)

EXAONE gives the existing KV research sampler a concrete model layout with attention present and no attention pre-norm.

Trigger: Point `science/kv_quant_exp.py` at an EXAONE checkpoint that can construct and load, and reach a targeted layer on a sample-cache miss.

Expected: A sampler supporting this layout would use the same branch input, Q/K norms and optional RoPE as normal attention.

Actual: `sample_qkv` directly calls `module.attn_norm.forward`, which would fail on `None` before projections. It also does not reproduce the Q/K normalization and unconditionally calls `attn.rope.apply`, unlike EXAONE global attention.

Locations: ff21ee46edb9ba74d709257f482c809a7bd406d0:science/kv_quant_exp.py — sample_qkv

Source evidence: call_2b06397c57aa4898bb64796522959d21, call_c53aed5effdd4c4e9e1c18d5b6d2927f, call_5eaabcf92c094b00a446fce893b149ff, call_2c8af29868594cc7a5d2a597b6769958, call_4fa802e5dd18419195240a9fa2eb6b2f

source_inspection: Read the script's literal caller and targeted-layer branch and compared them with the new block and ordinary attention path. [call_2b06397c57aa4898bb64796522959d21, call_c53aed5effdd4c4e9e1c18d5b6d2927f, call_5eaabcf92c094b00a446fce893b149ff]. Limits: The script defaults to Llama; this does not assert its default fails or that ordinary EXAONE forward uses the sampler.

### inherited-prefill-flag-can-skip-exaone-residual-updates (suspected; defect)

EXAONE inherits the shared mutable-params prefill shortcut without clearing its flag in `prepare_inputs`.

Trigger: After EXAONE `Model.prefill` reaches its final cache-affecting block, reuse the same dictionary for ordinary forward with otherwise valid forward arguments.

Expected: Ordinary forward applies attention post-normalization, the residual updates and the MLP.

Actual: `prefill` remains true, so each reached attention block takes its early return and skips the residual updates and MLP. The new model changes neither the flag lifetime nor the return condition.

Locations: ff21ee46edb9ba74d709257f482c809a7bd406d0:exllamav3/models/model.py — Model.prefill, ff21ee46edb9ba74d709257f482c809a7bd406d0:exllamav3/modules/transformer.py — TransformerBlock.forward, 544ba423bf9c58c940dca6cb36a1aa93f6cda41a:exllamav3/models/exaone4.py — Exaone4Model.prepare_inputs

Source evidence: call_23da5b887b58442caf766d02d2866364, call_66567b2018ce499a8de8ce85d323e5c7, call_2c8af29868594cc7a5d2a597b6769958, call_5eaabcf92c094b00a446fce893b149ff

source_inspection: Traced the inherited prefill mutation through the unchanged forward dispatcher and the new input hook. [call_23da5b887b58442caf766d02d2866364, call_2c8af29868594cc7a5d2a597b6769958, call_5eaabcf92c094b00a446fce893b149ff]. Limits: Conditional direct-API dictionary reuse; the presence of generator and example prefill calls does not establish that they reuse the dictionary.

## Uncertainty and limits

The Python check executed the parent dictionary-reading helper with a transcription of the EXAONE schedule and dimension arithmetic. It did not instantiate the model, import PyTorch or FlashAttention, read tensor payloads, or test GPU inference, conversion, numerical parity or long-context quality.

Headers cover representative dense layers, head and embedding naming, and selected quantized projections; they are not an every-layer, every-shard audit. The config reads establish the supplied values, not reference-model behavior for a null window pattern or the author's reason for forcing the last layer global.

Literal caller searches do not cover external or dynamic consumers. The model prompt helper was not checked against a reference tokenizer or chat template.
