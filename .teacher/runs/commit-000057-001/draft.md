# 1f7c1f709f0933c005052cd0f212b9f519ff0dd4


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/1f7c1f709f0933c005052cd0f212b9f519ff0dd4) · [Evidence ledger](draft.json)

Remove two excess spaces before N/A rfn output in conversion feedback, aligning it with numeric error output without changing conversion behavior.

- [Align unavailable error feedback](#conversion)

## Problem

The conversion progress line placed the N/A rfn field two spaces farther right than the numeric rfn field. [source; call_7df60df211e7429791f681c3c41cc674]

## Reasoning

Removing two leading spaces from the N/A literal matches the numeric branch's eight-space prefix without changing the module.num_slices == 1 condition. [source; call_7df60df211e7429791f681c3c41cc674]

## Impact

Only feedback formatting changes: the N/A field and following elapsed-time suffix move two columns left. Quantization, error calculation and tensor saving are unchanged. [source; call_7df60df211e7429791f681c3c41cc674, call_2b8ea058f07745a4a3f4a597518efaa8]

## Source Notes

Issue #7, “quantizing model: undefined symbol: __cxa_call_terminate,” reports a native-extension import failure and a reporter-supplied environment workaround. Its traceback mentions importing convert_model; that shared module reference does not establish a connection to this formatting change. [inference; call_4dafa31308414078a7df5dfe81772421, call_7df60df211e7429791f681c3c41cc674]

<a id="conversion"></a>

## Align unavailable error feedback

After advancing the module state and calculating error, main prints the module key, bits per weight or no_weights, rfn, and elapsed time. Single-slice modules retain numeric error output; the other branch retains N/A with corrected spacing. [source; call_2b8ea058f07745a4a3f4a597518efaa8, call_7df60df211e7429791f681c3c41cc674]

A scalar formatting check placed rfn at zero-based column 8 in both the numeric and corrected N/A fragments, versus column 10 previously. With error 0.125, both corrected fragments occupy 21 characters; the old N/A fragment occupied 23. [execution; call_eaee0df9b857476abe345dc11dc203f3]

## Uncertainty and limits

The check transcribed the formatting expressions into standard-library Python; it did not execute conversion or GPU code.

Equal field widths were checked for a representative numeric error, not every possible formatted value.
