# 1db3dce033981fe2d1825165a9389b3fdcd21b67


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/1db3dce033981fe2d1825165a9389b3fdcd21b67) · [Evidence ledger](draft.json)

Adds Qwen3ForCausalLM factory dispatch and a Llama-style builder with per-head Q/K RMSNorm. Reference metadata supports the dense dimensional mappings; runtime parity and FP8 loading compatibility remain unverified.

- [Qwen3 dispatch and per-head normalization](#models)

## Problem

The parent architecture registry has no Qwen3 entry. The change adds Qwen3ForCausalLM dispatch and a model builder that enables the existing per-head Q/K normalization mechanism. [source; call_d1fc751447c0476eb7810227c1b8a47c, call_832776fd9b2443ec92f38a1c6b4deb84, call_e946837a820743de974aebcd90f3c6ec]

## Reasoning

The new builder closely follows LlamaModel rather than Qwen2's thin subclass. Its significant architectural addition is a separate RMSNorm for each query and key head, using checkpoint keys self_attn.q_norm and self_attn.k_norm. [source; call_81596097bbea4cbaaa671164cfc70266, call_ccb76f846a94451fbe80302064920c2a, call_e946837a820743de974aebcd90f3c6ec]

## Impact

Config.from_directory can now select Qwen3Config through the registry; that config explicitly stores Qwen3Model as model_class, which Model.from_config instantiates. The registry edit and new module therefore jointly enable the normal factory path. [source; call_832776fd9b2443ec92f38a1c6b4deb84, call_e4b678c2f6524463bc52128f43982ba5, call_4127126a9d8349e48c42d4f7b09b78e3, call_fe48fff8b5ae4582bbdd3efc0ce622e6, call_e946837a820743de974aebcd90f3c6ec]

## Source Notes

Read the original models chapter and the Q/K-normalization entry. They establish the Llama-style construction being followed and the normalization capability this builder activates. The latter records an asymmetric constructor check for a K-only norm. [ancestor; call_64ee7d1739e246cabe20a07e5accbb08, call_05de82de161f46ae9f85bdf5449c8640]

The paired-normalization constructor branch remains unchanged: supplying Q requires K. Qwen3 supplies both modules, so its new construction satisfies that precondition and does not enter the K-only case recorded by the earlier entry. [source; call_16d44c64528f40c1ad459f36da9bb16e, call_e946837a820743de974aebcd90f3c6ec]

Issue #29, “Auto-YaRN for Qwen3? Maybe even set it dynamically?”, requests automatic or request-dependent scaling. Its connection here is inferred from the shared Qwen3 identifier and RoPE configuration: this patch uses the existing configuration reader, not a new automatic-scaling policy. In that discussion, turboderp describes batching and cache-reuse obstacles to dynamic scaling. [inference; call_ce7fd133ee2d4b4c8400b3fc751f0dbb, call_e946837a820743de974aebcd90f3c6ec, call_4127126a9d8349e48c42d4f7b09b78e3]

The other matching discussions do not establish motivation for this patch: PR #4, “chore: update config.py”, proposes a spelling correction; issue #7, “quantizing model: undefined symbol: __cxa_call_terminate”, reports an extension-import failure and the reporter's environment workaround. Their inferred connection is only the shared config.py dependency, not evidence that Qwen3 registration fixes either issue. [inference; call_161971c17c494d4192177b321c84417b, call_3f1662e7335d46eab7fc016e8a965e83, call_e946837a820743de974aebcd90f3c6ec]

<a id="models"></a>

## Qwen3 dispatch and per-head normalization

Qwen3Config retains the Llama configuration contract: explicit head_dim takes precedence, otherwise hidden_size // num_attention_heads is used; missing KV-head count defaults to query-head count. It requires the principal dimensions, layer count and RMS epsilon, accepts absent hidden_act but rejects a supplied value other than silu, and defaults embedding tying to false. RoPE settings use NEOX style through the common reader. [source; call_e946837a820743de974aebcd90f3c6ec, call_81596097bbea4cbaaa671164cfc70266, call_ca4b821ba8f24a72b21b3a863fe0609b, call_389e62d2447d412a8c5836a145b7fe34, call_a52515dd1f884258a58e1d1007f0b36e, call_4127126a9d8349e48c42d4f7b09b78e3]

The execution sequence is token embedding, sequential pre-normalized TransformerBlocks, final RMSNorm with half output, then vocabulary projection. Each block adds attention to the residual before normalizing and running the gated MLP. GatedMLP defaults to SiLU multiplication and uses gate_proj, up_proj and down_proj; attention uses separate q_proj, k_proj, v_proj and o_proj. [source; call_e946837a820743de974aebcd90f3c6ec, call_9b54d3c031754b1ea29271d8b4396769, call_1868db4532fc400a9d8b52fd31b2976f]

All three existing attention paths reshape Q and K into heads, apply the supplied RMSNorm modules with half output, and then apply RoPE. V is not normalized. RMSNorm flattens leading axes into rows, so each norm operates across head_dim rather than across the concatenated projection. The native wrapper requires matching weight width and a width divisible by four; the reference configurations' width 128 satisfies this dimensional guard. [source; call_16d44c64528f40c1ad459f36da9bb16e, call_a4d1b121ea294da392902e987bde5435, call_5bcfc29072634a0aaf36e354cc1bb3a5, call_dc265d6a6b3a41a78601899459f70297]

The new prepare_inputs hook preserves input_ids in params and delegates to prepare_for_attn, matching all seven existing direct callers found in the parent. None adds a caller-side guard omitted by Qwen3. The helper retains its backend checks: uncached modes reject a cache, while batch-shaped cached attention checks page alignment, capacity and the choice between past_len and cache_seqlens. [source; call_e946837a820743de974aebcd90f3c6ec, call_633c97f432c44ca3b17248bf238dc484, call_df331e523fe74b3587183f751dd9264c, call_81596097bbea4cbaaa671164cfc70266, call_16d44c64528f40c1ad459f36da9bb16e]

Qwen/Qwen3-0.6B, Qwen/Qwen3-0.6B-Base and Qwen/Qwen3-0.6B-FP8 each declare Qwen3ForCausalLM with hidden/intermediate widths 1024/3072, 16 query heads, eight KV heads, head_dim 128, 28 layers and tied embeddings. Each agrees with these constructor mappings; notably its attention width is 2048, not hidden_size. [source; call_dc265d6a6b3a41a78601899459f70297, call_c530fd33c7a4466ea224457693ced61b, call_931593eab8d0444db5014a2291b8a1bf, call_e946837a820743de974aebcd90f3c6ec]

Qwen/Qwen3-1.7B, Qwen/Qwen3-1.7B-Base and Qwen/Qwen3-1.7B-FP8 each agree with the mappings at widths 2048/6144, 16 query heads, eight KV heads, head_dim 128, 28 layers and tied embeddings. [source; call_0e715326593f4447a97bbb811130a100, call_c7ee7fa9ad2f4814ac74f980b2ee7d81, call_c8d07ee45276485a8e868ccd3880a44b]

Qwen/Qwen3-4B, Qwen/Qwen3-4B-Base and Qwen/Qwen3-4B-FP8 each agree at widths 2560/9728, 32 query heads, eight KV heads, head_dim 128, 36 layers and tied embeddings. Qwen/Qwen3-8B, Qwen/Qwen3-8B-Base and Qwen/Qwen3-8B-FP8 each agree at widths 4096/12288, the same head counts and layer count, but untied embeddings. [source; call_791de3958b94470491f8c82944255529, call_6aee1660ae5a4d27911f32dc937fddfd, call_f5859f98c03d4c92884eaaadefd2841a, call_d309878bb1944dc7b0b413b4374a8343, call_a7fc312fb6f24d8583424c2dcd76e690, call_1e966a361b1645c59639b4acafb38f47]

Qwen/Qwen3-14B, Qwen/Qwen3-14B-Base and Qwen/Qwen3-14B-FP8 each agree at widths 5120/17408, 40 query heads, eight KV heads, head_dim 128, 40 layers and untied embeddings. Qwen/Qwen3-32B and Qwen/Qwen3-32B-FP8 agree at widths 5120/25600, 64 query heads, eight KV heads, head_dim 128, 64 layers and untied embeddings. [source; call_7f74c53c71dd4d438701e1ddb1485c80, call_dbdc0e312e8e40128ed221782caa32ab, call_cee6e5a83ed44a6fa0029afb3360309b, call_76bb8e92ec79437591fb9fd73f3065c7, call_62b99b6846b3407c96d7f8017df9ae72]

All 17 inspected configs supply SiLU, RMS epsilon 1e-6, theta 1000000, vocabulary size 151936, null rope_scaling and disabled sliding-window attention. Thus none exercises the missing-head-dimension or missing-KV-head defaults. Base variants supply a 32768-position limit and EOS 151643; the other variants supply 40960 and EOS 151645. The FP8 variants additionally declare dynamic e4m3 quantization with 128×128 weight blocks. [source; call_dc265d6a6b3a41a78601899459f70297, call_c530fd33c7a4466ea224457693ced61b, call_931593eab8d0444db5014a2291b8a1bf, call_0e715326593f4447a97bbb811130a100, call_c7ee7fa9ad2f4814ac74f980b2ee7d81, call_c8d07ee45276485a8e868ccd3880a44b, call_791de3958b94470491f8c82944255529, call_6aee1660ae5a4d27911f32dc937fddfd, call_f5859f98c03d4c92884eaaadefd2841a, call_d309878bb1944dc7b0b413b4374a8343, call_a7fc312fb6f24d8583424c2dcd76e690, call_1e966a361b1645c59639b4acafb38f47, call_7f74c53c71dd4d438701e1ddb1485c80, call_dbdc0e312e8e40128ed221782caa32ab, call_cee6e5a83ed44a6fa0029afb3360309b, call_76bb8e92ec79437591fb9fd73f3065c7, call_62b99b6846b3407c96d7f8017df9ae72]

The six ordinary reference checkpoints' inspected first layers contain the expected q_norm.weight and k_norm.weight vectors of shape [128]. With H=hidden_size, I=intermediate_size and Q=query heads, their matrices match Q=[128Q,H], K/V=[1024,H], O=[H,128Q], gate/up=[I,H] and down=[H,I]. These are checkpoint-to-module shape correspondences, not numerical equivalence tests. [source; call_a1b4d15e3e42459cbbcc556627335a08, call_966079dc6e4f400bb86bcd0dadf7570d, call_d2fb5390330c4a9bbef4a95087ee1819, call_8fa647b813e9400cb7dc336c2ad99e09, call_4f923922c6ec4ddb9a7fd3af7b3910ba, call_519d58e61d0c4ffca0eedde9211c86a8, call_16d44c64528f40c1ad459f36da9bb16e, call_1868db4532fc400a9d8b52fd31b2976f]

The six FP8 headers preserve those first-layer dimensions and [128] Q/K norms, but store projection weights as F8_E4M3 alongside weight_scale_inv tensors. Those scale tensors are not consumed by the inspected Linear.load_fp16 implementation, so matching architecture names and shapes alone cannot establish FP8 checkpoint compatibility. [source; call_2a3491edbc5a4b2ba0262cdd2e88c918, call_c0fb1898934e4e18b940d8d86e5d2e8d, call_4ec8890097d842ee8ed6f96ab641a43a, call_2787fcefed66485dbbcc4bd4991c06ee, call_ee72713aacce4367a3edaef879d25461, call_96e161cc1c6240bfa9a6549999e8d83d, call_bbe84c83533045718baa2e07563f5958]

A bounded Python metadata calculation reproduced the projection dimensions and query-heads-per-KV-head ratios 2, 2, 4, 4, 5 and 8 for 0.6B through 32B. It also showed why explicit head_dim matters: fallback division would yield 64, 80 and 80 instead of 128 for 0.6B, 4B and 32B. All inspected projection dimensions are multiples of Linear's default 128-element padding unit. [execution; call_a37b0a97571642e8b2002a8eae0f8532, call_bbe84c83533045718baa2e07563f5958]

Reusing the shared builder pattern and attention backends avoids a new execution kernel, at the cost of duplicating most of LlamaModel's assembly. The likely reason for the separate builder is to activate checkpoint-specific Q/K norms without changing existing Llama or Qwen2 construction; this is an interpretation of the structural difference, not an explicit author explanation. [inference; call_e946837a820743de974aebcd90f3c6ec, call_81596097bbea4cbaaa671164cfc70266, call_ccb76f846a94451fbe80302064920c2a, call_c4741507e461436984794dbbc79dd5c1]

## Uncertainty and limits

No model loading, conversion, generation, CUDA execution, numerical parity test or performance benchmark was run.

Header inspection covers the embedding and first-layer tensors of one checkpoint per dimensional/storage configuration, not every layer or shard. Base-model headers were not independently compared.

FP8 configuration and header agreement does not establish FP8 loading support: the inspected Linear.load_fp16 path reads weights and optional biases, not weight_scale_inv tensors.

The arithmetic check uses transcribed metadata and Python integers; it does not execute repository tensor operations or reproduce floating-point kernel behavior.
