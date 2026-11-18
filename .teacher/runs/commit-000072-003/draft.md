# c44e56c73b2c67eee087c7195c9093520494d3bf


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/c44e56c73b2c67eee087c7195c9093520494d3bf) · [Evidence ledger](draft.json)

Adds GLM4 dispatch and construction using four-norm blocks, fused-source MLP weights, FP32 branch outputs and GPTJ partial RoPE. Reference dimensions match, but the new models reach an inherited partial-frequency bounds concern.

- [GLM4 construction, precision and checkpoint mapping](#models)

## Problem

The change adds Glm4ForCausalLM to architecture dispatch and supplies its configuration and model constructors. Config.from_directory can consequently select GLM4 instead of rejecting its architecture name. [source; call_5d16ebfbf5d34f418732e61c9bd7a7e0, call_36bc6d919b494d448036a7c0f1ae34b6]

## Reasoning

GLM4 is expressed through existing modules: separate attention projections, fused-source gate/up projections, four norms per block and GPTJ-style rotary embeddings. Registration and construction are complementary edits; neither alone provides the complete factory path. [source; call_5d16ebfbf5d34f418732e61c9bd7a7e0, call_1ad9eb442d4d443abcd80afa1e7df56d, call_c1fc037fc14747cbb5be8588aac77a69]

Reusing these primitives avoids a separate GLM execution implementation, but also exposes GLM checkpoints to the existing partial-RoPE frequency-read concern. [inference; call_1ad9eb442d4d443abcd80afa1e7df56d, call_79d0725509684d85b71542db1c12e009, call_e3c7714d314549c5b78dd5afc0071cb0]

## Impact

All six inspected GLM4-family configurations select the new registration. Representative tensor headers agree with its projection dimensions and checkpoint names; this establishes structural correspondence, not successful loading, conversion or generation. [source; call_c2ba4eaabacb4ad4b49642133f7ea581, call_febf46aea77d47b396a184e14fa8fa79, call_6f25a6e090e14bc5ba60fa6ee3232014, call_24b483487e5f41d48f8d95269723b82c, call_ed3433c433654ce4a0a6ce662f7383be, call_798c76bbcc0345f1b6297762b432a0cd, call_f2c8a61e42a74e12b9946b24a839c9d1, call_dd96e20bf0cf48ce8cc6c259ce7745b8, call_6ba0116097b4485b8ee9ff926b59e994]

## Source Notes

The root models entry documents the shared architecture factory, Phi3 fused-weight fallback and Gemma post-normalization construction. The DeciLM entry documents reuse of the same module and input-preparation interfaces. These entries supply historical context, not GLM execution evidence. [ancestor; call_2444df56b6bf47a79921f30214033e0f, call_a7125fdd151e4e9f939aad43ca5b07dd]

The GPTJ entry records native adjacent-pair rotation and an inherited partial-frequency bounds concern. The immediate-parent entry records FP32 linear outputs and an unsupported FP32 MLP-intermediate option. [ancestor; call_f0c2b8546d7d4a418954ac432f8fddc9, call_fa2de90c39ba40ada88caf0cca5e6efb]

Issue #7, “quantizing model: undefined symbol: __cxa_call_terminate,” reports an extension-import failure and a reporter-supplied environment workaround. Issue #15, “`cogito-v1-preview-qwen-32B` generates incoherent output for bpw <= 2.5,” discusses quantization regularization and reconversion. PR #4, “chore: update config.py,” proposes a spelling correction. None identifies GLM4 support as its remedy. [source; call_835fb7e2d69e4f18895fb150979d79dd, call_bdbe75ab37d7437bae72a82ccb5999c8, call_9abc0e289ff94c9a966d73bb1ec510c9]

<a id="models"></a>

## GLM4 construction, precision and checkpoint mapping

Glm4Config requires hidden size, query-head count, intermediate size, RMS epsilon and layer count. Missing KV-head count defaults to query-head count; missing or zero head_dim falls back to hidden_size // num_attention_heads. Tied embeddings default to false, and a supplied hidden_act must be silu. The shared RoPE reader carries theta, scaling, partial rotary factor and context limits, now with GPTJ style. [source; call_1ad9eb442d4d443abcd80afa1e7df56d, call_36bc6d919b494d448036a7c0f1ae34b6, call_50e52904d1bb463f95ed5fffcee4e1e3, call_2693942068a44bcb954b4132f9bdcc6c]

The module sequence is embedding, indexed transformer blocks, final RMSNorm and lm_head. Within each block, input_layernorm precedes attention, post_self_attn_layernorm follows attention before residual addition, post_attention_layernorm precedes the MLP, and post_mlp_layernorm follows it before the second residual addition. Both branches receive input norms, so this construction does not enter TransformerBlock's uninitialized-y case for a branch without a norm. [source; call_1ad9eb442d4d443abcd80afa1e7df56d, call_0ca37040fdf84b38a3260aef2d84691f]

Embedding defaults to FP32 output, establishing the residual stream. TransformerBlock explicitly requests FP16 pre-normalized branch inputs. GLM4 requests FP32 post-norm outputs and FP32 MLP down-projection output, while keeping gate/up intermediates FP16. The final norm returns FP16 for the output projection. Thus it uses the parent's new linear-output precision facility without enabling the incompatible FP32 MLP-intermediate setting. [source; call_1ad9eb442d4d443abcd80afa1e7df56d, call_a079c53d3c1049eca5b991d17c98d912, call_0ca37040fdf84b38a3260aef2d84691f, call_c175e70ee0d444efbe9e8d5a6d7e382c, call_c1fc037fc14747cbb5be8588aac77a69, call_3f6ce21b509b44e8a7c696390ac0b0cc]

Attention declares Q/K/V/O matrices with shapes [QD,H], [KD,H], [KD,H] and [H,QD]. GatedMLP first offers separate gate/up keys, then uses gate_up_proj as a fused source: rows [0,I) supply gate and [I,2I) supply up. Linear.load_fp16 slices that source along its first axis. Optional individual projection biases are loaded without an attention_bias constructor switch, covering the inspected 9B Q/K/V biases. [source; call_1ad9eb442d4d443abcd80afa1e7df56d, call_3e334f7374e74b6a83e012515d868a1d, call_c1fc037fc14747cbb5be8588aac77a69, call_3f6ce21b509b44e8a7c696390ac0b0cc, call_dd96e20bf0cf48ce8cc6c259ce7745b8]

The fused gate/up mechanism retains its existing prohibition on MLP slicing when intermediate_size exceeds MAX_MLP_INTERMEDIATE=55296. This constant is documented as a practical single-GPU quantization limit. Both GLM widths, 23040 and 13696, remain below it; the new call does not bypass the guard. [source; call_c1fc037fc14747cbb5be8588aac77a69, call_1c982ff3441741c89c0ee3bfc0692f5e, call_1ad9eb442d4d443abcd80afa1e7df56d, call_c2ba4eaabacb4ad4b49642133f7ea581, call_6f25a6e090e14bc5ba60fa6ee3232014]

zai-org/GLM-4-32B-0414, zai-org/GLM-4-32B-Base-0414 and zai-org/GLM-Z1-32B-0414 each declare H=6144, I=23040, 61 layers, 48 query heads, two KV heads and D=128. Each agrees with the constructor's dimensions and SiLU requirement, explicitly disables tied embeddings and attention biases, and supplies a 32768-position limit. The GLM-4-32B first-shard header matches embedding [151552,6144], Q/O [6144,6144], K/V [256,6144], fused gate/up [46080,6144], down [6144,23040] and four norm vectors of length 6144. [source; call_c2ba4eaabacb4ad4b49642133f7ea581, call_febf46aea77d47b396a184e14fa8fa79, call_24b483487e5f41d48f8d95269723b82c, call_f2c8a61e42a74e12b9946b24a839c9d1, call_1ad9eb442d4d443abcd80afa1e7df56d]

zai-org/GLM-4-9B-0414 and zai-org/GLM-Z1-9B-0414 each declare H=4096, I=13696, 40 layers, 32 query heads, two KV heads and D=128. Both fit the constructor's dimensions and defaults, with explicit SiLU, untied embeddings, attention_bias=true and a 32768-position limit. The inspected GLM-4-9B header matches Q/O [4096,4096], K/V [256,4096], fused gate/up [27392,4096], down [4096,13696], four 4096-element norms, and Q/K/V biases of lengths 4096/256/256. [source; call_6f25a6e090e14bc5ba60fa6ee3232014, call_ed3433c433654ce4a0a6ce662f7383be, call_dd96e20bf0cf48ce8cc6c259ce7745b8, call_1ad9eb442d4d443abcd80afa1e7df56d]

zai-org/GLM-Z1-Rumination-32B-0414 retains the 6144/23040 widths, 61 layers and 48 query heads, but supplies eight KV heads and a 131072-position limit. These values are read rather than replaced by the other 32B models' defaults. Its inspected first-layer header matches K/V [1024,6144], with the same Q/O, fused MLP and norm shapes as the other 32B layout. No inspected tensor name in these representative header portions lacks a corresponding loading path. [source; call_798c76bbcc0345f1b6297762b432a0cd, call_6ba0116097b4485b8ee9ff926b59e994, call_1ad9eb442d4d443abcd80afa1e7df56d, call_3f6ce21b509b44e8a7c696390ac0b0cc, call_c175e70ee0d444efbe9e8d5a6d7e382c]

All six configurations explicitly use head_dim=128, partial_rotary_factor=0.5, rope_theta=10000 and rms_norm_eps=1e-5. RoPE therefore builds 32 inverse frequencies for 64 rotated channels. GPTJ pairs adjacent channels rather than split halves, rotating the first 64 channels and copying the remaining 64. The native source still reads inv_freq[t] before deciding whether a thread only copies an unrotated pair. [source; call_c2ba4eaabacb4ad4b49642133f7ea581, call_febf46aea77d47b396a184e14fa8fa79, call_6f25a6e090e14bc5ba60fa6ee3232014, call_24b483487e5f41d48f8d95269723b82c, call_ed3433c433654ce4a0a6ce662f7383be, call_798c76bbcc0345f1b6297762b432a0cd, call_79d0725509684d85b71542db1c12e009, call_e3c7714d314549c5b78dd5afc0071cb0]

A standard-library scalar transcription reproduced the three projection layouts and query-heads-per-KV-head ratios 24, 16 and 6. It also counted 64 launched x indices versus 32 frequencies, leaving source-level indices 32–63 outside the frequency array for every inspected configuration. This was arithmetic validation, not execution of RoPE or a GPU memory test. [execution; call_74d5348874e64bab91acb51928ab3e62]

prepare_inputs retains input_ids in params and delegates to prepare_for_attn, exactly as the inspected Llama, Phi3, Gemma and DeciLM callers do. It omits no additional caller-side guard present in those implementations. The shared helper defaults to cache-free FlashAttention, rejects caches in cache-free modes, validates the batch-shaped cached mode and rejects unknown modes. [source; call_1ad9eb442d4d443abcd80afa1e7df56d, call_1173ce2a8bfe4f7c9723db310da5fa32, call_91480880654f4117a689d55850f84529, call_8fb3571bde9b42c9b48de17792617afb, call_624878fab22f4aeca1bd9dc3667d9d6f, call_72abdc16006f4b1badefa6c6ee5810cb, call_3e334f7374e74b6a83e012515d868a1d]

## Authoring-time findings — pending review

### glm4-partial-rope-frequency-read (suspected; defect)

GLM4's partial rotary configuration reaches the inherited unconditional frequency read outside the rotated-channel guard. The task leaves this native code unchanged.

Trigger: Attention executes native RoPE for any inspected GLM4-family configuration: head_dim=128 and partial_rotary_factor=0.5.

Expected: Threads copying the unrotated channels should not index beyond the 32-element inverse-frequency array.

Actual: rope launches 64 x threads and rope_kernel evaluates inv_freq[t] before its rotation/copy branch. Source-level indices 32–63 exceed the array. The inspected SDPA, cache-free FlashAttention and cached FlashAttention methods all call RoPE.apply, which calls ext.rope; actual compiled GPU consequences remain untested.

Locations: c44e56c73b2c67eee087c7195c9093520494d3bf:exllamav3/models/glm4.py — Glm4Config.__init__, e9a3b6a9256fc59f888b80a7d4a58883954b39de:exllamav3/exllamav3_ext/rope.cu — rope_kernel

Source evidence: call_1ad9eb442d4d443abcd80afa1e7df56d, call_79d0725509684d85b71542db1c12e009, call_e3c7714d314549c5b78dd5afc0071cb0, call_3e334f7374e74b6a83e012515d868a1d, call_2ffe2e89dc3d425390ab5af6f47b5bf0, call_f28abe4a14274b898f9239191e54a725

source_inspection: Compared the task configuration mapping with parent frequency construction, native launch and kernel read; searched the parent tree for native RoPE and attention callers and inspected all three attention call sites. [call_1ad9eb442d4d443abcd80afa1e7df56d, call_79d0725509684d85b71542db1c12e009, call_e3c7714d314549c5b78dd5afc0071cb0, call_2ffe2e89dc3d425390ab5af6f47b5bf0, call_f28abe4a14274b898f9239191e54a725, call_3e334f7374e74b6a83e012515d868a1d]. Limits: Establishes a source-level reachable bounds concern, not a measured device fault.

scalar_transcription: Computed partial dimension, frequency count, launched x range and out-of-range indices from the inspected expressions and configuration values. [call_74d5348874e64bab91acb51928ab3e62]. Limits: Python integer arithmetic only; does not model compiler optimization, CUDA execution or memory allocation.

## Uncertainty and limits

No model loading, conversion, PyTorch inference or CUDA execution was performed. The Python computation checks transcribed dimensions and indexing only.

Tensor inspection covers representative first-shard tensors for the three distinct configuration layouts, not every layer or final head. Headers establish names, shapes and stored BF16 dtype, not fused-row semantics or numerical equivalence.

The actual compiled-kernel consequences of the partial-frequency read are unmeasured; compiler optimization and device-memory behavior were not tested.

The numerical benefit or performance cost of GLM4's FP32 branch outputs was not measured.
