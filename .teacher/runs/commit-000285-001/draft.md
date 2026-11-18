# 9e1b479c8afff55154670a7477ed0d05c270727b


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/9e1b479c8afff55154670a7477ed0d05c270727b) · [Evidence ledger](draft.json)

Switches Linux CUDA provisioning to the local installer method and comments out NVIDIA repository setup and package holds; build success remains unverified.

- [Try local CUDA installation without the APT workaround](#build-release)

## Problem

The workflow's comments identify a CUDA dependency problem. This attempt replaces network installation with local installation and disables the explicit NVIDIA APT workaround; successful provisioning is not demonstrated. [source; call_097148f1a42046d5bf51565c57b95b3d, call_b265d2d5e95d443aaee3fc154196d2b9]

## Reasoning

These edits form a combined provisioning experiment: the installer method changes while repository registration and exact-version package installation are withdrawn. The evidence does not isolate either edit as a fix. [inference; call_097148f1a42046d5bf51565c57b95b3d]

## Impact

Four Linux CUDA wheel configurations retain CUDA 12.8.1 but request the local installer method. The CUDA-empty Linux packaging configuration also loses the previously unconditional Linux repository-setup step. Windows provisioning is unchanged. [source; call_b265d2d5e95d443aaee3fc154196d2b9, call_097148f1a42046d5bf51565c57b95b3d]

## Source Notes

Read the workflow-introduction entry and the entry introducing NVIDIA repository setup. They establish the inherited build orchestration and the repository step's broader Linux guard. [ancestor; call_9b5ee287698d4a9fbc07f15159f3dd57, call_6908b8d4423444c2856c283482e06ed0]

Issue #12, “Qwen2.5 Coder 0.5B Instruct | ValueError: Unsupported type in stop_conditions,” reports a chatbot failure; turboderp recommends chatml mode, and Volko61 acknowledges the mode mistake. Its subject does not substantiate this workflow change despite the shared number 12. [source; call_a60cc27cd05a4bc0a3e47eb680df63a3, call_6f8485b166f04adba06bda13de3f811f, call_024c2d004f934e99bca45936997b874a]

<a id="build-release"></a>

## Try local CUDA installation without the APT workaround

The Linux CUDA action remains Jimver/cuda-toolkit@v0.2.24, receiving matrix.cuda and linux-local-args='["--toolkit"]'. Only method changes from network to local; the existing non-Windows/nonempty-CUDA guard remains. [source; call_b265d2d5e95d443aaee3fc154196d2b9, call_097148f1a42046d5bf51565c57b95b3d]

The commented repository step previously constructed a distribution-specific NVIDIA URL, created /usr/share/keyrings, downloaded a signing key, wrote cuda.list and refreshed APT metadata. None of those explicit preparations remains active in this workflow. [source; call_b265d2d5e95d443aaee3fc154196d2b9, call_097148f1a42046d5bf51565c57b95b3d]

The second commented step previously requested both nvidia-persistenced and libnvidia-cfg1 at 575.57.08-0ubuntu1, allowed downgrades, and held both packages. That number is a package-release constraint, not the requested CUDA toolkit version. Disabling the step removes these explicit requests and holds, without establishing what the external installer will install. [source; call_097148f1a42046d5bf51565c57b95b3d, call_4df37cc573ea4fddbae3976e497f5c58, call_69a4723f52234876bf8d41a211ea76ad]

A bounded Python inspection counted nine matrix rows: five selected by the parent's Linux repository guard, four selected by the unchanged CUDA-action guard, and one CUDA-empty Linux row. All Linux CUDA rows request 12.8.1. [execution; call_11d71edfcaa542a89fb116e32cde33a0]

Downstream steps still install Torch 2.7.0 from a CUDA-version-derived index and invoke the non-isolated CUDA wheel build. The change therefore alters toolchain provisioning, not build targets or the release-upload condition. [source; call_b265d2d5e95d443aaee3fc154196d2b9, call_097148f1a42046d5bf51565c57b95b3d]

Removing explicit package-version control trades the workflow's visible workaround for reliance on the selected installer path. Whether local installation avoids the reported dependency problem cannot be concluded from the workflow alone. [inference; call_097148f1a42046d5bf51565c57b95b3d]

## Uncertainty and limits

The external Jimver/cuda-toolkit implementation was not available for inspection. The precise local-versus-network behavior, interpretation of --toolkit, and internal prerequisites remain unestablished.

No GitHub Actions job, installer, APT transaction or build ran. Package availability, dependency resolution and build success remain unverified.

The Python check inspected matrix declarations and modeled guards; it did not execute GitHub Actions expressions or provisioning commands.
