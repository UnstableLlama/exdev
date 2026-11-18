# a5caa423bbd9d8a61266a88fb237c18fb77ec0b8


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/a5caa423bbd9d8a61266a88fb237c18fb77ec0b8) · [Evidence ledger](draft.json)

Adds Qwen3MoeForCausalLM registration and assembly using normalized Qwen3 attention, routed expert MLPs and all-expert calibration; a conditional inherited fused-path shape mismatch remains.

- [Qwen3 MoE registration, expert routing and calibration](#models)

## Problem

The parent architecture registry supports dense Qwen3 but not Qwen3MoeForCausalLM; Config.from_directory rejects an architecture absent from that registry. [source; call_af812fb4337842bdadfcd6a69ca2c432, call_9555208412814f30995426b021cd2ccd]

## Reasoning

The new builder combines the existing Qwen3 normalized-attention assembly with BlockSparseMLP, supplying expert checkpoint keys, routing dimensions and all-expert calibration. [source; call_89bad8e3d4694c5d9864789ba0f54f41, call_0242adcdc71e4ba9bb9373cfd5e61480, call_cf72eb3dcebb46c492ad18e51318187d]

## Impact

Registration enables architecture-specific configuration dispatch without changing attention or expert kernels. The calibration switch activates an existing conversion mechanism rather than introducing a new converter. [source; call_f9343e620ca0483e8fb9c81967f926e7, call_89bad8e3d4694c5d9864789ba0f54f41, call_fa86a7a3557846ac870e30533824ab03]

## Source Notes

Read the earlier Qwen3 entry, which establishes the normalized-attention builder being followed, and the BlockSparseMLP entry, which records the conditional all-expert/fused-buffer mismatch. [ancestor; call_f73f21e32f1e45188a153662e9b97c13, call_ea35458fe5674505a0a0e77915e3ec83]

PR #4, “chore: update config.py,” proposes a spelling correction. Issue #7, “quantizing model: undefined symbol: __cxa_call_terminate,” reports native-extension import failure. Issue #34, “torch._C._LinAlgError on last layer of quant,” reports a Cholesky failure while converting a Cohere2 model. [source; call_f248979d9701418ba11ea7895cd0621c, call_451c4666461847c980c38fe6a1e83c02, call_2cedbc69a1b746e384e91df2ac12c068]

Their relationship to this task is only inferred shared-file context: config.py and convert_model.py occur in the inspected code and discussions. None establishes motivation for Qwen3 MoE support or successful execution of it. [inference; call_f248979d9701418ba11ea7895cd0621c, call_451c4666461847c980c38fe6a1e83c02, call_2cedbc69a1b746e384e91df2ac12c068, call_89bad8e3d4694c5d9864789ba0f54f41]

<a id="models"></a>

## Qwen3 MoE registration, expert routing and calibration

architectures.py imports Qwen3MoeModel and includes it in the registry comprehension. Its config_class declares Qwen3MoeForCausalLM, so the existing directory lookup selects Qwen3MoeConfig, which associates itself with Qwen3MoeModel. [source; call_f9343e620ca0483e8fb9c81967f926e7, call_89bad8e3d4694c5d9864789ba0f54f41, call_af812fb4337842bdadfcd6a69ca2c432, call_9555208412814f30995426b021cd2ccd]

Qwen3MoeConfig preserves explicit head_dim, otherwise using hidden_size // num_attention_heads; KV-head count defaults to query-head count and tied embeddings default to false. It requires moe_intermediate_size, num_experts and num_experts_per_tok. Supplied hidden_act must be silu and supplied norm_topk_prob must be true; both assertions permit omission. [source; call_89bad8e3d4694c5d9864789ba0f54f41, call_9555208412814f30995426b021cd2ccd]

Parent-tree searches found no norm_top spelling or moe_intermediate spelling; num_experts and num_experts_per_tok occur in BlockSparseMLP. The new norm_topk_prob assertion therefore restricts accepted configuration to the module's existing unconditional normalization of selected routing probabilities, rather than controlling a new branch. [source; call_18285422fa604769a00bc43f2b959f8e, call_6b6659b7601c466689432d367d3acd78, call_2653fbc2a6074af58627d88f04101da8, call_cf72eb3dcebb46c492ad18e51318187d, call_89bad8e3d4694c5d9864789ba0f54f41]

Each layer is a sequential pre-normalized TransformerBlock: attention is added to the residual, then the updated residual is normalized for the expert MLP and receives its output. Attention uses separate q_proj, k_proj, v_proj and o_proj tensors, with Q/K RMSNorm after head reshaping and before RoPE in all three existing backends. The builder selects NEOX-style RoPE through the shared configuration helper. [source; call_89bad8e3d4694c5d9864789ba0f54f41, call_e86e4e8d6a324a5ca7132e2b84ca1309, call_85789c51b02c459784b12d5cbaa94964, call_9555208412814f30995426b021cd2ccd]

BlockSparseMLP projects flattened tokens through mlp.gate, applies softmax, selects num_experts_per_tok experts and renormalizes their probabilities. Each expert computes down(silu(gate(x)) × up(x)); weighted results are accumulated into token order. The supplied keys expand to mlp.experts.{expert_idx}.{gate_proj,up_proj,down_proj}. Expert intermediates are half precision and the builder requests float output. [source; call_cf72eb3dcebb46c492ad18e51318187d, call_89bad8e3d4694c5d9864789ba0f54f41]

The ordinary expert path handles multiple flattened tokens or non-EXL3 experts. A single token with all expert projections EXL3 selects indexed multi-GEMM fusion; MultiLinear additionally requires matching dimensions and bit widths within each projection group, no biases or softcaps, and unit post-scaling. Parent-tree search found no existing BlockSparseMLP constructor call, so this task supplies a model-level consumer of that earlier module. [source; call_cf72eb3dcebb46c492ad18e51318187d, call_d15553f5f9224d429f2904c7e3877851, call_89bad8e3d4694c5d9864789ba0f54f41]

The constructor sets calibration_all_experts=True. Existing conversion forwards it as activate_all_experts during Hessian capture, then recomputes reference states without that flag and advances converted states using ordinary routing. This connects expert coverage during calibration to the new architecture; the attention/MLP calibration-map labels retain the established conversion interfaces. [source; call_0db61ffcdd264b23961f654e2336ac3c, call_fa86a7a3557846ac870e30533824ab03, call_89bad8e3d4694c5d9864789ba0f54f41, call_cf72eb3dcebb46c492ad18e51318187d]

The inherited single-token all-expert mismatch is carried over, not corrected: routing can return all experts while fused buffers remain sized by num_experts_per_tok. The new model enables the calibration flag, but this does not establish that normal conversion reaches the fully EXL3, single-token failure condition. [source; call_cf72eb3dcebb46c492ad18e51318187d, call_610dc55cab9e48bf82f707d56859385b, call_89bad8e3d4694c5d9864789ba0f54f41, call_fa86a7a3557846ac870e30533824ab03]

The output stack is final RMSNorm producing half precision followed by lm_head. A tied head may use model.embed_tokens as its alternate key only when tying is configured and the tensor collection reports no lm_head. prepare_inputs stores input_ids and calls prepare_for_attn exactly as the inspected Qwen3, Phi3, Llama, Glm4, Gemma2, DeciLM, Cohere2 and Cohere callers do; no additional caller-side guard is omitted. The shared helper defaults to uncached FlashAttention and retains its cache-preparation checks. [source; call_89bad8e3d4694c5d9864789ba0f54f41, call_456546f693c24747bcc960d71cce3a52, call_c7b9a95c4b414615b714082cb008032a, call_85789c51b02c459784b12d5cbaa94964]

Qwen/Qwen3-235B-A22B, Qwen/Qwen3-235B-A22B-FP8 and Qwen/Qwen3-235B-A22B-GPTQ-Int4 were each read. Each declares the registered architecture, hidden size 4096, 94 layers, 64 query heads, four KV heads, head dimension 128 and expert intermediate size 1536. Each specifies 128 experts, eight selected experts, silu, normalized top-k probabilities, epsilon 1e-6 and untied embeddings, agreeing with the builder's assembly. The quantized variants additionally declare their distinct storage formats; configuration agreement alone does not establish loader compatibility. [source; call_88e3ed1441b04372b4a9c26de4734ae5, call_027cdf3d1d3846c2b24659bc2c8c4c71, call_8bef024055b14cee872b309f53b89339, call_89bad8e3d4694c5d9864789ba0f54f41]

Qwen/Qwen3-30B-A3B, Qwen/Qwen3-30B-A3B-Base, Qwen/Qwen3-30B-A3B-FP8 and Qwen/Qwen3-30B-A3B-GPTQ-Int4 were each read. Each declares the registered architecture, hidden size 2048, 48 layers, 32 query heads, four KV heads, head dimension 128 and expert intermediate size 768. Each also specifies 128 experts, eight selected experts, silu, normalized top-k probabilities, epsilon 1e-6 and untied embeddings. All seven inspected configurations specify sparse step 1 and no MLP-only layers, consistent with constructing an expert MLP in every block; the new builder does not implement alternative sparse/dense schedules. [source; call_dc18cfe4286949b08379ae89bd3b260b, call_3b181a4f8c3b49e6ae29d825ac48d5f3, call_960a1020e1cd447093a016c1f7b1e9f7, call_0ab3f5534c5245ab8adc6e37f9be7a1a, call_88e3ed1441b04372b4a9c26de4734ae5, call_027cdf3d1d3846c2b24659bc2c8c4c71, call_8bef024055b14cee872b309f53b89339, call_89bad8e3d4694c5d9864789ba0f54f41]

A standard-library calculation gives query widths 4096 and 8192 for the 30B and 235B configurations, respectively, and KV width 512 for both. Their fallback head dimension would be 64 rather than the configured 128, showing why preserving explicit head_dim matters. This is integer shape arithmetic, not model execution. [execution; call_c7b9a95c4b414615b714082cb008032a]

Sampled BF16 headers agree with these dimensions. For 30B, layer-0 Q/K/V/O weights are [4096,2048], [512,2048], [512,2048] and [2048,4096]; for 235B they are [8192,4096], [512,4096], [512,4096] and [4096,8192]. Both contain Q/K norm weights [128] and routing-gate weights [128,hidden_size]. Sampled expert gate/up weights are [expert_intermediate,hidden_size] and down weights have the reverse orientation. Embedding and lm_head shapes are [151936,hidden_size], and sampled residual/final norm weights have hidden_size entries. [source; call_b10283b0200f4182b52aff02bb254c3f, call_fdd83a8173ab4fbd9f3a7b282ba66b8d, call_2fcb64425e114a379e4cd14c55e3116c, call_bce32e044e134de384ca1c426eebd5f3, call_53ee0a5802db426e84bae6195ea00207, call_0bffcefda0f34a39a4523a8a1e4fc1b0, call_9242235287534794a004e7d94965f8cc, call_c3bd9f0216074dfe9dd95ca9232d5728]

Reusing attention, expert dispatch and calibration avoids architecture-specific kernels, at the cost of inheriting their storage, fusion and routing constraints. This is a design interpretation, not evidence of a performance improvement. [inference; call_89bad8e3d4694c5d9864789ba0f54f41, call_cf72eb3dcebb46c492ad18e51318187d, call_85789c51b02c459784b12d5cbaa94964]

## Authoring-time findings — pending review

### inherited-all-expert-fused-shape (suspected; defect)

The new architecture retains BlockSparseMLP's conditional all-expert/fused-buffer cardinality mismatch.

Trigger: Forward one flattened token through fully EXL3 expert projections with activate_all_experts=True and num_experts unequal to num_experts_per_tok; the reference configurations use 128 versus eight.

Expected: Evaluate every expert for capture, or select an ordinary path that supports the all-expert count.

Actual: topk returns 128 expert indices but fused gate/up buffers have eight expert slots. exl3_mgemm checks the index dimension against the output expert dimension and rejects this combination. TransformerBlock.forward directly forwards params to the MLP; ParallelDecoderBlock is another parent-tree forwarding site, but the new model uses TransformerBlock. Conversion supplies the flag, although inspected code does not establish that ordinary conversion also supplies the fully EXL3, single-token conditions.

Locations: c6aa83f7e5a5e735c079d41244cbc704eda7e54e:exllamav3/modules/block_sparse_mlp.py — BlockSparseMLP.forward, a5caa423bbd9d8a61266a88fb237c18fb77ec0b8:exllamav3/models/qwen3_moe.py — Qwen3MoeModel.__init__

Source evidence: call_cf72eb3dcebb46c492ad18e51318187d, call_610dc55cab9e48bf82f707d56859385b, call_f9641e0f7cac4bafaa103a5b8e171746, call_e86e4e8d6a324a5ca7132e2b84ca1309, call_fa86a7a3557846ac870e30533824ab03, call_89bad8e3d4694c5d9864789ba0f54f41

source_inspection: Compared routing cardinality, fused allocations, native shape validation and decoder forwarding sites with the task's new builder and calibration flag. [call_cf72eb3dcebb46c492ad18e51318187d, call_610dc55cab9e48bf82f707d56859385b, call_e86e4e8d6a324a5ca7132e2b84ca1309, call_89bad8e3d4694c5d9864789ba0f54f41]. Limits: Conditional source path only; no tensor or CUDA execution.

scalar_transcription: Printed the reference configurations' all-expert index count 128 against fused output count eight. [call_c7b9a95c4b414615b714082cb008032a]. Limits: Integer dimension model, not execution of BlockSparseMLP or exl3_mgemm.

## Uncertainty and limits

No repository model construction, checkpoint loading, conversion, generation or CUDA execution was performed. The Python calculation checks transcribed integer dimensions only.

Tensor-header inspection sampled ordinary BF16 checkpoints for both dimensional configurations, not every expert, layer or shard. Complete tensor-name coverage, optional tensors and FP8/GPTQ checkpoint loading remain unverified.

No throughput, numerical-equivalence, conversion-quality or long-context accuracy measurement supports this annotation.
