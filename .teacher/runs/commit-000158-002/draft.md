# 9665ba99989955593d2fb148323c9a96c77d1bea


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/9665ba99989955593d2fb148323c9a96c77d1bea) · [Evidence ledger](draft.json)

Registers Mixtral and maps its configuration and checkpoint names onto existing attention and routed-expert modules. Reference configurations and sampled tensor layouts agree; conversion coverage and an inherited conditional fused-path mismatch remain suspected concerns.

- [Mixtral configuration, assembly and inherited execution paths](#models)

## Problem

The parent registry does not recognize MixtralForCausalLM; directory-based configuration dispatch therefore rejects it as an unknown architecture. [source; call_a5462626708c45f48cc4c90679bcae40, call_f946dbb3ae50497ab402e25421fd0890]

## Reasoning

The change registers a Mixtral-specific configuration and model builder while reusing existing attention, transformer-block and routed-expert implementations rather than adding kernels. [source; call_aac1f07bff33408d9495d73e53f0ab19, call_d5131c10b83a48a1b38611bbe396bc27]

## Impact

Mixtral becomes selectable through Config.from_directory and Model.from_config. Registration and assembly do not by themselves establish successful conversion or generation. [source; call_aac1f07bff33408d9495d73e53f0ab19, call_f946dbb3ae50497ab402e25421fd0890, call_70c9c088207f436f823c98992deedb1a]

## Source Notes

Read the Qwen3 MoE introduction entry and the BlockSparseMLP introduction entry. They establish the existing assembly pattern, all-expert calibration mechanism and a recorded conditional fused-buffer mismatch. [ancestor; call_3e8993f0f9b84139a2fbe47e95e410a9, call_4e6fc8a61eae4ca18fa074e5e3da6b83]

PR #4, “chore: update config.py,” proposes a spelling correction. Issue #7, “quantizing model: undefined symbol: __cxa_call_terminate,” reports extension loading. Their relationship to this change is only inferred shared configuration/model infrastructure, not evidence of Mixtral motivation. [inference; call_b3376caeb5114a53a2761c38a4971dc6, call_1f3cb52d65684f189259f9904e4ba3ad, call_f946dbb3ae50497ab402e25421fd0890]

Issue #33, “Error converting model,” initially reports file-opening failures and later discusses GLM output problems. Issue #34, “torch._C._LinAlgError on last layer of quant,” reports Cholesky failure. Issue #38, “Error converting nvidia/Llama-3_1-Nemotron-Ultra-253B-v1,” reports sliced-loading dimensions. Associations here are inferred from their tracebacks naming the inspected conversion or Linear code; none demonstrates a Mixtral failure. [inference; call_4ed7ad0bd7374b22add28b2bf9a1e455, call_edc7c0c58b3f40bbb7cd2a14a3a831fc, call_054904c17c654f31805b4031840c2cdd, call_cafa2c706ee4468f86249dd8773c5921, call_bbe13162088d4c61a3446fce9807e28f, call_e554464f43d346b287afd441a248c5b8]

<a id="models"></a>

## Mixtral configuration, assembly and inherited execution paths

Adding MixtralModel to the registry comprehension exposes MixtralForCausalLM with its configuration and model classes. The new configuration requires intermediate_size, num_local_experts and num_experts_per_tok, mapping them to the existing routed-MLP constructor. Parent searches distinguish these from Qwen3 MoE’s moe_intermediate_size and num_experts spellings. [source; call_aac1f07bff33408d9495d73e53f0ab19, call_d5131c10b83a48a1b38611bbe396bc27, call_af2ba0dd32d540e7865978653b550ea9, call_fb3459e5345d46748611a755e860f6ec, call_d4cda7493e834fb9a52c6619f10007a8]

Explicit head_dim is retained; otherwise it is hidden_size divided by query-head count using integer division. KV-head count defaults to query-head count, tied embeddings default to false, and a supplied hidden_act must be silu. RoPE uses the existing default-settings reader with NEOX style. [source; call_d5131c10b83a48a1b38611bbe396bc27, call_f946dbb3ae50497ab402e25421fd0890]

The builder closely follows Qwen3MoeModel, but omits its Q/K normalization, changes the MLP prefix to block_sparse_moe, maps gate/up/down to w1/w3/w2, and requests half rather than float MLP output. It also omits Qwen3MoeModel’s calibration_all_experts=True assignment. [source; call_d5131c10b83a48a1b38611bbe396bc27, call_50119befce924239b024a4c2bd79e78f]

Each layer applies input RMSNorm, attention and a residual addition, followed by post-attention RMSNorm, routed MLP and another residual addition. Attention uses q_proj/k_proj/v_proj/o_proj, no Q/K norms, no sliding window override and sm_scale=None. Its existing implementations handle uncached SDPA, uncached FlashAttention and cached FlashAttention; this patch supplies no new backend. [source; call_d5131c10b83a48a1b38611bbe396bc27, call_0febcec3f60643ffbdc02b9006bca2d8, call_f2429752a1c84585bf0736d259f4184b]

BlockSparseMLP projects router scores, applies softmax, selects top experts and renormalizes their weights. Each selected expert computes down(SiLU(w1(x)) × w3(x)); weighted outputs are accumulated into token order. The routing projection uses pad_to=1, preserving exactly the expert count, while expert projections retain Linear’s default 128-element alignment. [source; call_d5131c10b83a48a1b38611bbe396bc27, call_78fbdc61ce8747edb0718c48dc8bc502, call_e554464f43d346b287afd441a248c5b8]

The existing grouped-expert path handles multiple flattened tokens or non-EXL3 experts. One flattened token with every expert projection in EXL3 selects indexed multi-GEMMs. MultiLinear additionally requires matching dimensions and bit widths within each projection group, no biases or softcaps, and unit post-scaling. The new Mixtral caller inherits these restrictions. [source; call_78fbdc61ce8747edb0718c48dc8bc502, call_d5131c10b83a48a1b38611bbe396bc27]

The only pre-existing BlockSparseMLP model construction found is Qwen3 MoE. Its all-expert calibration override ensures every down projection is visited during capture. Mixtral instead inherits Model’s false default: conversion supplies that value to activate_all_experts, leaving capture sparse. Gate/up projections share block.mlp.input; each down projection has its own block.mlp.{expert}.down capture key. [source; call_3405f7921fee4410bbe054c0c120bc15, call_50119befce924239b024a4c2bd79e78f, call_70c9c088207f436f823c98992deedb1a, call_3b8a7cfe24864bc1bb01863f2d45d2fb, call_78fbdc61ce8747edb0718c48dc8bc502]

Assembly ends with model.norm and lm_head. Tying enables model.embed_tokens as an alternate head key; Linear still tries supported storage at its primary key first. prepare_inputs stores input_ids and delegates to prepare_for_attn, whose default is uncached FlashAttention and whose uncached preparation rejects a supplied cache. [source; call_d5131c10b83a48a1b38611bbe396bc27, call_e554464f43d346b287afd441a248c5b8, call_f2429752a1c84585bf0736d259f4184b]

mistralai/Mixtral-8x7B-v0.1 and Mixtral-8x7B-Instruct-v0.1 each match the registration and configuration mappings: hidden size 4096, intermediate size 14336, 32 layers, 32 query heads, eight KV heads, eight experts with two selected, vocabulary 32000 and maximum positions 32768. Both specify SiLU, RMS epsilon 1e-5, RoPE theta 1000000, untied embeddings and no sliding window. [source; call_cb8e3fc1f20b4b87a813b30a834cc8b1, call_4eec33d549e94a248a2ce0955c110ab8, call_d5131c10b83a48a1b38611bbe396bc27]

mistralai/Mixtral-8x22B-v0.1 and Mixtral-8x22B-Instruct-v0.1 each match the mappings with hidden size 6144, intermediate size 16384, 56 layers, 48 query heads, eight KV heads, eight experts with two selected and maximum positions 65536. Their vocabularies differ: 32000 for base and 32768 for Instruct. Both retain SiLU, epsilon 1e-5, theta 1000000, untied embeddings and no sliding window. [source; call_50dba8bd77f645c6a42d513f3408a91a, call_f70a0f57696445ada081df73ff943232, call_d5131c10b83a48a1b38611bbe396bc27]

Sampled checkpoint headers agree with the requested weight families and orientation: w1/w3 are [intermediate, hidden], w2 is [hidden, intermediate], router weights are [8, hidden], Q/O are [hidden, hidden], K/V are [1024, hidden], norms are [hidden], and embeddings/head are [vocabulary, hidden]. These stored matrices are transposed by Linear.load_fp16. Sampled headers contain no optional biases or EXL3 scale/su/suh/sv/svh/trellis tensors, so the ordinary weight-loading path applies to these samples; tying is disabled in all four configurations. Every tensor in the inspected shards belongs to a requested weight family; no unused stored tensor was identified there. [source; call_be406182c92c4a389522fdc03aa7a99f, call_d25236324f7f4558a6d5efe892b5ce73, call_d3c1677783e54b26bb21731358d9948d, call_10a80c9daa984b3f88ecc9d71033a3f4, call_19327663a96040ab8b282f080ca76e6c, call_956b0e39744b4ad19b6dbe89d1243edb, call_e554464f43d346b287afd441a248c5b8]

Standard-library arithmetic gives head dimension 128 and KV width 1024 for all inspected configurations. Query widths are 4096 and 6144, with four or six query heads per KV head. Hidden, intermediate and vocabulary dimensions are divisible by 128, so default alignment adds no padding. Selecting two of eight experts is 25% of the expert set, not a measured fraction of total computation. [execution; call_5708122539954b908a4fe826ebd2d6fd]

Reusing shared modules reduces architecture-specific implementation work, but also imports their calibration requirements and fused-path restrictions. The two edits are complementary: registration exposes the new builder, while the builder supplies the checkpoint-specific names and dimensions needed by that dispatch. [inference; call_aac1f07bff33408d9495d73e53f0ab19, call_d5131c10b83a48a1b38611bbe396bc27, call_78fbdc61ce8747edb0718c48dc8bc502]

## Authoring-time findings — pending review

### mixtral-sparse-calibration-coverage (suspected; defect)

Mixtral omits the existing all-expert calibration override, allowing expert-specific capture data to be missing during conversion.

Trigger: A Mixtral layer’s calibration tokens never select at least one expert, while conversion subsequently attempts to quantize all its expert projections.

Expected: Collect calibration input for every down projection, or handle an unvisited expert explicitly.

Actual: Model defaults calibration_all_experts to false. BlockSparseMLP skips unselected experts, and Linear creates capture entries only when forwarded. Conversion later indexes capture_H[linear.qmap] for every loaded quantization target, so an unvisited down projection has no entry and the lookup raises KeyError. The inspected Qwen3 MoE construction prevents this coverage gap with its true override. Direct convert_exl3 callers found were conversion main and test_quant_dequant; the test explicitly forwards its individual Linear before conversion and does not exercise routed coverage.

Locations: 9665ba99989955593d2fb148323c9a96c77d1bea:exllamav3/models/mixtral.py — MixtralModel.__init__, b728058b20789afd74bdc371428ff1b83bc0b0f2:exllamav3/conversion/convert_model.py — main

Source evidence: call_d5131c10b83a48a1b38611bbe396bc27, call_70c9c088207f436f823c98992deedb1a, call_78fbdc61ce8747edb0718c48dc8bc502, call_e554464f43d346b287afd441a248c5b8, call_3b8a7cfe24864bc1bb01863f2d45d2fb, call_bedb364f824640029a62bcb281864f37, call_0572f8fe89074f4186fe81d7b3c80dc3

source_inspection: Traced the inherited calibration default through conversion parameters, sparse expert visitation, lazy capture creation and the unconditional capture lookup. [call_70c9c088207f436f823c98992deedb1a, call_78fbdc61ce8747edb0718c48dc8bc502, call_e554464f43d346b287afd441a248c5b8, call_3b8a7cfe24864bc1bb01863f2d45d2fb]. Limits: Conditional on actual router coverage; no checkpoint calibration was executed.

scalar_transcription: Modeled repeated routing to experts zero and one; expert-specific capture keys for experts two through seven remain absent. [call_5708122539954b908a4fe826ebd2d6fd]. Limits: Dictionary bookkeeping only; does not simulate learned routing or execute repository conversion.

### inherited-all-expert-fused-dimensions (suspected; defect)

The previously recorded all-expert fused-buffer mismatch remains unchanged in the implementation newly used by Mixtral.

Trigger: Forward one flattened token through fully EXL3 Mixtral experts with activate_all_experts=True.

Expected: Evaluate all eight experts with suitably sized buffers or use the grouped-expert path.

Actual: Routing produces eight indices, but fused buffers retain num_experts_per_tok=2 slots. The first exl3_mgemm checks index count against the output expert dimension and rejects the mismatch. Model.forward passes caller parameters through TransformerBlock to its MLP, establishing conditional API reach. Parent search also found ParallelDecoderBlock forwarding parameters, but Mixtral uses TransformerBlock. Ordinary Mixtral conversion supplies false and does not establish this trigger.

Locations: b728058b20789afd74bdc371428ff1b83bc0b0f2:exllamav3/modules/block_sparse_mlp.py — BlockSparseMLP.forward, 9665ba99989955593d2fb148323c9a96c77d1bea:exllamav3/models/mixtral.py — MixtralModel.__init__

Source evidence: call_78fbdc61ce8747edb0718c48dc8bc502, call_32b7a2421e9240e68b14a254a224d870, call_ee4fbc172de04e0492876b896a2408e8, call_0febcec3f60643ffbdc02b9006bca2d8, call_70c9c088207f436f823c98992deedb1a, call_d5131c10b83a48a1b38611bbe396bc27

source_inspection: Compared unchanged routing cardinality and fused allocations with the native dimension check and inspected parameter-forwarding callers. [call_78fbdc61ce8747edb0718c48dc8bc502, call_32b7a2421e9240e68b14a254a224d870, call_0febcec3f60643ffbdc02b9006bca2d8]. Limits: No tensor allocation or native execution; conditional rather than a default-workflow failure.

scalar_transcription: Computed eight all-expert indices versus two fused slots for the inspected configurations. [call_5708122539954b908a4fe826ebd2d6fd]. Limits: Integer shape arithmetic, not a CUDA test.

## Uncertainty and limits

No repository model loading, conversion, tensor execution or CUDA testing was performed. The Python check models dimensions and capture bookkeeping only, not floating-point arithmetic or kernels.

Checkpoint inspection covers first and last shards of the 8x7B base and both 8x22B models, not every layer or shard. The 8x7B Instruct configuration was read, but its tensor headers were not separately inspected.

Numerical equivalence, long-context behavior, memory requirements and performance remain unmeasured.
