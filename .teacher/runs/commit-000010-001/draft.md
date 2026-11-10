# d43424e20171a6de5eed75dee0eb263b397e8c48


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/d43424e20171a6de5eed75dee0eb263b397e8c48) · [Evidence ledger](draft.json)

Merges the setup.py fix that supplies setup-relative native source paths instead of absolute paths, addressing the reported wheel-build rejection.

- [Setup-relative native source paths](#packaging)

## Problem

Issue #2 reports a wheel-build rejection of absolute source paths under Python 3.12 and PyTorch 2.6; the quoted error requires paths relative to setup.py. [source; call_085b5153a55140a1a06773039356d70f]

## Reasoning

The merge replaces abspath with relpath anchored at dirname(__file__), retaining the complete discovered source path rather than dropping nested directories. [source; call_0a5b446006a74a72b281b9341d0ec819]

## Impact

This addresses the reported path-format rejection without changing source selection or compiler settings. A PR commenter reports that the change fixed their error. [source; call_0a5b446006a74a72b281b9341d0ec819, call_58ccc641d3964133abbb9f7e71a2cd01]

## Source Notes

The earlier packaging entry describes the same setup-relative path fix; this merge incorporates that change. [ancestor; call_af16dd3c07744f7291eaf34e9e4d6839]

The PR explicitly claims to fix issue #2, and the maintainer acknowledges an oversight. [source; call_44a83d205a004b5b946a666564a8bcb2, call_63982da0084444f28d571044f91f8b00]

<a id="packaging"></a>

## Setup-relative native source paths

setup.py recursively collects .c, .cpp and .cu files from exllamav3/exllamav3_ext. When precompilation is enabled and PyTorch is available, sources feeds CUDAExtension, and setup_kwargs passes that extension and BuildExtension to setuptools. [source; call_b41c2680368447ef9d9ebfc5356bd1c7]

The replacement changes only path representation. Keeping os.path.join(root, file) preserves nested source locations, while anchoring relpath to setup.py supplies the relative representation requested by the reported error. [source; call_0a5b446006a74a72b281b9341d0ec819, call_085b5153a55140a1a06773039356d70f]

A standard-library transcription over the first-parent checkout found 16 eligible sources, eight nested. With the checkout root as the setup directory, every replacement path was relative and resolved to the same target as the original absolute path. [execution; call_03f1e63275f4479986feea2849b3887f]

## Uncertainty and limits

No wheel build or native compilation was executed. The standard-library path check assumes the working directory is the setup directory; it does not validate Windows separators or invocation from another directory.
