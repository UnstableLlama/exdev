# a5caa423bbd9d8a61266a88fb237c18fb77ec0b8


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/a5caa423bbd9d8a61266a88fb237c18fb77ec0b8) · [Evidence ledger](draft.json)

Registers Qwen3 MoE using normalized attention and routed experts, with all-expert calibration. Ordinary checkpoints match the inspected loader; published FP8/GPTQ formats do not. The inherited conditional all-expert fusion mismatch persists.

- [Qwen3 MoE assembly, checkpoint formats and calibration](#models)

## Problem

The parent registry has no Qwen3MoeForCausalLM mapping. The change adds configuration dispatch and a model builder, but architecture recognition does not imply support for every published checkpoint format. [source; call_5d3a4a9e4b73480495e890d0aedc5272, call_c8acbcd9188c4b83a837cfe962166888, call_66d5cd669ffb43ec9537b3f65dd5ed32]

## Reasoning

The builder follows Qwen3's normalized-attention assembly while replacing its dense gated MLP with the existing routed BlockSparseMLP. This reuses attention, loading and conversion mechanisms rather than introducing architecture-specific kernels. [source; call_026114a329984c96989dab5f64d014cf, call_6b02342d6630452fb3bcc5215c6277fd, call_8e055ad22ece43468677e2ff044020a1]

## Impact

The ordinary BF16 reference checkpoints match the inspected naming, dimensions and supported dtype conversion. The published FP8 variants encounter an unsupported dtype; GPTQ variants lack the weight names accepted by Linear. These are source-level compatibility conclusions, not completed loading tests. [source; call_e6c3af5517d74405b007af85164597e3, call_4c062278579043dab9f011f336ce65ac, call_76ecfc6d709c4251971cf2e098bd0b5e, call_32e16a05c3e945a0b5a835fc90c283db, call_75dcc671151544dd89abb8903eb41793, call_ace93ac624004e23b3862443b52fc171]

## Source Notes

Read ancestor entries 1db3dce and 6fc153d. The first explains Qwen3's explicit head dimensions and per-head Q/K normalization; the second establishes routed-MLP calibration and records the conditional all-expert fused-buffer mismatch. [ancestor; call_90e975c0cdd24df6beffe88798462a01, call_48c77bd348d64f808642d32791bc2bc4]

Issue #29, “Auto-YaRN for Qwen3? Maybe even set it dynamically?”, requests scaling automation; its connection is inferred from Qwen3 and RoPE configuration, not an explicit commit reference. The patch delegates RoPE settings to the existing helper. Issue #7, “quantizing model: undefined symbol: __cxa_call_terminate”, concerns extension import failure; #34, “torch._C._LinAlgError on last layer of quant”, concerns conversion factorization failure. Their inferred connection is shared config.py, linear.py and convert_model.py traceback context, not evidence that this architecture change addresses either error. PR #4, “chore: update config.py”, is a spelling correction. [inference; call_664a14c6d2c944859af329793ec486df, call_c4611b3acfbe415990b3a618aa15bee0, call_7fe6e21f8fd64a7298a9c13bf5e1b6c8, call_f52db93a46bc4f6494fb9605e8311f83, call_026114a329984c96989dab5f64d014cf]

<a id="models"></a>

## Qwen3 MoE assembly, checkpoint formats and calibration

Registration adds Qwen3MoeModel to the architecture comprehension and declares Qwen3MoeConfig.arch_string = Qwen3MoeForCausalLM. Config.from_directory can therefore choose the new configuration/model pair. The configuration accepts explicit head_dim, otherwise falling back to hidden_size // num_attention_heads; KV heads default to query heads, tying defaults to false, and supplied hidden_act and norm_topk_prob must be silu and true respectively. [source; call_c8acbcd9188c4b83a837cfe962166888, call_026114a329984c96989dab5f64d014cf, call_66d5cd669ffb43ec9537b3f65dd5ed32, call_6b908387837d467a99b397bbb68c3c6f]

The model builds embedding → sequential pre-normalized TransformerBlocks → final RMSNorm → vocabulary Linear. Each block adds attention to the residual, then normalizes that updated residual for the routed MLP. Q and K receive RMSNorm after reshaping into heads and before NEOX-style RoPE; V does not. Attention defaults remain full attention with unspecified softmax scale. prepare_inputs stores input_ids and delegates to prepare_for_attn, exactly as the eight inspected existing callers do; no caller-side guard is dropped. The helper defaults to uncached FlashAttention and retains its cached-mode parameter requirements. [source; call_026114a329984c96989dab5f64d014cf, call_56b18be17a03475da6e1922bfb8050e0, call_95d545f9d62a42d6a7ba8dcbde279a5a, call_b5c567ba735342339c807864b7e681a9, call_c397de4ce854433e9ba1f6f5526f98e6, call_5f275bf38b184da8a4fe3bb996a5462a]

All seven config.json files were read. Qwen/Qwen3-235B-A22B, its FP8 variant and its GPTQ-Int4 variant each specify hidden size 4096, 64 query heads, expert width 1536 and 94 layers. Qwen/Qwen3-30B-A3B, -Base, -FP8 and -GPTQ-Int4 each specify 2048, 32, 768 and 48 respectively. Every repository specifies head_dim=128, four KV heads, 128 experts, eight experts per token, silu, normalized top-k probabilities, RMS epsilon 1e-6, untied embeddings, vocabulary 151936 and rope_theta=1000000. These explicit values agree with the builder; its dimensional fallbacks are not used. [source; call_6b8f604172264a2990b74ff251878027, call_734095d8ad734768b4f040feb184893a, call_5655bc7ba6354b2c98659a152a13b0b1, call_e7fa356ae0724635b50252e4e5c76a11, call_bfe5361ba72d4ddc84bae04059c82106, call_7cf21e13582d425bb9ec856e2b4a87d7, call_fc322aa06f004b37851af54dfc1b79fe, call_026114a329984c96989dab5f64d014cf]

Other differing configuration values are intermediate_size=12288 versus 6144 and max_window_layers=94 versus 48; the new builder reads neither, using moe_intermediate_size and full attention instead. The 30B Base has eos_token_id=151643 and max_position_embeddings=32768, versus 151645 and 40960 elsewhere; base Config reads EOS and the RoPE helper reads the position limit. GPTQ configurations change torch_dtype to float16 and transformers_version to 4.51.3 versus bfloat16 and 4.51.0; the builder does not use these fields. Quantization metadata also differs: FP8 declares dynamic e4m3 blocks of 128×128 and exclusions, while GPTQ declares four-bit, group-size-128 packing with differing metadata layouts. Neither selects a new loading path here. [source; call_6b8f604172264a2990b74ff251878027, call_734095d8ad734768b4f040feb184893a, call_5655bc7ba6354b2c98659a152a13b0b1, call_e7fa356ae0724635b50252e4e5c76a11, call_bfe5361ba72d4ddc84bae04059c82106, call_7cf21e13582d425bb9ec856e2b4a87d7, call_fc322aa06f004b37851af54dfc1b79fe, call_66d5cd669ffb43ec9537b3f65dd5ed32, call_e6c3af5517d74405b007af85164597e3]

A scalar dimension check gives Q widths 4096/8192 for the 30B/235B configurations, KV width 512 for both and eight/sixteen query heads per KV head. The fallback head dimension would be 64, not the configured 128: retaining head_dim is essential because attention width is twice residual width. These dimensions are multiples of Linear's 128-element padding unit. [execution; call_5f275bf38b184da8a4fe3bb996a5462a]

Exact layer-zero Linear prefixes are model.layers.0.self_attn.{q_proj,k_proj,v_proj,o_proj}, model.layers.0.mlp.gate, and model.layers.0.mlp.experts.0.{gate_proj,up_proj,down_proj}; the expert pattern repeats through 127. For every prefix P, Linear first tests EXL3 groups P.{sv|svh}, P.{su|suh}, P.trellis. If present it requests .scale, .su, .suh, .sv, .svh and .bias optionally, and .trellis obligatorily. Otherwise it tests P.weight and requests that tensor transposed with float2half=True, plus optional P.bias. No fused-QKV alternative is configured. SafetensorsCollection group tests append dots literally; has_tensor performs an exact-key lookup. [source; call_026114a329984c96989dab5f64d014cf, call_95d545f9d62a42d6a7ba8dcbde279a5a, call_8e055ad22ece43468677e2ff044020a1, call_e6c3af5517d74405b007af85164597e3, call_4c062278579043dab9f011f336ce65ac]

Ordinary storage comprises Qwen3-235B-A22B, Qwen3-30B-A3B and Qwen3-30B-A3B-Base. In the 30B header, model.layers.0.self_attn.q_proj.weight is BF16 [4096,2048], model.layers.0.mlp.gate.weight is BF16 [128,2048], and expert-zero gate_proj.weight/up_proj.weight/down_proj.weight are BF16 [768,2048]/[768,2048]/[2048,768]. The 235B counterparts are BF16 [8192,4096], [128,4096], [1536,4096]/[1536,4096]/[4096,1536]. The Base attention/router header matches 30B. These .weight names select load_fp16; BF16 is supported and converted to half. The sampled modules supply neither biases nor EXL3 groups. No format-specific auxiliary tensor is identified as unused in these ordinary samples. [source; call_76ecfc6d709c4251971cf2e098bd0b5e, call_c015519c2d214748858c154a8e326e09, call_32e16a05c3e945a0b5a835fc90c283db, call_74766012e7fc43ffa26ba5b3ad3d5cb1, call_e6c3af5517d74405b007af85164597e3, call_4c062278579043dab9f011f336ce65ac]

FP8 storage comprises both -FP8 repositories. Their attention/expert prefixes retain .weight with the same matrix shapes as ordinary storage, but dtype F8_E4M3. Each adds .weight_scale_inv in F32: for 30B Q [32,16], expert gate/up [6,16], down [16,6]; for 235B Q [64,32], gate/up [12,32], down [32,12]. Router .gate.weight remains F32 [128,2048] or [128,4096]. Linear can convert the router's F32 through float2half, but convert_dtype rejects F8_E4M3 before weight conversion. All inspected weight_scale_inv tensors are never requested by this loader; the FP8 block-size metadata does not cause dequantization. [source; call_75dcc671151544dd89abb8903eb41793, call_8b2139cdf18d4cdbb29d429520612e57, call_2d55be4037a64aef8bdb88e2ab5efd9f, call_a0fd4b39eff14e6dac9f034ae3a3251c, call_e6c3af5517d74405b007af85164597e3, call_4c062278579043dab9f011f336ce65ac]

GPTQ storage comprises both -GPTQ-Int4 repositories. For 30B, Q stores .g_idx I32 [2048], .qweight I32 [256,4096], .qzeros I32 [16,512], .scales F16 [16,4096]. Expert-zero gate/up each store [2048], [256,768], [16,96], [16,768] with those respective suffixes/dtypes; down stores [768], [96,2048], [6,256], [6,2048]. Router .gate.weight is F16 [128,2048]. For 235B, Q's corresponding shapes are [4096], [512,8192], [32,1024], [32,8192]; gate/up are [4096], [512,1536], [32,192], [32,1536]; down is [1536], [192,4096], [12,512], [12,4096]; router is F16 [128,4096]. These integer/F16 dtypes are recognized by the collection, but Linear never requests these GPTQ suffixes. Neither .weight nor the EXL3 group exists for these sampled quantized projections, so Linear.load raises its unsupported-format ValueError. The router independently matches the ordinary F16 path. [source; call_ace93ac624004e23b3862443b52fc171, call_4d3654ff40db4a2ba7dced0319fb6386, call_cbef9fd5708c4756ad279c6b9f9ed3a8, call_4d2321b4429a40d1980715b0f8ce4adc, call_e6c3af5517d74405b007af85164597e3, call_4c062278579043dab9f011f336ce65ac]

Module.load traverses registered submodules in order; Attention registers Q first. Consequently the inspected ordinary load path accepts embedding and normalization weights and selects load_fp16 for Q. FP8 reaches Q's get_tensor and raises ValueError('Unknown dtype F8_E4M3'); GPTQ reaches Q's Linear.load and raises 'No tensors found for model.layers.0.self_attn.q_proj matching supported quantization format.' Thus the three ordinary variants are source-compatible with this path, while the four published quantized variants cannot complete it as written, assuming earlier device/file operations succeed. Neither failure is established by repository execution. [source; call_46be777cc0484a8ca1c4b99eef6a8b5f, call_95d545f9d62a42d6a7ba8dcbde279a5a, call_e6c3af5517d74405b007af85164597e3, call_4c062278579043dab9f011f336ce65ac, call_98922d18a95645cd8c80e7941556809c, call_b5c567ba735342339c807864b7e681a9]

The head condition probes bare lm_head, whereas every inspected head header stores lm_head.weight: BF16 in the three ordinary repositories, F32 in the two FP8 repositories and F16 in the two GPTQ repositories, shaped [151936,2048] or [151936,4096]. An exact lookup for the bare name does not match those stored names. All seven configurations set tie_word_embeddings=false, so short-circuit evaluation actually skips the probe and no alternate key is assigned. Linear would load lm_head.weight, with BF16/F32 converted to half; the earlier quantized-projection failures prevent reaching it during a complete load. Embedding and RMSNorm likewise append .weight and request float2half=True. [source; call_026114a329984c96989dab5f64d014cf, call_4c062278579043dab9f011f336ce65ac, call_e6c3af5517d74405b007af85164597e3, call_1369de78c93342409ca4685d83c5404e, call_504c4aa1a8294254baa20d375a58acf1, call_5406e93945aa48a0b4022ccde9e6239c, call_397d5a4aa61648c2935b65f7b05b9c39, call_291276dc724549f794e9306ec8245315, call_ace93ac624004e23b3862443b52fc171, call_76a50afbbf184ee890fa806d9051533f, call_98922d18a95645cd8c80e7941556809c, call_b5c567ba735342339c807864b7e681a9]

Routing computes softmax over 128 router scores, selects eight experts and renormalizes selected probabilities. Each expert computes down(silu(gate(x)) × up(x)); weighted outputs accumulate into token order. The builder requests half intermediate values and float MLP output. Multiple flattened tokens or non-EXL3 experts take the ordinary grouping path. One token with all expert projections EXL3 takes indexed multi-GEMM; MultiLinear additionally requires equal dimensions/bit widths within each projection group, no biases or softcaps and unit post-scale. Gate/up/down are separate calls, routing weights apply only to down, and -1 leaves kernel-shape selection automatic. Published GPTQ and FP8 storage are not EXL3 fusion formats. [source; call_026114a329984c96989dab5f64d014cf, call_8e055ad22ece43468677e2ff044020a1, call_ca866a9a29a14f8bbfdb1654f6622bc2]

Calibration labels are block.attn.input for Q/K/V, block.attn.o for O, no label for the router, block.mlp.input shared by every expert gate/up, and block.mlp.{expert_idx}.down separately for each down projection. The head uses block. Linear.capture_H accumulates XᵀX only for the first key sharing a label. Activating every expert makes gate/up share the normalized MLP input and supplies every down projection its own activated expert input. This is why the builder's calibration_all_experts=True complements the expert-map construction rather than being an independent inference option. Conversion captures with that flag, then recomputes reference outputs and advances states with ordinary top-eight routing. The router has no calibration map and is excluded from the mapped Linear conversion list. [source; call_026114a329984c96989dab5f64d014cf, call_95d545f9d62a42d6a7ba8dcbde279a5a, call_8e055ad22ece43468677e2ff044020a1, call_e6c3af5517d74405b007af85164597e3, call_4ec08f899de3456785a2e23146aaed64]

The ancestor's all-expert fusion observation persists unchanged: the new builder enables all-expert calibration but does not modify BlockSparseMLP's dispatch or buffer sizes. Whole-parent searches found no existing architecture construction of BlockSparseMLP; TransformerBlock.forward is the new builder's direct forwarding path, while conversion supplies the flag. Ordinary unquantized calibration avoids the fused branch because its experts are not EXL3, so the conditional defect is not evidence that normal initial conversion fails. [source; call_026114a329984c96989dab5f64d014cf, call_c1b45e6c2976436c9b9dc4839a2550ad, call_da29fee6d9024c84afff70c0aa246f8a, call_56b18be17a03475da6e1922bfb8050e0, call_8e055ad22ece43468677e2ff044020a1, call_4ec08f899de3456785a2e23146aaed64]

## Authoring-time findings — pending review

### published-fp8-load (suspected; external_compatibility)

Architecture registration does not provide a loader for the two published FP8 variants.

Trigger: Load either reference -FP8 checkpoint through the new model builder and ordinary SafetensorsCollection.

Expected: A compatible loading path would decode FP8 weights using their scale tensors.

Actual: Q's .weight passes name detection, but get_tensor calls convert_dtype, which raises ValueError('Unknown dtype F8_E4M3'). The .weight_scale_inv tensors are not requested.

Locations: a5caa423bbd9d8a61266a88fb237c18fb77ec0b8:exllamav3/models/qwen3_moe.py — Qwen3MoeModel.__init__, c6aa83f7e5a5e735c079d41244cbc704eda7e54e:exllamav3/loader/safetensors.py — convert_dtype

Source evidence: call_026114a329984c96989dab5f64d014cf, call_8b2139cdf18d4cdbb29d429520612e57, call_a0fd4b39eff14e6dac9f034ae3a3251c, call_e6c3af5517d74405b007af85164597e3, call_4c062278579043dab9f011f336ce65ac

source_inspection: Compared both FP8 configurations and layer-zero headers with Attention registration order, Linear.load_fp16 and collection dtype conversion. [call_734095d8ad734768b4f040feb184893a, call_7cf21e13582d425bb9ec856e2b4a87d7, call_95d545f9d62a42d6a7ba8dcbde279a5a, call_4c062278579043dab9f011f336ce65ac]. Limits: No actual load; preceding device and filesystem operations must succeed to reach this error.

### published-gptq-load (suspected; external_compatibility)

The two published GPTQ variants store names that Linear.load does not consume.

Trigger: Load either reference -GPTQ-Int4 checkpoint through Qwen3MoeModel.

Expected: A compatible loader would recognize and decode GPTQ's qweight, qzeros, scales and g_idx.

Actual: Neither the EXL3 group nor q_proj.weight matches; the first attention Linear raises 'No tensors found for model.layers.0.self_attn.q_proj matching supported quantization format.' All sampled GPTQ projection auxiliaries remain unread, although their dtypes are recognized.

Locations: a5caa423bbd9d8a61266a88fb237c18fb77ec0b8:exllamav3/models/qwen3_moe.py — Qwen3MoeModel.__init__, c6aa83f7e5a5e735c079d41244cbc704eda7e54e:exllamav3/modules/linear.py — Linear.load

Source evidence: call_026114a329984c96989dab5f64d014cf, call_4d3654ff40db4a2ba7dced0319fb6386, call_4d2321b4429a40d1980715b0f8ce4adc, call_e6c3af5517d74405b007af85164597e3

source_inspection: Compared both reference GPTQ header layouts against supported name groups and the first registered attention projection. [call_95d545f9d62a42d6a7ba8dcbde279a5a, call_e6c3af5517d74405b007af85164597e3, call_4d3654ff40db4a2ba7dced0319fb6386, call_4d2321b4429a40d1980715b0f8ce4adc]. Limits: Source-level failure path, not execution; no claim of GPTQ support was explicitly made by the commit message.

### inherited-all-expert-fusion (suspected; defect)

All-expert routing still conflicts with the fused path's top-eight-sized output buffers.

Trigger: Forward one flattened token through a fully EXL3 Qwen3 MoE block with activate_all_experts=True.

Expected: Evaluate all 128 experts or use the ordinary all-expert-capable path.

Actual: Routing yields 128 indices, but fused buffers retain eight expert slots; the first exl3_mgemm fails its indices-dimension versus C-dimension check. TransformerBlock forwards params unchanged. Initial unquantized calibration does not take this fused branch.

Locations: c6aa83f7e5a5e735c079d41244cbc704eda7e54e:exllamav3/modules/block_sparse_mlp.py — BlockSparseMLP.forward, a5caa423bbd9d8a61266a88fb237c18fb77ec0b8:exllamav3/models/qwen3_moe.py — Qwen3MoeModel.__init__

Source evidence: call_8e055ad22ece43468677e2ff044020a1, call_ca866a9a29a14f8bbfdb1654f6622bc2, call_56b18be17a03475da6e1922bfb8050e0, call_026114a329984c96989dab5f64d014cf, call_da29fee6d9024c84afff70c0aa246f8a

source_inspection: Rechecked the ancestor observation against unchanged parent implementation, the new builder and conversion's flag preparation. [call_48c77bd348d64f808642d32791bc2bc4, call_8e055ad22ece43468677e2ff044020a1, call_4ec08f899de3456785a2e23146aaed64, call_ca866a9a29a14f8bbfdb1654f6622bc2]. Limits: Conditional API reach, not proof that normal conversion or generation triggers it.

scalar_transcription: Computed 128 all-expert indices versus eight fused expert slots for the reference configurations. [call_5f275bf38b184da8a4fe3bb996a5462a]. Limits: Integer cardinality model only; no repository forward or kernel execution.

## Uncertainty and limits

No checkpoint payloads, model loading, generation, conversion or CUDA kernels were executed. Header compatibility does not establish numerical correctness, resource sufficiency or performance.

Header inspection sampled layer-zero modules and head tensors, not every tensor in every shard. Claims about unused format-specific tensors describe the inspected loader's requests, not a complete checkpoint inventory.

The standard-library computation checks transcribed dimensions and routing cardinality only; it does not emulate tensor arithmetic, floating-point precision or GPU execution.
