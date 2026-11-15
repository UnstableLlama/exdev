# 448815bc1cf7b17e714a52fe6f70bcb53da48147


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/448815bc1cf7b17e714a52fe6f70bcb53da48147) · [Evidence ledger](draft.json)

Adds callback and generator-based progress to autosplit model loading while retaining blocking load. Explicit-device loading omits the new notifications, and iterator exhaustion is necessary to reach cleanup.

- [Iterable loading progress and callback delivery](#models)

## Problem

The loader exposed a blocking load operation and an optional progress bar, but no callback or iterable progress interface. [source; call_74dd42bb83fb44e99939e5ed73e27378]

## Reasoning

The change moves loading orchestration into load_gen and makes load exhaust that generator with generator=False. This shares loading logic while preserving the blocking interface. [source; call_95016320fa484754b1adc4026ad5f26f]

## Impact

Autosplit loading can report progress through a callback, generator yields, or both, alongside the existing progress bar. Explicit-device loading does not receive the new notifications. [source; call_95016320fa484754b1adc4026ad5f26f, call_74dd42bb83fb44e99939e5ed73e27378]

## Source Notes

The earlier loader documentation entry explains the distinction between usage budgets and reserved memory; this change retains those argument-normalization branches. [ancestor; call_fb6e1d5f490f49f1a55c0447a7b381bd]

Issue #7, “quantizing model: undefined symbol: __cxa_call_terminate,” reports an extension import failure; issue #15, “`cogito-v1-preview-qwen-32B` generates incoherent output for bpw <= 2.5,” concerns quantization quality. Neither establishes motivation for this loader interface change. The inferred connection to #7 is only its traceback passing through model.py. [inference; call_e02592d307004596b3962070f90d76c7, call_38bc171a817d40e3a02dc5649dc3ed4f, call_95016320fa484754b1adc4026ad5f26f]

<a id="models"></a>

## Iterable loading progress and callback delivery

_load_autosplit invokes the callback and optionally yields (idx, module_count) before attempting each module. Consequently idx counts completed modules, starting at zero; retries on another device do not emit additional notifications. A final (module_count, module_count) notification follows successful completion of the loop. [source; call_95016320fa484754b1adc4026ad5f26f, call_74dd42bb83fb44e99939e5ed73e27378]

Autosplit still loads a module, forwards dummy state through it to estimate memory requirements, and retries on another device after an out-of-memory failure. The new notifications surround this existing mechanism rather than changing its placement policy. [source; call_74dd42bb83fb44e99939e5ed73e27378, call_95016320fa484754b1adc4026ad5f26f]

The generator pauses before each module and again at its terminal progress tuple. Memory-limit reset, dummy-state release and safetensor-context closure occur only after iteration resumes beyond that terminal tuple. Consumers should exhaust the iterator rather than treat receipt of the final tuple as completed cleanup. [source; call_95016320fa484754b1adc4026ad5f26f, call_74dd42bb83fb44e99939e5ed73e27378]

A two-module scalar transcription emitted progress (0,2), (1,2), and (2,2), with cleanup and context closure occurring only on the subsequent exhaustion step. Disabling yields still performed both modeled loads and cleanup when the generator was exhausted. [execution; call_180388d61caf441c83ae91edf45ef2f4]

The new loading example demonstrates repeated load/unload cycles, attaching and detaching a cache, callback-only loading, generator iteration, and combining callback, iterator and progress bar. Its generator examples use ordinary for loops, which exhaust the iterator. [source; call_5b8f80b4dee244a98a6928a94e362f7c]

A whole-parent-tree search found only Model.load calling the private _load_autosplit helper; the diff updates that call with both newly required arguments. [source; call_6bc1d0769dd748acb77c3cd33a76747a, call_95016320fa484754b1adc4026ad5f26f]

## Authoring-time findings — pending review

### single-device-progress (suspected; behavior_change)

The advertised progress interfaces cover autosplit loading but silently omit explicit-device loading.

Trigger: Call load(device=..., callback=...) or iterate load_gen(device=...).

Expected: Receive callback or iterator progress for the selected loading mode.

Actual: The device branch calls unchanged _load_single(progressbar, device), which neither invokes the callback nor yields progress. Iterating load_gen still performs loading but produces no progress tuples.

Locations: 448815bc1cf7b17e714a52fe6f70bcb53da48147:exllamav3/models/model.py — Model.load_gen

Source evidence: call_95016320fa484754b1adc4026ad5f26f, call_74dd42bb83fb44e99939e5ed73e27378

source_inspection: Compared the unchanged explicit-device callee with the autosplit additions. Whole-tree caller search found explicit-device load calls in tests/generator_stresstest.py, whose inspected setup uses cuda:1 and optionally cuda:2 without callbacks. Those existing calls demonstrate branch use, not an existing notification failure; the omission affects callers adopting the new interfaces. [call_8685f1405ae24244828e636045b28d7e, call_6846d67a48884d5293231998bc5885e8, call_74dd42bb83fb44e99939e5ed73e27378, call_95016320fa484754b1adc4026ad5f26f]. Limits: Source inspection only; external callers and dynamic invocation were not established.

## Uncertainty and limits

No model loading, CUDA allocation, cache lifecycle, or PyTorch inference-mode behavior was executed. The bounded Python check models notification and cleanup ordering only.

Direct load_gen iteration lacks the inference-mode decorator retained on load; the runtime consequences were not tested.
