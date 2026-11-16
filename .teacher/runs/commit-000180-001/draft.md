# bc3d38f04de2afbddf51e89986f91090137dec8a


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/bc3d38f04de2afbddf51e89986f91090137dec8a) · [Evidence ledger](draft.json)

Adds an optional profiling helper and imports it in six runtime modules; absent profiling instrumentation becomes an identity decorator, without adding active profiling sites.

- [Optional profiling through import-time initialization](#profiling)

## Problem

The new helper addresses optional profiling: its docstring specifies making @profile a no-op when kernprof has not injected it. [source; call_27c32e488286466b995742b080168a5b]

## Reasoning

Importing profile_opt installs an identity decorator in builtins only if profile is absent. An existing binding is preserved, and the module exports that binding as profile. [source; call_27c32e488286466b995742b080168a5b]

Using builtins enables bare @profile decorators without importing profile into each module's globals. The tradeoff is a process-wide binding rather than a module-local fallback. [inference; call_27c32e488286466b995742b080168a5b, call_82ee358926414547b847fb0f307d23b2]

## Impact

Six modules import the helper: generator, job, custom sampler, attention, block-sparse MLP and transformer. These imports activate its initialization; the diff adds no profiling decorators or changes to their computational methods. [source; call_a9d44bf7c1b44135875d0d1abc7332b2, call_92a2402bd3cd4cf78639bf3b76c2966b, call_8adf6aae66d8407e9d6260d5be76814f, call_020c38ccfb6741c883c08963e16d840e, call_9c559139eeaf44028222107f2fb69355, call_1ab70d6f86d44e7d9a4064e1af505ac3]

## Source Notes

Whole-parent-tree search for profile found no existing Python profiling decorator or helper usage; matches were comments, build-script profiler references and calibration text. This does not exclude external instrumentation. [source; call_457cd9bb8a9c4fb494b382d5b7dbb788]

The parent entry read describes the preceding routing optimization and records a conditional all-expert fused-buffer mismatch. This task only adds a module-level import to that file; inspection shows its routing cardinality, fused guard and buffer allocations remain unchanged. [source; call_1eda6fd90bd84c4581e8c7f23113f966, call_7ae930b7a18949249da401c0b2ed5b2d, call_9c559139eeaf44028222107f2fb69355]

Issue #12, “Qwen2.5 Coder 0.5B Instruct | ValueError: Unsupported type in stop_conditions,” concerns chat mode selection. Issue #16, “RuntimeError: CUDA error: invalid configuration argument,” concerns conversion and tokenizer truncation. Their inferred connection here is only shared traceback paths—job.py and attention/transformer files—not evidence motivating this profiling utility. [inference; call_1eac693912be4f1eb311253ca3d9abae, call_bbf34e0f55dc42d6b5ec1aec1dd2b0b5, call_92a2402bd3cd4cf78639bf3b76c2966b, call_020c38ccfb6741c883c08963e16d840e, call_1ab70d6f86d44e7d9a4064e1af505ac3]

<a id="profiling"></a>

## Optional profiling through import-time initialization

The helper and its six imports work together: imports establish the fallback before subsequent definitions can use bare @profile. The fallback returns the original function rather than introducing a wrapper, while an already injected profiler remains available. [source; call_27c32e488286466b995742b080168a5b, call_a9d44bf7c1b44135875d0d1abc7332b2, call_92a2402bd3cd4cf78639bf3b76c2966b, call_8adf6aae66d8407e9d6260d5be76814f, call_020c38ccfb6741c883c08963e16d840e, call_9c559139eeaf44028222107f2fb69355, call_1ab70d6f86d44e7d9a4064e1af505ac3]

A standard-library transcription passed checks for fallback function identity, bare-decorator name resolution and preservation of a preexisting profile binding. These checks establish those isolated Python semantics, not profiler integration. [execution; call_82ee358926414547b847fb0f307d23b2]

## Uncertainty and limits

No package import, kernprof integration, GPU execution or performance measurement was performed. The standalone check executed a transcription of the new helper, not the repository implementation.

The helper's stated kernprof injection convention was not independently verified against eligible profiler documentation.
