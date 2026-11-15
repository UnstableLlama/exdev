# 24aa1b7c7c44324d1da0e86fdda9f60316b7d01f


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/24aa1b7c7c44324d1da0e86fdda9f60316b7d01f) · [Evidence ledger](draft.json)

Adds composable min-p filtering and makes it the default before temperature scaling, replacing default top-p filtering.

- [Relative-probability filtering and revised defaults](#sampling)

## Problem

The sampler offered top-k and cumulative top-p filtering but no probability cutoff relative to the most likely token. [source; call_cc8aee7c156a4f0c89c67da90fb70c5c, call_cad0396b1b2943918f88727bc70a460d]

## Reasoning

SS_MinP retains weights at least min_p times the row maximum. Unlike top-p, it can operate without sorting and does not target a cumulative probability mass. [source; call_cad0396b1b2943918f88727bc70a460d, call_cc8aee7c156a4f0c89c67da90fb70c5c]

## Impact

The package exports SS_MinP, and DefaultSampler changes from temperature 0.75 followed by top-p 0.75 to min-p 0.08 followed by temperature 0.8. Existing explicit TopPSampler construction remains unchanged. [source; call_f1cfce236be9463f863991defb7c21d8, call_4ce759ad816e499096aa1d093e79ed7a, call_8bd794e9987d4bfa9a90b2c1d0baa30d]

## Source Notes

The earlier sampling entry identified a sorted-argmax assignment defect. Inspection of the parent and task diff shows that it is carried over, not corrected by this addition. [source; call_8a373489aba347d5802373334195800d, call_cc8aee7c156a4f0c89c67da90fb70c5c, call_cad0396b1b2943918f88727bc70a460d]

Issue #7, “quantizing model: undefined symbol: __cxa_call_terminate,” concerns extension loading; issue #15, “`cogito-v1-preview-qwen-32B` generates incoherent output for bpw <= 2.5,” concerns quantization regularization. Neither discussion supplies a stated motivation for this sampling change. [source; call_66a6812427334b0a8d7d04ef5f797ea7, call_8c09bad4cc0b4d64aa00ff3e501cea32]

<a id="sampling"></a>

## Relative-probability filtering and revised defaults

SS_MinP asserts 0 < min_p <= 1. For normalized unsorted probabilities it reduces the last dimension with amax; for normalized sorted probabilities it reads the first column. Both branches multiply by a >= threshold mask and mark the result unnormalized while preserving sortedness and token-index mappings. [source; call_cad0396b1b2943918f88727bc70a460d]

Its prep method requests SS_Normalize for raw logits or unnormalized weights. CustomSampler constructs prerequisites using an unchanged INIT planning state, so the new default actually runs normalization, min-p, temperature, then sampling. Normalization converts input logits to float before softmax. [source; call_cad0396b1b2943918f88727bc70a460d, call_cc8aee7c156a4f0c89c67da90fb70c5c, call_4ce759ad816e499096aa1d093e79ed7a]

The default cutoff is 8% of the largest probability, not an absolute probability of 0.08. Temperature follows filtering and raises retained weights to 1/0.8 = 1.25, changing their relative weights without changing the already selected support for finite positive inputs. [source; call_cad0396b1b2943918f88727bc70a460d, call_4ce759ad816e499096aa1d093e79ed7a, call_cc8aee7c156a4f0c89c67da90fb70c5c]

SS_Sample consumes these unnormalized weights through gumbel_noise_log and torch.argmax. The native wrapper requires matching float tensors; its kernel logs each weight and adds Philox-generated Gumbel noise. No additional normalization or sorting is inserted in the new default. [source; call_cc8aee7c156a4f0c89c67da90fb70c5c, call_9aa6bfd478274602bb4ded9c761cd0e4, call_4ce759ad816e499096aa1d093e79ed7a]

A scalar transcription on probabilities [0.5, 0.3, 0.125, 0.04, 0.035] produced threshold 0.04, retaining the equality-boundary token and removing only 0.035. Sorted and unsorted masks agreed; min_p=1 retained both tied maxima in [0.4, 0.4, 0.2]. [execution; call_5dffa793ded24326b231168f6df0725a]

Avoiding the old default's full sort is a plausible computational advantage, but the change also alters truncation semantics and temperature ordering; it is not merely an equivalent faster implementation. [inference; call_cc8aee7c156a4f0c89c67da90fb70c5c, call_4ce759ad816e499096aa1d093e79ed7a]

## Authoring-time findings — pending review

### inherited-sorted-argmax (suspected; defect)

The unchanged sorted branches of SS_Argmax do not populate the sample tensor.

Trigger: A custom chain reaches SS_Argmax with sorted logits or sorted probabilities, including a sorted min-p composition.

Expected: Map each row's selected position back to its token ID and assign state.sample.

Actual: The branches assign indexed values to state.state, then overwrite it with DONE; state.sample remains None, so forward cannot return its reshaped sample if indexing reaches completion.

Locations: 24aa1b7c7c44324d1da0e86fdda9f60316b7d01f:exllamav3/generator/sampler/custom.py — SS_Argmax.run

Source evidence: call_cc8aee7c156a4f0c89c67da90fb70c5c, call_cad0396b1b2943918f88727bc70a460d, call_6d9d3c99556044358f373889e6c75075, call_8bd794e9987d4bfa9a90b2c1d0baa30d

source_inspection: Whole-parent-tree SS_Argmax search and preset inspection found built-in uses starting directly from INIT. The new default uses SS_Sample, so this observation concerns custom sorted-greedy compositions rather than DefaultSampler. [call_6d9d3c99556044358f373889e6c75075, call_8bd794e9987d4bfa9a90b2c1d0baa30d, call_4ce759ad816e499096aa1d093e79ed7a]. Limits: No repository execution or external custom-caller inventory.

## Uncertainty and limits

Checks used standard-library binary64 scalar arithmetic, not PyTorch, CUDA, cuRAND or repository execution.

No generation-quality, sampling-frequency or performance measurements establish benefits of the new defaults; the rationale for choosing 0.08 and 0.8 is unestablished.
