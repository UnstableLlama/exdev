# 2432c64e68ba4e3cbeccc3eaeba44c97731132d3


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/2432c64e68ba4e3cbeccc3eaeba44c97731132d3) · [Evidence ledger](draft.json)

Adds application-specific cache defaults while preserving the 8192-token fallback and explicit CLI overrides, resolving longctx.py's unsupported keyword.

- [Application-specific cache defaults](#model-init)

## Problem

The shared parser hardcoded an 8192-token cache default, while eval/longctx.py already requested default_cache_size=65536 through an unsupported keyword. [source; call_4f32d02d7fcb4594a6944bf479e6e7fa, call_110c6c8ecde74fe396753d41c9e3f5c6]

## Reasoning

Adding an optional default_cache_size parameter lets applications choose their default without changing the existing command-line option. The same value supplies both argparse's default and its help text. [source; call_4a1f6eff9303448489034604ccf2ac77]

## Impact

The change removes the long-context entry point's unsupported-keyword failure. Callers omitting the new parameter retain 8192; cache=False still omits cache arguments. [source; call_4a1f6eff9303448489034604ccf2ac77, call_110c6c8ecde74fe396753d41c9e3f5c6]

## Source Notes

The parent annotation identified the long-context script's argument-registration failure; inspection of this diff shows that specific incompatibility is removed, not carried over. [source; call_9ba396691d0e44ddac8625a6759b2797, call_4a1f6eff9303448489034604ccf2ac77, call_110c6c8ecde74fe396753d41c9e3f5c6]

PR #22, “OpenAI compatible API example,” discusses an API example and cache_quant usage. Its relationship here is only inferred from its use of model_init.add_args and cache options; it does not establish motivation for this default-cache change. [inference; call_d9821ce82d66467091d60e111b699219, call_2c776767100e428d9c9482d8da2690e1, call_4a1f6eff9303448489034604ccf2ac77]

<a id="model-init"></a>

## Application-specific cache defaults

default_cache_size is a Python helper argument, not a new CLI flag. The existing -cs/--cache_size remains an integer option. Its default remains 8192 tokens unless the application supplies another value. [source; call_4a1f6eff9303448489034604ccf2ac77]

The parsed cache_size flows unchanged through model_init.init into Cache(max_num_tokens=...) for both FP16 and quantized cache construction. Thus 65536 in longctx.py requests token capacity, rather than changing cache precision or a generation-length limit. [source; call_4f32d02d7fcb4594a6944bf479e6e7fa, call_110c6c8ecde74fe396753d41c9e3f5c6]

An isolated argparse check reproduced the parent's unexpected-keyword TypeError. With the inspected changes applied to the extracted helper, omitted overrides yielded 8192, an application override yielded 65536, explicit -cs 4096 took precedence, and cache=False produced no cache fields. The overridden help text also passed its check. [execution; call_28f5b26f25e947ac89fb435cf16ac74e]

## Uncertainty and limits

Validation executed an isolated parent helper and a reconstruction incorporating the inspected diff, not the complete package or evaluation script. Model loading, GPU allocation and long-context inference were not tested.
