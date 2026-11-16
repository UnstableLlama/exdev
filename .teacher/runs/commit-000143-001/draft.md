# ae04741f22324cc746ab78c27365e53e3f9f1cf4


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/ae04741f22324cc746ab78c27365e53e3f9f1cf4) · [Evidence ledger](draft.json)

Adds a manual Linux/Windows CUDA wheel build matrix, a non-precompiled packaging job and opt-in versioned GitHub release uploads; build success and compatibility remain untested.

- [Manual wheel builds and optional release publication](#build-release)

## Problem

The change adds a manually invoked workflow for building distribution wheels and optionally uploading them to a versioned GitHub release. [source; call_c4c92bc5486746bbb97d3d02baf6b8c9]

## Reasoning

Separate CUDA and non-precompiled builds reuse setup.py's existing extension switch: EXLLAMA_NOCOMPILE suppresses CUDAExtension registration, while the CUDA jobs leave compilation enabled. [source; call_c4c92bc5486746bbb97d3d02baf6b8c9, call_af2dd240644f4243b8674a4e6dec381f]

## Impact

The matrix declares eight CUDA wheel builds across Ubuntu 22.04 and Windows 2022, Python 3.10–3.13, CUDA 12.8.1 and Torch 2.7.0, plus one Ubuntu/Python 3.11 non-precompiled build. No ROCm configuration is populated. [source; call_c4c92bc5486746bbb97d3d02baf6b8c9]

## Source Notes

Closed issue #17, “ModuleNotFoundError: No module named 'torch' when installing requirements.txt,” concerns Flash-Attention installation and selecting CUDA-enabled Torch. Its relevance is inferred from the workflow's explicit Torch installation and CUDA index selection; the discussion does not establish that this workflow fixes that issue. [inference; call_635c86e1cc3b4adc8a0213565ba69fc9, call_c4c92bc5486746bbb97d3d02baf6b8c9]

<a id="build-release"></a>

## Manual wheel builds and optional release publication

workflow_dispatch accepts a required string release input defaulting to '0'. Publication requires exactly '1' and a parsed package version other than 'None'. The workflow grants contents: write and disables matrix fail-fast, allowing other configurations to continue when one fails. [source; call_c4c92bc5486746bbb97d3d02baf6b8c9]

All commands use PowerShell. Linux jobs first free disk space and CUDA jobs install the toolkit through Jimver/cuda-toolkit. Windows jobs install pinned Visual Studio Build Tools, assemble CUDA from individually versioned NVIDIA archives, export toolkit paths, and enter the Visual Studio developer shell before compiling. [source; call_c4c92bc5486746bbb97d3d02baf6b8c9]

CUDA jobs install Torch from a CUDA-specific index, then build tooling with setuptools pinned to 69.5.1. They pass TORCH_CUDA_ARCH_LIST='8.0 8.6 8.9 9.0 10.0 12.0+PTX' and invoke a non-isolated wheel build with a CUDA/Torch build tag. These architecture values are compilation targets, not measured runtime support. [source; call_c4c92bc5486746bbb97d3d02baf6b8c9]

setup.py recursively collects C, C++ and CUDA sources and registers CUDAExtension when Torch is available and EXLLAMA_NOCOMPILE is absent. The non-CUDA matrix row instead installs CPU Torch and sets EXLLAMA_NOCOMPILE=1, selecting packaging without that extension. [source; call_af2dd240644f4243b8674a4e6dec381f, call_50a9532f8e5f4120b5ec6c9f7d8b894e, call_c4c92bc5486746bbb97d3d02baf6b8c9]

A bounded Python transcription matched the existing version string as 0.0.1 and derived release tag v0.0.1, Torch index https://download.pytorch.org/whl/cu128 and build-tag input +cu128-torch2.7.0 from the workflow's string transformations. [execution; call_d3b6d3d52d32423c983f46b9d8c5af81, call_234e3f255c984eed8475462fc4fc4093, call_c4c92bc5486746bbb97d3d02baf6b8c9]

Each job's release step selects only ./dist/*.whl, uses the parsed version for the release name and v-prefixed tag, and permits overwriting assets. There is no upload-artifact step or source-archive upload, so the default non-release invocation provides no configured durable distribution handoff. [source; call_c4c92bc5486746bbb97d3d02baf6b8c9]

Explicit toolchain and architecture choices favor repeatable, broadly targeted builds over relying on a runner's detected GPU. Non-isolated builds make the preceding environment setup consequential; the commit provides build orchestration rather than installation or inference validation. [inference; call_c4c92bc5486746bbb97d3d02baf6b8c9, call_af2dd240644f4243b8674a4e6dec381f]

## Uncertainty and limits

No GitHub Actions job, PowerShell command, package build, upload or GPU compatibility test was executed. Availability and behavior of external actions, installers and package versions remain unverified.

The Python check models string operations only; it does not execute PowerShell or establish setuptools' final wheel-name normalization.

The step named Build sdist invokes python -m build -n without an explicit distribution selector. Its exact output set was not established by execution or eligible build-tool documentation.
