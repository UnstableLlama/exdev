# 7c9b9fbd3d8f8e156880591284ca2ab17ea65715


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/7c9b9fbd3d8f8e156880591284ca2ab17ea65715) · [Evidence ledger](draft.json)

Restores NVIDIA repository setup and exact-version install-and-hold commands, while rolling Linux CUDA back to 12.8.1 and its installer action to v0.2.24. Build success remains unverified.

- [Restore the NVIDIA package workaround and CUDA 12.8.1](#build-release)

## Problem

The author labels this another unsuccessful provisioning attempt: “Attempt #11, it didn't stick.” The workflow comment identifies a CUDA dependency problem, but neither establishes its exact failure mode. [source; call_cafb6a59f2cb4318b39b8439c983422f]

## Reasoning

Repository registration supplies an apparent prerequisite for requesting the two exact NVIDIA package releases. Restoring it alongside package holds, a toolkit rollback and an action rollback makes this a combined provisioning experiment, not evidence that any individual edit fixes the problem. [inference; call_cafb6a59f2cb4318b39b8439c983422f]

## Impact

Linux CUDA builds return to toolkit 12.8.1 and consequently select the cu128 PyTorch index and wheel build tag instead of cu129. Windows provisioning remains unchanged. Repository setup also runs for the Linux source-distribution row, although that row skips package pinning and CUDA installation. [source; call_cafb6a59f2cb4318b39b8439c983422f, call_5487c07716fe4c528440496e05902a4a]

## Source Notes

Read the earlier repository-setup entry, which establishes the provenance of the restored script and records the earlier removal of a PowerShell-incompatible heredoc. [ancestor; call_2b47b09633cc425d807db567e1cfeeb5]

The task retains ordinary package commands rather than restoring the defective heredoc. Repository setup explicitly selects Bash; the install-and-hold step inherits the job's PowerShell default. [source; call_cafb6a59f2cb4318b39b8439c983422f, call_5487c07716fe4c528440496e05902a4a]

Issue #11, “AssertionError: bias is wrong datatype,” reports quantization failing at a bias dtype assertion. turboderp says the latest commit should fix it, and reporter async0x42 confirms success. These reports do not establish success of this workflow-only change. [source; call_9406d72d07594e24ac4f702cc0371cbf, call_e88e26fb92fd47f581258fcd8c17cd15, call_83abad0433f04cc9821f7285eded5816]

Closed issue #46, “Manually compiling results in gibberish,” concerns source-build output on Debian with CUDA 12.9; its reporter later cannot reproduce on main. A possible connection is only inference from the shared CUDA 12.9/build context, not a matching APT failure or an explicit task link. [inference; call_22f74c2f767748ae8290c6a2fc262fc4, call_cafb6a59f2cb4318b39b8439c983422f]

<a id="build-release"></a>

## Restore the NVIDIA package workaround and CUDA 12.8.1

Four Ubuntu wheel rows, covering Python 3.10–3.13, change CUDA 12.9.0 to 12.8.1. Torch remains 2.7.0 and the target architecture list is unchanged. The Linux installer action changes from v0.2.25 to v0.2.24 while retaining matrix.cuda, network installation and the --toolkit argument. [source; call_cafb6a59f2cb4318b39b8439c983422f, call_5487c07716fe4c528440496e05902a4a]

The restored repository step derives the Ubuntu repository name by removing periods from lsb_release output and prefixing ubuntu, with x86_64 fixed as the repository architecture. It creates /usr/share/keyrings, downloads the signing key there, writes a signed-by repository declaration to /etc/apt/sources.list.d/cuda.list, and refreshes APT metadata. It does not explicitly create /etc/apt/sources.list.d. [source; call_cafb6a59f2cb4318b39b8439c983422f]

The next step requests nvidia-persistenced and libnvidia-cfg1 together at 575.57.08-0ubuntu1, allowing downgrades, then requests holds for both together. That number is an exact package release, not the CUDA toolkit version. Unlike the parent's commented sequence, there is one installation transaction followed by one hold command. Whole-parent apt-get search found only the commented workflow calls. [source; call_cafb6a59f2cb4318b39b8439c983422f, call_c856e32dc5af4c6aa24713ba46518265]

The repository guard selects all Linux rows; package pinning and Linux CUDA installation require a non-Windows runner and nonempty matrix.cuda. Thus the source-distribution row acquires repository/network preparation without acquiring CUDA installation, expanding its prerequisites. [source; call_cafb6a59f2cb4318b39b8439c983422f, call_5487c07716fe4c528440496e05902a4a]

A bounded Python model read the parent matrix and applied the inspected version substitution: five rows select repository setup, four select package pinning, and all eight CUDA rows derive cu128. The modeled distribution transformation maps 22.04 to ubuntu2204. [execution; call_ec72530b50554cfe95f385dd02f9d951]

## Uncertainty and limits

No GitHub Actions job, Bash or PowerShell provisioning script, APT transaction, CUDA installation or wheel build was executed. Package availability, dependency resolution and successful holds remain unverified.

The implementations of Jimver/cuda-toolkit v0.2.24 and v0.2.25 were not available in the inspected repository evidence; their internal behavior and differences are unestablished.

The Python calculation models matrix guards and string transformations; it does not execute PowerShell or validate external package indexes.
