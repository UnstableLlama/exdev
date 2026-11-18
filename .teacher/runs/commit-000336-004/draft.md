# 37f80fb98cf6247f9da12d9b942253f38f6dbd82


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/37f80fb98cf6247f9da12d9b942253f38f6dbd82) · [Evidence ledger](draft.json)

Fixes the cache-detach mismatch message so assertions report both layer counts instead of raising TypeError. Matching-count detachment is unchanged.

- [Report mismatched cache-layer counts on detach](#cache)

## Problem

With assertions enabled, detaching a cache from a model with a different number of cache layers raised TypeError instead of the intended AssertionError. The failure message tried to call model_num_layers, even though len(model.get_cache_layers()) had already produced an integer. [source; call_847071d347214205bbe5bd88c17c71de, call_b6eeb02c98304ddb9d1c7a21362b5556]

## Reasoning

Turboderp's commit message, “Fix typo,” matches the one-line edit: interpolate the computed count rather than calling it. The patch keeps the same layer-count check and leaves the removal loop untouched. Cache.attach_to_model already formats its corresponding mismatch message this way. [source; call_b6eeb02c98304ddb9d1c7a21362b5556, call_847071d347214205bbe5bd88c17c71de]

## Impact

The correction affects the mismatch path, whether the caller supplies a model or defaults to the cache's original model. A whole-parent literal search found one direct caller, examples/loading.py. That example constructs the cache on the same model it later unloads and detaches from, so its ordinary path uses matching counts and does not evaluate the changed message. [source; call_97e988a6c88c402ab2fc2c544148a762, call_ced43a42102a446eb69683a2d2d9885f, call_847071d347214205bbe5bd88c17c71de, call_b6eeb02c98304ddb9d1c7a21362b5556]

## Source Notes

The initial generation chapter describes detachment as removing cache registration. The later “Support per-layer cache shape” entry records the switch to the ordered cache-capable module list and the mismatch-message defect; “TP: Auto layer split logic” records that the defect persisted at that point. [ancestor; call_764c433b5b49497cbbf249e8cfc6df67, call_7d226b8760374b9489bf7bf4eec35db3, call_e84b28cabfd04b5ea89a1809cb6009a8]

The per-layer cache change introduced the integer call when it replaced the configured hidden-layer count with len(model.get_cache_layers()). The same call survives in the task parent; this patch removes it without reverting the use of the model's cache-layer list. [source; call_67bf9739f45d4b37845c07ef6cc64b23, call_fa56a84a4a0e484f8e05f67d11ab3525, call_847071d347214205bbe5bd88c17c71de, call_b6eeb02c98304ddb9d1c7a21362b5556]

Issue #1, “Cache Quantization Strategy,” asks how the KV cache is encoded. Issue #50, “RuntimeError: Insufficient VRAM in split for model and cache despite remaining 1GB VRAM (exllamav3 + tabbyAPI),” reports memory pressure while loading. Both concern the model's KV cache, but neither describes the detach assertion, and the diff changes neither cache encoding nor allocation. [inference; call_5fa5d9dc978549e9b775edf752fb66f0, call_33c9d19daf2e4d419986975cd86c1cbe, call_b6eeb02c98304ddb9d1c7a21362b5556]

Issue #7, “quantizing model: undefined symbol: __cxa_call_terminate,” overlaps the historical per-layer patch through models/model.py in its import traceback, but reports a native-extension import failure. Issue #52, “Error converting moonshotai/Kimi-Dev-72B,” overlaps that historical patch through a comment naming models/llama.py, but reports a Cholesky failure during conversion. Neither overlap connects the report to detachment. [inference; call_e5888c0665434182b604e1c826e7f693, call_b590b649b88b412dbffd8439ee04112f, call_fa56a84a4a0e484f8e05f67d11ab3525, call_b6eeb02c98304ddb9d1c7a21362b5556]

<a id="cache"></a>

## Report mismatched cache-layer counts on detach

Cache construction records the size of the original model's cache-layer list and attaches one cache layer per module in that list. On detachment, the assertion compares the target's count with the stored count before any removal. When the counts match, detachment still removes each paired cache object from its module's registration list; this count check is not an identity check or a tensor-freeing operation. [source; call_847071d347214205bbe5bd88c17c71de, call_b6eeb02c98304ddb9d1c7a21362b5556]

A Python check extracted the parent method and applied the one-line replacement. With assertions enabled, a one-layer cache and a two-layer target produced TypeError before the edit and `AssertionError: Cannot detach cache with 1 layers from model with 2 layers.` after it. Neither mismatch removed a registration; the matching-count case removed its registration in both versions. Compiling with optimization level 1 skipped the assertion in both versions, so the edit does not make the check unconditional. [execution; call_b6eeb02c98304ddb9d1c7a21362b5556, call_e258705845ee40ff86a087a41da3983e]

## Uncertainty and limits

The execution isolated the method with stand-in objects; it did not import the package or run the loading example, a real model, Torch, or CUDA.

The literal caller search does not cover dynamic references or external callers. No motivating report is established.
