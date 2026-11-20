# 3279fe188edb9e4be423fc828e5a8444c6aa6d06


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/3279fe188edb9e4be423fc828e5a8444c6aa6d06) · [Evidence ledger](draft.json)

Adds optional query, KV, and output projection modules to Attention. All 19 inspected model call sites retain their named linears. Query and output substitutions reuse existing forward calls, but the combined KV branch leaves loading, forward projection, and conversion allocation looking for missing separate projections.

- [Allow caller-supplied attention projections](#attention)

## Problem

Attention previously constructed all four projections as Linear children from checkpoint keys. This change lets a caller supply projection modules instead, but only the query and output substitutions are connected to the existing forward path. The combined key/value module is registered without replacing the downstream reads of the separate K and V projections. [source; call_60e1b076d3ee4b4584eddba00d376871, call_06809d1868bd43bda26e8d05fdff03bd]

## Reasoning

This is a constructor-level extension, not a new attention backend. It preserves the named Linear path and lets callers substitute Q and output independently. The K/V substitution changes the object layout from two children to one, so it also needs changes in loading, projection execution, and conversion allocation. Registering the new child supplies lifecycle integration, not those missing operations. [inference; call_60e1b076d3ee4b4584eddba00d376871, call_dd42cf6b1f62418481a9df556c84bcd6, call_06809d1868bd43bda26e8d05fdff03bd, call_fee8347a63394d3c911aa7bae8c1427c]

## Impact

The whole-parent Python AST check found 19 explicit constructor calls. All supply four truthy named keys and none passes a projection module: Cohere, Cohere2, DeciLM, Dots1, both Ernie variants, EXAONE4, Gemma2, both Gemma3 sites, GLM4, Llama, both Mistral3 sites, Mixtral, Phi3, Qwen3, Qwen3 MoE, and SmolLM3. Gemma3's second site uses `out_proj` rather than `o_proj`; Phi3 additionally passes `key_fused_qkv='qkv_proj'`. All 19 therefore retain the named Linear branches. The check parsed source; it did not instantiate the models. [execution; call_165e4952ff0f448689dccbbc66cd7055, call_fcb202335b694744a4eeafe68f405bf8, call_60e1b076d3ee4b4584eddba00d376871]

Dots1 still clears the first output projection's `qmap` on its named Linear. The QGEMM and quantization tests use Llama projection keys for lookup, not injected modules; the Transformers wrapper occurrences are example tensor names, not reads of Attention attributes. Neither transformer block's allocation method was adapted to a combined KV child. [source; call_82d7c7f1e4604394a9270d8494db8fc5, call_10d358e9ce274941a643bea8a5abbb04, call_a71b63c211fe44819344c98b6a2fed13, call_fee8347a63394d3c911aa7bae8c1427c, call_60e1b076d3ee4b4584eddba00d376871]

## Source Notes

The initial modules chapter describes Attention's shared projection pipeline, explicit child registration, and fused checkpoint row slicing. The projection-bitrate entry explains the separate `qbits_mod_key` and `qmap` roles and records the exact-budget allocator boundary. The Q/K LayerNorm entry records the former tensor-truth dispatch problem and native RoPE reduction and padding concerns. [ancestor; call_352c9515cedb47f894afc21b01d97e8f, call_d462349fb4484b39a34a2e47a0de7c25, call_6a77dbd2c9c84fd4b96220ed4c427614, call_db0cfda1370c468590938340ff5d23f6]

In the inspected parent, all three normalization dispatches already use `self.q_norm_tensor is None`, so this change does not carry over the tensor-truth failure. The native RoPE frequency reads and normalization reduction remain unchanged, as does the allocator's exact-budget selection on paths that reach it. [source; call_06809d1868bd43bda26e8d05fdff03bd, call_03ba9ecd51354855abb0d60122100140, call_b2949c875ac54be3b0efc13d59902f38, call_60e1b076d3ee4b4584eddba00d376871]

Closed issue #16, “RuntimeError: CUDA error: invalid configuration argument,” is relevant by traceback overlap: conversion went through `decode_flash_attn_nc`, `project_qkv`, and `self.q_proj.forward` into Hessian capture. The discussion attributed the failure to tokenizer truncation and reported overriding it at tokenizer load. The shared call path is not evidence that projection injection fixes the issue or was motivated by it. [inference; call_2ba0f18df268490cb0a436bf79cd6512, call_06809d1868bd43bda26e8d05fdff03bd, call_60e1b076d3ee4b4584eddba00d376871]

Issue #27, “Attention Backend,” asks about supporting FlashInfer alongside FlashAttention, and #44, “Please Switch to Flash-Infer,” reports a Turing compatibility concern. The overlap is the unchanged attention backend dispatch. Issue #29, “Auto-YaRN for Qwen3? Maybe even set it dynamically?”, overlaps through the unchanged RoPE interface. None establishes a link to the constructor change. [inference; call_7947373fd9894ce69bdfead15e63c5bb, call_ff4f30b59b514080b4e0fdff5e00d04b, call_6bdcdf6a7c284bc0ae0b0b6b3c4714b4, call_06809d1868bd43bda26e8d05fdff03bd, call_60e1b076d3ee4b4584eddba00d376871]

Other source-path matches concern different operations: #7, “quantizing model: undefined symbol: __cxa_call_terminate,” traces an extension import through `rope.py`; #33, “Error converting model,” originally reports a file-open failure in conversion and later tracks a separate GLM sampling symptom; PR #26, “Superior 3INST parameters,” discusses decoder multipliers and conversion experiments. Their overlap is with the imported rotary code or the conversion workflow, not with the changed constructor branches. [inference; call_486a7234b0b54e929b86ec19cee7b1d4, call_308178e4a822462a867fad3b394c1849, call_f6c580b5a3a6486bbab7f5a4311f0a47, call_6cf9257b62114fdf949af7d218b9e25c, call_46e463f9cb504d0bb277da8371722c15, call_60e1b076d3ee4b4584eddba00d376871]

Issues #34, “torch._C._LinAlgError on last layer of quant,” #42, “converting to 3.0 bpw causes error; block state has 0 inf values and 34 NaN values,” and #52, “Error converting moonshotai/Kimi-Dev-72B,” report conversion factorization failures. #53, “Command A support,” began as a model-support request and later reports a similar conversion failure. These overlap through `convert_model.py`, `Linear`, or the inspected model builders, but the reported failures occur outside projection construction. #48, “`RuntimeError` when requesting logprobs with Gemma 3 models,” overlaps through Gemma3 but reports a logits-buffer size mismatch. PR #4, “chore: update config.py,” is a spelling correction. These are contextual matches, not evidence of fixes in this commit. [inference; call_6a24241cdcb04db5b2f9993c34182b08, call_b6c97571fc5c4ae49280b2fb2f6275dc, call_d8558467fda849e6a63ff69771c99668, call_05cc0829bdbb40a1b582976f99b15039, call_be410e738d2345d7b062a58826d99d6c, call_4a54938639ae4b8c8d3d3be4487accfa, call_18d890159977471ba164ecf7fd1258a1, call_46e463f9cb504d0bb277da8371722c15, call_165e4952ff0f448689dccbbc66cd7055, call_60e1b076d3ee4b4584eddba00d376871]

<a id="attention"></a>

## Allow caller-supplied attention projections

`Attention.__init__` appends `q_proj`, `kv_proj`, and `o_proj`, each annotated `Module | None`. Truthy `key_q` and `key_o` take precedence over the corresponding objects; otherwise the constructor asserts and stores the supplied object. Truthy `key_k` selects separate K and V linears and asserts `key_v`. Falsy `key_k` instead asserts and stores `kv_proj`, even if `key_v` was provided. The selected objects become children for recursive load, unload, and traversal. [source; call_60e1b076d3ee4b4584eddba00d376871, call_dd42cf6b1f62418481a9df556c84bcd6]

Named linears keep their dimensions and metadata. Q maps hidden width to query-head count times head width; K and V each map hidden width to KV-head count times head width. Output maps flattened query heads back to hidden width. The named Q/K/V linears share the `.input` calibration label; the named output uses `.o` and receives `out_dtype`. The supplied objects are stored as-is, without those constructor settings being applied to them. The unchanged wrapper still casts the final attention result via `to2`. [source; call_60e1b076d3ee4b4584eddba00d376871, call_06809d1868bd43bda26e8d05fdff03bd]

The unchanged Q and output consumers call `.forward(tensor, params)`, so substitutes must accept those arguments and satisfy the downstream shape contract. Q must produce a result viewable as batch × sequence × query heads × head width; output receives batch × sequence × flattened query width. A substitute that is not a `Linear` is not itself selected by the converter's Linear-only filter, even though it is registered; any qualifying Linear descendants would still need entries in the allocation strategy. [source; call_06809d1868bd43bda26e8d05fdff03bd, call_46e463f9cb504d0bb277da8371722c15, call_b2949c875ac54be3b0efc13d59902f38, call_60e1b076d3ee4b4584eddba00d376871]

Three different mechanisms should not be confused. `key_fused_qkv` still slices one stored weight into consecutive Q, K, and V output-row ranges for separate linears. `multi_kv` still batches two eligible bias-free EXL3 linears with matching output widths and inner K values; `project_qkv` uses that path only at 32 or fewer input tokens across the batch. The new `kv_proj` argument is a single supplied child, not either existing fusion mechanism, and neither mechanism invokes it. [source; call_60e1b076d3ee4b4584eddba00d376871, call_06809d1868bd43bda26e8d05fdff03bd, call_16927df5d11f44c480b494f1f4c9f3f2]

## Authoring-time findings — pending review

### combined-kv-child-not-consumed (suspected; defect)

The constructor accepts a combined KV child, but loading, forwarding, and allocation still assume separate K and V attributes.

Trigger: Construct a fresh Attention with valid Q/output choices, a falsy `key_k`, and a truthy `kv_proj`. Then load it after its children load successfully, call `project_qkv` with a valid input and `multi_kv` unset, or run a containing block's allocation with valid quantization arguments.

Expected: The chosen KV module should be invoked to produce K and V on the supported inference path, and unsupported allocation should be rejected explicitly or handled without reading absent attributes.

Actual: `Attention.load` first loads the registered children and then reads `self.k_proj` in its EXL3 fusion probe. If loading is bypassed, `project_qkv` reaches the same missing attribute in the separate projection branch. All three decode methods call `project_qkv`; the research sampler also calls it directly after loading its model. Both transformer block allocators read `self.attn.k_proj` before calling `allocate_transformer`, so conversion can fail at allocation before load. The explicit in-tree model builders do not select this branch.

Locations: 3279fe188edb9e4be423fc828e5a8444c6aa6d06:exllamav3/modules/attn.py — Attention.__init__ / load / project_qkv, db533103b1827e83b55bac4f4531eeef3684a57f:exllamav3/modules/transformer.py — TransformerBlock.allocate_q / ParallelDecoderBlock.allocate_q

Source evidence: call_60e1b076d3ee4b4584eddba00d376871, call_06809d1868bd43bda26e8d05fdff03bd, call_0fc9f5029b5d4528a3476164db08d3ca, call_07c6a097332f4489a424c3ba31c073f1, call_fee8347a63394d3c911aa7bae8c1427c, call_46e463f9cb504d0bb277da8371722c15, call_165e4952ff0f448689dccbbc66cd7055

scalar_transcription: A stub with only `kv_proj` and `multi_kv=None` raised `AttributeError` on the attribute reads modeled for the load probe, the projection fallback, and allocation. [call_783df40d98644618a502d8beb46a2eea]. Limits: The stub models the missing attributes; it did not run Attention, Torch, or a model loader.

### fused-key-alone-no-longer-sufficient (suspected; external_compatibility)

Omitting individual projection keys now means injection rather than building a Linear that can fall back to a fused checkpoint key.

Trigger: An external caller supplies a valid `qmap`, output key, and `key_fused_qkv`, omits `key_q`, and supplies no `q_proj`; the checkpoint has the fused weight but no separate query weight.

Expected: If preserving that call form, the query Linear should still fall back to the fused weight's query slice.

Actual: Previously the constructor built the query Linear even with the default key and passed it the fused key and range; `Linear.load_fp16` could use the fused weight when the primary weight was missing. The new constructor instead asserts `q_proj` before loading. The inspected Phi3 caller is not affected because it supplies both fused and individual keys.

Locations: 3279fe188edb9e4be423fc828e5a8444c6aa6d06:exllamav3/modules/attn.py — Attention.__init__

Source evidence: call_60e1b076d3ee4b4584eddba00d376871, call_06809d1868bd43bda26e8d05fdff03bd, call_16927df5d11f44c480b494f1f4c9f3f2, call_165e4952ff0f448689dccbbc66cd7055

source_inspection: Compared the old constructor's unconditional Linear creation and fused-weight fallback with the new truthiness branch and all explicit parent call forms. [call_60e1b076d3ee4b4584eddba00d376871, call_16927df5d11f44c480b494f1f4c9f3f2, call_165e4952ff0f448689dccbbc66cd7055]. Limits: No external caller or fused-only checkpoint was run; this describes the call form, not an observed regression in a shipped model.

### inherited-exact-allocation-budget (suspected; defect)

The unchanged transformer allocator can skip an exactly affordable option. This is distinct from failing to reach the allocator with an injected KV child.

Trigger: The separate-projection allocation path has a candidate whose cost equals the computed budget and another candidate of lower cost.

Expected: Select the largest candidate within budget, including an exact match.

Actual: The search tuple `(budget,)` sorts before `(budget, pattern)`. With four unit-weight projections and a budget of 14, the actual parent allocator chose four 3-bit projections costing 12 and returned a surplus of 2 instead of selecting the 14-bit candidate.

Locations: db533103b1827e83b55bac4f4531eeef3684a57f:exllamav3/conversion/allocation.py — allocate_transformer

Source evidence: call_b2949c875ac54be3b0efc13d59902f38, call_77abd08c794342289ff2d07ec4ad9905, call_fee8347a63394d3c911aa7bae8c1427c, call_60e1b076d3ee4b4584eddba00d376871

repository_execution: Ran the parent implementation of `allocate_transformer` through `runpy` at 3.25 bpw and zero incoming surplus using four stub projections. [call_7acdde06fe094063b98c868cfb5063c1]. Limits: Isolated Python allocator call, not a conversion run or a measurement of real model allocation frequency.

### inherited-native-rope-reads-and-reduction (suspected; defect)

The constructor change does not alter the inherited native RoPE bounds and reduction concerns on paths that reach rotation.

Trigger: Use native RoPE with a frequency vector shorter than the launched x-lane count, for example a full rotary width of 80 or a rotary width of 64 on a 128-wide head. With fused RMS normalization, a padded head width also reaches unguarded weight reads, and nonuniform lane inputs exercise the shared reduction writes.

Expected: Read frequencies and weights only within their logical bounds and store one complete reduction per warp.

Actual: For a one-dimensional frequency vector the kernel reads `inv_freq[t]` before checking the rotary lane bound. Normalization reads a half2 weight per lane without a padding guard and all lanes write their shuffle-down result to the same per-warp sum slot. Attention's decode methods still call RoPE after projection when configured, and `test_rope.py` has width-80 direct calls with and without normalization. Integer launch arithmetic gives 64 x-lanes against 40 frequency entries at width 80, or 32 entries in the 128/64 partial case.

Locations: db533103b1827e83b55bac4f4531eeef3684a57f:exllamav3/exllamav3_ext/rope.cu — rope_kernel / rope

Source evidence: call_03ba9ecd51354855abb0d60122100140, call_30c6ad68f20542828ff947415c3392b5, call_06809d1868bd43bda26e8d05fdff03bd, call_60e1b076d3ee4b4584eddba00d376871, call_82d7c7f1e4604394a9270d8494db8fc5

source_inspection: Compared the native launch, frequency and weight reads, reduction helper, rotary wrapper, and direct test call with the constructor-only diff. [call_03ba9ecd51354855abb0d60122100140, call_30c6ad68f20542828ff947415c3392b5, call_783df40d98644618a502d8beb46a2eea, call_82d7c7f1e4604394a9270d8494db8fc5, call_60e1b076d3ee4b4584eddba00d376871]. Limits: No CUDA execution or race detection; compiler behavior and runtime consequences were not measured.

scalar_transcription: Computed the lane count by rounding half the head width up to a multiple of the 32-lane warp width, then compared it with the frequency count. [call_783df40d98644618a502d8beb46a2eea]. Limits: Integer launch arithmetic only; does not model GPU scheduling, memory loads, or half-precision arithmetic.

## Uncertainty and limits

No Attention instance, model inference, GPU kernel, or end-to-end conversion was executed. The quantitative checks were limited to a Python attribute model, integer launch arithmetic, and an isolated allocator call with stub projections.

Literal whole-tree searches and the Python AST scan cover explicit calls, attributes, and import aliases; they do not rule out dynamic or external uses. No existing caller in the inspected tree specifies an output contract for a combined KV module.
