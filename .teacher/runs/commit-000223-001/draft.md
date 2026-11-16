# 95c41ce0e15aa7362cc50aaf5d4efcd7dd4c2225


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/95c41ce0e15aa7362cc50aaf5d4efcd7dd4c2225) · [Evidence ledger](draft.json)

Makes ordinary MLP honor its activation selector, preserving SiLU by default and adding tanh-approximate GELU; unsupported strings remain unchecked.

- [Selectable activation for ordinary MLP](#modules)

## Problem

Ordinary MLP accepted activation_fn but ignored it: forward always applied SiLU. [source; call_800507643ca842c185878503bc45dce0]

## Reasoning

The constructor now resolves the activation once and forward invokes that callable between the up and down projections. Storing the callable and replacing the hard-coded call are dependent edits. [source; call_678f89cd89d94c01b8e058e52277a7cc]

## Impact

The default remains SiLU; selecting "gelu" now requests PyTorch GELU with approximate="tanh". Projection construction and output-dtype conversion are unchanged. [source; call_678f89cd89d94c01b8e058e52277a7cc, call_800507643ca842c185878503bc45dce0]

The whole-parent-tree MLP search found no ordinary MLP construction sites or subclasses. Consequently, the demonstrated benefit is to the exposed module API, not an established existing model workflow. [source; call_ebedf6a47d9f4a8b852063db570a1be3]

## Source Notes

The preceding alignment entry records that activation_fn was newly accepted but unused. That entry was read; inspection of this patch shows its ignored-GELU observation is addressed. [ancestor; call_d2d95b0edb544e1493bfbb3457544567]

Issue #38, “Error converting nvidia/Llama-3_1-Nemotron-Ultra-253B-v1,” concerns sliced GatedMLP loading and tensor-size mismatch. Its connection to this task is only an inferred shared-file relationship: the traceback names mlp.py, but this patch changes ordinary MLP activation, not sliced loading. [inference; call_6e7735e0ef15418c9a29e6c2da2ff1c3, call_678f89cd89d94c01b8e058e52277a7cc]

<a id="modules"></a>

## Selectable activation for ordinary MLP

MLP now computes down(activation(up(x))) using a constructor-selected callable: F.silu for "silu", or a lambda invoking F.gelu with the tanh approximation for "gelu". This is selection at construction time, not a per-forward option; changing activation_fn alone afterward would not rebuild activation_fn_call. [source; call_678f89cd89d94c01b8e058e52277a7cc, call_800507643ca842c185878503bc45dce0]

The design resembles the existing GatedMLP selector but does not reuse its fused multiplication operations: ordinary MLP has one intermediate tensor, whereas GatedMLP passes gate and up tensors to ext.silu_mul or ext.gelu_mul. No existing F.gelu call was found in the parent tree. [source; call_800507643ca842c185878503bc45dce0, call_d88ce8dfaae7425487e8299693adb0cb]

TransformerBlock and ParallelDecoderBlock call their supplied mlp.forward without supplying an activation argument, so this patch does not require a forward-call signature change. Those consumers do not choose the new activation. [source; call_4e034e0018164798ac97a0e962c42fa3, call_678f89cd89d94c01b8e058e52277a7cc]

## Authoring-time findings — pending review

### unsupported-activation (suspected; defect)

Unrecognized activation strings leave the forward callable unset rather than producing an explicit configuration error.

Trigger: An external caller constructs an otherwise valid ordinary MLP with activation_fn="relu", then calls forward.

Expected: Reject the unsupported selection during construction or provide a defined activation.

Actual: Neither match arm assigns activation_fn_call; forward attempts to access it after the up projection. No in-tree ordinary MLP constructor caller was found, so reach is limited to the exposed API rather than a demonstrated model workflow.

Locations: 95c41ce0e15aa7362cc50aaf5d4efcd7dd4c2225:exllamav3/modules/mlp.py — MLP.__init__ / MLP.forward

Source evidence: call_678f89cd89d94c01b8e058e52277a7cc, call_800507643ca842c185878503bc45dce0, call_ebedf6a47d9f4a8b852063db570a1be3

source_inspection: Compared the complete patch with the parent MLP implementation and searched the whole parent tree for MLP references; inspected transformer forward consumers. [call_678f89cd89d94c01b8e058e52277a7cc, call_ebedf6a47d9f4a8b852063db570a1be3, call_4e034e0018164798ac97a0e962c42fa3]. Limits: No constructor or forward execution; external callers were not inspected.

## Uncertainty and limits

No PyTorch operation, model or GPU kernel was executed. PyTorch's implementation of the selected activations was not available in the inspected repository evidence; numerical accuracy and performance are unestablished.

No useful source-grounded numerical computation was needed for this callable-dispatch change; a scalar formula substitution would not test the selected PyTorch implementation.

Literal repository searches do not establish compatibility for dynamic or external callers.
