# 33466d785591bdd69dd43821e22730a55f0067f9


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/33466d785591bdd69dd43821e22730a55f0067f9) · [Evidence ledger](draft.json)

Implements optional token-probability diagnostics, but leaves default generation with unbound return values and reports probabilities that can differ from the final sampling distribution.

- [Probability reporting through the existing streaming interface](#generation)

## Problem

Job already exposed probability and top-token options, but their enabled branches were placeholders that left return values unassigned. [source; call_70aaa906ec62402385cf096fbb4359e1]

## Reasoning

The change computes one float softmax when either output is requested, gathers the sampled token's probability, and sorts the distribution only when top-token output is requested. This supplies the existing four-value return interface without changing the sampler API. [source; call_82d895a578024b818574576e1a18384e]

## Impact

Enabled options now receive computed values, but the default disabled-options path loses its None assignments and fails at return. Reported probabilities also need not equal the final sampling probabilities promised by the existing documentation. [source; call_82d895a578024b818574576e1a18384e, call_70aaa906ec62402385cf096fbb4359e1, call_d0d0defe8bf74083916ac84d349ad189]

## Source Notes

The root generation entry was read completely. It records the optional-output placeholders and the downstream buffer contract; the task changes that recorded failure rather than simply carrying it over. [ancestor; call_ddf496fde2f24e25b3ede72b2fe0f86b, call_75ea932c48c541398bb99e064ef1ea0a]

Issue #12, “Qwen2.5 Coder 0.5B Instruct | ValueError: Unsupported type in stop_conditions,” concerns constructor validation and a chat-template selection mistake. Its relationship to this task is only an inferred shared-file connection: the traceback names job.py, but the task changes receive_logits, not stop-condition validation. [inference; call_9af095496c184f9fa946b7afdcc5bcca, call_1e1482d9d7334411a74deae61454e43c, call_82d895a578024b818574576e1a18384e]

<a id="generation"></a>

## Probability reporting through the existing streaming interface

receive_logits still samples first. It then applies softmax to logits.float() along the vocabulary dimension. For a single-sequence, single-position input, squeeze(0) and gather produce a (1,1) chosen-token probability; descending sorting followed by slicing produces (1,1,k) token IDs and probabilities when k does not exceed vocabulary width. Zero disables top-token reporting; it is not a sampling cutoff. [source; call_82d895a578024b818574576e1a18384e, call_acbe54802ffd4a15af8d2ef2d3fceca0]

Whole-parent searches locate one active receive_logits caller in Generator.iterate_gen and one commented threading alternative. The active caller passes each position's logits, unpacks all four outputs, and forwards them unchanged to receive_sample. Existing conditional appends and buffers agree with the new single-sequence shapes and emit token_probs, top_k_tokens and top_k_probs, including held terminal output. No constructor defaults or consumer changes accompany the implementation. [source; call_16f986731d0e43fc89143e7c0f8e15aa, call_a4b80b50a30a4c5687dee752cc4dd694, call_3c95386bee874355a6c016d0c8af433f, call_4f7a9574bff24e71b6fa7fd502dcbbd2, call_0bbf63c9d4e64d2e84f706ae380f9fb2, call_acbe54802ffd4a15af8d2ef2d3fceca0, call_70aaa906ec62402385cf096fbb4359e1]

Computing diagnostics outside the sampler avoids extending its return interface, but duplicates normalization and uses a full vocabulary sort for top-token output. It also disconnects diagnostics from the sampler's transformed distribution: CustomSampler masks padded vocabulary entries in place, but clones for allowed/blocked-token masks and performs default min-p and temperature processing in separate probability state. [source; call_82d895a578024b818574576e1a18384e, call_d0d0defe8bf74083916ac84d349ad189, call_aadfdf31404742629319b18c8040e94d]

A scalar transcription returned values for all three enabled-option combinations but raised UnboundLocalError for both options disabled. For logits [0,2], raw softmax assigns the higher token 0.880797; default min-p 0.08 retains both tokens, and temperature 0.8 changes its normalized sampling probability to 0.924142. [execution; call_f9aee3d96d6146a1beacd4a777f9b846]

## Authoring-time findings — pending review

### disabled-options-unbound (suspected; defect)

Default generation no longer initializes optional return values.

Trigger: receive_logits completes sampling with return_probs=False and return_top_tokens=0, the constructor defaults.

Expected: Return the sampled token followed by three None values.

Actual: The outer conditional is skipped and the return references unassigned next_k_tokens, next_k_probs and next_prob. The sole active direct caller, Generator.iterate_gen, cannot proceed to receive_sample. Generator.generate constructs jobs without overriding these defaults.

Locations: 33466d785591bdd69dd43821e22730a55f0067f9:exllamav3/generator/job.py — Job.receive_logits

Source evidence: call_82d895a578024b818574576e1a18384e, call_70aaa906ec62402385cf096fbb4359e1, call_16f986731d0e43fc89143e7c0f8e15aa, call_acbe54802ffd4a15af8d2ef2d3fceca0

scalar_transcription: Executed the changed conditional assignments using scalar/list stand-ins across four option combinations; only the disabled combination raised UnboundLocalError. [call_f9aee3d96d6146a1beacd4a777f9b846]. Limits: Not execution of Job, its sampler or tensor operations.

### reported-probabilities-not-final (suspected; defect)

Probability diagnostics do not generally represent the documented final sampling distribution.

Trigger: Enable probability or top-token reporting while using distribution-changing sampling, including DefaultSampler, or allowed/blocked-token constraints.

Expected: Report chosen-token and top-token probabilities after applicable sampling transformations and constraints.

Actual: receive_logits normalizes its logits argument rather than the transformed sampler state. DefaultSampler's min-p and temperature changes are absent; cloned token constraints are absent too, so forbidden tokens can appear in reported top candidates. The active generator caller passes these diagnostics directly to streaming buffers without correction.

Locations: 33466d785591bdd69dd43821e22730a55f0067f9:exllamav3/generator/job.py — Job.receive_logits

Source evidence: call_82d895a578024b818574576e1a18384e, call_70aaa906ec62402385cf096fbb4359e1, call_d0d0defe8bf74083916ac84d349ad189, call_aadfdf31404742629319b18c8040e94d, call_acbe54802ffd4a15af8d2ef2d3fceca0

source_inspection: Compared the documented final-probability contract with CustomSampler's cloned masks and separate probability transformations. [call_70aaa906ec62402385cf096fbb4359e1, call_d0d0defe8bf74083916ac84d349ad189]. Limits: Does not characterize arbitrary external samplers.

scalar_transcription: Calculated raw and default-temperature-adjusted probabilities for logits [0,2], obtaining 0.880797 versus 0.924142 for the higher token. [call_f9aee3d96d6146a1beacd4a777f9b846]. Limits: Double-precision arithmetic model, not native random sampling or GPU validation.

## Uncertainty and limits

No repository generation, PyTorch tensor operation, CUDA kernel or performance benchmark was executed. The bounded check models Python branching and probability arithmetic with standard-library doubles.

Single-sequence output shapes were traced; successful collective multi-sequence sampling and arbitrary external sampler behavior are not established.
