# c82af98d57c4ffd21b67baad0eb89a5ed9091759


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/c82af98d57c4ffd21b67baad0eb89a5ed9091759) · [Evidence ledger](draft.json)

Fuses Q/K head normalization into RoPE and repairs output comparisons in tests. Performance is unmeasured; inspection identifies overwritten normalization settings, a shared reduction race and padded input-read concerns.

- [Fused head normalization and rotary execution](#rope)

## Problem

Attention previously launched separate Q/K RMSNorm operations before RoPE. This change combines normalization and rotation in the rotary kernel. [source; call_b695234c7a8c482b813b72ad7971611a, call_7c87294f88f54572ac145f7f3beaf808]

## Reasoning

Keeping each head in shared memory permits normalization followed by rotation before writing it back. Avoiding separate normalization outputs and launches is a plausible performance motivation, not a measured speedup. [inference; call_7c87294f88f54572ac145f7f3beaf808, call_b695234c7a8c482b813b72ad7971611a]

## Impact

All three Attention decode routes pass loaded normalization weights into RoPE when present; without RoPE they retain separate RMSNorm calls. Tests now compare returned outputs and enable both rotary styles, but source inspection identifies normalization-parameter, reduction and bounds concerns. [source; call_b695234c7a8c482b813b72ad7971611a, call_c5f0239bc487498a80203d11b474ba4c, call_7c87294f88f54572ac145f7f3beaf808]

## Source Notes

Read the initial modules entry, native GPTJ entry, GPTJ-reference entry and immediately preceding BlockSparseMLP entry. They establish the existing rotation conventions, normalization interface and previously recorded reference, frequency-read and persistent-workspace limitations. [ancestor; call_107e641f665a4c4b8d7183c17212524b, call_d3d90fd7c7804893a68f3487d777c265, call_fd27736a185344209902761263fcccf6, call_e230cd570c014cbb83aa5065e048f8a6]

Issue #7, “quantizing model: undefined symbol: __cxa_call_terminate,” and closed issue #6, “No ROCm runtime is found, using ROCM_HOME='/usr',” concern installation/import failures. Their connection here is inferred only from rope.py traceback overlap. Issue #29, “Auto-YaRN for Qwen3? Maybe even set it dynamically?”, concerns scaling policy in that file, not normalization fusion. [inference; call_b45e56029963457c8e8f5dc4adc1ce6f, call_c8d35f7374fd49e089610409824963d3, call_47d619ae90a047abb28bde6881d858bc, call_af1bc25881064fe7ba463e9d79d87aef]

Closed issue #16, “RuntimeError: CUDA error: invalid configuration argument,” reports conversion failure attributed in the discussion to tokenizer truncation. Its inferred connection is the attention traceback path, not evidence that this kernel change addresses that failure. [inference; call_121ddfc0ed2b4ccb85b8a94cf9a7869b, call_b695234c7a8c482b813b72ad7971611a]

<a id="rope"></a>

## Fused head normalization and rotary execution

RoPE.apply adds optional Q/K normalization tensors, epsilon and constant bias, forwarding them to the extended native declaration. Its existing contiguity, allocation and return handling remains. Whole-tree searches found the sole ext.rope call in this wrapper; the binding still exposes the native function directly. [source; call_af1bc25881064fe7ba463e9d79d87aef, call_98ea14adc4eb4157a8953ccf10229212, call_5c4f0c491e9d4844a0ac11af5c1f52e1, call_e2bc93e68d084acf82515b2bd6202978, call_a153613c9ba64e22b1bb22c476151c19]

Attention.load captures the loaded RMSNorm weight data; unload clears those references. SDPA, uncached FlashAttention and cached FlashAttention all pass these tensors through an in-place RoPE call. These edits are coupled: replacing separate normalization requires both loaded weights and the extended wrapper/kernel interface. [source; call_b695234c7a8c482b813b72ad7971611a, call_ea5d96f191024e0f99714b204f99a9d7, call_65a56009c4d2468d9398ca9fc1b4b6fa]

The unchanged science/kv_quant_exp.py caller still supplies only positional arguments and therefore selects the new no-normalization defaults. The three production Attention callers and tests are updated. Qwen3 and Qwen3 MoE construct paired zero-bias norms using config.rms_norm_eps; Gemma3 constructs paired norms with constant_bias=1.0. These constructors expose why preserving the supplied normalization settings matters. [source; call_0840e11e43c3478989eb7cf379fe0e1e, call_a4a7521cb2694db68c9dbaf608412820, call_e4cefe49b21f4a35ac5b544c3a7371ba, call_98b73c3af155480990f50e86f7ef758a, call_1dd57e6a099848bc939c56588f640a35, call_a3d150db22c9498bb21f075f9f5a9840]

Each block covers one token and batch element. The x dimension is rounded to 32-thread warps, with each thread handling two half elements; consequently shared head storage is padded to multiples of 64 elements. The y dimension distributes Q and K heads under the existing 1024-thread cap. Heads are loaded into shared memory, optionally normalized, rotated and stored. [source; call_7c87294f88f54572ac145f7f3beaf808, call_9c4c8e9031994297ac23675c9fa2d34f]

Normalization computes reciprocal sqrt(mean(x²)+epsilon), converts normalized values to half, then multiplies by half-precision weight plus constant bias. Rotation uses float intermediates: NEOX pairs t with t+partial_head_dim/2; GPTJ pairs adjacent channels. Only the rotary prefix is modified after normalization, so the remainder retains its normalized values. [source; call_7c87294f88f54572ac145f7f3beaf808]

The separate RMSNorm alternative flattens heads into rows and invokes a native kernel with float weight/scaling arithmetic and a final output conversion; it also applies a clamp helper to half inputs. The fused path instead rounds before half weight multiplication. The formulas therefore do not imply bitwise equivalence, even apart from the recorded correctness concerns. [source; call_ea5d96f191024e0f99714b204f99a9d7, call_40247a4f019f4db3875fe143954c64b2, call_7c87294f88f54572ac145f7f3beaf808]

Tests repair the previously discarded-return comparison, enable GPTJ and NEOX, and parameterize normalization on/off. The reference explicitly normalizes before rotating. Tolerances change from 1e-6 to 3e-3; all query-only cases are removed. Existing scalar, per-batch and explicit-token position cases remain. [source; call_c5f0239bc487498a80203d11b474ba4c, call_f80c039b042e483fa8506b5726125d73]

The auxiliary edits remove the RMSNorm specialization TODO and replace BlockSparseMLP's output-dtype fallback expression. They do not alter the MLP dispatch, persistent output ownership or per-call dtype handling. [source; call_54fb83564a6649468753076253c0eadf, call_693c246646fd4604b0ff6f69736b3e56, call_7494838537624e73885bc637c15f7082]

## Authoring-time findings — pending review

### normalization-settings-overwritten (suspected; defect)

Attention overwrites the normalization settings it just copied from Q norm.

Trigger: Use RoPE with paired head norms whose epsilon differs from 1e-6 or whose constant bias is nonzero; Gemma3 supplies bias 1.0.

Expected: The fused path preserves the supplied RMSNorm epsilon and bias.

Actual: Later constructor assignments reset norm_eps to 1e-6 and norm_constant_bias to 0.0. All three decode routes forward those reset values. Qwen3 and Qwen3 MoE agree on zero bias but lose any nondefault configured epsilon; Gemma3 loses its explicit unit bias.

Locations: c82af98d57c4ffd21b67baad0eb89a5ed9091759:exllamav3/modules/attn.py — Attention.__init__

Source evidence: call_b695234c7a8c482b813b72ad7971611a, call_e4cefe49b21f4a35ac5b544c3a7371ba, call_a3d150db22c9498bb21f075f9f5a9840, call_98b73c3af155480990f50e86f7ef758a, call_1dd57e6a099848bc939c56588f640a35

source_inspection: Compared constructor assignment order, all matched head-norm construction sites and the three decode consumers. [call_b695234c7a8c482b813b72ad7971611a, call_65a56009c4d2468d9398ca9fc1b4b6fa]. Limits: No model execution.

### warp-sum-store-race (suspected; defect)

Every lane stores its shuffle-down reduction result to the same shared warp-sum slot.

Trigger: Enable fused normalization with nonuniform per-lane square sums.

Expected: Store the complete warp sum once, as the existing block_reduce_sum_f caller does with lane_id==0.

Actual: apply_norm omits that guard. Different lane results compete for sums[warps*t_head+warp_id], which is subsequently used for normalization. This reaches normalization-enabled Attention and test calls through RoPE.apply.

Locations: c82af98d57c4ffd21b67baad0eb89a5ed9091759:exllamav3/exllamav3_ext/rope.cu — rope_kernel::apply_norm

Source evidence: call_7c87294f88f54572ac145f7f3beaf808, call_31d40665fa954a828cf56a027fb3adfc, call_693ff7ef4b404e0eb505c22dad6e0434

source_inspection: Read both existing warp_reduce_sum_f calls in block_reduce_sum_f; the shared-memory store there is lane-zero guarded, unlike the new call. [call_31d40665fa954a828cf56a027fb3adfc, call_7c87294f88f54572ac145f7f3beaf808]. Limits: No GPU race detection or observed output.

scalar_transcription: A Python shuffle-down model with inputs 1 through 32 produced lane results 528, 544 and 1024 at lanes 0, 1 and 31; only lane zero matched the expected total 528. [call_6f31dbedb1394e37bba8cf6c7cf8f7fd]. Limits: Models lane arithmetic, not device store ordering.

### padded-thread-read-bounds (suspected; defect)

Warp padding broadens the inherited unguarded frequency-read concern and introduces unguarded normalization-weight reads for padded lanes.

Trigger: Use a head dimension not divisible by 64, such as the new 80-wide test, or use partial rotary frequencies shorter than the launched x dimension.

Expected: Inactive lanes avoid frequency and weight reads outside their logical arrays.

Actual: All x threads read inv_freq[t], and normalization reads a half2 weight without a head-width guard. For D=80, 64 threads address a 40-element full-width frequency array and 128 half-weight elements despite an 80-element norm vector. The shared activation load is padded, but these input arrays are not.

Locations: c82af98d57c4ffd21b67baad0eb89a5ed9091759:exllamav3/exllamav3_ext/rope.cu — rope_kernel

Source evidence: call_7c87294f88f54572ac145f7f3beaf808, call_c5f0239bc487498a80203d11b474ba4c, call_5c4f0c491e9d4844a0ac11af5c1f52e1, call_0840e11e43c3478989eb7cf379fe0e1e

scalar_transcription: Counted excess frequency indices and half-weight elements for dimensions 32, 64, 80, 96, 128 and 256 using the inspected launch formula. [call_6f31dbedb1394e37bba8cf6c7cf8f7fd]. Limits: Source-level bounds analysis, not evidence of an observed CUDA fault or compiler-emitted load.

### inherited-reference-input-limits (suspected; defect)

The previously recorded optional-K and partial-width reference failures remain; the test change removes query-only coverage rather than repairing the reference.

Trigger: Call apply_torch(q, None), or use full-width 128-channel Q/K with partial_rotary_factor=0.5.

Expected: Rotate Q without K, or rotate the 64-channel prefix while preserving the tail.

Actual: The first case reaches unconditional k.float(); the second multiplies full-width inputs by 64-wide coefficients. apply_torch is unchanged by this task. Its sole matched repository caller remains the test, which now supplies K and full rotary width.

Locations: c82af98d57c4ffd21b67baad0eb89a5ed9091759:exllamav3/util/rope.py — RoPE.apply_torch

Source evidence: call_5c4f0c491e9d4844a0ac11af5c1f52e1, call_af1bc25881064fe7ba463e9d79d87aef, call_58ae7f39beaf476eb80a495ee3dbcf5b, call_c5f0239bc487498a80203d11b474ba4c

source_inspection: Compared the inherited reference implementation with the complete wrapper and test diffs; the discarded-return defect is removed, but these input limitations are carried over. [call_5c4f0c491e9d4844a0ac11af5c1f52e1, call_c5f0239bc487498a80203d11b474ba4c]. Limits: No Torch execution.

### inherited-all-expert-workspace-mismatch (suspected; defect)

The MLP dtype-expression cleanup leaves the previously recorded all-expert workspace mismatch unchanged.

Trigger: One flattened token, quantized fused experts, activate_all_experts=True and num_experts different from num_experts_per_tok.

Expected: Allocate matching expert planes or select the ordinary path.

Actual: Native routing returns num_experts selections, while persistent expert buffers retain num_experts_per_tok planes. The fused dispatch does not check activate_all_experts. Generic decoder callers forward params, but this does not establish that default workflows request the failing combination.

Locations: c82af98d57c4ffd21b67baad0eb89a5ed9091759:exllamav3/modules/block_sparse_mlp.py — BlockSparseMLP.forward

Source evidence: call_7494838537624e73885bc637c15f7082, call_c2b40230975a4154909f259616cf28a6, call_693c246646fd4604b0ff6f69736b3e56, call_b24e5af4674743c182770f72f7390f4c, call_232abb3986c643c5a1e13c2f8c6c1413

source_inspection: Compared routing cardinality, buffer dimensions, dispatch and decoder call sites with the one-line task edit. [call_7494838537624e73885bc637c15f7082, call_c2b40230975a4154909f259616cf28a6, call_693c246646fd4604b0ff6f69736b3e56]. Limits: No multi-GEMM execution.

### inherited-persistent-output-contract (suspected; behavior_change)

The earlier fused MLP output ownership and dtype behavior remains unchanged.

Trigger: Retain a fused result across another call, or request an out_dtype different from the load-time workspace dtype.

Expected: An independently retained result and an honored per-call dtype override.

Actual: The returned view aliases reusable cfg.out_d and does not apply the per-call override. Inspected decoder callers consume the result immediately and omit the override, so they do not demonstrate a failure from these conditions.

Locations: c82af98d57c4ffd21b67baad0eb89a5ed9091759:exllamav3/modules/block_sparse_mlp.py — BlockSparseMLP.forward

Source evidence: call_7494838537624e73885bc637c15f7082, call_693c246646fd4604b0ff6f69736b3e56, call_232abb3986c643c5a1e13c2f8c6c1413

source_inspection: Traced the unchanged returned slice to load-time storage and inspected both matched decoder consumers. [call_7494838537624e73885bc637c15f7082, call_232abb3986c643c5a1e13c2f8c6c1413]. Limits: No tensor lifetime or dtype execution test.

## Uncertainty and limits

No CUDA build, repository test, model inference or performance benchmark was executed.

The Python check models integer bounds and shuffle arithmetic; it does not execute CUDA, establish race outcomes or reproduce FP16 rounding and device scheduling.

Literal repository searches cover inspected callers, not dynamic or external consumers. Direct external extension callers must supply the four newly required native arguments.

The test continues to use full rotary width, epsilon 1e-6, zero normalization bias and cuda:2; it does not establish integration correctness for nondefault model normalization settings.
