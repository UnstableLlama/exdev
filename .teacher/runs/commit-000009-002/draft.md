# 5567364846845473185e60bb7c4dd0aea786574a


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/5567364846845473185e60bb7c4dd0aea786574a) · [Evidence ledger](draft.json)

Changes native extension source paths from absolute to setup-relative, addressing the wheel-build rejection reported in issue #2 while preserving nested source locations.

- [Setup-relative native source paths](#packaging)

## Problem

Issue #2 reports wheel-building failure because setup.py supplies absolute native-source paths. The reported environment used Python 3.12 and PyTorch 2.6; the error explicitly requires paths relative to the setup.py directory. [source; call_b27f5de4d8d3458aa7815d70b4651da5]

## Reasoning

Replace abspath with relpath anchored at dirname(__file__), satisfying the reported relative-path requirement while retaining each recursively discovered file's root directory. [source; call_032110b696ba4a1f8133fd915f343333]

## Impact

The change affects the source list passed to CUDAExtension when precompilation is enabled and PyTorch is available; source suffix filtering, compiler arguments and extension registration remain unchanged. [source; call_032110b696ba4a1f8133fd915f343333, call_5cbd4ed385954cce928aa891decb1d0c]

## Source Notes

The issue's final edit reports successful wheel building with the same expression after removing build metadata and purging pip's cache. This is reporter-provided evidence, not an independently executed installation test. [source; call_b27f5de4d8d3458aa7815d70b4651da5]

<a id="packaging"></a>

## Setup-relative native source paths

setup.py recursively walks exllamav3/exllamav3_ext and selects .c, .cpp and .cu files. Its sources list feeds CUDAExtension, which reaches setuptools through setup_kwargs alongside BuildExtension. The patch changes path representation rather than which files are selected. [source; call_5cbd4ed385954cce928aa891decb1d0c, call_032110b696ba4a1f8133fd915f343333]

Keeping os.path.join(root, file) preserves nested generator and quant directories. The issue's preliminary alternative used sources_dir instead of root, discarding those subdirectories; the committed expression instead makes the complete discovered path relative to setup.py. [source; call_b27f5de4d8d3458aa7815d70b4651da5, call_032110b696ba4a1f8133fd915f343333]

A standard-library transcription over the ancestor checkout found 16 matching sources, including 8 nested sources. With the checkout root as the setup directory, all replacement paths were relative and resolved to the same targets as the original absolute paths, including quant/exl3_gemm.cu. [execution; call_e590d155296b49358d1d4c2fa0b5dbc0]

The patch addresses the path-format rejection without changing compilation itself. It does not remove existing build artifacts, so the reporter's cache-cleanup step remains separate from the code change. [source; call_032110b696ba4a1f8133fd915f343333, call_b27f5de4d8d3458aa7815d70b4651da5]

## Uncertainty and limits

No wheel build or native compilation was run. The standard-library check models path construction with the checkout root as the setup directory; it does not validate setuptools behavior, Windows path handling or invocation from another working directory.
