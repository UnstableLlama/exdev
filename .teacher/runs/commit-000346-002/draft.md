# 67e0fd74413228c85e1edc65cfc7c39365b1a6ca


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/67e0fd74413228c85e1edc65cfc7c39365b1a6ca) · [Evidence ledger](draft.json)

Refactors the tensor-parallel planner to separate storage from peak overhead and emit aligned KV-head and channel ranges. It does not enable TP loading. A stale transformer import can block module initialization, and the new budget retry and device mask still admit infeasible cases.

- [Estimate tensor-parallel memory and emit aligned shard ranges](#tp-auto-allocation)

## Problem

The parent tensor-parallel (TP) planner used remaining memory as a split weight without handling an all-zero weight vector. It also emitted offsets in allocation units even when those units represented groups of channels. Attention supplied one unit per KV head without checking whether a shard boundary aligned to 128 channels. [source; call_28f6efdfaf11464bbf7119bbae823efa, call_b10bef17aa13469a80b6b834b1fe73aa, call_d1dc5d2e1b5a431b8e74b16745e8224c]

## Reasoning

The two offset changes work together. Attention now describes a shard in whole groups of KV heads; compile_tp_plan multiplies the cumulative group offsets by the number of heads per group. Without that multiplication the emitted offsets would count groups, not heads. The same multiplication converts standalone Linear's 128-channel blocks to channel offsets. The 128-channel rule is consistent with the existing EXL3 output-width alignment, but the diff does not establish that every prospective TP kernel needs the same alignment or that the particular grouping rule is necessary for all formats. [inference; call_3457c1674a594876896cd546146fb73e, call_b5db84f96ba240f18f189a30568feebd, call_523707b4aac540a9a2880fde2723f5cc, call_730abc226cd74aa0aefda2a85fde0c75]

The planner trades a hard capacity constraint for a best-effort estimate: increasing the budget can restore positive weights and let planning continue, but it neither frees memory nor proves the resulting shards fit. Likewise, pinning a one-device component to slot 0 trades eligibility based on available room for a fixed placement; the source does not explain why slot 0 was chosen. [inference; call_28f6efdfaf11464bbf7119bbae823efa, call_b5db84f96ba240f18f189a30568feebd]

## Impact

The planner's initial_split return changes from one totals list to a tuple of three lists in the order total, storage, overhead. print_split is updated in the same diff to read the three new attributes instead of estimate. Whole-parent searches found no explicit caller of initial_split or compile_tp_plan and no explicit TPAllocator instantiation. Model.load_gen still uses the separate whole-module autosplit path for non-TP loading and raises NotImplementedError in its TP branch; the diff does not wire in TP loading. [source; call_b5db84f96ba240f18f189a30568feebd, call_1cd2549131764fe1ab92cba9b414de0f, call_44d8acb1fdfb4a4f9cc5bba630db9a26, call_45fc831f037746f6b5ae69149fd05344, call_71745d945a2e4d62a5f62aa2a4a60336]

The old import survives in transformer.py even though the allocator file is renamed and ten other importers migrate. The modules initializer imports transformer.py eagerly, so even an import that asks only for Linear can encounter the missing module. This reaches architecture imports, factory paths that resolve the architecture registry, conversion's top-level import of Linear, and utilities such as science/kv_quant_exp.py. It is not limited to callers that opt into TP. [source; call_cb515bc3d8024851b7e80b35902817a5, call_b5db84f96ba240f18f189a30568feebd, call_fb0071eec5be403a919dad5f2920b1c1, call_1c3b35e6e30d44ababf2b143dd5fa8ab, call_84609799a2ab4bd793280dbdcf760558, call_df32284ef95149d4a434a7c6e09b8ca9, call_9224a112ed7940a6bcb19a11bdbd4891, call_74a3cff606f84103b98dc40288de46ef]

## Source Notes

The supplied attribution names turboderp as the author. The message, “TP: Refactor/fix auto allocation,” describes the planner work; neither the message nor the diff identifies a motivating issue or claims to enable TP loading. [source; call_ec274921d9ec42d2a0d343d5bae48bd2, call_b5db84f96ba240f18f189a30568feebd]

The earlier entry “TP: Auto layer split logic” describes the introduction of the record collector and greedy planner without a loader integration. It records over-budget results, zero denominators, full-cache scratch counted per forward token, the empty-child assertion, and the separate-K/V assumption. [ancestor; call_b9ff0818c2cf4b3098268c13224bcf03, call_3d160b52c45740efbcdae97f497ba01b]

Issue #50, “RuntimeError: Insufficient VRAM in split for model and cache despite remaining 1GB VRAM (exllamav3 + tabbyAPI),” quotes the error raised by the unchanged whole-module loader after it exhausts active devices. Issue #54, “GPU split isn't followed here?”, asks about TabbyAPI split settings and observed VRAM and reports a change after adjusting the allocator backend. Their relevance is to the distinction between observed whole-module loading and TP estimates, not evidence that this commit fixes either report. [inference; call_830d69d06a7240488830d92ca5b7cb29, call_b7d7a408626a4af995fca3f8e57a9339, call_2f25e3f82f6a46c9a5bff8c569a63472, call_71745d945a2e4d62a5f62aa2a4a60336]

The conversion reports overlap by file, not by planner call. #8, “RuntimeError: shape '[5120, -1, 128]' is invalid for input of size 776524800,” traces lm_head quantization through Linear.convert_exl3, not attention grouping. #11, “AssertionError: bias is wrong datatype,” traces Linear.convert_exl3 into an EXL3 bias assertion. #16, “RuntimeError: CUDA error: invalid configuration argument,” traces conversion's Attention forward into Linear.capture_H. #38, “Error converting nvidia/Llama-3_1-Nemotron-Ultra-253B-v1,” traces a tensor-size mismatch through sliced MLP and Linear loading. #55, “Possible GLM4 32B regression,” traces an int/None comparison in the FP16 loader through Module, MLP and Linear. [inference; call_de33b4d13da84ecdbd38ee260754632a, call_dff641079d7c4601aa134656c0be14a3, call_29376bae64dc4392af6290e15ce3a2b1, call_7b914c0c965d4cdebef968b8d502a839, call_a19fe4d5c3d3441e9a96ecb44cf0a99c, call_1f732f7c9f1e45159618d28c33d3a292, call_3457c1674a594876896cd546146fb73e, call_2d4284481a8e4b59806a6f015d0b2a6d]

Further conversion context: #43, “Error converting abliterated Qwen3 mlabonne/Qwen3-30B-A3B-abliterated”; #58, “linalg.cholesky error converting OpenBuddy (Qwen3) 32B QAT”; #34, “torch._C._LinAlgError on last layer of quant”; and #52, “Error converting moonshotai/Kimi-Dev-72B,” trace from Linear.convert_exl3 to factorization. #42, “converting to 3.0 bpw causes error; block state has 0 inf values and 34 NaN values,” reports NaNs and failure at the head in conversion through the same method. #53, “Command A support,” starts as a model-support and quant availability request. Their overlap does not establish a relationship to TP allocation. [inference; call_7da3e4e9aa8e436eb5090f14cad0ebbf, call_0641801bb9c24dfdbc109992c21e7609, call_136bc4861b6845baa8fe6a2c24143c71, call_2dab80e6f7ac442cbb363d9062f81dbf, call_ee71e9b3f5f64778a887e63d3f6f944e, call_471a26a9a936406282d0591d4cbd0506, call_2d4284481a8e4b59806a6f015d0b2a6d]

Other nearby discussions describe different mechanisms: #7, “quantizing model: undefined symbol: __cxa_call_terminate,” passes through the package and model initializers but fails loading the compiled extension, not the allocator module; #48, “`RuntimeError` when requesting logprobs with Gemma 3 models,” concerns a logits-buffer copy, not the Gemma vision MLP's allocation hook; #57, “Batch process interrupted,” concerns batched_translation.py stopping while creating jobs, with no matching planner call. #27, “Attention Backend,” asks about FlashInfer versus FlashAttention, not KV-head partitioning; #1, “Cache Quantization Strategy,” describes independent K/V bitrates, relevant to the cache being estimated but not evidence of a change to its implementation here. [inference; call_1bd91d54b94e4167b6db41a736dab006, call_3115d3a0276c4bfcbeb8b96cf0f4b901, call_33aa0b2a50bb43b2b9d62566f556e03b, call_911e6974f8d94b3a9387829e6aa6ca23, call_fc8b8f70fbfe416a9de69b7376ea6941, call_3457c1674a594876896cd546146fb73e, call_13b39b7a03e34b8e8a365f2e4cd8c574]

<a id="tp-auto-allocation"></a>

## Estimate tensor-parallel memory and emit aligned shard ranges

TPAllocation records describe work to estimate, not tensors to load. Module.make_tp_allocation concatenates child records in registration order; Attention supplies a combined projection-and-cache record, and BlockSparseMLP may append its shared experts' record. Embedding and PosEmbedding emit no records. Conv still raises, now with an explicit message. Plain MLP no longer returns an estimate for its up/down projections and raises instead; the two explicit constructors found are Gemma3's vision encoder block and Mistral3's multimodal projector. Direct collection there is affected, while either vision model's module list also contains an earlier Conv. GatedMLP still has its own estimator. [source; call_df5d070b92d14baeb40bf111b5e92adb, call_d1dc5d2e1b5a431b8e74b16745e8224c, call_2bdbba0fb2d84eaf9adb9cc6c58c0060, call_2f25e3f82f6a46c9a5bff8c569a63472, call_1a202d2435a04e0fb1dc92e6cf435695, call_13b39b7a03e34b8e8a365f2e4cd8c574, call_d3fae00e293c48d6b753a3e966ffc6d1, call_56f713c8433a4a66b19e404f08012881]

For each component, initial_split subtracts accumulated persistent bytes and the maximum temporary charge seen so far from each device's working budget and clips the result at zero. If every weight is zero, it retries with each working budget multiplied by 11/10 and rounded down in bytes. It does this before masking devices: limit 1 keeps only slot 0; other non-None limits still keep the slots with the most remaining room. ratio_split floors proportional quotas in indivisible allocation units and distributes leftovers by largest fractional remainder. Replicated charges depend on the positive-weight mask, not the rounded split. Split charges are prorated; only overhead_to_split gets the forward-token multiplier, with output_num_tokens used for the final component. Persistent costs sum across components; temporary costs take a per-device maximum. The new report shows the two terms and their sum, with a 1024³ divisor despite the GB label. [source; call_28f6efdfaf11464bbf7119bbae823efa, call_b5db84f96ba240f18f189a30568feebd, call_b10bef17aa13469a80b6b834b1fe73aa]

Attention starts with one head per group and doubles the group size while group size × head_dim is below 128, halving the number of groups each time and requiring an even count at each halving. The resulting width must be divisible by 128. This reaches an aligned boundary without splitting a head, but it rejects some widths even if a larger group could work: at head_dim 96 it stops at two heads (192 channels) and asserts instead of trying four heads (384 channels). This condition applies to allocation, not to Attention.forward. [source; call_3457c1674a594876896cd546146fb73e, call_d1dc5d2e1b5a431b8e74b16745e8224c]

compile_tp_plan keeps per-device, per-key half-open intervals, including empty intervals, and scales both endpoints by channel_width or 1. Attention now emits head offsets; standalone Linear and unsliced GatedMLP emit 128-channel boundaries; BlockSparseMLP still emits expert offsets; LayerNorm and RMSNorm leave width unset and are unchanged in this conversion. Already-sliced GatedMLP does not agree with either a slice-index or a true channel-offset interpretation: it still declares one allocation unit per slice but supplies width 128 regardless of the actual slice widths. [source; call_b5db84f96ba240f18f189a30568feebd, call_3457c1674a594876896cd546146fb73e, call_523707b4aac540a9a2880fde2723f5cc, call_56f713c8433a4a66b19e404f08012881, call_1478a93b924d4c04a9a0d66b31a648f1, call_2bdbba0fb2d84eaf9adb9cc6c58c0060, call_9783a04b342842d194708f98bb281b61, call_fc5d4d7b9423440ab7fb4cbf0132a375]

A bounded Python transcription gave four two-head groups for eight 64-channel KV heads. With weights 3:1, the groups split 3:1 and compile to head intervals [0,6) and [6,8). Three 64-channel heads and head widths of 96 or 192 hit the new assertions in the tested examples. A depleted 100-byte budget with 115 bytes already charged rose to 110, then 121; budgets from zero through nine bytes were fixed points of the growth step. [execution; call_ba25788889e742a3a0a6bff576b6ec01]

## Authoring-time findings — pending review

### stale-transformer-import (suspected; defect)

The allocator move leaves a mandatory import at the old module path.

Trigger: In a clean task installation with earlier prerequisites satisfied, import exllamav3.modules or an architecture or conversion module that imports it.

Expected: The initializer imports both decoder block classes using the relocated TPAllocation definition.

Actual: The initializer reaches transformer.py, whose top-level import names the removed util.tp_split path; package initialization is expected to stop there before allocation is called.

Locations: 67e0fd74413228c85e1edc65cfc7c39365b1a6ca:exllamav3/modules/transformer.py — TPAllocation import

Source evidence: call_b5db84f96ba240f18f189a30568feebd, call_cb515bc3d8024851b7e80b35902817a5, call_fb0071eec5be403a919dad5f2920b1c1, call_1c3b35e6e30d44ababf2b143dd5fa8ab

source_inspection: Cross-checked all literal old-path imports against the move and traced the eager initializer and its importers. [call_cb515bc3d8024851b7e80b35902817a5, call_b5db84f96ba240f18f189a30568feebd, call_1c3b35e6e30d44ababf2b143dd5fa8ab, call_84609799a2ab4bd793280dbdcf760558]. Limits: No installed-package import ran; an old file left on disk could mask the failure.

### budget-growth-can-stall (suspected; defect)

The new retry replaces one zero-weight failure with a possible nonterminating loop.

Trigger: Call initial_split directly with a nonempty component list and max_mem=[0], or reach a component with exhausted budgets that cannot grow under integer flooring.

Expected: Find positive weights or return an explicit infeasible-budget error.

Actual: With zero capacity the next budget is still zero and the while loop has no progress check or retry limit.

Locations: 67e0fd74413228c85e1edc65cfc7c39365b1a6ca:exllamav3/models/model_tp_alloc.py — TPAllocator.initial_split

Source evidence: call_b5db84f96ba240f18f189a30568feebd, call_1cd2549131764fe1ab92cba9b414de0f

scalar_transcription: Evaluated the growth expression and found all whole-byte values from 0 through 9 unchanged. [call_ba25788889e742a3a0a6bff576b6ec01]. Limits: Did not run the infinite loop; the search found no named in-tree caller.

### slot-zero-mask-removes-all-room (suspected; defect)

Checking for positive weights before enforcing the single-device limit does not protect the split after masking.

Trigger: Call initial_split with a positive channel count on a one-device-limited component, slot 0 already exhausted, and another device still having room. For example, budgets [10,20] after a prior slot-0-only component charged 10 bytes give residuals [0,20].

Expected: Apply the fixed-slot constraint before testing feasibility, then either obtain a usable weight for slot 0 or report that it cannot fit.

Actual: The positive residual on slot 1 skips the retry, the mask zeroes slot 1, and ratio_split divides by zero for Python integer inputs.

Locations: 67e0fd74413228c85e1edc65cfc7c39365b1a6ca:exllamav3/models/model_tp_alloc.py — TPAllocator.initial_split

Source evidence: call_b5db84f96ba240f18f189a30568feebd, call_b10bef17aa13469a80b6b834b1fe73aa, call_1cd2549131764fe1ab92cba9b414de0f

scalar_transcription: Modeled the residual and mask steps and observed ZeroDivisionError from the transcribed split. [call_ba25788889e742a3a0a6bff576b6ec01]. Limits: Direct planner inputs only; no named in-tree planner caller was found.

### planner-still-lacks-fit-and-axis-checks (suspected; defect)

The new retry does not fix the inherited over-budget result or the independent zero-channel denominator.

Trigger: Call initial_split with budgets [4,4] and a record with storage_per_device=5 and default split sizes; separately pass a record with channels_to_split=0 and positive remaining room.

Expected: Report an infeasible replica or reject a zero-sized axis before prorating costs.

Actual: The first case returns totals [5,5] for rounded split [1,0]; the second gets zero shares from ratio_split and divides by the zero axis length in accounting.

Locations: 67e0fd74413228c85e1edc65cfc7c39365b1a6ca:exllamav3/models/model_tp_alloc.py — TPAllocator.initial_split

Source evidence: call_28f6efdfaf11464bbf7119bbae823efa, call_b5db84f96ba240f18f189a30568feebd, call_b10bef17aa13469a80b6b834b1fe73aa, call_1cd2549131764fe1ab92cba9b414de0f

scalar_transcription: Checked rounding and replica totals for the first case and the zero share before the unchanged accounting denominator for the second. [call_ba25788889e742a3a0a6bff576b6ec01]. Limits: Synthetic planner inputs; no loader or actual device allocation was exercised.

### gated-mlp-slice-offset-unit-mismatch (suspected; defect)

The range scaling newly propagates GatedMLP's inherited width metadata mismatch into the compiled plan.

Trigger: Compile an allocation for a GatedMLP already split into two slices, giving each device one slice; the constructor can create slices when the intermediate size exceeds its split threshold.

Expected: Represent the two slice indices or translate them into channel boundaries using the actual slice widths.

Actual: The record counts slices but multiplies offsets by 128, emitting [0,128) and [128,256) irrespective of those widths.

Locations: 67e0fd74413228c85e1edc65cfc7c39365b1a6ca:exllamav3/models/model_tp_alloc.py — TPAllocator.compile_tp_plan, 67e0fd74413228c85e1edc65cfc7c39365b1a6ca:exllamav3/modules/mlp.py — GatedMLP.make_tp_allocation

Source evidence: call_b5db84f96ba240f18f189a30568feebd, call_56f713c8433a4a66b19e404f08012881, call_1478a93b924d4c04a9a0d66b31a648f1, call_44d8acb1fdfb4a4f9cc5bba630db9a26

scalar_transcription: Scaled the cumulative offsets for two one-slice assignments. [call_ba25788889e742a3a0a6bff576b6ec01]. Limits: No in-tree consumer of compile_tp_plan was found, so no resulting tensor mis-slice was observed.

### inherited-quantized-cache-scratch-scaling (suspected; defect)

Changing the attention split unit leaves the inherited token multiplier on full-cache scratch intact.

Trigger: Collect an attention record with an attached quantized cache, directly or via a containing module, then estimate it for more than one forward token.

Expected: Charge the full-size K/V reconstruction pair once per call and scale only token-dependent activations with token count.

Actual: Attention puts the full-cache pair in overhead_to_split, and the planner multiplies it by the forward-token count before prorating. Conversely, the replicated overhead field is documented per token but charged once.

Locations: 67e0fd74413228c85e1edc65cfc7c39365b1a6ca:exllamav3/modules/attn.py — Attention.make_tp_allocation, 67e0fd74413228c85e1edc65cfc7c39365b1a6ca:exllamav3/models/model_tp_alloc.py — TPAllocator.initial_split

Source evidence: call_d1dc5d2e1b5a431b8e74b16745e8224c, call_3457c1674a594876896cd546146fb73e, call_2f25e3f82f6a46c9a5bff8c569a63472, call_b5db84f96ba240f18f189a30568feebd, call_8ca72cda40c34a799cea34ea01d4e381

scalar_transcription: Isolated the cache term: 1,024 cache positions, eight heads, head width 128 and two bytes per element give a 4 MiB K/V pair, counted as 32 MiB at eight forward tokens. [call_ba25788889e742a3a0a6bff576b6ec01]. Limits: This is estimate arithmetic, not peak VRAM or a live model-loading path.

### inherited-combined-kv-estimator-failure (suspected; defect)

The new head grouping still cannot be reached for the constructor's combined-K/V form.

Trigger: Construct Attention with named Q/O projections and a supplied kv_proj instead of key_k/key_v, then ask it for a record directly or through Module's child traversal.

Expected: Account for the combined projection or reject it explicitly.

Actual: The constructor only assigns kv_proj in that branch, but the estimator reads k_proj.storage_size() before reaching the new grouping logic.

Locations: 67e0fd74413228c85e1edc65cfc7c39365b1a6ca:exllamav3/modules/attn.py — Attention.make_tp_allocation

Source evidence: call_d3dcdd5a03514d84a0c347ee5b606e29, call_d1dc5d2e1b5a431b8e74b16745e8224c, call_3457c1674a594876896cd546146fb73e, call_df5d070b92d14baeb40bf111b5e92adb

source_inspection: Compared the constructor branches to the unchanged estimate reads and checked the parent collector and literal kv_proj assignment references. [call_bf7478075fc84c4ab0adef2239b9ce82, call_8ca72cda40c34a799cea34ea01d4e381, call_d3dcdd5a03514d84a0c347ee5b606e29, call_d1dc5d2e1b5a431b8e74b16745e8224c]. Limits: Conditional on the accepted custom constructor form; the literal search does not rule out dynamically supplied arguments.

### inherited-empty-collector-assertion (suspected; defect)

The generic allocation collector still cannot return an empty plan for a no-op decoder block.

Trigger: With assertions enabled, directly collect an allocation from a DeciLM TransformerBlock with both attention and FFN marked no_op, assuming the module imports have succeeded.

Expected: Return no records for a block with no child work.

Actual: None children are not registered, so the inherited collector asserts on the empty list before returning. The Module diff only changes its allocator import.

Locations: 67e0fd74413228c85e1edc65cfc7c39365b1a6ca:exllamav3/modules/module.py — Module.make_tp_allocation

Source evidence: call_2f25e3f82f6a46c9a5bff8c569a63472, call_fb0071eec5be403a919dad5f2920b1c1, call_e1193c0bed374f219d7da6141cfe0710, call_8ca72cda40c34a799cea34ea01d4e381

source_inspection: Traced the two no_op branches through registration to the unchanged collector guard and searched for explicit callers. [call_2f25e3f82f6a46c9a5bff8c569a63472, call_fb0071eec5be403a919dad5f2920b1c1, call_8ca72cda40c34a799cea34ea01d4e381]. Limits: No model-level allocation caller was found; this is not a claim about ordinary DeciLM forward execution.

## Uncertainty and limits

No package import, model load, CUDA allocation, sharded forward or distributed communication was executed. The scalar transcription uses Python integers and floating-point division, not NumPy fixed-width arithmetic or GPU allocator behavior. It does not measure memory fit, speed or accuracy.

Literal whole-tree searches establish explicit references, not dynamic callers or external users of the old import, estimate attribute or return value. The import finding assumes a clean installation without a stale copy or shim of util.tp_split; a bare top-level import that has not yet reached exllamav3.modules was not shown to fail.

The diff leaves FlashAttention temporary workspace unmodeled and does not supply a tensor slicer that consumes the emitted ranges. Compatibility with every available checkpoint head shape and the desired offset convention for already-sliced GatedMLP were not established.
