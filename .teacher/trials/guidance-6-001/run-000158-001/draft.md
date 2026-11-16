# 9665ba99989955593d2fb148323c9a96c77d1bea


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/9665ba99989955593d2fb148323c9a96c77d1bea) · [Evidence ledger](draft.json)

Adds MixtralForCausalLM dispatch and model assembly using existing attention and MoE components. Four checkpoint configurations match the mappings; runtime behavior remains untested, including an inherited conditional fused-path mismatch.

- [Mixtral registration and routed-expert assembly](#models)

## Problem

Mixtral was mentioned as planned support, but the parent architecture registry had no MixtralForCausalLM entry; directory-based configuration dispatch would reject it. [source; call_3564ee4ae2e4408180b4c2282671dbe0, call_a60baf5e46d9457493212e576677bd0a, call_fcd8805d821a46bb90b485a0b5632e8f]

## Reasoning

The change supplies Mixtral-specific configuration and checkpoint-key mappings while reusing existing attention, transformer blocks and routed-expert execution. Registration and the new classes work together: the registry derives its dispatch key from MixtralConfig.arch_string. [source; call_baad383a78ab49189623a17995834fb2, call_9db0e1ecb9f0495d913ba981c2f5844e, call_a60baf5e46d9457493212e576677bd0a]

## Impact

Config.from_directory can now select MixtralConfig, and Model.from_config can instantiate MixtralModel. This establishes an assembly path, not measured checkpoint-loading or generation success. [source; call_fcd8805d821a46bb90b485a0b5632e8f, call_25a17435c16e4b8e993acff257fd6eef, call_9db0e1ecb9f0495d913ba981c2f5844e, call_baad383a78ab49189623a17995834fb2]

## Source Notes

The Qwen3 MoE ancestor entry was read. It describes the closely related model assembly, all-expert calibration policy and a conditional fused-path shape mismatch. [ancestor; call_8d9d7d804ca64912ab0b3c9ada7fda92]

PR #4, “chore: update config.py,” proposes a spelling correction. Issue #7, “quantizing model: undefined symbol: __cxa_call_terminate,” reports extension loading. Their relevance here is inferred only from the shared configuration file, not an explicit relationship to Mixtral support. [inference; call_ee87130eca5649d1865ded83292497bb, call_b14b699f1e3145838a3c6543d42e3e3a, call_fcd8805d821a46bb90b485a0b5632e8f]

Issue #33, “Error converting model,” initially reports file-opening failure and later discusses GLM output; #34, “torch._C._LinAlgError on last layer of quant,” reports Cholesky failure; #38, “Error converting nvidia/Llama-3_1-Nemotron-Ultra-253B-v1,” reports a sliced-loading dimension mismatch. Any association with this task is inferred solely from their shared convert_model.py path; none establishes a Mixtral failure. [inference; call_c4ef6c2b660b482ebb0f2a54274e70b7, call_70458752782243468fbcf13d4c4ba921, call_6a9e85e76c0e4061b01b77cf1c5018ce, call_e5c8b772eb6d460cbbf37c332011cbad, call_2702ab39be80411a9f97a0187bd5b567]

<a id="models"></a>

## Mixtral registration and routed-expert assembly

MixtralConfig maps intermediate_size to moe_intermediate_size and num_local_experts to num_experts, unlike Qwen3 MoE's moe_intermediate_size and num_experts configuration keys. num_experts_per_tok remains the routing cardinality. A supplied hidden_act must be silu, although omission is allowed. [source; call_9db0e1ecb9f0495d913ba981c2f5844e, call_90591634815742eaa9b70ef62d8134bb, call_fcd8805d821a46bb90b485a0b5632e8f, call_3313b805f38b4a15bbec3390dc2a531f, call_6f2e3690ab27498d9bf2b3e7275f29f4, call_980c74d5bff6469fa048a8fbc7fa7254]

Head dimension uses the explicit head_dim when truthy, otherwise hidden_size // num_attention_heads. KV heads default to query heads, and tied embeddings default to false. RoPE uses the shared configuration reader with NEOX style. [source; call_9db0e1ecb9f0495d913ba981c2f5844e, call_fcd8805d821a46bb90b485a0b5632e8f]

The model assembles an embedding, one sequential pre-normalized TransformerBlock per layer, final RMSNorm and vocabulary projection. Each block adds attention to its residual before normalizing for the MLP and adding that result. Attention uses separate q_proj/k_proj/v_proj/o_proj tensors, without Q/K normalization or an explicit sliding window. [source; call_9db0e1ecb9f0495d913ba981c2f5844e, call_04bcb961098246cda437429eb3ef3cab, call_d369e1a2290344d799e9294d4006d9ab]

Under model.layers.{idx}.block_sparse_moe, gate is the router and expert w1/w3/w2 are respectively gate/up/down projections. BlockSparseMLP computes softmax routing, selects and renormalizes top-k weights, then accumulates weighted down(SiLU(gate(x)) × up(x)). Mixtral requests half-precision intermediates and outputs. The router uses pad_to=1, preserving exactly num_experts outputs. [source; call_9db0e1ecb9f0495d913ba981c2f5844e, call_5ed61e047df345db88ccabcf2cea706a]

Multiple flattened tokens or non-fully-EXL3 experts take the expert-grouped path. A single token with all EXL3 projections takes indexed multi-GEMMs. Fusion requires equal projection dimensions and bit widths within each group, no biases or softcaps, and unit post-scaling. Reuse therefore inherits these preconditions rather than adding a Mixtral-specific kernel. [source; call_5ed61e047df345db88ccabcf2cea706a]

Unlike Qwen3MoeModel, MixtralModel does not enable calibration_all_experts; it retains Model's false default. Conversion forwards that value during capture, so Mixtral calibration uses ordinary selected-expert routing rather than Qwen3 MoE's all-expert capture policy. [source; call_9db0e1ecb9f0495d913ba981c2f5844e, call_90591634815742eaa9b70ef62d8134bb, call_25a17435c16e4b8e993acff257fd6eef, call_a68997c5dfc74c0ca80481d0c900e0a9, call_2702ab39be80411a9f97a0187bd5b567]

The final head can fall back to model.embed_tokens when tying is enabled and lm_head is absent. prepare_inputs stores input_ids and delegates to shared attention preparation, whose default is uncached FlashAttention and whose cached mode prepares cache positions and block tables. [source; call_9db0e1ecb9f0495d913ba981c2f5844e, call_d369e1a2290344d799e9294d4006d9ab]

mistralai/Mixtral-8x7B-v0.1 and mistralai/Mixtral-8x7B-Instruct-v0.1 each match the registration and key mappings: hidden size 4096, intermediate size 14336, 32 layers, 32 query heads, eight KV heads, eight experts and two selected experts. Both omit head_dim, specify SiLU, untied embeddings, null sliding_window, RMS epsilon 1e-5 and RoPE theta 1,000,000; vocabulary size is 32000. [source; call_b692fbfb383549a6be3d3278ffc3fa86, call_0b65dda417ab4ae6abf296690261c6b1, call_9db0e1ecb9f0495d913ba981c2f5844e]

mistralai/Mixtral-8x22B-v0.1 and mistralai/Mixtral-8x22B-Instruct-v0.1 each match the mappings with hidden size 6144, intermediate size 16384, 56 layers, 48 query heads, eight KV heads, eight experts and two selected experts. Both omit head_dim and specify the same activation, tying, window, epsilon and theta choices as the 8x7B configurations. Base vocabulary size is 32000; Instruct uses 32768. All four configurations advertise bfloat16, whereas this builder explicitly requests half precision for expert intermediates and outputs. [source; call_a379374e9d464ea5bfde3bc5cf27dc4a, call_1012b9b5739f41fa8ef8c5b8afb5d1c0, call_b692fbfb383549a6be3d3278ffc3fa86, call_0b65dda417ab4ae6abf296690261c6b1, call_9db0e1ecb9f0495d913ba981c2f5844e]

A standard-library arithmetic check gives fallback head dimension 128 for both sizes, KV projection width 1024, and query widths 4096/6144. This yields four/six query heads per KV head. Two selected experts out of eight is 25% of the expert set, not a measured fraction of total inference work. [execution; call_448c9c4b827d4918b2e4975a0cfc83fd]

## Authoring-time findings — pending review

### inherited-all-expert-fused-shape (suspected; defect)

The newly connected Mixtral assembly carries over BlockSparseMLP's conditional mismatch between all-expert routing and fused buffer sizes.

Trigger: One flattened token, fully EXL3 expert projections, activate_all_experts=True, and num_experts different from num_experts_per_tok.

Expected: Evaluate all requested experts using matching buffers or the expert-grouped path.

Actual: Routing produces num_experts indices, but fused buffers retain num_experts_per_tok entries. exl3_mgemm checks those dimensions for equality: the inspected Mixtral configurations produce eight versus two. The task does not modify this implementation. Parent caller search found TransformerBlock.forward and ParallelDecoderBlock.forward forwarding params to their MLP; Mixtral uses TransformerBlock. Mixtral's default conversion policy does not set the triggering flag true, so this is not evidence that ordinary conversion fails.

Locations: 9665ba99989955593d2fb148323c9a96c77d1bea:exllamav3/models/mixtral.py — MixtralModel.__init__, b728058b20789afd74bdc371428ff1b83bc0b0f2:exllamav3/modules/block_sparse_mlp.py — BlockSparseMLP.forward

Source evidence: call_9db0e1ecb9f0495d913ba981c2f5844e, call_5ed61e047df345db88ccabcf2cea706a, call_78e1cefebe1d46a0914cec7281517401, call_c476322da19a4efda2c94b8cdcd79ef0, call_04bcb961098246cda437429eb3ef3cab, call_2702ab39be80411a9f97a0187bd5b567

source_inspection: Compared routing cardinality, fused allocations, native dimension check, decoder callers and the task's model assembly. [call_5ed61e047df345db88ccabcf2cea706a, call_78e1cefebe1d46a0914cec7281517401, call_04bcb961098246cda437429eb3ef3cab, call_9db0e1ecb9f0495d913ba981c2f5844e]. Limits: Conditional source reasoning, not a CUDA reproduction.

scalar_transcription: Computed eight all-expert indices versus two fused expert slots for the inspected configurations. [call_448c9c4b827d4918b2e4975a0cfc83fd]. Limits: Integer shape arithmetic only; no repository tensor implementation executed.

## Uncertainty and limits

No repository model execution, conversion or GPU test was performed. The Python check models dimension arithmetic only, not tensor precision or kernel behavior.

All four indexed Mixtral configurations were read, but checkpoint tensor headers and numerical equivalence were not validated.

Conversion calibration coverage, memory consumption, throughput and long-context accuracy remain unmeasured.
