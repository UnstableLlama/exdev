# dfd01ce7c68baf52656c1fe2387b4371b227a199


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/dfd01ce7c68baf52656c1fe2387b4371b227a199) · [Evidence ledger](draft.json)

Extends tensor-diagnostic path filtering with three debugger-style indexed-variable names, leaving traversal and tensor lifetime unchanged.

- [Suppress additional debugger-style tensor-reference paths](#runtime)

## Problem

The tensor diagnostic's existing exclusion predicate did not cover paths containing global_vars[, local_vars[ or updated_globals[. The patch adds those three spellings. [source; call_7174c6a3ee854dfd8ebc55bd10153125]

## Reasoning

Filtering inside collect suppresses matching tensor references before result recording, without changing traversal or freeing tensors. [source; call_4b1d64273f3941629709f0e60f946fe3, call_7174c6a3ee854dfd8ebc55bd10153125]

## Impact

The whole-parent-tree literal search found an import in quantize.py but no invocation of list_gpu_tensors. The demonstrated scope is diagnostic reporting, not a newly activated conversion path. [source; call_d35b4f6d848e4f8a80e2e52b38037a3a, call_7174c6a3ee854dfd8ebc55bd10153125]

## Source Notes

The earlier debugger-filter entry describes adding dbg.value_resolve_thread_list; this patch retains that exclusion. [ancestor; call_434851e47aed452d9d75d3e5a7e1640b]

Issue #7, “quantizing model: undefined symbol: __cxa_call_terminate”, reports a native-extension import failure, not debugger-reference filtering. [source; call_d1bf41d1923d4f91a74cd92776ef04fe]

<a id="runtime"></a>

## Suppress additional debugger-style tensor-reference paths

list_gpu_tensors traverses globals, thread frames, attributes, dictionaries and sequences. collect applies tensor/device and size checks, then path exclusions, before grouping references by tensor identity for size-sorted, per-device tables. The patch changes only the exclusion list. [source; call_4b1d64273f3941629709f0e60f946fe3, call_7174c6a3ee854dfd8ebc55bd10153125]

The added strings match indexed paths produced by dictionary and sequence traversal. Matching is substring-based, not debugger-object detection: ordinary application paths containing those strings are also suppressed, while another unfiltered reference can still expose the same tensor. [source; call_4b1d64273f3941629709f0e60f946fe3, call_7174c6a3ee854dfd8ebc55bd10153125]

A standard-library predicate transcription newly excluded examples for all three added strings, retained model.weight and model.global_vars_weight, and preserved the existing debugger-thread exclusion. It also excluded model.global_vars['weight'], illustrating the name-based boundary. [execution; call_7d1e81f30868427a9398e70b779e166b]

This favors a small diagnostic-output filter over debugger-aware traversal pruning; it does not establish reduced traversal cost or memory use. [inference; call_4b1d64273f3941629709f0e60f946fe3, call_7174c6a3ee854dfd8ebc55bd10153125]

## Uncertainty and limits

No live debugger session, tensor traversal or CUDA behavior was tested; the computation tested only a transcribed string predicate.

Literal searches do not exclude dynamic or external callers. The provenance of the three new path spellings in debugger internals remains unverified.
