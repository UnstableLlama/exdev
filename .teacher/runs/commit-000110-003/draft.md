# 1db3dce033981fe2d1825165a9389b3fdcd21b67


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/1db3dce033981fe2d1825165a9389b3fdcd21b67) · [Evidence ledger](draft.json)

Adds dense Qwen3 architecture dispatch and Llama-style assembly with per-head Q/K RMSNorm before RoPE. Reference configurations and representative tensors match the structural mapping; GPU equivalence and complete checkpoint compatibility remain untested.

- [Qwen3 dispatch, checkpoint mapping and per-head normalization](#models)

## Problem

The parent registry has no Qwen3 entry. The change adds Qwen3ForCausalLM dispatch and a model builder that supplies per-head Q/K normalization. [source; call_c0c60893e93340738a759da43f98ae17, call_1da1a4c30fa6446bbc2b4ca8160d83b9, call_701254c026304f409bb4dc24e34b11ab]

## Reasoning

Qwen3 closely follows the existing Llama builder, adding Q/K RMSNorm modules rather than introducing another attention implementation. Registration and construction are complementary: the registry selects Qwen3Config, which explicitly assigns Qwen3Model. [source; call_52cb84003c8c480380dc968df60e3abd, call_701254c026304f409bb4dc24e34b11ab, call_c1fb750872d64970aee0030b4f5055e2, call_f074dbec87f240f79f9aade69e9c14e6]

## Impact

The existing configuration/model factories can now select the dense Qwen3 architecture. This adds neither a new attention backend nor FP8 checkpoint decoding. [source; call_1da1a4c30fa6446bbc2b4ca8160d83b9, call_701254c026304f409bb4dc24e34b11ab, call_d25418fff69f4937947467d013a8b025, call_48a9d675e4914135b2395db7c712e365]

## Source Notes

Read the original models chapter, the class-owned registry entry, and the Q/K normalization entry. They establish the reused Llama layout, metadata-driven dispatch, and optional normalization mechanism respectively. [ancestor; call_9619c21b7d4f4c2397c0f68c39027564, call_6d26808702b140fa9180a8aa7ad972f0, call_e1da4f48208f4297a14fc6bbd2ffa42c]

The earlier Q/K entry records asymmetric constructor validation. Inspection shows it remains unchanged: a K-only norm is discarded. Qwen3 supplies both norms, so its builder does not exercise that case. [source; call_e1da4f48208f4297a14fc6bbd2ffa42c, call_45190be9639444be8529a59e7cc3d564, call_701254c026304f409bb4dc24e34b11ab]

Issue #29, “Auto-YaRN for Qwen3? Maybe even set it dynamically?”, requests automatic or request-dependent scaling. Downtown-Case raised it; turboderp discussed batching and cache-reuse difficulties. Its connection to this change is inferred from Qwen3 and the shared RopeSettings mechanism, not an explicit commit reference. The patch does not implement that proposal. [inference; call_719dd3cb705a4901a48bed94da22ae0d, call_701254c026304f409bb4dc24e34b11ab, call_887f4692bc5144349d0e25fb1132bbd3]

PR #4, “chore: update config.py,” proposes a spelling correction. Issue #7, “quantizing model: undefined symbol: __cxa_call_terminate,” reports an extension import failure and an environment workaround. Their inferred overlap with inspected code is config.py’s filename and RopeSettings import respectively; neither establishes a Qwen3 architecture defect. [inference; call_866c9f47611d40d6b290bf99518e88e1, call_71d79d80a64f44ccafc192a08d5f779f, call_f074dbec87f240f79f9aade69e9c14e6]

<a id="models"></a>

## Qwen3 dispatch, checkpoint mapping and per-head normalization

ARCHITECTURES derives the new record from Qwen3Model.config_class and Qwen3Config.arch_string. Config.from_directory selects that configuration class from the single architectures entry; Model.from_config subsequently constructs config.model_class. Unlike the thin Qwen2 wrapper, Qwen3Config explicitly passes its own model class to Config. [source; call_1da1a4c30fa6446bbc2b4ca8160d83b9, call_701254c026304f409bb4dc24e34b11ab, call_c1fb750872d64970aee0030b4f5055e2, call_f074dbec87f240f79f9aade69e9c14e6, call_d25418fff69f4937947467d013a8b025, call_c00ec6fa1e444d80aa35912a5379a24a]

Qwen3Config preserves the Llama configuration contract: explicit head_dim takes precedence over hidden_size // num_attention_heads; missing KV-head count defaults to query-head count; hidden_act may be absent but otherwise must be silu; intermediate width, layer count and RMS epsilon are required. Tied embeddings default to false. These fields feed the projection widths, block count, norms and head fallback in the new builder. [source; call_701254c026304f409bb4dc24e34b11ab, call_52cb84003c8c480380dc968df60e3abd, call_f074dbec87f240f79f9aade69e9c14e6, call_ac85d7bc5fbf45fcb99f33bf7c399a1f, call_ce5f1544b78442d7a611b5a07d1c60ec, call_8a125fae906f454dba167a3cf4d833ec, call_372e58c4b0b344ddaf457792feadaca2, call_8e2d62c92b81455d961e553a46d05f1c, call_b4d91a7225874bdda09f5af1270185ff, call_aed694873e64410aa9a30f6851f7ba99]

The module sequence is token embedding, one TransformerBlock per layer, final RMSNorm with half output, then the vocabulary projection. Each block maps input_layernorm, self_attn.{q,k,v,o}_proj, post_attention_layernorm and mlp.{gate,up,down}_proj. With residual width H, head width D, query heads Q, KV heads K and intermediate width I, the projection shapes are [QD,H], [KD,H], [KD,H], [H,QD], [I,H], [I,H] and [H,I]. The two added self_attn.{q,k}_norm weights have width D, not H or QD. [source; call_701254c026304f409bb4dc24e34b11ab, call_45190be9639444be8529a59e7cc3d564, call_c8114d51ddf7483eb5437e5214836afe, call_7ac6d10c8fa54e7ea078a1b914e42ff0]

Attention registers both norms for loading and applies them after reshaping projections into individual heads, before RoPE, in SDPA, uncached FlashAttention and cached FlashAttention. V is not normalized. RMSNorm.forward flattens all leading axes into rows and invokes the native kernel, so the operation is per head: x·w/sqrt(mean(x²)+epsilon). Q/K outputs are explicitly half precision. The native wrapper requires half weights, matching last-axis width and width divisible by four; the reference head width 128 satisfies that width condition. [source; call_45190be9639444be8529a59e7cc3d564, call_c8114d51ddf7483eb5437e5214836afe, call_b149b543f6374cd19d91e9582a935fea, call_c8f8bbb799854e22a1d89ba87757d18b]

The parent-tree q_norm search finds only Attention’s optional implementation, not a model builder enabling it. Qwen3 therefore activates an existing capability. Reusing the generic RMSNorm kernel avoids another implementation, but its 1024-thread launch and existing specialization TODO do not establish efficient execution for 128-element heads. [inference; call_2bca98f285864cb8826a83190074e14f, call_701254c026304f409bb4dc24e34b11ab, call_c8114d51ddf7483eb5437e5214836afe, call_b149b543f6374cd19d91e9582a935fea]

All 17 inspected Qwen3 configs declare Qwen3ForCausalLM, D=128, K=8, SiLU, RMS epsilon 1e-6, vocabulary 151936, theta 1000000, null rope_scaling and disabled sliding-window attention. Thus their explicit settings, rather than the builder’s missing-field fallbacks, determine these values. The unrestricted Attention defaults agree with these configs. [source; call_c8f8bbb799854e22a1d89ba87757d18b, call_109c9d528a7a41d795103b7a9e3ca272, call_854739b1cb7c4e4aaafd3fa1e3924c25, call_888d4268550b465d8a74118b81a059aa, call_1d895079e34c48bbab18ccbdae509216, call_52fba9be7bde4a4ca7a5e8d036fc31ee, call_81944fe29e2a4004b4c9f18f32fca107, call_4d7d1fd7d4b54f15b442a540bebe2d50, call_a5302c1a9ac3406c84ba3abb012d4faa, call_734b96d9f0bb4c348e52f2c7c8c2ce60, call_0fb4942aa1e6435ab78035508124e73f, call_b2ac3bb3b01c4f30a60797c5e4c1929f, call_e85f2a6318d5493f947de2235a88b725, call_fc6fc4a49b0548948a16b8dcd40be779, call_30ca6e1690d74bd589fd97d5877a0ad5, call_f5f88be075014ea486d935ef8bfd23f4, call_0271ee34667345b5b9751b883f8abcbb, call_45190be9639444be8529a59e7cc3d564]

Qwen/Qwen3-0.6B, Qwen3-0.6B-Base and Qwen3-0.6B-FP8 each map to H=1024, I=3072, Q=16 and 28 layers, with tied embeddings. The complete ordinary 0.6B header matches all requested dense weights, including Q [2048,1024], K/V [1024,1024], O [1024,2048] and Q/K norms [128]. Both embedding and lm_head weights exist despite tying being enabled; optional projection biases and EXL3 storage groups are absent, selecting ordinary weights without biases. [source; call_c8f8bbb799854e22a1d89ba87757d18b, call_109c9d528a7a41d795103b7a9e3ca272, call_854739b1cb7c4e4aaafd3fa1e3924c25, call_7ac6d10c8fa54e7ea078a1b914e42ff0, call_df7f410876b74acb88e2d7d0d6c0c702]

Qwen/Qwen3-1.7B, Qwen3-1.7B-Base and Qwen3-1.7B-FP8 each map to H=2048, I=6144, Q=16 and 28 layers, with tied embeddings. The inspected Base header’s first layer matches Q/O [2048,2048], K/V [1024,2048], gate/up [6144,2048], down [2048,6144] and Q/K norms [128]. [source; call_888d4268550b465d8a74118b81a059aa, call_1d895079e34c48bbab18ccbdae509216, call_52fba9be7bde4a4ca7a5e8d036fc31ee, call_cec86771c6ef45cab5359e11929d9e86]

Qwen/Qwen3-4B, Qwen3-4B-Base and Qwen3-4B-FP8 each map to H=2560, I=9728, Q=32 and 36 layers, with tied embeddings. The inspected ordinary first layer matches Q [4096,2560], K/V [1024,2560], O [2560,4096], gate/up [9728,2560], down [2560,9728] and Q/K norms [128]. [source; call_81944fe29e2a4004b4c9f18f32fca107, call_4d7d1fd7d4b54f15b442a540bebe2d50, call_a5302c1a9ac3406c84ba3abb012d4faa, call_db9c84cc8ade4fc5b86246d282239c3d]

Qwen/Qwen3-8B, Qwen3-8B-Base and Qwen3-8B-FP8 each map to H=4096, I=12288, Q=32 and 36 layers, with untied embeddings. The inspected ordinary first layer matches Q/O [4096,4096], K/V [1024,4096], gate/up [12288,4096], down [4096,12288] and Q/K norms [128]. [source; call_734b96d9f0bb4c348e52f2c7c8c2ce60, call_0fb4942aa1e6435ab78035508124e73f, call_b2ac3bb3b01c4f30a60797c5e4c1929f, call_8f3a86ab886945e2af29308866206b46]

Qwen/Qwen3-14B, Qwen3-14B-Base and Qwen3-14B-FP8 each map to H=5120, I=17408, Q=40 and 40 layers, with untied embeddings. The inspected ordinary first layer matches Q/O [5120,5120], K/V [1024,5120], gate/up [17408,5120], down [5120,17408] and Q/K norms [128]. [source; call_e85f2a6318d5493f947de2235a88b725, call_fc6fc4a49b0548948a16b8dcd40be779, call_30ca6e1690d74bd589fd97d5877a0ad5, call_8be375d5120d47b0ad14a734da8b72c2]

Qwen/Qwen3-32B and Qwen3-32B-FP8 each map to H=5120, I=25600, Q=64 and 64 layers, with untied embeddings. The inspected ordinary first layer matches Q [8192,5120], K/V [1024,5120], O [5120,8192], gate/up [25600,5120], down [5120,25600] and Q/K norms [128]. [source; call_f5f88be075014ea486d935ef8bfd23f4, call_0271ee34667345b5b9751b883f8abcbb, call_6fea6c35825849fca616311d176cb213]

A bounded Python calculation reproduced these six projection layouts and query-heads-per-KV-head ratios 2, 2, 4, 4, 5 and 8. It also showed why explicit D matters: deriving H/Q would yield 64 for 0.6B and 80 for 4B and 32B, rather than their supplied 128. All transcribed linear widths satisfy the existing 128-element padding alignment. [execution; call_49aae48f4a4c4a4780a625259242ec8c]

Tying is implemented as a loading fallback, not forced runtime weight sharing. The builder probes the exact name lm_head, whereas ordinary headers name lm_head.weight; this can enable the alternate embedding key even when the head exists. Linear.load still tries the primary head before its alternate, so the ordinary 0.6B head remains preferred. [source; call_701254c026304f409bb4dc24e34b11ab, call_48a9d675e4914135b2395db7c712e365, call_df7f410876b74acb88e2d7d0d6c0c702, call_7ac6d10c8fa54e7ea078a1b914e42ff0]

The Base configs use maximum position count 32768 and EOS 151643; the other inspected configs use 40960 and EOS 151645. Shared configuration loading preserves those distinctions. All select default, unscaled NEOX RoPE because rope_scaling is null; Qwen3 adds no automatic YaRN policy. [source; call_109c9d528a7a41d795103b7a9e3ca272, call_1d895079e34c48bbab18ccbdae509216, call_4d7d1fd7d4b54f15b442a540bebe2d50, call_0fb4942aa1e6435ab78035508124e73f, call_fc6fc4a49b0548948a16b8dcd40be779, call_c8f8bbb799854e22a1d89ba87757d18b, call_f074dbec87f240f79f9aade69e9c14e6, call_887f4692bc5144349d0e25fb1132bbd3, call_701254c026304f409bb4dc24e34b11ab]

prepare_inputs preserves the same tensor/dictionary contract as all seven existing architecture hooks: retain input_ids, invoke prepare_for_attn and return the tensor. Model.forward and prefill consume it that way. The new hook omits no guard present in those existing hooks; cached preparation still requires the shared cache/page/position parameters. The science sampling utility also consumes the returned tensor, but manually projects Q/K without applying optional Q/K norms; its inspected default remains a Llama model, not Qwen3. [source; call_701254c026304f409bb4dc24e34b11ab, call_7669bfaa58e5417da8ba0269de735a3b, call_8520c39450b047cb8c03008ab873a359, call_d0fe972f32c54102abeba3f576b6b6ce, call_d25418fff69f4937947467d013a8b025, call_45190be9639444be8529a59e7cc3d564, call_41e46bc3f2dc4928a6407b584a340f41]

## Authoring-time findings — pending review

### inherited-architecture-mismatch-diagnostic (suspected; defect)

Qwen3 inherits the existing undefined-variable architecture-mismatch diagnostic; the task does not repair it.

Trigger: Directly construct Qwen3Config against a config whose single architecture is not Qwen3ForCausalLM, with assertions enabled.

Expected: Reject the mismatch with an AssertionError identifying the expected architecture.

Actual: Config.__init__ evaluates an assertion message containing undefined expect_arch, producing NameError instead. Config.from_directory normally chooses the matching class first, so stable supported files do not reach this branch through that factory.

Locations: 1db3dce033981fe2d1825165a9389b3fdcd21b67:exllamav3/models/qwen3.py — Qwen3Config.__init__, f97c5ce619feb3aa9f4ceb568c9e350d166df866:exllamav3/models/config.py — Config.__init__

Source evidence: call_701254c026304f409bb4dc24e34b11ab, call_f074dbec87f240f79f9aade69e9c14e6, call_aa526956ffbd4fd2bea9166c9ed863b5

source_inspection: Compared the new superclass call, unchanged assertion and factory call site with the earlier recorded observation. [call_701254c026304f409bb4dc24e34b11ab, call_f074dbec87f240f79f9aade69e9c14e6, call_6d26808702b140fa9180a8aa7ad972f0]. Limits: No configuration constructor was executed; the reach stated is the direct constructor mismatch path.

### fp8-checkpoint-format-boundary (suspected; external_compatibility)

Matching Qwen3ForCausalLM dispatch does not make the indexed FP8 variants loadable by the existing tensor loader.

Trigger: Load a stored F8_E4M3 projection from any of the six inspected Qwen3 FP8 configurations.

Expected: FP8 compatibility would require decoding the stored dtype and applying its block scales, or rejecting that format before ordinary-weight loading.

Actual: Linear selects the ordinary .weight path, whose get_tensor call reaches convert_dtype. That function rejects F8_E4M3 as an unknown dtype. The inspected FP8 headers also contain projection weight_scale_inv tensors that this loading path never reads. This is an existing format limitation exposed by the newly recognized architecture, not evidence that the commit promised FP8 support.

Locations: f97c5ce619feb3aa9f4ceb568c9e350d166df866:exllamav3/loader/safetensors.py — convert_dtype, f97c5ce619feb3aa9f4ceb568c9e350d166df866:exllamav3/modules/linear.py — Linear.load_fp16

Source evidence: call_df7f410876b74acb88e2d7d0d6c0c702, call_48a9d675e4914135b2395db7c712e365, call_c86c9fd844c64c65b9ae4afd99fa2f7a, call_ec60c1aed676433c857ca2b0a9bed884, call_7f0f64f1e564432993129cfb94715bd2, call_daaa77fedecb4b2d875683c56aa83a72, call_7afe64659c30492b8d8bfe5857d40279, call_607bd61805454126abf4364548a46116, call_4e54134239c04a9187fef6aeb005ce81

source_inspection: Inspected first-layer FP8 weights and scale tensors for all six sizes, Linear’s loading choice, and both active convert_dtype call sites in get_tensor and list_tensors. [call_c86c9fd844c64c65b9ae4afd99fa2f7a, call_48a9d675e4914135b2395db7c712e365, call_df7f410876b74acb88e2d7d0d6c0c702]. Limits: No checkpoint payload was loaded. Header inspection was representative rather than exhaustive across FP8 shards.

## Uncertainty and limits

No package import, checkpoint loading, GPU inference, numerical parity test or benchmark was executed. The Python calculation checks transcribed dimensions, not repository kernels.

The complete Qwen3-0.6B header was inspected. Other header reads cover representative first-layer tensors, not every layer, shard, optional tensor or vocabulary head; their complete checkpoint compatibility remains unverified.

Configuration and tensor metadata establish structural correspondence, not weight values, reference-output equivalence or usable long-context quality.

Literal searches and inspected in-tree call sites do not establish compatibility for external subclasses or dynamic consumers.
