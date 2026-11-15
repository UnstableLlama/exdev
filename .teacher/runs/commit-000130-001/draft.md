# 2e7b00d3b0d1731e86d127b992ae6298dd70a504


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/2e7b00d3b0d1731e86d127b992ae6298dd70a504) · [Evidence ledger](draft.json)

Flushes unresolved Unicode output once re-decoded text exceeds 20 characters, avoiding prolonged holding but introducing an early-flush path that bypasses string checks.

- [Escape from unresolved Unicode buffering](#generation)

## Problem

Unresolved replacement characters could keep accumulating output in Job's held buffers instead of streaming it. The parent returned metadata-only events whenever re-decoding still contained �. [source; call_580f8ffeba384dd29447142ef75f6997]

## Reasoning

The change retains short-buffer waiting but flushes when the re-decoded string exceeds 20 characters. This trades continued Unicode reconstruction for forward progress; it is a character-length heuristic, not a timeout or token limit. [source; call_2fca40b8b43e4f5b88e87ed423886144, call_580f8ffeba384dd29447142ef75f6997]

## Impact

The escape flush emits the existing held_text and associated token/probability/logit buffers, clears them, and continues generation without EOS. It does not replace held_text with test_decode on this failure branch. [source; call_2fca40b8b43e4f5b88e87ed423886144, call_580f8ffeba384dd29447142ef75f6997]

## Source Notes

Issue #21, “Build Failure on Windows: CUDA 12.4 / PyTorch 2.7.0+cu126 / VS 2022,” reports compilation failures and was closed without an identified solution; its text does not establish a connection to this streaming change. [source; call_2ae57eee9ac64b0183e8afb8542a9070]

The earlier generation entry records a banned-string checkpoint attribute error and a terminal-budget bypass. Both remain in the inspected parent code and are untouched by this patch. [source; call_580f8ffeba384dd29447142ef75f6997, call_2fca40b8b43e4f5b88e87ed423886144]

<a id="generation"></a>

## Escape from unresolved Unicode buffering

receive_sample appends token pieces and optional output data before checking stop tokens and the generation budget. Only held text containing one through four replacement characters enters the re-decode branch; five or more already bypass that branch. Successful re-decoding replaces held_text and proceeds to string checks. [source; call_580f8ffeba384dd29447142ef75f6997]

On unsuccessful re-decoding, the patch changes only emit_held: false through length 20, true above 20. emit appends an event either way and returns the EOS flag and sampled token, so holding text never meant suspending the sampling loop itself. [source; call_2fca40b8b43e4f5b88e87ed423886144, call_580f8ffeba384dd29447142ef75f6997]

Whole-parent search found one direct receive_sample call site in generator.py. It consumes sampled logits, tests the returned EOS flag, and otherwise continues ordinary or speculative sampling; the new flush therefore does not mark the job completed. [source; call_9a1d3b93b61042769a0cdef8aa30aee6, call_724c74e0a9b844faa2c911f9a4a42278]

A standard-library predicate transcription confirmed that a single replacement character followed by ordinary characters remains held at length 20 and selects flushing at length 21. A 21-character fixture ending in 'bad' also selects this return before string matching. [execution; call_4bb4cd8bbbd248229906abacec723c95]

## Authoring-time findings — pending review

### unicode-flush-bypasses-string-checks (suspected; defect)

The new escape flush can expose banned text or miss a stop string.

Trigger: Before token-budget termination, held_text contains one through four replacement characters, re-decoding still contains one, and test_decode exceeds 20 characters while the buffer contains a configured banned or stop string.

Expected: Apply string suppression or stopping before emitting the buffered text.

Actual: The new branch returns through emit_held=True before either string matcher runs, emitting and clearing the buffer. The sole located direct caller continues sampling because EOS is false.

Locations: 2e7b00d3b0d1731e86d127b992ae6298dd70a504:exllamav3/generator/job.py — Job.receive_sample

Source evidence: call_2fca40b8b43e4f5b88e87ed423886144, call_580f8ffeba384dd29447142ef75f6997, call_724c74e0a9b844faa2c911f9a4a42278, call_9a1d3b93b61042769a0cdef8aa30aee6

scalar_transcription: Checked the new predicate with � followed by 17 x characters and 'bad': length 21 selects the early flush. [call_4bb4cd8bbbd248229906abacec723c95]. Limits: Assumes the stated tokenizer output; does not execute the tokenizer or native string matcher.

### retained-checkpoint-token-attribute (suspected; defect)

The inherited banned-string rewind still restores the wrong token-buffer attribute.

Trigger: A full banned-string match reaches rewind_checkpoint.

Expected: Restore held_tokens so rejected IDs appear only in suppressed_tokens.

Actual: The code assigns self.held_token instead of self.held_tokens; the subsequent flush can emit rejected IDs from the unchanged buffer. This remains reachable through the single located receive_sample caller.

Locations: 2e7b00d3b0d1731e86d127b992ae6298dd70a504:exllamav3/generator/job.py — Job.receive_sample.rewind_checkpoint

Source evidence: call_580f8ffeba384dd29447142ef75f6997, call_2fca40b8b43e4f5b88e87ed423886144, call_9a1d3b93b61042769a0cdef8aa30aee6

source_inspection: Compared checkpoint restoration with the buffer read by emit and confirmed the task leaves both unchanged. [call_580f8ffeba384dd29447142ef75f6997, call_2fca40b8b43e4f5b88e87ed423886144]. Limits: Tensor operations were not executed.

### retained-terminal-string-bypass (suspected; defect)

The inherited token-budget flush still precedes banned-string checking.

Trigger: A non-stop token completes a banned string when new_tokens reaches max_new_tokens minus num_draft_tokens.

Expected: Suppress the banned string before terminal emission.

Actual: receive_sample flushes held output and returns EOS before reaching the banned-string matcher. The located generator caller then completes the job.

Locations: 2e7b00d3b0d1731e86d127b992ae6298dd70a504:exllamav3/generator/job.py — Job.receive_sample

Source evidence: call_580f8ffeba384dd29447142ef75f6997, call_2fca40b8b43e4f5b88e87ed423886144, call_724c74e0a9b844faa2c911f9a4a42278

source_inspection: Inspected terminal branch ordering and caller EOS handling; neither is changed by the patch. [call_580f8ffeba384dd29447142ef75f6997, call_724c74e0a9b844faa2c911f9a4a42278]. Limits: No generation execution.

## Uncertainty and limits

No tokenizer, tensor-buffer implementation, model generation or repository tests were executed. The scalar check models only string predicates and branch ordering.

No tuning evidence establishes why 20 characters is the appropriate cutoff. The condition does not guarantee bounded elapsed waiting when decoded length does not grow.
