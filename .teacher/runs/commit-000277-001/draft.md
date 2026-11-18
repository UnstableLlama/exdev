# 90660d69b5d3550195c447e6f0e7521e497df49b


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/90660d69b5d3550195c447e6f0e7521e497df49b) · [Evidence ledger](draft.json)

Replaces the Linux CUDA dependency preference file with explicit installation and holding of nvidia-persistenced 570.148.08-1ubuntu1; installation success remains unverified.

- [Install and hold the CUDA dependency explicitly](#build-release)

## Problem

The workflow describes a temporary CUDA dependency workaround involving nvidia-persistenced. Previously it wrote an APT preference but did not explicitly install the selected version. [source; call_bbfa373653574f4795151661d7bffe75, call_efa312e1d2264cf3ae117dffe4985ab0]

## Reasoning

The replacement attempts to establish the package version before CUDA installation, rather than merely providing package-selection preferences to a later installer. [inference; call_efa312e1d2264cf3ae117dffe4985ab0, call_bbfa373653574f4795151661d7bffe75]

## Impact

The unchanged condition selects the four Ubuntu CUDA wheel jobs, excluding Windows and the CUDA-empty source-distribution job. The subsequent CUDA installer and wheel-building commands are unchanged. [source; call_bbfa373653574f4795151661d7bffe75, call_efa312e1d2264cf3ae117dffe4985ab0]

## Source Notes

The earlier pin-introduction entry was read. It records an indentation defect in the original preference-writing block. [ancestor; call_a33315fdd01b46ceb2c4a19e00cddf42]

That original indentation defect is absent from the inspected parent: its preference lines are already indented. This task removes the entire preference-writing block, so the recorded defect is not carried over. [source; call_bbfa373653574f4795151661d7bffe75, call_efa312e1d2264cf3ae117dffe4985ab0]

Whole-parent search locates nvidia-persistenced only in this workflow and finds no existing apt-mark invocation. The broader CUDA search also returns documentation, calibration text and native code, but is truncated; those matches do not establish the reported dependency diagnosis. [source; call_c4a2f1a95ab74b8fbb23fb4d09f52652, call_9635d3dd750d4a4f9c07b50ad978d424, call_82378041b44e4215875993e7c703e860]

The supplied PR #4 body says only “containg -> containing”; it provides no corroboration for the CUDA workaround. [source; call_7bcd42fb8bab462c83efa992a3e45e84]

<a id="build-release"></a>

## Install and hold the CUDA dependency explicitly

The step now runs apt-get update, requests nvidia-persistenced=570.148.08-1ubuntu1 with -y --allow-downgrades, then invokes apt-mark hold nvidia-persistenced. The version is a literal package-build selection, not a CUDA version or numerical threshold. [source; call_efa312e1d2264cf3ae117dffe4985ab0]

The removed block wrote /etc/apt/preferences.d/99-nvidia-persistenced with the same version and Pin-Priority: 1001. The replacement no longer creates that preference file; it substitutes explicit installation and a hold command for preference-based selection. [source; call_efa312e1d2264cf3ae117dffe4985ab0]

Both this step and the following Jimver/cuda-toolkit@v0.2.24 step require a non-Windows runner and nonempty matrix.cuda. The latter retains CUDA 12.8.1, network installation and linux-local-args=['--toolkit']. [source; call_bbfa373653574f4795151661d7bffe75, call_efa312e1d2264cf3ae117dffe4985ab0]

The apparent tradeoff is stronger preparation of package state before the CUDA action, at the cost of depending on one exact distribution package build. Installation and holding are coupled parts of that workaround; neither source inspection nor the commit's “Attempt #4” framing proves it succeeds. [inference; call_efa312e1d2264cf3ae117dffe4985ab0, call_bbfa373653574f4795151661d7bffe75]

## Uncertainty and limits

No GitHub Actions, PowerShell, APT or CUDA installation was executed. Package availability, dependency resolution and successful wheel creation remain unverified.

The job retains its default pwsh shell. Removing the heredoc does not by itself establish successful execution of the replacement commands.

The exact package version's suitability and the operational effects of --allow-downgrades and apt-mark hold were not independently verified against eligible package-manager documentation.

No useful scalar computation would validate this package-manager change; a numerical transcription would not test its central behavior.
