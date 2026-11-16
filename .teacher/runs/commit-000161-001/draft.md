# 48747ba09dee3ec78964653df0eb926c53f41c2e


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/48747ba09dee3ec78964653df0eb926c53f41c2e) · [Evidence ledger](draft.json)

Disables loader-side weight and bias padding for sliced FP16 linears, allowing existing CPU slicing to operate on full checkpoint tensors while preserving padding for unsliced loads.

- [Slice before imposing local tensor dimensions](#loading)

## Problem

Sliced FP16 linears requested loader padding to their local dimensions before LinearFP16 could extract the slice from the full checkpoint tensor. The loader allocates exactly pad_to, then copies the entire source into it; padding therefore cannot accommodate a source wider than that destination. [source; call_0c83d1331ee2407d93c6f472f022d1a9, call_0f908f8c675745d2b05d3d608208012a, call_ea5b8081f9a54f6789da70cfbf0b090a]

## Reasoning

The fix passes pad_to=None for both weight and optional bias when is_sliced is true. This preserves checkpoint dimensions until the existing LinearFP16 constructor selects the requested rows or columns. [source; call_286a242cc5f44b679662f0b48bd08438, call_ea5b8081f9a54f6789da70cfbf0b090a]

## Impact

Unsliced linears retain loader-side padding. FP16 conversion, weight transposition, CPU staging for slices and subsequent device transfer remain unchanged; EXL3 loading and the fused-weight fallback are not edited. [source; call_286a242cc5f44b679662f0b48bd08438, call_0c83d1331ee2407d93c6f472f022d1a9]

## Source Notes

Issue #38, “Error converting nvidia/Llama-3_1-Nemotron-Ultra-253B-v1,” reports a 49,920-versus-399,360 copy failure. Its relationship to this fix is inferred from the traceback through GatedMLP.load, Linear.load_fp16 and the loader's padded copy, matching the inspected data flow; the supplied commit does not explicitly cite the issue. [inference; call_fab156415fb745848b95e48276ab68a4, call_286a242cc5f44b679662f0b48bd08438, call_f7d5bd53cc3b4e688342a41b9d9b96b3, call_0f908f8c675745d2b05d3d608208012a]

Other overlapping discussions describe distinct failures: #8, “RuntimeError: shape '[5120, -1, 128]' is invalid for input of size 776524800,” concerns quantization padding; #11, “AssertionError: bias is wrong datatype,” concerns bias dtype; #16, “RuntimeError: CUDA error: invalid configuration argument,” was attributed in discussion to tokenizer truncation. Shared linear.py paths do not establish that this patch addresses those reports. [inference; call_0b0a620b2b7c43bcbe15c049280c3ff0, call_c5562210f040491dbd1a377fcd6bc0cd, call_e75ee99bb7de4f118c5d29f39b5453e0, call_286a242cc5f44b679662f0b48bd08438]

#34, “torch._C._LinAlgError on last layer of quant,” reports Cholesky failure. #33, “Error converting model,” initially reports file-opening failure, later identified as too many open files, and subsequently discusses repetitive GLM4 output. Their overlap with inspected loading/conversion files is not evidence of the same padding failure. [inference; call_74e6840f0358438f9e4098332d3fb2cd, call_802bc4425b89444cbb8ecce50ee2368c, call_1cc1faa9b97c481bb29000179e42ead7, call_286a242cc5f44b679662f0b48bd08438]

<a id="loading"></a>

## Slice before imposing local tensor dimensions

Linear determines is_sliced by comparing its padded local dimensions with full_in_features and full_out_features. Its default alignment of 128 rounds dimensions upward; it is not a slice-count threshold. [source; call_0c83d1331ee2407d93c6f472f022d1a9]

GatedMLP builds gate/up slices along output features and down slices along input features, preserving full dimensions and offsets. Alternate keys let these sliced modules load the original unsliced checkpoint tensors. Loading a selected MLP slice directly loads its gate, up and down linears. [source; call_f7d5bd53cc3b4e688342a41b9d9b96b3]

With padding disabled for sliced loads, LinearFP16 receives the transposed full weight on CPU. It slices dimensions that match the declared full dimensions, slices bias alongside output columns, copies the selected weight into independent storage, and then the existing unswap_cpu path transfers it to the requested device. This is not partial file I/O: the loader still reads the complete tensor. [source; call_286a242cc5f44b679662f0b48bd08438, call_0c83d1331ee2407d93c6f472f022d1a9, call_ea5b8081f9a54f6789da70cfbf0b090a, call_0f908f8c675745d2b05d3d608208012a]

A standard-library shape check using issue #38's dimensions gives exactly eight 49,920-wide slices of 399,360 columns, with each slice divisible by 128. The old destination slice remains only 49,920 columns despite a 399,360-column source; slicing the full source instead yields eight correctly sized intervals. [execution; call_7218dfa36fac420a9d23c7b35012c869]

The earlier deferred-loading entry describes moving ordinary FP16 transposition and padding into the loader and excluding sliced linears from deferral. This patch narrows that padding policy without replacing the existing CPU slicing mechanism. [ancestor; call_b0af4c7d65914f6e921dd80548f81107]

## Uncertainty and limits

No repository implementation, PyTorch tensor copy, GPU operation or complete model conversion was executed. The bounded Python check models dimensions and slicing only.

Compatibility of every sliced checkpoint shape, including dimensions requiring additional alignment padding, was not established.
