# 083729ba09c51485813e707672966e12ca54b9df


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/083729ba09c51485813e707672966e12ca54b9df) · [Evidence ledger](draft.json)

Broadens tensor-diagnostic path filtering for debugger references and imports the helper into quantize.py without adding a call.

- [Exclude additional debugger paths from tensor diagnostics](#runtime)

## Problem

The tensor diagnostic previously excluded only paths containing '.stderr.dbg.'. This change broadens that filter to include 'dbg.value_resolve_thread_list', consistent with the commit's reported PyCharm-debugger motivation. [source; call_16a1a459754843a5ba412abb6655b569]

## Reasoning

Filtering occurs inside collect, after tensor, device and size checks but before recording the reference. It suppresses matching diagnostic paths; it does not release tensors or prune the traversal queue. [source; call_b81de8bb666243e784f819e244f0e88d, call_16a1a459754843a5ba412abb6655b569]

## Impact

quantize.py imports list_gpu_tensors alongside free_mem, but the patch adds no invocation. A whole-parent-tree literal search found only the helper definition and its explanatory comment, not callers. [source; call_4a128cc477614cfa8e124ca43bc8aa0c, call_db35159dc0444684bb9ffe131476129e]

## Source Notes

The earlier cleanup entry describes the optional non-CUDA filter and per-device diagnostic tables; this change leaves those interfaces intact. [ancestor; call_503ad2242d604546b3a06ef0f388b9a5]

Issue #7, 'quantizing model: undefined symbol: __cxa_call_terminate', reports an extension import failure and a reporter-described environment workaround, not debugger references. [source; call_46e3685520e94ee99cb39ddebe9bfe12]

<a id="runtime"></a>

## Exclude additional debugger paths from tensor diagnostics

list_gpu_tensors traverses globals, thread-frame locals, attributes, dictionary entries and sequences, collecting tensor references by object identity for size-sorted, per-device tables. The new any-substring predicate retains the existing exclusion and adds a second spelling. [source; call_b81de8bb666243e784f819e244f0e88d, call_16a1a459754843a5ba412abb6655b569]

Because exclusion is path-based rather than object-based, an otherwise reachable tensor can still be recorded through an unfiltered reference. The tradeoff is a narrow diagnostic-output filter rather than debugger-aware object detection. [inference; call_b81de8bb666243e784f819e244f0e88d, call_16a1a459754843a5ba412abb6655b569]

A scalar predicate check preserved exclusion of the old stderr path, newly excluded worker.dbg.value_resolve_thread_list[0], and retained model.weight. A dictionary-form path containing dbg['value_resolve_thread_list'] did not match either substring, illustrating the filter's literal spelling boundary. [execution; call_6b311919be0c42b89dc9d88f91a371b7]

## Uncertainty and limits

No live PyCharm session, tensor traversal or CUDA execution was tested. The parent-tree search found no literal PyCharm occurrence establishing debugger internals.

The Python check transcribed only the string predicate; it did not execute list_gpu_tensors. Literal caller searches do not exclude external or dynamic use.
