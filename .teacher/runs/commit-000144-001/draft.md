# 10222646d08f8bbdeebf0813d1cbf9e641154a99


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/10222646d08f8bbdeebf0813d1cbf9e641154a99) · [Evidence ledger](draft.json)

Integrates a manual Linux/Windows CUDA wheel matrix and opt-in versioned release uploads into dev; actual build and compatibility results remain untested.

- [Integrating manual distribution builds](#build-release)

## Problem

The merge adds manual wheel-building and optional GitHub release publication to the first-parent tree; its diff contains only the new build workflow. [source; call_5fe8295d3e96417eae10999af7e569a4]

## Reasoning

The workflow separates CUDA compilation from non-precompiled packaging using setup.py's existing EXLLAMA_NOCOMPILE switch, rather than changing extension code. [source; call_5fe8295d3e96417eae10999af7e569a4, call_55be74efa3ce419b9a502c4784ea8f9c]

## Impact

Eight CUDA configurations cover Ubuntu 22.04 and Windows 2022 with Python 3.10–3.13, CUDA 12.8.1 and Torch 2.7.0. A ninth Ubuntu/Python 3.11 configuration disables extension compilation. No ROCm matrix entry is populated. [source; call_5fe8295d3e96417eae10999af7e569a4]

## Source Notes

The second-parent annotation already describes this manual build-and-release workflow. This merge integrates that build orchestration into dev rather than introducing a new inference mechanism. [ancestor; call_5a2c02a3c47f4edd97f7190677e94f0a]

Closed issue #33, “Error converting model,” reports a conversion failure later diagnosed as “Too many open files,” followed by the reporter confirming normal conversion. It does not establish a fix attributable to this workflow-only change. [source; call_b1fa03fe79874bb6b43a384e2829aea4, call_b222168774e4448dad1d668803c48b28, call_5fe8295d3e96417eae10999af7e569a4]

<a id="build-release"></a>

## Integrating manual distribution builds

workflow_dispatch accepts a required string release input defaulting to '0'. Upload requires exactly '1' and a parsed package version other than 'None'. Matrix fail-fast is disabled, and the workflow grants contents: write. [source; call_5fe8295d3e96417eae10999af7e569a4]

Commands run under PowerShell. Windows jobs install pinned Visual Studio Build Tools, assemble CUDA from versioned NVIDIA archives and enter the developer shell before building. Linux CUDA jobs use the cuda-toolkit action; Linux jobs also free disk space. [source; call_5fe8295d3e96417eae10999af7e569a4]

CUDA jobs install Torch from a CUDA-specific index, pin setuptools to 69.5.1 and request a non-isolated wheel build. TORCH_CUDA_ARCH_LIST supplies compilation targets 8.0, 8.6, 8.9, 9.0, 10.0 and 12.0+PTX; these settings are not runtime compatibility measurements. [source; call_5fe8295d3e96417eae10999af7e569a4]

setup.py recursively collects native sources and registers CUDAExtension only when Torch is available and EXLLAMA_NOCOMPILE is absent. The non-CUDA job installs CPU Torch and sets EXLLAMA_NOCOMPILE=1, suppressing that extension registration. [source; call_55be74efa3ce419b9a502c4784ea8f9c, call_5fe8295d3e96417eae10999af7e569a4]

A standard-library Python transcription of the version and CUDA string operations produced version 0.0.1, release tag v0.0.1, Torch index https://download.pytorch.org/whl/cu128 and build-tag input +cu128-torch2.7.0. [execution; call_ebc81726edb940cdb17cc759c74cbfda, call_f277f5e56ed2498d986c410d6e859695, call_5fe8295d3e96417eae10999af7e569a4]

Publication selects only ./dist/*.whl, permits overwriting assets and uses the package version for the release name and v-prefixed tag. There is no source-archive upload or upload-artifact step, so the default non-release run has no configured artifact handoff. [source; call_5fe8295d3e96417eae10999af7e569a4]

Explicit toolchain versions and architecture targets favor controlled builds over reliance on runner GPU detection. Non-isolated builds make the preceding dependency installation consequential, while opt-in publication separates build attempts from release distribution. [inference; call_5fe8295d3e96417eae10999af7e569a4]

## Uncertainty and limits

No GitHub Actions job, PowerShell command, package build, release upload or GPU compatibility test was executed; external installer and action behavior remains unverified.

The Python check models string transformations, not PowerShell execution or setuptools wheel-name normalization.

The step named Build sdist invokes python -m build -n without an explicit distribution selector; its resulting output set was not established.
