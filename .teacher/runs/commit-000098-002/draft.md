# 875e503e84ddf27441f551a2c7dc50982c8cd48c


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/875e503e84ddf27441f551a2c7dc50982c8cd48c) · [Evidence ledger](draft.json)

Registers Cohere models using parallel decoder blocks, LayerNorm and scaled logits; reference inspection exposes missing Command R+ Q/K normalization and distinguishes dense checkpoints from unsupported bitsandbytes storage.

- [Cohere architecture assembly and checkpoint compatibility](#models)

## Problem

CohereForCausalLM needs an architecture registration and a constructor mapping its checkpoint tensors to shared modules. [source; call_007e13b535714f2291fa9b3baa9df907, call_cae5db434bca4573862b9b0a35311bb6]

## Reasoning

The implementation combines shared-input parallel decoder blocks, LayerNorm, GPTJ-style RoPE and output-logit scaling rather than introducing new attention kernels. Reusing these components reduces architecture-specific execution code, but also inherits their limits. [inference; call_cae5db434bca4573862b9b0a35311bb6, call_8ce7bc11687a4297a3436ef7977a5158, call_0efe00ff77a94998a14817dc08d9a68d]

## Impact

Config.from_directory can now select CohereConfig, whose model_class is CohereModel. Registration does not establish compatibility with every checkpoint declaring CohereForCausalLM: Command R+ requires Q/K normalization absent from the selected Attention implementation. [source; call_007e13b535714f2291fa9b3baa9df907, call_975ac99230d5424d816387cd6e6dd32f, call_cae5db434bca4573862b9b0a35311bb6, call_49a4d09a1fb44909afa10d2b7c054eec, call_0efe00ff77a94998a14817dc08d9a68d]

## Source Notes

The parallel-decoder ancestor records shared-normalization composition and conditional failures for missing components or plain MLP allocation. The output-scale ancestor establishes the previously unused post_scale mechanism. The original models chapter describes the common architecture factory and checkpoint-mapping pattern. [ancestor; call_44e5a1165ac3406bb0841cbf67a34c70, call_161ade8503b04a8cb4e084d52906e2b1, call_5d33466ef3be438ab7bbaa2d99ef794f]

Those parallel-block inconsistencies remain in the unchanged implementation, but Cohere supplies all three components and uses GatedMLP, avoiding the recorded triggers. [source; call_cae5db434bca4573862b9b0a35311bb6, call_8ce7bc11687a4297a3436ef7977a5158]

Parent-tree Cohere occurrences include the architecture roadmap and an existing chat template; architecture execution support is distinct from prompt formatting. [source; call_dcf3470ba45a45099e85fcc8a1f62456, call_007e13b535714f2291fa9b3baa9df907]

The inspected discussions are “quantizing model: undefined symbol: __cxa_call_terminate,” “`cogito-v1-preview-qwen-32B` generates incoherent output for bpw <= 2.5,” and “Build Failure on Windows: CUDA 12.4 / PyTorch 2.7.0+cu126 / VS 2022.” They concern extension loading, quantization quality and compilation, respectively; none identifies this Cohere addition as its remedy. [source; call_446c6a494cb246bf95ff99bcc012777e, call_170feb4dd7cd47f0abce771f5d77bf19, call_143282b6959a454b8b2ca6f5d46c12ca]

<a id="models"></a>

## Cohere architecture assembly and checkpoint compatibility

Dispatch remains based on the single architectures entry in config.json. The new registry entry selects CohereConfig; Model.from_config then constructs its CohereModel. The registration and constructor are complementary: the former exposes the latter through the normal factory. [source; call_007e13b535714f2291fa9b3baa9df907, call_975ac99230d5424d816387cd6e6dd32f, call_98b8d0c4a9054fe2bd7b82704a139e6c, call_cae5db434bca4573862b9b0a35311bb6]

CohereConfig reads residual width, MLP width, layer count and query/KV head counts. Missing KV count defaults to query count; missing or zero head_dim becomes hidden_size // num_attention_heads. It permits absent hidden_act but rejects a supplied value other than silu. LayerNorm epsilon defaults to 1e-5, tied embeddings to true, and logit_scale to 0.0625. Shared RoPE configuration reads theta, scaling and position limits, with GPTJ style supplied by Cohere. [source; call_cae5db434bca4573862b9b0a35311bb6, call_975ac99230d5424d816387cd6e6dd32f]

Each block computes y = LayerNorm(x), then x += Attention(y) and x += GatedMLP(y). Both branches consume the same normalized input; “parallel” denotes their dependency structure, not concurrent scheduling. The normalizer requests half output. The final model.norm also produces half output before lm_head. [source; call_cae5db434bca4573862b9b0a35311bb6, call_8ce7bc11687a4297a3436ef7977a5158, call_364985f6716f4e6a9153f30b3ca279a1]

Checkpoint names are model.embed_tokens, model.layers.i.input_layernorm, self_attn.{q,k,v,o}_proj, mlp.{up,gate,down}_proj, model.norm and lm_head. For residual width H, intermediate width I and head width D, Attention constructs Q [QD,H], K/V [KD,H] and O [H,QD] projections. The head offers model.embed_tokens as an alternate key when tying is enabled and the constructor's lm_head check fails; Linear still tries its primary key before the alternate within each supported storage path. [source; call_cae5db434bca4573862b9b0a35311bb6, call_0efe00ff77a94998a14817dc08d9a68d, call_9340ae05aaa04911848d120a0f6fc7ad]

logit_scale is passed to Linear.post_scale, which multiplies the backend output in place after optional softcapping. Cohere supplies no softcap, so its head applies a direct output multiplier, not a weight-storage transformation. head_bits remains the separate head quantization budget. [source; call_cae5db434bca4573862b9b0a35311bb6, call_9340ae05aaa04911848d120a0f6fc7ad]

prepare_inputs follows the inspected Llama, Phi3, Gemma, GLM4 and DeciLM call sites: retain input_ids in params, then call prepare_for_attn without additional guards. The helper defaults to uncached FlashAttention, rejects caches for uncached modes, and checks batch-shaped cached requests. Model.prefill sets prefill only at the last KV-affecting block; ParallelDecoderBlock then returns after attention's residual addition and skips its MLP. [source; call_b4e23dbb214c4e0992a4e56dd2ee44e6, call_74f8eee9778b4b26aa03e0c294360f18, call_0efe00ff77a94998a14817dc08d9a68d, call_98b8d0c4a9054fe2bd7b82704a139e6c, call_8ce7bc11687a4297a3436ef7977a5158]

CohereLabs/aya-23-8B supplies H=4096, I=14336, 32 layers and Q/K=32/8; aya-23-35B supplies H=8192, I=22528, 40 layers and Q/K=64/64. Both use epsilon 1e-5, scale 0.0625 and use_qk_norm=false. Their sampled projection and MLP headers agree with the constructor dimensions; the 8B embedding is [256000,4096]. [source; call_94593f009e8e4abba94ef77c5b3e6199, call_2db3d65ff7724a86b3c4f06c3b0330f4, call_183f88967cab4ab18ce99f7195b3d250, call_dfd7350a32c24d4b9224d5bb86b8aae4]

CohereLabs/aya-expanse-8b retains the 4096/14336, 32-layer, 32/8-head dimensions but explicitly changes scale to 0.125, which overrides the default. aya-expanse-32b uses H=8192, I=24576, 40 layers and 64/8 heads with scale 0.0625. Both disable Q/K normalization. Sampled headers match their respective dimensions, including K/V width 1024. [source; call_08a2f72cecae4df3978f3f0b82071986, call_dac6c9f8c1ac41fb834cc076f00e8d25, call_f1f544a25d0140daac0615cc70e432ca, call_5bf2bf7e2d754bf089c0a3d0b7bf921d]

CohereLabs/c4ai-command-r-v01 uses the 8192/22528, 40-layer, 64/64-head layout, explicitly ties embeddings and specifies scale 0.0625. Its sampled embedding and square attention matrices match. c4ai-command-r-08-2024 instead uses I=24576 and eight KV heads, matching its sampled [1024,8192] K/V matrices; its config disables Q/K normalization and retains scale 0.0625. [source; call_9651902e135f4363842d9a130fedfb13, call_1fd566b0c4c8413ab3dfd6e6dbed7607, call_34b2d9df655d490cac7379d0851b541c, call_52a4d44ddcdb4c8c817f6617b8712b1e]

CohereLabs/c4ai-command-r-plus and c4ai-command-r-plus-08-2024 both use H=12288, I=33792, 64 layers, 96/8 heads and scale 0.8333333333333334. Their sampled linear matrices match those dimensions, but both enable use_qk_norm and store q_norm.weight [96,128] and k_norm.weight [8,128]. The new constructor and shared Attention never load or apply those tensors. [source; call_49a4d09a1fb44909afa10d2b7c054eec, call_a1082472c24a4a42b4c96f01c41dc645, call_19da404c81d643aba855b6c3aa58f41f, call_11ba769cf989423b9e4c078d7e5cb647, call_cae5db434bca4573862b9b0a35311bb6, call_0efe00ff77a94998a14817dc08d9a68d]

CohereLabs/c4ai-command-r-v01-4bit and c4ai-command-r-plus-4bit retain their corresponding base dimensions and scales but declare bitsandbytes FP4 storage. Sampled MLP weights are U8 [92274688,1] and [207618048,1], not dense [I,H] matrices. Their absmax, quant_map and quant_state.bitsandbytes__fp4 tensors have no reader in the inspected Linear loading paths, which implement EXL3 or ordinary weights rather than bitsandbytes decoding. [source; call_380772f5bc6444858e175ab6f7ec96db, call_53c26225f97f439084742913bf76354a, call_59a083dbeea44ab58ba52d3c24dd35c4, call_ddb7732d382e445b89e9702c52755e85, call_9340ae05aaa04911848d120a0f6fc7ad]

A scalar metadata check derived head_dim=128 for all four distinct dimension families and verified that their linear widths, including vocabulary size 256000, are multiples of Linear's 128-element padding unit. It also evaluated the configured scales as 1/16, 1/8 and 5/6 and reproduced the two packed MLP element counts as H×I/2. [execution; call_bfeaa3de8504466abb2555975c9a6efa, call_9340ae05aaa04911848d120a0f6fc7ad]

## Authoring-time findings — pending review

### cohere-qk-normalization-omitted (suspected; defect)

Architecture registration includes Command R+ configurations requiring Q/K normalization, but the constructed attention path omits it.

Trigger: Construct and run a CohereForCausalLM checkpoint with use_qk_norm=true, such as either inspected dense Command R+ release.

Expected: Apply the checkpoint's Q/K normalization or explicitly reject that unsupported configuration.

Actual: CohereConfig does not read or reject use_qk_norm. Attention projects and reshapes Q/K, then applies RoPE; all three attention implementations retain TODO comments for Q/K norms. Stored q_norm and k_norm weights are unused.

Locations: 875e503e84ddf27441f551a2c7dc50982c8cd48c:exllamav3/models/cohere.py — CohereModel.__init__, 2bc4822f61e3fce361ba56df0ef413c7a16061d1:exllamav3/modules/attn.py — Attention.forward

Source evidence: call_cae5db434bca4573862b9b0a35311bb6, call_0efe00ff77a94998a14817dc08d9a68d, call_49a4d09a1fb44909afa10d2b7c054eec, call_a1082472c24a4a42b4c96f01c41dc645, call_19da404c81d643aba855b6c3aa58f41f, call_11ba769cf989423b9e4c078d7e5cb647

source_inspection: Compared configs and tensor headers with the new constructor and every Attention decode branch. Parent-tree search found no use_qk_norm consumer. Direct attention callers are the sequential and parallel blocks; Cohere installs the latter, reached by Model.forward and Model.prefill. [call_1ea443467d30448688be59f59ad998e7, call_dc53e9a9fad94d678f6a8483ed93da86, call_8ce7bc11687a4297a3436ef7977a5158, call_98b8d0c4a9054fe2bd7b82704a139e6c]. Limits: No model execution or generated-output comparison; the numerical impact is unmeasured.

## Uncertainty and limits

No repository model execution, checkpoint loading, GPU kernel test, generation-quality comparison or performance measurement was performed.

Header inspection sampled named tensors from each reference checkpoint, not every shard or tensor. Matching dimensions do not prove numerical equivalence or rotary-coordinate semantics.

The arithmetic check uses Python integers and scalar floating point; it does not model FP16 rounding or CUDA execution.

Reference configuration and header bytes are supplied hash-verified mirror evidence, not locally executed model artifacts.
