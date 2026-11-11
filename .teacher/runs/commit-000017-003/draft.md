# 11822a5505f26056e07f92edd3c7056734264957


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/11822a5505f26056e07f92edd3c7056734264957) · [Evidence ledger](draft.json)

Explicitly includes the native extension tree in the package manifest so JIT installations can retain sources and headers needed by the runtime loader.

- [Carry native sources into JIT installations](#packaging)

## Problem

JIT installation needs native source files after installation, but the previous manifest explicitly included only Hadamard data. [source; call_2e97a9b795d44e759ffce867adc739d1, call_6ea8983b5e3449119ea9c0a353fc4b8b]

## Reasoning

Adding recursive inclusion of the native extension tree supplies a packaging rule independent of whether setup.py constructs a precompiled extension. [inference; call_2e97a9b795d44e759ffce867adc739d1, call_22b87af931524305a470773eb29d3224]

## Impact

The change targets availability of JIT build inputs, not compiler flags, kernel behavior or dependency versions. [source; call_2e97a9b795d44e759ffce867adc739d1]

## Source Notes

Issue #6 is titled “No ROCm runtime is found, using ROCM_HOME='/usr'”; its reporter says they do not have AMD, and its traceback ends at assert len(sources) > 0 after exllamav3/ext.py calls load. [source; call_203c0721c73748b9ab5a6c5981d0d756]

That report is plausibly related because its load call matches the inspected JIT loader and its empty-source assertion fits missing packaged sources. This does not establish that the commit addresses the ROCm warning or that the author linked the issue. [inference; call_203c0721c73748b9ab5a6c5981d0d756, call_6ea8983b5e3449119ea9c0a353fc4b8b, call_2e97a9b795d44e759ffce867adc739d1]

<a id="packaging"></a>

## Carry native sources into JIT installations

MANIFEST.in retains include exllamav3/util/hadamard_data/* and adds recursive-include exllamav3/exllamav3_ext *. The wildcard covers the native tree rather than only compilation units, including nested headers and sources. [source; call_2e97a9b795d44e759ffce867adc739d1, call_8573483ce98740dfb8177c4e61d5ecaa]

setup.py enables include_package_data and disables precompilation when EXLLAMA_NOCOMPILE is present. Its CUDAExtension configuration exists only when precompilation is enabled and Torch is available; otherwise setup_kwargs is empty. [source; call_22b87af931524305a470773eb29d3224]

At runtime, ext.py first imports exllamav3_ext. On ModuleNotFoundError it recursively discovers .c, .cpp and .cu files beneath the installed Python module's exllamav3_ext directory, then passes them to torch.utils.cpp_extension.load with that directory as an include path. [source; call_6ea8983b5e3449119ea9c0a353fc4b8b]

The broad recursive rule preserves both translation units and supporting headers without maintaining a second extension-specific file list. Its tradeoff is including the whole native subtree rather than narrowly selecting build inputs. Precompilation remains the existing alternative; neither build path's implementation changes. [inference; call_2e97a9b795d44e759ffce867adc739d1, call_8573483ce98740dfb8177c4e61d5ecaa, call_22b87af931524305a470773eb29d3224, call_6ea8983b5e3449119ea9c0a353fc4b8b]

## Uncertainty and limits

No distribution build, installation or native compilation was executed; actual archive and installed-package contents remain unverified.

There is no useful numerical scalar check for this manifest-only change. Packaging-tool behavior requires a build rather than arithmetic emulation.
