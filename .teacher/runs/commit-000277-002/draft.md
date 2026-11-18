# 90660d69b5d3550195c447e6f0e7521e497df49b


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/90660d69b5d3550195c447e6f0e7521e497df49b) · [Evidence ledger](draft.json)

Replaces the PowerShell-incompatible APT preference heredoc with an exact-version nvidia-persistenced installation and hold before Linux CUDA setup; successful dependency resolution remains unverified.

- [Replace the preference heredoc with installation and hold](#build-release)

## Problem

The workflow's CUDA dependency workaround used a heredoc despite inheriting shell: pwsh. This attempt replaces that script with direct package-management commands. [source; call_c198240f6a5c46fcb35ad0cd1c1573a7, call_30d07d40336740b9b0cddc6dddf0c05c]

## Reasoning

Instead of writing an APT preference, the step refreshes package indexes, requests nvidia-persistenced=570.148.08-1ubuntu1 with -y --allow-downgrades, and then requests an apt-mark hold. The exact version is a package release identifier, not the CUDA toolkit version. [source; call_c198240f6a5c46fcb35ad0cd1c1573a7]

The apparent strategy is to establish the desired installed package state before CUDA installation, rather than influence subsequent selection through a preference file. Whether this resolves the reported dependency problem is unverified. [inference; call_c198240f6a5c46fcb35ad0cd1c1573a7, call_30d07d40336740b9b0cddc6dddf0c05c]

## Impact

The unchanged guard selects the four Ubuntu CUDA matrix rows, covering Python 3.10–3.13. Windows rows and the non-CUDA source-distribution row skip this step. The subsequent network installer remains Jimver/cuda-toolkit@v0.2.24 with --toolkit. [source; call_30d07d40336740b9b0cddc6dddf0c05c, call_c198240f6a5c46fcb35ad0cd1c1573a7]

## Source Notes

Read the immediate parent's entry, which records the heredoc/PowerShell incompatibility and does not establish successful dependency resolution. [ancestor; call_f05181c5681d42a5bd99316b5d2dd6a2]

Whole-parent searches found nvidia-persistenced only in this workflow and apt-get only in its existing update command; there was no existing apt-get install call to compare. [source; call_093d8310b23b4e3d947916f7495fab22, call_bddd32c1bc20464eac90bd83d8180f6a]

The supplied PR #4 body describes only “containg -> containing”; it provides no evidence for this CUDA workaround. [source; call_4f7c33a1ace74f5d85bb03188449176c]

<a id="build-release"></a>

## Replace the preference heredoc with installation and hold

Source comparison shows that the inherited heredoc defect is removed: tee, the preference body, priority 1001 and EOF disappear. The job still uses pwsh, but the replacement no longer contains the incompatible heredoc construct. [source; call_c198240f6a5c46fcb35ad0cd1c1573a7, call_30d07d40336740b9b0cddc6dddf0c05c]

The three commands are coupled: index refresh precedes the exact-version installation request, and the hold follows it before the CUDA installer. This replaces a file-based selection policy with an attempted installed-state workaround; no preference file is written by the new block. [source; call_c198240f6a5c46fcb35ad0cd1c1573a7, call_30d07d40336740b9b0cddc6dddf0c05c]

## Uncertainty and limits

No Actions job, PowerShell interpreter, APT transaction or CUDA installation was executed. Package availability, downgrade success and subsequent hold behavior remain unestablished.

The external CUDA action's implementation and the underlying dependency conflict were not inspected; command ordering alone does not prove resolution.

No useful scalar computation would establish these package-manager and shell behaviors.

The broad CUDA search was truncated; its returned occurrences include runtime code, documentation and calibration text, not evidence that those occurrences share this dependency defect.
