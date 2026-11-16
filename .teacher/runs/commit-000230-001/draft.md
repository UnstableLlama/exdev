# 2f8254fe00445db8554ff5150db42f9b49c73687


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/2f8254fe00445db8554ff5150db42f9b49c73687) · [Evidence ledger](draft.json)

Adds optional per-call RoPE angle tables across attention, Python and CUDA while preserving vector defaults. Table construction remains external; row validation and inherited kernel concerns remain.

- [Position-indexed rotary angles](#rope)

## Problem

RoPE previously formed every rotation angle as position × a one-dimensional inverse-frequency vector. That cannot directly express arbitrary position-dependent angles supplied by a model. [source; call_29601bd97be34a48ad951021860cadbe]

## Reasoning

The three edits form one interface: attention retrieves an optional tensor, RoPE.apply forwards it instead of its stored frequencies, and CUDA interprets a two-dimensional tensor as a position-indexed angle table. The existing vector path remains the default. [source; call_d21258cd66d14a97bcdd4b74bccd4fbd, call_58d8db9a61c74a5281af06ab0409b3a3, call_73b05e7c0c824bad9617d356051ef114]

## Impact

This provides special-RoPE plumbing rather than a complete Pixtral implementation: the diff adds neither a table producer nor a model registration. The whole-parent-tree search for “Pixtral” returned no matches. [source; call_2d4921ad5b5348ac98f5692857b7edc2, call_d21258cd66d14a97bcdd4b74bccd4fbd, call_58d8db9a61c74a5281af06ab0409b3a3, call_73b05e7c0c824bad9617d356051ef114]

## Source Notes

Read the earlier fused-normalization entry c82af98. It establishes the normalization-before-rotation design and records normalization-setting, reduction-store and padded-read concerns. [ancestor; call_451687443a7443b4aa04aa4bad3c37a7]

The earlier overwritten-normalization-settings concern is no longer present in the inspected parent constructor: supplied norm settings and no-norm defaults occupy separate branches. The task leaves this arrangement unchanged. The kernel's reduction-store and padded-read concerns remain. [source; call_d2774d71d33841fb960f1c16cd08effa, call_29601bd97be34a48ad951021860cadbe, call_73b05e7c0c824bad9617d356051ef114]

Issue #29, “Auto-YaRN for Qwen3? Maybe even set it dynamically?”, discusses automatic scaling policy and cache/batching difficulties. Its relationship to this task is inferred from the shared rope.py frequency mechanism; it does not establish that this change implements dynamic YaRN. [inference; call_fca3d9d082f74486a619e6f320906b89, call_58d8db9a61c74a5281af06ab0409b3a3]

Issue #7, “quantizing model: undefined symbol: __cxa_call_terminate,” and issue #6, “No ROCm runtime is found, using ROCM_HOME='/usr',” concern import/installation failures. Issue #16, “RuntimeError: CUDA error: invalid configuration argument,” concerns conversion and is attributed in discussion to tokenizer truncation. Their connections here are inferred only from rope.py or attn.py traceback overlap, not evidence that this change fixes those reports. [inference; call_d16726fb9a174db1bbb53dc9fea45fb3, call_1cc26810e694452096959450ace1f039, call_0024e6b2f12f48deae2f20ff75aac64b]

<a id="rope"></a>

## Position-indexed rotary angles

All three Attention routes—SDPA without cache, FlashAttention without cache, and cached FlashAttention—retrieve params['inv_freq'] through get_for_device with default None. Rotation remains conditional on self.rope. The helper transfers the tensor to the layer device and caches it in params['dev_cache']; like the existing position-tensor calls, this assumes the value remains read-only for that dictionary's lifetime. [source; call_d21258cd66d14a97bcdd4b74bccd4fbd, call_d2774d71d33841fb960f1c16cd08effa, call_051b4b43dbe842e4ace453d53c18b6d4, call_2e66a84263114037b5369d5c3d99f67c]

RoPE.apply appends an optional inv_freq argument. None selects self.inv_freq without changing stored state; an override is passed directly to ext.rope. The native signature is unchanged. The science/kv_quant_exp.py caller and test_rope.py calls omit the new trailing argument and therefore retain stored-frequency behavior. compute_sincos and apply_torch remain stored-frequency paths, not override-table references. [source; call_58d8db9a61c74a5281af06ab0409b3a3, call_cc144836a4f04c92a396f59720df463a, call_d5885e36251c4a9a89fe7305341e2d15, call_33edd5f98e204ec2a9d5b9011d0b41de, call_1f2962fde7ea420ab7a5cc655b581899]

For a vector, CUDA retains angle = inv_freq[t] × pos. For a table, it reads angle = inv_freq[pos × width + t] without multiplying by position again. These are precomputed angles, not precomputed sine/cosine values: CUDA still evaluates both trigonometric functions and multiplies by the RoPE object's existing attn_factor. [source; call_73b05e7c0c824bad9617d356051ef114, call_cc144836a4f04c92a396f59720df463a]

The last dimension determines partial_head_dim = 2 × width, because each angle rotates a pair of channels. Two-dimensional inputs must have width = query head_dim / 2, so this table interface requires full rotary width even though the vector path retains partial-width behavior. Float32 is checked; the former mandatory one-dimensional check is replaced by a two-dimensional check only for rank greater than one. [source; call_73b05e7c0c824bad9617d356051ef114, call_aea6444c7949466d8a2ddfa910677cc0, call_29601bd97be34a48ad951021860cadbe]

Table row selection reuses existing position semantics: token index plus scalar offset, token index plus a per-batch offset, or an explicit per-token position ID. Native validation rejects supplying both position tensors. One table is shared across the batch; batch-specific angles require callers to arrange distinct row IDs. NEOX still pairs the two rotary halves, while GPTJ pairs adjacent channels. [source; call_29601bd97be34a48ad951021860cadbe, call_73b05e7c0c824bad9617d356051ef114]

A standard-library scalar check confirmed that a flattened table built as table[p,t] = p × frequency[t] reproduces the old angle calculation for four positions and four frequencies. This checks the indexing interpretation, not either CUDA rotation implementation. [execution; call_ed02ce0f86f84e2fb3336c585d1850d1]

The design trades a larger position-by-channel tensor and its device storage for arbitrary angles while retaining the existing rotation and fused-normalization kernel. Keeping the vector path avoids requiring such tables for ordinary RoPE; no measured speed advantage is established. [inference; call_73b05e7c0c824bad9617d356051ef114, call_051b4b43dbe842e4ace453d53c18b6d4]

## Authoring-time findings — pending review

### table-row-bounds (suspected; defect)

The new table path does not validate that resolved positions name existing rows.

Trigger: Pass a float32 table of shape (2, 64), 128-wide Q/K, and position=2 through RoPE.apply or an enabled Attention RoPE route.

Expected: Reject a position outside the supplied table before launching a read.

Actual: Shape validation accepts the width, but the first table index is 128, equal to the entire table's element count. No inspected wrapper or native guard checks row bounds. The three Attention routes forward caller-supplied overrides; no default workflow producing this invalid table was identified.

Locations: 2f8254fe00445db8554ff5150db42f9b49c73687:exllamav3/exllamav3_ext/rope.cu — rope_kernel

Source evidence: call_73b05e7c0c824bad9617d356051ef114, call_29601bd97be34a48ad951021860cadbe, call_d21258cd66d14a97bcdd4b74bccd4fbd, call_1f2962fde7ea420ab7a5cc655b581899

scalar_transcription: Calculated the first flattened index for position 2 in a two-row, 64-column table. [call_ed02ce0f86f84e2fb3336c585d1850d1]. Limits: No GPU memory access or resulting fault was observed.

### inherited-padded-input-reads (suspected; defect)

Warp-padded threads still read frequencies and normalization weights without logical-width guards; table lookup inherits this issue.

Trigger: Use head_dim=80, present in the existing tests, or a vector shorter than the launched rotary-thread width.

Expected: Inactive lanes avoid reading beyond frequency rows and norm-weight arrays.

Actual: The launch rounds 40 channel pairs to 64 threads. All threads read frequencies before the rotary-width guard; table mode can cross into the next row or beyond the final row. With fused normalization, padded lanes also read half2 norm weights beyond the 80-element vector. These reads remain reachable through RoPE.apply and the three Attention routes.

Locations: 2f8254fe00445db8554ff5150db42f9b49c73687:exllamav3/exllamav3_ext/rope.cu — rope_kernel

Source evidence: call_29601bd97be34a48ad951021860cadbe, call_73b05e7c0c824bad9617d356051ef114, call_33edd5f98e204ec2a9d5b9011d0b41de, call_1f2962fde7ea420ab7a5cc655b581899

scalar_transcription: Applied the inspected warp-rounding formula: D=80 launches 64 x threads for 40 frequencies, leaving 24 excess indices. [call_ed02ce0f86f84e2fb3336c585d1850d1]. Limits: Index analysis does not establish compiler-emitted loads or observed CUDA faults.

### inherited-normalization-store-race (suspected; defect)

The unchanged fused normalization stores every lane's reduction result to the same shared warp slot.

Trigger: Enable fused Q/K RMS normalization with nonuniform per-lane square sums.

Expected: Store the complete warp sum once, using a lane-zero guard.

Actual: rope_kernel::apply_norm writes warp_reduce_sum_f(sum) from every lane to sums[warps*t_head+warp_id]. The inspected block_reduce_sum_f helper guards its corresponding store with lane_id==0. The task leaves the unguarded store unchanged; normalization-enabled Attention and test calls still reach it.

Locations: 2f8254fe00445db8554ff5150db42f9b49c73687:exllamav3/exllamav3_ext/rope.cu — rope_kernel::apply_norm

Source evidence: call_29601bd97be34a48ad951021860cadbe, call_2c0762e12b3141fea05b749b33e61468, call_73b05e7c0c824bad9617d356051ef114, call_d2774d71d33841fb960f1c16cd08effa, call_33edd5f98e204ec2a9d5b9011d0b41de

source_inspection: Compared the kernel store with the reduction helper and inspected the production and test call sites. [call_29601bd97be34a48ad951021860cadbe, call_2c0762e12b3141fea05b749b33e61468]. Limits: No GPU race detection or numerical failure was measured.

## Uncertainty and limits

No CUDA build, repository test, model inference or performance benchmark was run. The Python calculation models angle/index arithmetic, not GPU execution, float32 trigonometry or FP16 rounding.

Literal searches do not establish compatibility for dynamically accessed or external callers.

The existing tests omit override tables; they exercise stored frequencies, both rotary layouts and optional normalization.

No supplied model configuration or executed producer establishes Pixtral-specific angle construction.
