# c8836d9f5abf58ca7967c08beb39a23be675e10e


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/c8836d9f5abf58ca7967c08beb39a23be675e10e) · [Evidence ledger](draft.json)

Adds filename and errno diagnostics for native Safetensors open failures and expands read-error reporting, with an incomplete errno handoff in deferred CUDA loading.

- [Safetensors failure diagnostics](#loading)

## Problem

Native Safetensors open failures previously raised only “Error opening file,” omitting both the filename and operating-system error. [source; call_f552362b72494a7c835101de327d86b1]

## Reasoning

The patch captures errno immediately after a failed fopen and includes the filename, strerror description and numeric errno in TORCH_CHECK. Python adds a filename message before re-raising RuntimeError in both native loading branches. [source; call_6bebc10cc86d49eca964daddfcb04e42, call_cae1ab32a4ca4e4baf048c0c5dc9afa8]

## Impact

This improves failure diagnostics rather than repairing the underlying file-open failure: there is no retry, fallback or change to successful handle caching. Python header reading and the explicit python loading backend remain unchanged. [source; call_6bebc10cc86d49eca964daddfcb04e42, call_cae1ab32a4ca4e4baf048c0c5dc9afa8, call_21480e974c4c4f6cab39052a2799605b]

## Source Notes

Issue #33, “Error converting model,” reports a conversion traceback through get_tensor into stloader_open_file with the old generic error. Its relationship to this patch is inferred from that exact call and message match, plus a turboderp comment promising more informative diagnostics; the discussion does not establish the filesystem root cause. [inference; call_a25ff05dabe84afc9ddb8ec25a48af73, call_9fa62498bdbe44bbaecf98f04bf297c3, call_6bebc10cc86d49eca964daddfcb04e42]

Closed issue #17, “ModuleNotFoundError: No module named 'torch' when installing requirements.txt,” concerns installation and Flash-Attention dependencies, not a reported Safetensors file-open failure. [source; call_a8b0019f78cb41b799da5136441d9d4a]

<a id="loading"></a>

## Safetensors failure diagnostics

get_tensor resolves a tensor key to its filename and lazily opens native handles only when none are cached. The new Python guards cover both immediate mt_fread loading and deferred job creation; failed opens print the filename and propagate the exception without caching a result. [source; call_21480e974c4c4f6cab39052a2799605b, call_cae1ab32a4ca4e4baf048c0c5dc9afa8]

For immediate reads, worker error paths now copy errno into shared load_errnum, and the post-join check formats its description and number. CUDA copy failures still emit cudaGetErrorString separately. These changes add diagnostic information without changing chunk scheduling or transfer selection. [source; call_f552362b72494a7c835101de327d86b1, call_6bebc10cc86d49eca964daddfcb04e42]

Deferred error reporting is asymmetric: the CPU worker captures errno but retains the generic post-join exception; the CUDA post-join exception gains errno formatting, but its worker never assigns load_errnum. [source; call_f552362b72494a7c835101de327d86b1, call_6bebc10cc86d49eca964daddfcb04e42]

## Authoring-time findings — pending review

### deferred-cuda-error-number (suspected; defect)

The new deferred-CUDA diagnostic reports an initialized zero rather than the worker's error number.

Trigger: A read, seek or CUDA-copy failure reaches stloader_deferred_cuda's worker error label and subsequently reaches its post-join failure check.

Expected: The diagnostic should preserve the relevant failure information rather than present zero as the captured error number.

Actual: load_errnum is initialized to zero and never assigned in this function; the worker sets only load_failed, so the new exception formats strerror(0) and errno=0.

Locations: c8836d9f5abf58ca7967c08beb39a23be675e10e:exllamav3/exllamav3_ext/stloader.cpp — stloader_deferred_cuda

Source evidence: call_f552362b72494a7c835101de327d86b1, call_6bebc10cc86d49eca964daddfcb04e42, call_799a05a0f7694cb58045ece543cb9d0f, call_21480e974c4c4f6cab39052a2799605b

source_inspection: Compared the complete parent function with the task diff. Whole-parent-tree literal caller search found the Python invocation in SafetensorsCollection.end_deferred_load and the native binding; the inspected caller passes CUDA workloads to this function. The observation therefore concerns deferred CUDA loads, not every get_tensor call. [call_f552362b72494a7c835101de327d86b1, call_6bebc10cc86d49eca964daddfcb04e42, call_799a05a0f7694cb58045ece543cb9d0f, call_21480e974c4c4f6cab39052a2799605b]. Limits: No failure was induced; native exception propagation and runtime error text were not tested.

## Uncertainty and limits

No native extension, filesystem failure or CUDA path was executed. A scalar computation would not meaningfully validate errno propagation, thread synchronization or exception handling.

The underlying cause of the conversion failure reported in issue #33 remains unestablished.
