# ff72058d5052ab8c65250dbd03cc96620dc03cf5


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/ff72058d5052ab8c65250dbd03cc96620dc03cf5) · [Evidence ledger](draft.json)

Comments out five forced cleanup calls in conversion and EXL3 quantization, skipping both Python collection and CUDA cache clearing at those points without changing quantization calculations.

- [Skip forced cleanup at conversion boundaries](#conversion)

## Problem

Conversion explicitly invoked garbage collection and CUDA cache clearing at repeated module and quantizer boundaries. [source; call_1492d1f996fc4ec4a09f82264982866f, call_b03f2650a960436bbe28373e82315f69, call_4fa411aabf224deeb56a862dbc7af08d]

## Reasoning

Skipping these calls avoids forced cleanup at those boundaries. This is narrower than disabling garbage collection globally, and broader than skipping only GC: free_mem() calls both gc.collect() and torch.cuda.empty_cache(). [source; call_4fa411aabf224deeb56a862dbc7af08d, call_1492d1f996fc4ec4a09f82264982866f, call_b03f2650a960436bbe28373e82315f69]

## Impact

The likely tradeoff is less cleanup overhead versus less eager reclamation and cache release; neither conversion speed nor peak memory improvement is established by the source. [inference; call_4fa411aabf224deeb56a862dbc7af08d, call_1492d1f996fc4ec4a09f82264982866f, call_b03f2650a960436bbe28373e82315f69]

<a id="conversion"></a>

## Skip forced cleanup at conversion boundaries

In main(), two free_mem() calls become comments: after saving the converted module tensors and deleting the temporary tensor dictionary, and after unloading the module. Saving, del tensors, calibration-state advancement, module.unload(), and checkpoint handling remain in place. [source; call_1492d1f996fc4ec4a09f82264982866f, call_150260e818a14a50bd0d09ada4e94f80]

In quantize_exl3(), three calls become comments: immediately before LDLQ, immediately after LDLQ, and after the proxy-error calculation. The quantized weights and encoded output still feed metric calculation, optional weight reconstruction, and packed-tensor construction; the patch does not change those calculations or returned values. [source; call_b03f2650a960436bbe28373e82315f69, call_6c389c5cd3c84d119e326e3b14cd277c]

The implementation chooses to omit the combined cleanup helper rather than separate garbage collection from CUDA cache clearing. Explicit reference clearing remains in the metric path, so removing the helper does not mean retaining every temporary reference. [source; call_4fa411aabf224deeb56a862dbc7af08d, call_6c389c5cd3c84d119e326e3b14cd277c, call_b03f2650a960436bbe28373e82315f69]

## Uncertainty and limits

No conversion or GPU workload was executed. A scalar computation would not establish the runtime or allocator effects of removing these cleanup calls.
