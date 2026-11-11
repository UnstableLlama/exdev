# b1c7f251d27b35fe9679ad1007dd6f9b8a723d4c


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/b1c7f251d27b35fe9679ad1007dd6f9b8a723d4c) · [Evidence ledger](draft.json)

Fixes the proxy-error variable name so quantize_exl3 returns its computed metric instead of referencing an undefined name.

- [Restore the proxy-error return value](#quantizer)

## Problem

quantize_exl3 computed proxy_err_2 but returned proxy_err, leaving the return name undefined after quantization and packing. [source; call_8b7cd238d7ba4af98a7e121f417b5e06]

## Reasoning

The one-line fix assigns the existing normalized error calculation to proxy_err, matching the unchanged return contract without altering the calculation. [source; call_ca6b95741bf9400598bfe61712684906, call_8b7cd238d7ba4af98a7e121f417b5e06]

## Impact

This removes the return-name failure blocking the inspected direct caller, Linear.convert_exl3, from constructing LinearEXL3 and returning the metric. [source; call_ca6b95741bf9400598bfe61712684906, call_f4e52671382e4f6ca131cf312bc4c6f0]

## Source Notes

The earlier memory-management entry recorded this undefined-name defect. Inspection of the parent function and task patch shows that this change removes that specific defect. [source; call_b7892164f2384217abad72dd0492e21f, call_8b7cd238d7ba4af98a7e121f417b5e06, call_ca6b95741bf9400598bfe61712684906]

<a id="quantizer"></a>

## Restore the proxy-error return value

After LDLQ, the metric uses transformed-space residual E = weight_r - weight_q and reference W = weight_r. Each scalar einsum sums X[i,k] * H[i,j] * X[j,k]; the residual contraction is divided by the reference contraction. The 1e-8 denominator floor protects against a zero or smaller denominator and is unchanged. [source; call_8b7cd238d7ba4af98a7e121f417b5e06, call_ca6b95741bf9400598bfe61712684906]

Renaming the assignment preserves sequential contractions, tensor-reference cleanup, optional weight reconstruction and packed-tensor construction. The returned tuple remains weight_q, proxy_err, out_tensors; changing the local assignment is sufficient to reconnect the computed scalar to that interface. [source; call_ca6b95741bf9400598bfe61712684906, call_8b7cd238d7ba4af98a7e121f417b5e06]

Linear.convert_exl3 unpacks this tuple, constructs LinearEXL3 from the packed tensors while preserving the original bias, and returns either proxy_err alone or proxy_err with weight_q. [source; call_7145f2f95edf4949af7b80539dbcbd26, call_f4e52671382e4f6ca131cf312bc4c6f0]

An isolated standard-library check using the inspected assignment and return statements raised NameError for the parent spelling. With the patched spelling, numerator 2 and denominator 4 returned metric 0.5; denominator zero returned 200000000.0 through the unchanged floor. This checks scalar binding and division only. [execution; call_d0ce85746d9240dba00a34ac16a78132]

## Uncertainty and limits

No full quantizer, PyTorch or CUDA execution was performed. The scalar check isolates assignment and return behavior, not tensor arithmetic or successful end-to-end conversion.

Caller inspection covers the direct Linear.convert_exl3 call found by literal search, not every broader conversion entry point.
