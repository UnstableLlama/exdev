# fd934384c4a750fd5e0744ce1f9c7044f8e982a2


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/fd934384c4a750fd5e0744ce1f9c7044f8e982a2) · [Evidence ledger](draft.json)

Adds optional per-head Q/K RMSNorm before RoPE across all attention backends, reusing the existing native kernel without enabling it in model builders.

- [Optional per-head Q/K RMS normalization](#modules)

## Problem

Attention previously left Q/K normalization as TODOs in all three decoding paths. [source; call_2374c3aa5aa648b3a64677568d2ef632]

## Reasoning

The change accepts optional RMSNorm modules and applies them after splitting projections into heads, before RoPE and attention. This normalizes each head's last dimension rather than the full concatenated projection. [source; call_2374c3aa5aa648b3a64677568d2ef632, call_06e0125a77414007ae0921386022cac6, call_5f56afc493a84ee88741b76b14ac773a]

## Impact

This supplies an attention-layer capability, not a newly enabled model architecture: all seven direct Attention construction sites found in the parent omit these optional arguments, and the task changes no model builders. [source; call_fcd12d5be89c43108fb605fb6951a0a2, call_6935c99690d64edd85cd5efeb5be571d, call_2374c3aa5aa648b3a64677568d2ef632, call_506b39a52eda4b5699c192aedb7c2e8e]

## Source Notes

An earlier entry distinguishes RMSNorm.forward_torch from native-dispatching forward; the new attention calls use forward, not the Torch reference implementation. [ancestor; call_ee14cf8c27db407b8424fcbebd91cd40]

<a id="modules"></a>

## Optional per-head Q/K RMS normalization

When q_norm is supplied, Attention requires k_norm and registers both as submodules. Registration includes them in recursive loading, unloading, iteration and weight counting; RMSNorm loads its own keyed weight tensor. [source; call_2374c3aa5aa648b3a64677568d2ef632, call_32d98ed73fc043bfb83c91f9e1e8741f, call_5f56afc493a84ee88741b76b14ac773a]

SDPA, uncached FlashAttention and cached FlashAttention all normalize Q and K with explicit half-precision output. V is unchanged. Cached attention receives normalized, subsequently rotary-transformed K; SDPA's existing sliding-window and softcapping exclusions remain. [source; call_2374c3aa5aa648b3a64677568d2ef632, call_06e0125a77414007ae0921386022cac6]

RMSNorm.forward flattens batch, sequence and head axes into rows and restores the original shape afterward. Its native implementation scales each row by reciprocal square root of mean square plus epsilon, then by weight plus optional constant bias. The native wrapper requires half weights, matching last-axis width and width divisible by four. [source; call_5f56afc493a84ee88741b76b14ac773a, call_6059f462bfd24ac184a834cd55022420]

A scalar illustration with heads [1,2,3,4] and [2,4,6,8], unit weights and epsilon 1e-6 produced a first component of 0.365148 under per-head normalization versus 0.230940 when normalizing the concatenated projection, demonstrating that the placement of the reshape matters. [execution; call_609bdc67f35f47d9a3064ffd5550e49f]

The RMSNorm file changes only by adding a TODO about a specialized Q/K kernel. The reused kernel launches 1024 threads per row and handles four elements per vector group; an illustrative width of 128 has only 32 such groups. This suggests a reason to investigate a smaller-head specialization, but does not establish that it would be faster. [inference; call_506b39a52eda4b5699c192aedb7c2e8e, call_6059f462bfd24ac184a834cd55022420, call_609bdc67f35f47d9a3064ffd5550e49f]

## Authoring-time findings — pending review

### asymmetric-norm-validation (suspected; defect)

The constructor enforces its stated paired-normalization invariant only when Q normalization is present.

Trigger: Construct Attention with q_norm=None and a non-null k_norm.

Expected: Reject the incomplete pair consistently with the assertion message requiring both norms or neither.

Actual: The else branch sets both attributes to None, silently discarding the supplied K norm. No inspected in-tree builder supplies either new argument, so the observed reach is the new constructor interface rather than an existing model workflow.

Locations: fd934384c4a750fd5e0744ce1f9c7044f8e982a2:exllamav3/modules/attn.py — Attention.__init__

Source evidence: call_2374c3aa5aa648b3a64677568d2ef632, call_fcd12d5be89c43108fb605fb6951a0a2, call_6935c99690d64edd85cd5efeb5be571d

source_inspection: Compared both constructor branches and inspected all seven direct construction sites found by whole-parent search. [call_2374c3aa5aa648b3a64677568d2ef632, call_fcd12d5be89c43108fb605fb6951a0a2, call_6935c99690d64edd85cd5efeb5be571d]. Limits: No Attention object was instantiated; external and dynamic callers were not established.

## Uncertainty and limits

No repository inference, CUDA kernel test, numerical parity test or performance benchmark was run. The scalar check uses Python double precision and does not reproduce GPU reductions, half-precision rounding or clamping.

Caller coverage covers literal Attention construction sites and inspected Python AST calls, not external consumers or dynamically constructed calls.
