# 6a991a8bc095bca97c5e6f4670b013b50b424571


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/6a991a8bc095bca97c5e6f4670b013b50b424571) · [Evidence ledger](draft.json)

Updates the Linux CUDA action to v0.2.25 and disables the nvidia-persistenced workaround. Despite the message naming CUDA 12.9, the matrix still requests 12.8.1; build success remains unverified.

- [Update the Linux CUDA installer, retaining CUDA 12.8.1](#build-release)

## Problem

The workflow carries a workaround for a reported CUDA dependency problem: explicitly install and hold nvidia-persistenced before Linux CUDA installation. [source; call_9729b038a3aa405aa3cae5b050f13e3b]

## Reasoning

The change couples removal of that workaround with updating Jimver/cuda-toolkit from v0.2.24 to v0.2.25. This appears to test the newer installer without the package constraint; successful dependency resolution is not established. [inference; call_99ef9b81da734ed593e6525fc55e731f]

## Impact

Only the Linux CUDA installation path changes. Windows provisioning, the CUDA matrix values, Torch selection and packaging commands remain unchanged. [source; call_99ef9b81da734ed593e6525fc55e731f, call_9729b038a3aa405aa3cae5b050f13e3b]

## Source Notes

Read the workflow-introduction entry and the earlier pin-repair entry. They establish the inherited build orchestration and an earlier PowerShell/heredoc defect. [ancestor; call_f1c674bb936c4236927d1a6eb23d4338, call_105baeadc2e0402880997f5065bdca0d]

That earlier heredoc defect is absent from the inspected parent: its workaround instead uses three ordinary sudo commands. The task comments those commands out entirely. [source; call_9729b038a3aa405aa3cae5b050f13e3b, call_99ef9b81da734ed593e6525fc55e731f]

Issue #5 concerns quantized-format stability and Ampere performance, not installer dependency resolution; its supplied discussion does not validate this change. [source; call_de087e5d84fb47db8005136b12049caf, call_ca362588604341e3a06f8c8019decb85, call_f773a34901bd40debc83eddc1a04f3cf]

Closed issue #21, “Build Failure on Windows: CUDA 12.4 / PyTorch 2.7.0+cu126 / VS 2022,” reports compilation failures and closes without a solution. Its relationship here is only inferred from shared CUDA/build-toolchain concerns; the task changes the Linux installer, not the reported Windows path. [inference; call_db20be21634445fca5e126e3fd6fa6b0, call_99ef9b81da734ed593e6525fc55e731f]

<a id="build-release"></a>

## Update the Linux CUDA installer, retaining CUDA 12.8.1

Despite the commit message's “try CUDA Toolkit 12.9,” the diff changes an action release, not the requested toolkit version. The installer still receives matrix.cuda, and all eight CUDA rows still specify 12.8.1. [source; call_99ef9b81da734ed593e6525fc55e731f, call_9729b038a3aa405aa3cae5b050f13e3b]

The removed step refreshed APT metadata, requested exactly nvidia-persistenced=570.148.08-1ubuntu1 with downgrades allowed, and requested a package hold. No remaining occurrence supplies that explicit install-and-hold sequence. Its removal relinquishes that package constraint, but does not itself demonstrate a failing input path. [source; call_a54778186ff74835a410562b5b7d944a, call_9729b038a3aa405aa3cae5b050f13e3b, call_99ef9b81da734ed593e6525fc55e731f]

The updated action retains network installation, linux-local-args='["--toolkit"]', and the non-Windows/nonempty-CUDA guard. Consequently the changed path applies to the four Ubuntu CUDA rows, not Windows or the CUDA-empty packaging row. [source; call_9729b038a3aa405aa3cae5b050f13e3b, call_99ef9b81da734ed593e6525fc55e731f]

A bounded Python inspection counted nine matrix rows, eight requesting CUDA 12.8.1 and four affected Ubuntu CUDA rows. Transcribing the workflow's version-string transformation produced suffix 128, consistent with the unchanged cu128 Torch index selection. [execution; call_86931543e95a4faebf5f8ab570c37e2f]

The two edits form one installer experiment rather than independent runtime features: the newer action runs without the prior package workaround. Neither edit changes model inference or quantized storage. [inference; call_99ef9b81da734ed593e6525fc55e731f]

## Uncertainty and limits

No Actions job, PowerShell script, APT transaction, CUDA installation or wheel build was executed.

The external action's v0.2.25 implementation and package-resolution behavior were not inspected; no evidence establishes that it fixes the dependency problem.

The Python check reads matrix declarations and models version-string transformation; it does not execute PowerShell or the installer.
