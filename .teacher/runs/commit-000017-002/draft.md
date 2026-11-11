# 11822a5505f26056e07f92edd3c7056734264957


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/11822a5505f26056e07f92edd3c7056734264957) · [Evidence ledger](draft.json)

Explicitly includes the native extension tree in the package manifest to support the existing JIT-compilation fallback.

- [Ship native sources for deferred compilation](#packaging)

## Problem

The manifest explicitly included only Hadamard data, while the JIT loader needs native source files beneath the installed exllamav3 package. [source; call_24bc0b33faf34b3e906f5d8966c8bccc, call_167ba4e9c236419a8e67ecbfbc4e6055]

## Reasoning

Explicitly including the extension tree addresses the source-availability requirement of deferred compilation without requiring installation-time precompilation. [inference; call_24bc0b33faf34b3e906f5d8966c8bccc, call_d53216550bb3407b9763631130a9286b, call_167ba4e9c236419a8e67ecbfbc4e6055]

## Impact

The change adds recursive inclusion of the entire extension directory, preserves Hadamard-data inclusion, and leaves compiler configuration and runtime loading unchanged. [source; call_24bc0b33faf34b3e906f5d8966c8bccc]

<a id="packaging"></a>

## Ship native sources for deferred compilation

MANIFEST.in adds `recursive-include exllamav3/exllamav3_ext *`. Unlike a compilation-unit-only filter, this requests the whole nested extension tree, allowing supporting files as well as native compilation units to accompany the package. [source; call_24bc0b33faf34b3e906f5d8966c8bccc]

setup.py enables include_package_data and disables precompilation whenever EXLLAMA_NOCOMPILE is present, regardless of its value. With precompilation enabled and Torch available, it instead supplies CUDAExtension and BuildExtension to setuptools. [source; call_d53216550bb3407b9763631130a9286b]

At runtime, ext.py first imports exllamav3_ext. On ModuleNotFoundError it walks the extension directory relative to its own installed file, collects .c, .cpp and .cu files, and passes them to torch.utils.cpp_extension.load together with that directory as an include path. The manifest addition supports this existing fallback rather than changing how compilation is selected. [source; call_167ba4e9c236419a8e67ecbfbc4e6055, call_24bc0b33faf34b3e906f5d8966c8bccc]

The earlier installation entry documents both precompiled and EXLLAMA_NOCOMPILE installation paths and notes the original manifest's Hadamard-data inclusion. [ancestor; call_13d8559dc82247818dca80f94a892630]

## Uncertainty and limits

No distribution build, installation, or JIT compilation was executed; actual archive and wheel contents remain unverified.

A scalar computation would not validate this packaging change; its meaningful check requires building and inspecting installation artifacts.
