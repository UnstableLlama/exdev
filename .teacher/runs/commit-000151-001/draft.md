# 95cfa726b63049e455e2037e1325ae6961e3be98


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/95cfa726b63049e455e2037e1325ae6961e3be98) · [Evidence ledger](draft.json)

Makes SS_TopK accept integer inputs without calling their is_integer method, while retaining integral-float validation and unchanged top-k masking.

- [Version-independent integer validation for top-k](#sampling)

## Problem

SS_TopK unconditionally called top_k.is_integer(), even though its argument is annotated int. This makes construction depend on that method being available on integer inputs. [source; call_935ef1dfe124452a9d8742f9e77f8666]

## Reasoning

The added isinstance(top_k, int) branch short-circuits validation for integers. Other inputs still use is_integer(), and accepted values still pass through int(top_k); integral floats remain supported rather than imposing an integer-only API. [source; call_935ef1dfe124452a9d8742f9e77f8666]

## Impact

The fix covers TopKSampler's non-greedy branch and ComboSampler's non-greedy branch, including its default top_k=0. ComboSampler constructs SS_TopK before CustomSampler can replace a disabled top-k step with a no-op. Greedy branches bypass this constructor. [source; call_8ab9e176091b4c75b4bb7e8abb88291f, call_10809f4831ee44e291274185e9fb7842]

## Source Notes

PR #35, “humaneval.py: fix top_k type, remove rep_p, add qwen3,” reports an indexing-type issue. Its relationship to this fix is inferred from the shared top_k input, not an explicit upstream link. Issue #21, “Build Failure on Windows: CUDA 12.4 / PyTorch 2.7.0+cu126 / VS 2022,” instead reports extension-compilation failures and supplies no evidence for this constructor change. [inference; call_78ed8135e8eb42b0b02dc677d245ca07, call_a2d40ed3ee6d4e4f962d4c48015f2468, call_935ef1dfe124452a9d8742f9e77f8666]

<a id="sampling"></a>

## Version-independent integer validation for top-k

This is a constructor-validation change, not a sampling-algorithm change. SS_TopK still requests descending sorting, masks positions starting at k with zero probabilities or negative-infinite logits, and becomes a no-op for k<1 through CustomSampler. [source; call_935ef1dfe124452a9d8742f9e77f8666, call_10809f4831ee44e291274185e9fb7842]

A bounded check extracted the parent constructor and applied the diff's assertion replacement. On Python 3.14.4, both versions accepted 0, 1, 5 and 5.0, stored integers, and rejected 5.5 with AssertionError. This checks those validation cases only, not compatibility with older interpreters. [execution; call_5bd32e5ea87e42a6906aa50c2e736bca]

## Uncertainty and limits

The precise older-Python version boundary is unestablished by eligible documentation or execution here.

The isolated constructor check ran on Python 3.14.4, where the parent already accepts integers; it does not reproduce the reported older-interpreter failure or test tensor sampling.
