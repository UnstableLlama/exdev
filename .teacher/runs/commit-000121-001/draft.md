# 3c801c61b01407d13e609524941333c9a9198f80


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/3c801c61b01407d13e609524941333c9a9198f80) · [Evidence ledger](draft.json)

Renames the CUDA safetensors loader and its header to distinguish them from stloader.cpp, updating includes while retaining automatic build-source discovery.

- [Distinct loader translation-unit names](#build)

## Problem

The change addresses the reported object-filename conflict by separating the CUDA loader's basename from stloader.cpp. [inference; call_4d2298a09c4c40049f2acd170a153134]

## Reasoning

Renaming stloader.cu to stloader_cu.cu removes the shared stem without merging translation units or changing loader algorithms. This would avoid collisions in build paths that derive object names by replacing the source extension. [inference; call_4d2298a09c4c40049f2acd170a153134]

## Impact

Both installation-time and JIT builds discover .cu and .cpp sources recursively, so the renamed CUDA file requires no explicit source-list update. [source; call_77ff12f382634acf8e050e08d99cb347, call_8526f0cf6c494636b3c08b30db6165c7]

## Source Notes

Issue #7, “quantizing model: undefined symbol: __cxa_call_terminate,” reports an extension-import failure and a reporter-provided toolchain workaround. Its relationship here is only an inferred shared extension-build context: its traceback names ext.py's import, not a loader object-name collision. [inference; call_966a25dbb7eb44778dcdc10b0ab1453f, call_8526f0cf6c494636b3c08b30db6165c7]

<a id="build"></a>

## Distinct loader translation-unit names

The CUDA implementation becomes stloader_cu.cu, and its header becomes stloader_cu.cuh. Both stloader.cpp and the CUDA implementation update their include directives; the header contents remain identical. [source; call_e5040ee0124e457b94971110ad6983f8, call_4d2298a09c4c40049f2acd170a153134, call_00dc1d05b2c7407b8b5f4653cce6040f]

The whole-parent-tree search finds precisely these two references to the old header name. The patch updates both, preserving the host/CUDA declaration boundary while changing filesystem names rather than callable interfaces. [source; call_d0c3df97491d41fc87103610c483e333, call_e5040ee0124e457b94971110ad6983f8, call_4d2298a09c4c40049f2acd170a153134, call_00dc1d05b2c7407b8b5f4653cce6040f]

setup.py passes discovered sources to CUDAExtension with BuildExtension; ext.py passes its discovered sources to torch.utils.cpp_extension.load when the prebuilt extension is absent. The rename therefore fits both existing discovery mechanisms without changing their selection conditions or compiler flags. [source; call_77ff12f382634acf8e050e08d99cb347, call_8526f0cf6c494636b3c08b30db6165c7]

## Uncertainty and limits

No build was executed; the affected compiler/backend and its actual object-naming rule are unestablished.

This filename-and-include change offers no useful numerical computation to validate; loader runtime correctness was not tested.
