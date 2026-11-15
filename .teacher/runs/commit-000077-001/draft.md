# 1f5a43fc72f3c45d6db757c7907d4793ec88f026


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/1f5a43fc72f3c45d6db757c7907d4793ec88f026) · [Evidence ledger](draft.json)

Exports CacheLayer_quant at package level and documents its independent key/value bitrates, without changing cache computation or defaults.

- [Expose and document the configurable quantized cache](#cache)

## Problem

CacheLayer_quant was exported by exllamav3.cache but omitted from the top-level package. Cache's docstring also named obsolete per-bitrate classes instead of the implemented configurable class. [source; call_79320b5a41764984800c60c794c663e3, call_288ef68a45dc46aea6b8ce8ef27db9eb, call_993474fd5bab4e20a5fdec30633ad865]

## Reasoning

The change aligns the public import surface and constructor documentation with existing functionality rather than introducing a new cache implementation. [inference; call_288ef68a45dc46aea6b8ce8ef27db9eb, call_993474fd5bab4e20a5fdec30633ad865, call_9c68f67370a04327aecc9e996adda91d]

## Impact

The package now exposes CacheLayer_quant for top-level imports. Existing model_init code already imports it from .cache and supplies both bitrates, so that construction path needs no adjustment. [source; call_288ef68a45dc46aea6b8ce8ef27db9eb, call_fe7d9c53ff5f4dbe81e84015ff36e78b]

## Source Notes

This is a missing re-export, not evidence that importing exllamav3 itself previously failed: its cache package initializer already imported the quantized class. [source; call_79320b5a41764984800c60c794c663e3, call_39be7b1c2ed445aaa3410c027b6362ba]

Issue #7, “quantizing model: undefined symbol: __cxa_call_terminate,” reports a native-extension import failure; its connection here is only an inferred file overlap because its traceback includes exllamav3/__init__.py. The diff does not address that native symbol. Issue #15, “`cogito-v1-preview-qwen-32B` generates incoherent output for bpw <= 2.5,” concerns weight conversion, not this cache export. [inference; call_78b736596d5a41bb96c7da8716166006, call_720a350452654ff99e10b62f03f8e54c, call_288ef68a45dc46aea6b8ce8ef27db9eb, call_993474fd5bab4e20a5fdec30633ad865]

<a id="cache"></a>

## Expose and document the configurable quantized cache

Cache.__init__ retains its optional layer_type and **kwargs interface. Omitting layer_type still selects CacheLayer_fp16; explicitly selecting CacheLayer_quant forwards k_bits and v_bits to every cache layer. [source; call_0fca16cc883b444d9d38162638c7dab6, call_993474fd5bab4e20a5fdec30633ad865]

The new parameter descriptions correctly distinguish key and value precision. CacheLayer_quant requires both arguments, asserts each is between 2 and 8, and uses them independently to size the compressed key and value tensors. The task changes neither these requirements nor the encoding path. [source; call_9c68f67370a04327aecc9e996adda91d, call_993474fd5bab4e20a5fdec30633ad865]

The earlier cache entry describes independent key/value precision and records a detachment diagnostic defect. Inspection of the current parent and task diff shows that diagnostic remains unchanged; this documentation cleanup does not repair it. [inference; call_fdeff58255954ebb8e162ac3150d07b9, call_0fca16cc883b444d9d38162638c7dab6, call_993474fd5bab4e20a5fdec30633ad865]

## Authoring-time findings — pending review

### inherited-detach-diagnostic (suspected; defect)

The inherited mismatched-layer detachment diagnostic still calls an integer as a function.

Trigger: With assertions enabled, call Cache.detach_from_model using a model whose cache-layer count differs from the cache's count.

Expected: Raise AssertionError with a diagnostic describing the incompatible counts.

Actual: Formatting the assertion message evaluates model_num_layers(), producing TypeError instead. Matching counts bypass the expression.

Locations: 1f5a43fc72f3c45d6db757c7907d4793ec88f026:exllamav3/cache/cache.py — Cache.detach_from_model

Source evidence: call_0fca16cc883b444d9d38162638c7dab6, call_993474fd5bab4e20a5fdec30633ad865

source_inspection: The task leaves the diagnostic unchanged. Whole-parent-tree search found one direct caller in examples/loading.py, which passes the same model used to construct the cache and therefore does not demonstrate the mismatch trigger. [call_9fe530dcaa2b4497a9d301f03320cd0a, call_f8f60787cddb41839b8c247db4885d5a, call_0fca16cc883b444d9d38162638c7dab6, call_993474fd5bab4e20a5fdec30633ad865]. Limits: Source inspection only; external callers and dynamic calls were not established.

## Uncertainty and limits

No package import, model loading or GPU cache operation was executed. This export-and-docstring change has no useful numerical computation to validate.

The documentation does not spell out that both quantized bitrates are required or their asserted 2–8 range; these constraints were established from the constructor, not runtime testing.
