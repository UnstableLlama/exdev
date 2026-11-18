# bc256477d64744c36b2f9340f50c3c2467cfd921


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/bc256477d64744c36b2f9340f50c3c2467cfd921) · [Evidence ledger](draft.json)

Requests CUDA 12.9.0 for Linux wheels, updates the Linux installer action and comments out the NVIDIA APT workaround; successful provisioning remains unverified.

- [Disable the package workaround and request Linux CUDA 12.9](#build-release)

## Problem

This is another CUDA provisioning experiment: the workflow disables its explicit NVIDIA APT workaround while updating the Linux toolkit request and installer action. [source; call_ecc58076860c40339aea4d970dd5a81b]

## Reasoning

The edits should be evaluated together: removing repository registration and package holds changes the environment in which the newer installer requests CUDA 12.9.0. The source does not isolate which edit might resolve the dependency problem mentioned in the retained comment. [inference; call_ecc58076860c40339aea4d970dd5a81b, call_ffeb1abdea29480e8852acc154a639d1]

## Impact

The Linux version change also changes the downstream Torch index and wheel build-tag input, not just toolkit installation. Windows retains CUDA 12.8.1. [source; call_ecc58076860c40339aea4d970dd5a81b, call_ffeb1abdea29480e8852acc154a639d1]

## Source Notes

Read the workflow-introduction, NVIDIA-repository-setup and immediate-parent entries. They establish the inherited orchestration, the repository setup's broader Linux scope, and the previous removal of explicit libnvidia-cfg1 installation; none establishes successful provisioning. [ancestor; call_8b5c156da1ff46f9a64f6ebdda46b9a5, call_f838835551794a4ebdc8bb10ae7049e3, call_7188d6c8a4dc44ddbb035de3c8c73633]

The supplied issue #10 evidence contains an empty issue body and a rocket-emoji comment, providing no technical explanation for the workflow change. [source; call_59b0af1d7b8b48e8bf96de4474623b0e, call_1d8e447c3e804acca2eb4e9ea9d930b7]

<a id="build-release"></a>

## Disable the package workaround and request Linux CUDA 12.9

Four Ubuntu 22.04 wheel rows, covering Python 3.10–3.13, change CUDA 12.8.1 to 12.9.0. Torch remains 2.7.0 and the architecture list remains unchanged. The four Windows rows and CUDA-empty packaging row retain their previous matrix values. [source; call_ecc58076860c40339aea4d970dd5a81b, call_ffeb1abdea29480e8852acc154a639d1]

Both workaround steps become comments. The workflow therefore no longer explicitly registers NVIDIA's repository, refreshes its indexes through these steps, installs nvidia-persistenced=575.57.08-0ubuntu1 with downgrades allowed, or holds either NVIDIA package. The newly added libnvidia-cfg1 installation line is also commented out and never becomes an active installation request. [source; call_ecc58076860c40339aea4d970dd5a81b]

The disabled repository step previously selected every Linux row, including CUDA-empty packaging; the disabled package step selected only non-Windows rows with nonempty CUDA. Removing these steps also removes their explicit preparation and constraints, rather than replacing them with equivalent guarantees elsewhere in the inspected workflow. [source; call_ffeb1abdea29480e8852acc154a639d1, call_ecc58076860c40339aea4d970dd5a81b]

The Linux installer changes from Jimver/cuda-toolkit@v0.2.24 to v0.2.25 while retaining matrix.cuda, network installation, --toolkit and the non-Windows/nonempty-CUDA guard. The action release, toolkit version and NVIDIA package release are separate version constraints. [source; call_ecc58076860c40339aea4d970dd5a81b, call_ffeb1abdea29480e8852acc154a639d1]

The downstream dependency step removes the toolkit patch component and periods to select the Torch index; the build step reuses that result in its tag. A bounded Python transcription counted four changed rows and derived 129 for Linux versus 128 for Windows, yielding Linux index https://download.pytorch.org/whl/cu129 and build-tag input +cu129-torch2.7.0. [execution; call_76fb1a1ac5ba4dce98df7b3899fdcd8e, call_ffeb1abdea29480e8852acc154a639d1]

## Uncertainty and limits

No GitHub Actions job, APT transaction, PowerShell command or CUDA build was executed. Dependency resolution and build success remain unverified.

The external Jimver action implementations were not inspected; their internal differences and prerequisites are unestablished.

Availability of Torch 2.7.0 at the newly derived cu129 index is not established by the supplied source.

The Python check models matrix selection and string transformations only; it does not execute PowerShell or establish final wheel filename normalization.
