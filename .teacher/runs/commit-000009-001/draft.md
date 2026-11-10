# 5567364846845473185e60bb7c4dd0aea786574a


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/5567364846845473185e60bb7c4dd0aea786574a) · [Evidence ledger](draft.json)

Changes native extension source paths from absolute checkout paths to paths relative to setup.py, without changing source selection or compilation settings.

- [Relative extension source paths](#build-source-paths)

## Problem

The extension source list previously embedded absolute checkout paths in the build configuration. [source; call_36a41d29dcbb427c8d802ad385e5f6e4]

## Reasoning

Expressing source paths relative to setup.py removes the checkout-specific absolute prefix while retaining the discovered source files. [source; call_36a41d29dcbb427c8d802ad385e5f6e4]

## Impact

This makes extension source metadata independent of the checkout's absolute location under the usual project-root invocation. [inference; call_36a41d29dcbb427c8d802ad385e5f6e4, call_8bfa10371fc14652be7b1e44b2b52bb8]

<a id="build-source-paths"></a>

## Relative extension source paths

The source-list comprehension still walks exllamav3/exllamav3_ext and selects .c, .cpp and .cu files. Only path normalization changes: abspath becomes relpath with os.path.dirname(__file__) as its base. [source; call_36a41d29dcbb427c8d802ad385e5f6e4, call_ba2e8f8a006c40c590bb8d69a4161909]

The resulting list feeds PyTorch's CUDAExtension when Torch is available and EXLLAMA_NOCOMPILE is absent. Compiler flags, source filtering and the precompilation gate remain unchanged. [source; call_ba2e8f8a006c40c590bb8d69a4161909, call_36a41d29dcbb427c8d802ad385e5f6e4]

A standard-library path-expression check modeled project-root invocation using both relative and absolute setup.py filenames. For bindings.cpp, the new expression produced a relative path resolving to the same target as the old absolute path. This checked path arithmetic, not the packaging implementation. [execution; call_8bfa10371fc14652be7b1e44b2b52bb8]

## Uncertainty and limits

No package installation, distribution build or native compilation was run; compatibility improvements are inferred rather than measured.

Source discovery still starts from a working-directory-relative directory. The change does not establish support for invoking setup.py from arbitrary working directories.
