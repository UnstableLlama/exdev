# cf220845799b12c9475232e2cb309db360f083d3


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/cf220845799b12c9475232e2cb309db360f083d3) · [Evidence ledger](draft.json)

Fixes uninitialized optional outputs when probability reporting is disabled; enabled diagnostics and their inherited distribution mismatch remain unchanged.

- [Initialize optional sampling outputs on every return path](#generation)

## Problem

With the default return_probs=False and return_top_tokens=0, Job.receive_logits skipped every assignment to its optional outputs, then referenced them at return. [source; call_7d301b17f49143c393e63591e5bfaba7]

## Reasoning

Initialize all three optional outputs to None before testing the reporting options. Enabled branches overwrite only the requested outputs; removing their else assignments is safe because the new initialization supplies those defaults. [source; call_0fbb377cc1f644499369da030837007c]

## Impact

Removes the disabled-options unbound-local failure without changing the four-value return order or enabled probability calculations. [source; call_0fbb377cc1f644499369da030837007c]

## Source Notes

The immediate parent's entry was read in full. It records both the disabled-options failure and a separate mismatch between reported probabilities and the final sampling distribution. [ancestor; call_4a4330f56cad47ceb64b4d66ec4faa63]

Issue #12, “Qwen2.5 Coder 0.5B Instruct | ValueError: Unsupported type in stop_conditions,” reports constructor validation failure and discusses using chatml instead of llama3 mode. Its connection here is only an inferred shared-file relationship: its traceback names job.py, whereas this patch changes receive_logits, not constructor validation. [inference; call_7056bcc6f017462e97d03e6f991b9768, call_5faeaf4eb88b4c83a2f66d78b8ba325e, call_0fbb377cc1f644499369da030837007c]

<a id="generation"></a>

## Initialize optional sampling outputs on every return path

Sampling still happens first. Probability softmax runs only when return_probs is enabled or return_top_tokens is positive; zero disables top-token reporting. The patch adds no tensor computation to the disabled path. [source; call_7d301b17f49143c393e63591e5bfaba7, call_0fbb377cc1f644499369da030837007c]

A whole-parent search found one active direct caller, Generator.iterate_gen, and one commented threading alternative. The active caller unpacks all four values and forwards them to receive_sample, whose probability-buffer appends are guarded by the same reporting options. None therefore fits the existing disabled-output consumer contract. [source; call_de0814043b06449fad52d3d3089aaf8d, call_e33d2277b2bc4d348f0f025165796464, call_c0dfd402c3f149ba9eb9694d70c96783, call_7d301b17f49143c393e63591e5bfaba7]

A scalar branch transcription tested all four enabled/disabled combinations before and after the edit. Only the old both-disabled case raised UnboundLocalError; the new case returned the token plus three None values. The other three combinations retained identical stand-in outputs. [execution; call_6e0150aba872430497eb0fa25d6be52f]

Source comparison removes the parent's recorded initialization defect but carries over its probability-reporting mismatch: the patch leaves the post-sampling softmax of logits unchanged rather than obtaining the sampler's transformed distribution. [source; call_0fbb377cc1f644499369da030837007c, call_7d301b17f49143c393e63591e5bfaba7, call_eb7edfe47e1648738e7411310ab82764]

## Authoring-time findings — pending review

### inherited-probability-contract (suspected; defect)

Optional diagnostics still need not represent the documented final sampling probabilities.

Trigger: Enable probability or top-token reporting with CustomSampler while supplying allowed_tokens or blocked_tokens that exclude a token with finite input logits.

Expected: Final sampling probabilities reflect the constraints, excluding forbidden candidates.

Actual: CustomSampler clones logits before applying these constraints. Job.receive_logits subsequently normalizes its original logits, so excluded tokens retain reported probability and can appear in top-token output. The sole active direct caller forwards those diagnostics unchanged into receive_sample's streaming buffers.

Locations: cf220845799b12c9475232e2cb309db360f083d3:exllamav3/generator/job.py — Job.receive_logits

Source evidence: call_7d301b17f49143c393e63591e5bfaba7, call_eb7edfe47e1648738e7411310ab82764, call_0fbb377cc1f644499369da030837007c, call_de0814043b06449fad52d3d3089aaf8d, call_e33d2277b2bc4d348f0f025165796464

source_inspection: Compared the final-probability documentation, cloned constraint masks, unchanged diagnostic calculation and direct caller's forwarding. [call_7d301b17f49143c393e63591e5bfaba7, call_eb7edfe47e1648738e7411310ab82764, call_0fbb377cc1f644499369da030837007c, call_e33d2277b2bc4d348f0f025165796464]. Limits: No tensor execution; this observation concerns the inspected CustomSampler path, not every external sampler.

## Uncertainty and limits

The executed check transcribed Python assignment branches with string stand-ins; it did not execute Job, PyTorch operations, sampling or GPU generation.

End-to-end generation success and performance were not measured.
