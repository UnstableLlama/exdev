# a5caa423bbd9d8a61266a88fb237c18fb77ec0b8


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/a5caa423bbd9d8a61266a88fb237c18fb77ec0b8) · [Evidence ledger](draft.json)

Adds Qwen3MoeForCausalLM registration, normalized-attention/routed-expert assembly and all-expert calibration. Configuration mappings were checked; runtime compatibility remains untested, and an inherited conditional fused-path mismatch persists.

- [Qwen3 MoE assembly and calibration](#models)

## Problem

The parent registry lacks Qwen3MoeForCausalLM, so Config.from_directory rejects that architecture before model construction. [source; call_76a7fb171b00482886735b17497e6765, call_9e5f5e6655e745d79b1286d02fff0831, call_f45fd0fe29b9469fbe1b3e72075aa30f]

## Reasoning

The new builder combines Qwen3-style normalized attention with the existing BlockSparseMLP and enables all-expert calibration rather than introducing new inference kernels. [source; call_07cd83fdad164378a2b5d968c2a1888e, call_1d7bc409230746fb8d5cb7e87bbb4930, call_97b554b1e6594ba5953b476a05a9b454]

## Impact

Registry dispatch now selects Qwen3MoeConfig and Qwen3MoeModel. The change supplies model assembly and calibration policy; it does not establish successful loading or generation for every checkpoint format. [source; call_5c6e15f005f64e2e9b3c9a5300b9c753, call_07cd83fdad164378a2b5d968c2a1888e]

## Source Notes

The earlier BlockSparseMLP entry records an all-expert fused-path shape mismatch. Fresh inspection finds that implementation unchanged and newly connected to Qwen3MoeModel; its conditional failure is recorded here. [ancestor; call_00bd8c686a644175a4ad9f392c727a9f]

Issue #29, “Auto-YaRN for Qwen3? Maybe even set it dynamically?”, requests scaling-policy changes. Its relationship here is inferred only from shared Qwen3/RoPE configuration; this patch delegates to the existing configuration helper. [inference; call_5d534736d451454d9f9b9a5b789c68b2, call_07cd83fdad164378a2b5d968c2a1888e]

PR #35, “humaneval.py: fix top_k type, remove rep_p, add qwen3”, concerns sampling and evaluation. PR #4, “chore: update config.py”, proposes a spelling correction. Issue #7, “quantizing model: undefined symbol: __cxa_call_terminate”, reports extension loading, while issue #34, “torch._C._LinAlgError on last layer of quant”, reports Cholesky failure. Any association with this task is inferred from Qwen3 terminology or shared inspected configuration/conversion files, not an explicit task reference. [inference; call_6c193376451a43438dd637b008e49cae, call_c7a1b26152254e42893b4113900f0017, call_e4ffd418080a49c2af9085cf862dc20b, call_ab168d21db3f48f3928d3955fec21b00, call_9e5f5e6655e745d79b1286d02fff0831, call_25723010c6b24d25bd921de272a03b04]

<a id="models"></a>

## Qwen3 MoE assembly and calibration

Qwen3MoeConfig declares the new architecture string and supplies Qwen3MoeModel to Config. Adding the model to the registry comprehension exposes both classes through existing directory-based dispatch. [source; call_5c6e15f005f64e2e9b3c9a5300b9c753, call_07cd83fdad164378a2b5d968c2a1888e, call_76a7fb171b00482886735b17497e6765, call_9e5f5e6655e745d79b1286d02fff0831]

Configuration requires moe_intermediate_size, num_experts and num_experts_per_tok. A supplied hidden_act must be silu and a supplied norm_topk_prob must be true; both assertions allow omission. Explicit head_dim is retained, otherwise the builder uses hidden_size // num_attention_heads. KV heads default to query heads and tied embeddings default to false. [source; call_07cd83fdad164378a2b5d968c2a1888e, call_9e5f5e6655e745d79b1286d02fff0831, call_815e7ffb46a74d51b75a53e1d1ad99a8, call_0e3af3962b024d0da155d193f8eca3a2]

Each layer is a sequential pre-normalized TransformerBlock: attention output is added to the residual, then the updated residual is normalized for the routed MLP. Attention uses separate q_proj/k_proj/v_proj/o_proj keys and applies Q/K RMSNorm after reshaping into heads, before RoPE. The builder selects NEOX-style RoPE and leaves attention scaling unspecified. [source; call_07cd83fdad164378a2b5d968c2a1888e, call_6698d41eaf3b48178d679c4b86a84ca3, call_7393619fdffb4b56a5a0867cb4cd2405]

The router is model.layers.{idx}.mlp.gate; expert projections are experts.{expert_idx}.gate_proj, up_proj and down_proj. BlockSparseMLP applies softmax to router logits, selects top experts, renormalizes their weights, and accumulates weighted down(SiLU(gate(x)) × up(x)) outputs. The new builder requests half-precision intermediates and float output. [source; call_07cd83fdad164378a2b5d968c2a1888e, call_97b554b1e6594ba5953b476a05a9b454]

The existing expert-grouped path handles multiple flattened tokens or non-EXL3 experts. Single-token, fully EXL3 execution uses indexed multi-GEMMs; fusion additionally requires matching dimensions and bit widths within each projection group, no biases or softcaps, and unit post-scaling. Thus registration inherits these execution preconditions rather than defining a new MoE kernel. [source; call_97b554b1e6594ba5953b476a05a9b454, call_22ff47b703e14a97ace7eaff44b36f9d, call_07cd83fdad164378a2b5d968c2a1888e]

calibration_all_experts=True causes conversion's capture pass to request every expert, ensuring each down projection receives calibration inputs. Conversion separately recomputes reference outputs without that flag. Gate/up projections share block.mlp.input, while down projections have expert-specific calibration maps; the router has no quantization map. [source; call_07cd83fdad164378a2b5d968c2a1888e, call_25723010c6b24d25bd921de272a03b04, call_97b554b1e6594ba5953b476a05a9b454, call_7fe7e87e88f24235a50fa22b5334c587]

The assembly finishes with model.norm producing half precision and an lm_head vocabulary projection. Tied embeddings supply model.embed_tokens as an alternate head key only when tying is enabled and lm_head is absent. prepare_inputs stores input_ids and delegates to existing attention preparation, whose default is uncached FlashAttention. [source; call_07cd83fdad164378a2b5d968c2a1888e, call_7393619fdffb4b56a5a0867cb4cd2405]

Qwen/Qwen3-235B-A22B, Qwen/Qwen3-235B-A22B-FP8 and Qwen/Qwen3-235B-A22B-GPTQ-Int4 each match the new architecture and specify hidden size 4096, expert intermediate size 1536, 94 layers, 64 query heads, four KV heads and head dimension 128. Each specifies 128 experts with eight selected per token, SiLU, normalized top-k probabilities and untied embeddings. FP8 and GPTQ variants additionally declare their respective quantization formats. [source; call_718db87a4068461582b0901f7c9f86f2, call_b520cc1f9ea04a3e8f22d4e8f47d9b90, call_cb90403af83b443b9c79250d949e689f, call_07cd83fdad164378a2b5d968c2a1888e]

Qwen/Qwen3-30B-A3B, Qwen/Qwen3-30B-A3B-Base, Qwen/Qwen3-30B-A3B-FP8 and Qwen/Qwen3-30B-A3B-GPTQ-Int4 each match the registration and specify hidden size 2048, expert intermediate size 768, 48 layers, 32 query heads, four KV heads and head dimension 128. Each also specifies 128 experts, eight selected experts, SiLU, normalized top-k probabilities and untied embeddings. Base specifies 32768 maximum positions; the other three specify 40960. FP8/GPTQ metadata does not change these architectural dimensions. [source; call_9b5febaa362348888cfabbaa1a5f693c, call_59846477aa0741cea44225283cb53ab9, call_dee3a9daf5974026a55aabe104bf2ebc, call_73a65c7753d549878ecef3cec186d2af, call_07cd83fdad164378a2b5d968c2a1888e]

A standard-library calculation gives query widths 4096 and 8192 for the 30B and 235B configurations, respectively, and KV width 512 for both. The fallback head dimension would be 64 rather than the configured 128. Eight of 128 experts is 6.25% of the expert set, not a measured fraction of total model computation. [execution; call_97250612b4df4ff8966dd927c98eb053]

Reusing normalized attention and routed experts avoids architecture-specific kernels. Activating all experts only during capture trades additional calibration work for expert coverage while retaining ordinary sparse routing for reference outputs. [inference; call_07cd83fdad164378a2b5d968c2a1888e, call_97b554b1e6594ba5953b476a05a9b454, call_25723010c6b24d25bd921de272a03b04]

## Authoring-time findings — pending review

### inherited-all-expert-fused-shape (suspected; defect)

The new architecture inherits the existing mismatch between all-expert routing and single-token fused buffer sizes.

Trigger: BlockSparseMLP.forward receives one flattened token, fully EXL3 expert projections, activate_all_experts=True, and num_experts != num_experts_per_tok.

Expected: Evaluate every expert, either with appropriately sized fused buffers or through the expert-grouped path.

Actual: Routing produces num_experts indices while fused output buffers retain num_experts_per_tok entries. The first exl3_mgemm call checks those dimensions for equality. For all inspected Qwen3 MoE configurations this is 128 versus 8. The task leaves the implementation unchanged. Parent-tree caller search found TransformerBlock.forward and ParallelDecoderBlock.forward forwarding params to their MLP; this architecture uses TransformerBlock. Conversion supplies the all-expert flag during unquantized capture, so this does not establish that ordinary conversion triggers the fully EXL3 failure.

Locations: c6aa83f7e5a5e735c079d41244cbc704eda7e54e:exllamav3/modules/block_sparse_mlp.py — BlockSparseMLP.forward, a5caa423bbd9d8a61266a88fb237c18fb77ec0b8:exllamav3/models/qwen3_moe.py — Qwen3MoeModel.__init__

Source evidence: call_97b554b1e6594ba5953b476a05a9b454, call_22ff47b703e14a97ace7eaff44b36f9d, call_07cd83fdad164378a2b5d968c2a1888e, call_a8159b7003c34462acbaaf071634cfb1, call_6698d41eaf3b48178d679c4b86a84ca3, call_25723010c6b24d25bd921de272a03b04

source_inspection: Compared routing cardinality, fused allocations, the native dimension check, decoder forwarding sites and conversion's capture call. [call_97b554b1e6594ba5953b476a05a9b454, call_22ff47b703e14a97ace7eaff44b36f9d, call_6698d41eaf3b48178d679c4b86a84ca3, call_25723010c6b24d25bd921de272a03b04]. Limits: Conditional source-level reach; no tensor or CUDA execution.

scalar_transcription: Computed the inspected configurations' all-expert index count and fused output expert count: 128 != 8. [call_97250612b4df4ff8966dd927c98eb053]. Limits: Python integer shape arithmetic only; it does not execute BlockSparseMLP or the native check.

## Uncertainty and limits

No model loading, conversion, generation, or GPU execution was performed. The scalar check covers dimension arithmetic only.

All seven indexed model configurations were inspected, but tensor headers and checkpoint-format loading were not validated. Matching architecture metadata does not establish FP8 or GPTQ checkpoint compatibility.

Numerical equivalence, long-context accuracy, memory requirements, and performance remain unmeasured.
