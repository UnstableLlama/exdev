# 11822a5505f26056e07f92edd3c7056734264957


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/11822a5505f26056e07f92edd3c7056734264957) · [Evidence ledger](draft.json)

Adds recursive manifest inclusion of the native extension tree so JIT installations can carry their deferred compilation inputs.

- [Ship native inputs for deferred compilation](#packaging)

## Problem

The manifest explicitly included Hadamard data but not the native extension tree, leaving JIT installation without an explicit packaging rule for its build inputs. [source; call_51e2c51b1f6d4385bc680137f3a95863]

## Reasoning

JIT compilation needs source files after installation, not just during package construction: ext.py locates exllamav3_ext beside itself and recursively collects C, C++ and CUDA sources. [source; call_5634ee015395436fbcce2a3daf847ae6]

## Impact

The added recursive inclusion rule addresses distribution of the native build inputs without changing compilation flags, native code or extension-loading behavior. [source; call_51e2c51b1f6d4385bc680137f3a95863]

## Source Notes

The initial implementation's explanation already identifies precompiled and JIT installation paths and the original Hadamard-only manifest inclusion. [ancestor; call_1725ae33001f4e5294bddd7dcc3c7017]

<a id="packaging"></a>

## Ship native inputs for deferred compilation

MANIFEST.in preserves the Hadamard-data rule and adds `recursive-include exllamav3/exllamav3_ext *`. The wildcard covers the extension tree broadly rather than restricting inclusion to compiled translation-unit suffixes. [source; call_51e2c51b1f6d4385bc680137f3a95863]

setup.py enables include_package_data and supplies CUDAExtension only when precompilation is enabled and Torch is available. Presence of EXLLAMA_NOCOMPILE disables precompilation regardless of its value, so this installation route cannot rely on that extension declaration to describe its sources. [source; call_e714064cd14248b0a29d144823422ae8]

At runtime, ext.py first imports the prebuilt extension. On ModuleNotFoundError it instead walks the package-local extension directory for .c, .cpp and .cu files and passes them to torch.utils.cpp_extension.load, together with that directory as an include path. [source; call_5634ee015395436fbcce2a3daf847ae6]

Explicitly shipping the entire tree supports deferred compilation and its accompanying include files independently of setup-time precompilation. The tradeoff is broader packaged content than a suffix-limited source list; the existing prebuilt-extension route remains available. [inference; call_51e2c51b1f6d4385bc680137f3a95863, call_e714064cd14248b0a29d144823422ae8, call_5634ee015395436fbcce2a3daf847ae6]

## Uncertainty and limits

No source distribution, wheel, installation or JIT compilation was executed; actual artifact contents and successful compilation remain unverified.

A scalar computation would not meaningfully validate this manifest change; its consequential behavior depends on packaging and native-build tooling.
