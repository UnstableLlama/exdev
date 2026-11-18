# 8a230d7856b3eca45f92a7ec5c843535acdd4021


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/8a230d7856b3eca45f92a7ec5c843535acdd4021) · [Evidence ledger](draft.json)

Re-enables the Linux CUDA package workaround with nvidia-persistenced=575.57.08-0ubuntu1, retaining CUDA 12.8.1 and installer v0.2.25. Build success remains unverified.

- [Restore the package workaround with a different exact version](#build-release)

## Problem

The workflow comment identifies a CUDA dependency problem. This attempt restores an explicit nvidia-persistenced installation workaround, requesting a different package release. [source; call_a6726dd275f34150aa9b33d2c7d9015e]

## Reasoning

Re-enabling the step and changing its version are coupled: the parent’s 570.148.08-1ubuntu1 commands were commented out, whereas the task actively requests 575.57.08-0ubuntu1 before CUDA installation. This appears to test a new installed-package constraint rather than a new CUDA toolkit version. [inference; call_a6726dd275f34150aa9b33d2c7d9015e, call_f0074b2eb8be464abf78cb96bd1ae2de]

## Impact

The restored step shares the Linux CUDA installer’s non-Windows/nonempty-CUDA guard. Windows provisioning and the CUDA-empty source-distribution job are unchanged. [source; call_a6726dd275f34150aa9b33d2c7d9015e, call_f0074b2eb8be464abf78cb96bd1ae2de]

## Source Notes

Read the immediate-parent entry and the earlier direct-install workaround entry. They describe disabling the workaround and replacing an incompatible PowerShell heredoc with ordinary package-management commands, respectively. [ancestor; call_2188bbcde9cd4f3385a955ac8c01dd52, call_085136fa76de4eaeb4e446564a457360]

The task retains shell: pwsh but restores only ordinary sudo commands; the earlier heredoc construct remains absent. Whole-parent searches found apt-get and nvidia-persistenced only in this workflow’s commented workaround. [source; call_f0074b2eb8be464abf78cb96bd1ae2de, call_a6726dd275f34150aa9b33d2c7d9015e, call_d16b4d5897484297a30f7674f1487d22, call_62483f9cab1544ddaaa07d105b59420a]

Supplied issue #6, “No ROCm runtime is found, using ROCM_HOME='/usr',” reports a chat startup traceback ending in an empty-source assertion. Discussion suggests a ROCm PyTorch installation; the reporter later says installation succeeded despite the notification. This does not establish the CUDA package workaround’s effectiveness. [source; call_18cbd2eedb9548d68feb5ed47448bd0b, call_de81a0c60b0f455ebf68874825ed68d2, call_870e44fb53c148c589b5d81cf29c2f7a, call_03d3654824984cdda8aadb572cdc3057]

<a id="build-release"></a>

## Restore the package workaround with a different exact version

The enabled sequence refreshes APT indexes, requests nvidia-persistenced=575.57.08-0ubuntu1 with -y and --allow-downgrades, then requests apt-mark hold. The version identifies a package release, not a CUDA compute capability or toolkit version. No APT preference file is written. [source; call_a6726dd275f34150aa9b33d2c7d9015e]

Installation precedes the hold and both precede Jimver/cuda-toolkit@v0.2.25. The installer still receives matrix.cuda, network installation and --toolkit; the task changes neither the action release nor its inputs. [source; call_a6726dd275f34150aa9b33d2c7d9015e, call_f0074b2eb8be464abf78cb96bd1ae2de]

A bounded Python inspection counted nine matrix rows, eight requesting CUDA 12.8.1. Four Ubuntu CUDA rows satisfy the restored step’s selection criteria, covering Python 3.10–3.13. [execution; call_da5a6561552f4beb9e1740a1db91cf18]

The strategy trades unconstrained package selection for an exact installed version followed by a hold. It is an installer experiment, not evidence that the requested package can be installed or that subsequent CUDA provisioning succeeds. [inference; call_a6726dd275f34150aa9b33d2c7d9015e, call_f0074b2eb8be464abf78cb96bd1ae2de]

## Uncertainty and limits

No Actions job, PowerShell script, APT transaction, CUDA installation or wheel build was executed. Package availability and dependency resolution remain unverified.

The external CUDA action and linked NVIDIA forum discussion were not inspected; the underlying dependency conflict is not established.

The Python computation counted parent matrix declarations; it did not execute GitHub Actions conditions or package-management commands.
