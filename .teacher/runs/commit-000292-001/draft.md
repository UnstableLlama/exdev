# 47d83f567ccc93633d70354f93f153dad6266812


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/47d83f567ccc93633d70354f93f153dad6266812) · [Evidence ledger](draft.json)

Supplies the previously referenced Ernie 4.5 dense and MoE text-model implementations. Reference configurations support the structural mapping; prompt formatting and inherited sparse export/fusion limitations remain.

- [Ernie 4.5 text-model assembly and inherited runtime contracts](#models)

## Problem

The parent registry already names Ernie models, but their implementation files are missing. This change supplies dense and MoE text-model configurations and builders. [source; call_d46eff2cd2a5424f959df0c0798892ff, call_0fa8934292154046a1ec6208da0da370, call_9a65015b9bd84d9c9b800ddd9260aabb]

## Reasoning

Both implementations assemble existing transformer components rather than introducing kernels. The MoE builder combines an initial dense prefix with routed experts and optional shared experts. [source; call_0fa8934292154046a1ec6208da0da370, call_9a65015b9bd84d9c9b800ddd9260aabb]

## Impact

The added files satisfy the registry's missing relative imports and provide the configuration classes selected by Config.from_directory. Successful importing, loading and inference were not executed. [source; call_d46eff2cd2a5424f959df0c0798892ff, call_5eff207f97f74e7fbef2fe09fb154db9, call_0fa8934292154046a1ec6208da0da370, call_9a65015b9bd84d9c9b800ddd9260aabb]

## Source Notes

Read the Dots1 introduction and BlockSparseMLP refactor entries. They establish the closely followed dense/routed/shared assembly, explicit router selection, missing Ernie files, custom-bias export mismatch and conditional fused-path limitations. [ancestor; call_5cab33d840314261a9e73a739a58b290, call_b4fe3a8d46f44b3eb8c705cab3b58e97]

The connection to issue #51, “dots.llm1 support,” is inferred from the closely followed Dots1 builder. That discussion requests Dots support and reports a Dots-specific first-output-projection workaround; it does not establish that Ernie needs that workaround. [inference; call_127f319c5ea247d19bd11afec8f3142a, call_07399c735468417fbc0d51bb0df8d91d, call_9a65015b9bd84d9c9b800ddd9260aabb]

Other inspected discussions are background, not established motivation: #7, “quantizing model: undefined symbol: __cxa_call_terminate,” concerns native-extension loading; PR #4, “chore: update config.py,” corrects spelling; PR #26, “Superior 3INST parameters,” discusses decoder parameters. Their inferred connections are shared configuration/import or conversion code, not Ernie-specific failures. [inference; call_15ad9be107b1472180ab75a7fe76795e, call_b55a564f6a044540b68932e15368e37d, call_25f795ef7e364dd4b8d5ea759d0454b2, call_5a9be9d97a7746f1bc385b76fbb52d17, call_5eff207f97f74e7fbef2fe09fb154db9, call_b4b57bb36619424aa4d937dff5057039]

The inspected reports #33, “Error converting model,” #34, “torch._C._LinAlgError on last layer of quant,” #42, “converting to 3.0 bpw causes error; block state has 0 inf values and 34 NaN values,” #52, “Error converting moonshotai/Kimi-Dev-72B,” and #58, “linalg.cholesky error converting OpenBuddy (Qwen3) 32B QAT,” concern other models' conversion failures. Their inferred association is the shared convert_model.py traceback path, not evidence that this change fixes them. [inference; call_7d208701710d42ec9531b85d9b9cb3ce, call_acb93a050c2a40e2861b61d8d07e2182, call_e632ee0f6fc94eb8a83c5cc624eefa41, call_e247cb823b4a431ba2361203a8fea6b1, call_3d56c96e32194c3a9dd546bcc9d83bcb, call_b4b57bb36619424aa4d937dff5057039]

Issue #53, “Command A support,” requests another architecture's quantized models; #55, “Possible GLM4 32B regression,” reports a loading TypeError; #48, “`RuntimeError` when requesting logprobs with Gemma 3 models,” reports vocabulary-padding disagreement. Connections to this task are inferred only through shared conversion, MLP or model files inspected here. [inference; call_e2addede09bb409dbd7228d3eda8630d, call_800ef6eb3d974a5dbb04eb5dfddbaddd, call_f17652d6b5d2480aac82dbf6c1f69647, call_232994da25b041f79c8f301fff0f8dee, call_2589bbb14fff410f8ad785c710e012af]

<a id="models"></a>

## Ernie 4.5 text-model assembly and inherited runtime contracts

Ernie4_5Config identifies Ernie4_5_ForCausalLM; Ernie4_5MoEConfig identifies Ernie4_5_MoeForCausalLM. Both expose only a text model. The existing registry imports these exact classes, and Config.from_directory imports that registry before selecting any architecture. Supplying both files removes the missing-module condition recorded by the earlier refactor, whose reach was therefore broader than Ernie alone. [source; call_0fa8934292154046a1ec6208da0da370, call_9a65015b9bd84d9c9b800ddd9260aabb, call_d46eff2cd2a5424f959df0c0798892ff, call_5eff207f97f74e7fbef2fe09fb154db9, call_53e33c7fe443401d94f9bb763605e718]

Both configurations accept an explicit head_dim, otherwise deriving hidden_size // num_attention_heads; KV heads default to query heads. Supplied hidden_act must be silu. Hidden size, intermediate width, layer count and RMS epsilon are required; embedding tying defaults false. Both request GPTJ RoPE through the existing settings reader, which reads theta, scaling, rotary fraction and position limits. [source; call_0fa8934292154046a1ec6208da0da370, call_9a65015b9bd84d9c9b800ddd9260aabb, call_5eff207f97f74e7fbef2fe09fb154db9]

The pipeline is embedding → pre-normalized TransformerBlocks → final RMSNorm → vocabulary Linear. TransformerBlock adds attention to the residual before normalizing for the MLP and adding its output. Embedding defaults to FP32 output; both builders request FP16 gated intermediates, FP32 MLP down outputs and FP16 final normalization. Attention uses separate q_proj/k_proj/v_proj/o_proj names without Q/K normalization. [source; call_0fa8934292154046a1ec6208da0da370, call_9a65015b9bd84d9c9b800ddd9260aabb, call_621b63f49188430798fe2427c378a872, call_c84c4260ad574b9cb2840101bd1a3f4d, call_d25673fe05b64e3898c774056da9a771, call_232994da25b041f79c8f301fff0f8dee]

The MoE mapping reads moe_num_experts, moe_k, moe_intermediate_size and moe_num_shared_experts. moe_layer_start_index defaults zero and defines the dense-prefix boundary: idx below it uses GatedMLP, all later layers use BlockSparseMLP. A supplied moe_layer_interval must equal one, so interleaved sparse layers are rejected rather than implemented. Shared experts default to zero; a positive count creates one combined GatedMLP of width expert_width × count. [source; call_9a65015b9bd84d9c9b800ddd9260aabb, call_27d1237f87a14c328ae8a863aa72c417, call_07399c735468417fbc0d51bb0df8d91d, call_30c7b0cb8d804011ad4b48dba85e044f]

Ernie omits router_type and therefore selects routing_std, unlike Dots1's explicit dots route. Mixtral and Qwen3 MoE also use the standard default. routing_std selects top-k router logits and softmax-normalizes the selected values; one token reuses buffers unless all-expert activation is requested. Ernie supplies scale 1.0 and single-group values, but this selected helper uses neither those values nor the optionally loaded moe_statics.e_score_correction_bias. The supplied moe_gate_act assertion permits only softmax when present. [source; call_9a65015b9bd84d9c9b800ddd9260aabb, call_c3967061bf19417081b20e0328f9045d, call_07399c735468417fbc0d51bb0df8d91d, call_20a740e00cb8485684a3b26810128f0f, call_30c7b0cb8d804011ad4b48dba85e044f, call_dc1aed38ab22428a971d2f95171eb0ea]

Each routed expert computes down(silu(gate(x)) × up(x)); selected outputs are weighted and accumulated, then shared output is added without routing weights. Multiple flattened tokens or non-EXL3 experts use ordinary expert evaluation. One token with fully EXL3 experts uses the inherited fused path. The shared GatedMLP supplies the gates/ups/downs lists that TransformerBlock.allocate_q consumes. [source; call_c3967061bf19417081b20e0328f9045d, call_232994da25b041f79c8f301fff0f8dee, call_621b63f49188430798fe2427c378a872, call_9a65015b9bd84d9c9b800ddd9260aabb]

All four dense configs were read: baidu/ERNIE-4.5-0.3B-Base-PT, -Base-Paddle, -PT and -Paddle. Each matches the dense architecture string and specifies hidden size 1024, explicit head_dim 128, 16 query heads, two KV heads, 18 layers, MLP width 3072 and tied embeddings. Thus none uses the head-dimension fallback, which would instead yield 64. All specify vocabulary 103424, RMS epsilon 1e-5, theta 500000 and position limit 131072. [source; call_0d0b95e7257c406297331acdba21f256, call_610b0ab2ee0e4dbcb02a469f17228478, call_488af759c5bc43a59125aff6971406d3, call_96309f3274fb496fb2d1859dbfe824ad, call_0fa8934292154046a1ec6208da0da370]

All four 21B configs were read: baidu/ERNIE-4.5-21B-A3B-Base-PT, -Base-Paddle, -PT and -Paddle. Each matches the MoE architecture and maps to hidden size 2560, 20 query/four KV heads, 28 layers, dense width 12288, expert width 1536, 64 routed experts, six selected experts and two shared experts. Each overrides the dense-prefix default to one and interval to one, enables tying and omits head_dim and moe_gate_act. The instruction variants additionally declare next-token prediction layers, which this builder does not assemble. [source; call_5ef4b05612494c6297b451498a531d9b, call_d928b3578eaf40c5ae45da15a9cca605, call_5d07abe8fbb4484884f2d7d95a6189b4, call_7ad17b1e6cb84635984ae59f39aa24cb, call_9a65015b9bd84d9c9b800ddd9260aabb]

The 300B configs were read individually: baidu/ERNIE-4.5-300B-A47B-Base-PT, -Base-Paddle, -PT, -Paddle, -2Bits-Paddle, -FP8-Paddle and -W4A8C8-TP4-Paddle. Each matches the MoE architecture and the same structural mapping: hidden size 8192, 64 query/eight KV heads, 54 layers, dense width 28672, expert width 3584, 64 experts and eight selected experts. Each sets a three-layer dense prefix, interval one and untied embeddings; each omits head_dim and shared-expert count, selecting derived dimension 128 and no shared branch. The three quantized Paddle configs declare distinct quantization schemes that these constructors do not translate. [source; call_5755ca838b034995bfd12e0739779192, call_c1dbad515a8c4781ad304090d741e411, call_be2f2b2f8a2d4464a8ba84bdba420536, call_4931f347690142c4ab819fe016ca7679, call_7a18fb3a477a41108cb181e5ccfaa6ae, call_ecdf4f33b54a4e2dbd3354fc2de1264c, call_2194b36bee9b44c099f8561729c34e9c, call_9a65015b9bd84d9c9b800ddd9260aabb]

A bounded integer transcription calculated query/KV widths of 2048/256 for 0.3B, 2560/512 for 21B and 8192/1024 for 300B. It also calculated 27 sparse blocks and shared width 3072 for 21B, versus 51 sparse blocks and no shared branch for 300B. These calculations do not execute model components. [execution; call_2589bbb14fff410f8ad785c710e012af]

The complete 0.3B-Base-PT header matches all ordinary dense tensor names and orientations: embedding [103424,1024], query [2048,1024], key/value [256,1024], output [1024,2048], gate/up [3072,1024], down [1024,3072] and norms [1024]. lm_head.weight is absent, so the embedding alternate supplies the head. No bias, weight_scale_inv or EXL3 groups appear in that header; Linear consequently takes its ordinary weight path rather than EXL3 loading. [source; call_fd4d4d17ddc949b3b32b6592a01bf81e, call_7008fd35620d4bbf8297b2b1ef9d969d, call_0fa8934292154046a1ec6208da0da370, call_7d42836d5a514e2f9050fdce2d29be90]

21B-Base-PT samples match embedding/head [103424,2560], dense gate/up [12288,2560], dense down [2560,12288], expert gate/up [1536,2560], expert down [2560,1536], router [64,2560], shared gate/up [3072,2560], shared down [2560,3072] and final norm [2560]. Its correction tensor exists under the requested moe_statics suffix with shape [1,64]. 300B-Base-PT samples match dense gate/up [28672,8192], down [8192,28672], expert gate/up [3584,8192], expert down [8192,3584] and router [64,8192]; its correction tensor also has shape [1,64]. The standard router never reads these stored correction tensors. [source; call_cd8dd6013b5749029d8e5ffe424cdabe, call_638f1c309982496f879d9de06b75a607, call_1dfa0cbfa00a4123919cd6d9fd1a37f9, call_3e364e62b17f432d8a9ef12ab95f6a51, call_98217a8919034285a070d7c86a080aba, call_66f79ff9386349178801cf051e29cb73, call_c3967061bf19417081b20e0328f9045d]

Paddle header samples demonstrate why matching config dimensions alone is insufficient: 0.3B-Base-Paddle uses ernie.* names, fused qkv_proj and up_gate_proj, and transposed projection orientations. The 300B 2Bits, FP8 and W4A8C8-TP4 samples use ernie.*.quant_weight and weight_scale forms; the TP4 sample is rank-partitioned. These are not the model.* separate projections or EXL3 groups requested by the added builders and Linear loader. [source; call_e2f0a80f659c4fe6869ee6660d5c323d, call_842a715503c849158983c388d5691cca, call_bb0eaedd0654466f865dc2a2666f803b, call_c12ad4c9615647aaa623985b72dede99, call_7008fd35620d4bbf8297b2b1ef9d969d, call_9a65015b9bd84d9c9b800ddd9260aabb]

prepare_inputs stores input_ids and delegates to prepare_for_attn. Inspection of all thirteen existing literal caller sites found the same argument preparation and no additional caller-side guards. The helper retains its own uncached-mode cache rejection and cached-mode shape requirements. Ernie's new calls therefore do not bypass a guard present at those existing sites. [source; call_74440ea0880d48b9b3dbb4590fa909a0, call_2589bbb14fff410f8ad785c710e012af, call_d25673fe05b64e3898c774056da9a771, call_0fa8934292154046a1ec6208da0da370, call_9a65015b9bd84d9c9b800ddd9260aabb]

Ernie MoE enables calibration_all_experts. Conversion passes that flag during Hessian capture so every expert down projection receives data, then recomputes reference states without it. This follows Dots1 and Qwen3 MoE rather than changing ordinary inference routing. The custom-bias export mismatch and conditional fused-buffer/result contracts recorded by ancestors remain unchanged in the reused implementation. [source; call_9a65015b9bd84d9c9b800ddd9260aabb, call_8a5b6f86225d4b688d4feaf7ee82a2a3, call_07399c735468417fbc0d51bb0df8d91d, call_30c7b0cb8d804011ad4b48dba85e044f, call_c3967061bf19417081b20e0328f9045d]

## Authoring-time findings — pending review

### ernie-chat-template-mismatch (suspected; external_compatibility)

Both convenience formatters emit ChatML rather than the inspected Ernie instruction templates.

Trigger: Call default_chat_prompt for ERNIE-4.5-0.3B-PT or ERNIE-4.5-21B-A3B-PT.

Expected: Match the checkpoint template's begin-of-sentence marker, User:/Assistant: labels and assistant generation prefix.

Actual: The new methods emit im_start/im_end blocks. Whole-parent search found only a direct caller in the vision-only imgsearch example, not evidence that normal text generation calls this helper. The inherited Dots formatter mismatch is therefore carried into new methods, with Ernie-specific expected formatting.

Locations: 47d83f567ccc93633d70354f93f153dad6266812:exllamav3/models/ernie4_5.py — Ernie4_5Model.default_chat_prompt, 47d83f567ccc93633d70354f93f153dad6266812:exllamav3/models/ernie4_5_moe.py — Ernie4_5MoEModel.default_chat_prompt

Source evidence: call_0fa8934292154046a1ec6208da0da370, call_9a65015b9bd84d9c9b800ddd9260aabb, call_1810efe059a0479f862cf785e9122986, call_1179c13a6c514bf4bf46f7cc2c7ba329, call_e1425c5c93994ebdbe26126715adb039, call_b04570176d1e4c12904365e8fc0b9d99

source_inspection: Compared both added formatters with pinned tokenizer templates and inspected the located direct caller. [call_1810efe059a0479f862cf785e9122986, call_1179c13a6c514bf4bf46f7cc2c7ba329, call_b04570176d1e4c12904365e8fc0b9d99]. Limits: No generation test; external caller reach is unknown.

### ernie-custom-bias-export (suspected; defect)

Ernie exercises the inherited disagreement between custom correction-bias lookup and export naming.

Trigger: Load a present moe_statics.e_score_correction_bias and export the sparse module through get_tensors, including conversion's tensor collection.

Expected: Preserve the configured correction-bias tensor name for reload.

Actual: load requests <mlp>.moe_statics.e_score_correction_bias, but get_tensors emits <mlp>.gate.e_score_correction_bias. Conversion collects those tensors and reloads modules from the resulting dictionary. Ernie's optional custom lookup then loses the tensor; its current standard routing ignores the bias, so a routing-output change is not established.

Locations: 47d83f567ccc93633d70354f93f153dad6266812:exllamav3/models/ernie4_5_moe.py — Ernie4_5MoEModel.__init__, e1484296dd5878d85f782d4b9b36c2917cf2dbcb:exllamav3/modules/block_sparse_mlp.py — BlockSparseMLP.get_tensors

Source evidence: call_9a65015b9bd84d9c9b800ddd9260aabb, call_c3967061bf19417081b20e0328f9045d, call_d87b584e0cbb4e0a97e3c47be9a7598b, call_b4b57bb36619424aa4d937dff5057039, call_638f1c309982496f879d9de06b75a607

source_inspection: Traced configured lookup, hard-coded export suffix and conversion's collection/reload sequence. [call_c3967061bf19417081b20e0328f9045d, call_b4b57bb36619424aa4d937dff5057039]. Limits: No serialization round trip was executed.

### ernie-inherited-all-expert-fusion (suspected; defect)

All-expert routing retains selected-expert-sized fused buffers.

Trigger: One flattened token through fully EXL3 Ernie experts with activate_all_experts=True.

Expected: Evaluate all experts with compatible storage or select the ordinary path.

Actual: routing_std returns 64 expert indices, but load allocates six planes for the inspected 21B configs or eight for 300B. Dispatch still selects fusion, whose first exl3_mgemm checks index count against output planes. TransformerBlock forwards params directly. Initial unquantized calibration avoids fusion, so this does not establish failure of ordinary initial conversion.

Locations: e1484296dd5878d85f782d4b9b36c2917cf2dbcb:exllamav3/modules/block_sparse_mlp.py — BlockSparseMLP.forward

Source evidence: call_c3967061bf19417081b20e0328f9045d, call_a85535df047f4b33a958d3fc3d085590, call_621b63f49188430798fe2427c378a872, call_df02642fab344346a556674958a8c689, call_8a5b6f86225d4b688d4feaf7ee82a2a3

scalar_transcription: Calculated 64 all-expert indices versus six or eight allocated fused planes. [call_2589bbb14fff410f8ad785c710e012af]. Limits: Integer shape arithmetic, not extension or GPU execution.

### ernie-inherited-fused-result-contract (suspected; behavior_change)

The reused fused sparse path returns workspace-backed storage and ignores a per-call dtype override.

Trigger: Retain a fused sparse result across another fused call, or request an out_dtype different from the allocated output dtype.

Expected: An independent result honoring the override, consistent with the ordinary path.

Actual: The fused return is a view of cfg.out_d without the ordinary path's to2 conversion. Another call reuses that storage. The located TransformerBlock caller immediately adds the result and supplies no override, so that caller does not demonstrate either incompatibility.

Locations: e1484296dd5878d85f782d4b9b36c2917cf2dbcb:exllamav3/modules/block_sparse_mlp.py — BlockSparseMLP.forward

Source evidence: call_c3967061bf19417081b20e0328f9045d, call_a85535df047f4b33a958d3fc3d085590, call_621b63f49188430798fe2427c378a872

source_inspection: Compared ordinary and fused returns with the decoder call sites. [call_c3967061bf19417081b20e0328f9045d, call_621b63f49188430798fe2427c378a872]. Limits: No tensor lifetime or dtype test.

## Uncertainty and limits

No repository import, checkpoint load, conversion, generation or CUDA kernel was executed. The Python calculation checks integer dimensions only.

Checkpoint headers were sampled for representative layouts, not exhaustively across every layer, shard or variant. Optional bias, scale and EXL3 suffix presence is established only where explicitly inspected.

Matching architecture strings and configuration dimensions does not establish direct Paddle checkpoint compatibility; sampled Paddle tensors use different prefixes, fused projections, orientations or quantized representations.

The intended inference role of Ernie's correction-bias tensors is not established by the available configurations. Source inspection establishes that the selected standard router ignores them, not whether that matches the reference implementation.

Prompt-template disagreement was inspected for the 0.3B-PT and 21B-A3B-PT checkpoints; generation-quality consequences and other variants' templates were not tested.
