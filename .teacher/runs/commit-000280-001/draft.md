# 454ff4c6007fa6e1b64f765506da78447bce4cff


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/454ff4c6007fa6e1b64f765506da78447bce4cff) · [Evidence ledger](draft.json)

Adds NVIDIA APT repository setup before the existing persistenced install-and-hold workaround and rolls the Linux CUDA action back to v0.2.24; build success remains unverified.

- [Enable NVIDIA's APT repository before the package workaround](#build-release)

## Problem

The workflow attempts to install and hold nvidia-persistenced before installing CUDA. This change adds NVIDIA repository setup before that request; successful dependency resolution is not established. [source; call_80ccdd4d49e340158ef993881d2feb9f, call_b340325d60824b37b99c298bdcdad128]

## Reasoning

Repository registration and metadata refresh supply an apparent prerequisite for the existing exact-version package request. The simultaneous installer rollback makes this a combined provisioning experiment, not evidence that either edit independently resolves the dependency conflict. [inference; call_80ccdd4d49e340158ef993881d2feb9f, call_b340325d60824b37b99c298bdcdad128]

## Impact

The new repository step selects every Linux row, including the CUDA-empty source-distribution row. Package installation and the CUDA action retain their narrower non-Windows/nonempty-CUDA guards; Windows provisioning is unchanged. [source; call_80ccdd4d49e340158ef993881d2feb9f, call_b340325d60824b37b99c298bdcdad128]

## Source Notes

Read the workflow-introduction, direct-package-workaround and installer-update entries. They establish the inherited orchestration, the replacement of a PowerShell-incompatible heredoc, and the earlier move to action v0.2.25. [ancestor; call_af8ce0e642b54d788953883ed86d0022, call_cc77ab80ba934c6caa62fa982cbe3c0d, call_e231c36052bd4bbc8856b2308a141e9e]

The earlier heredoc defect remains absent: the existing package workaround uses ordinary sudo commands, while the newly added shell-specific script explicitly selects Bash rather than inheriting PowerShell. [source; call_80ccdd4d49e340158ef993881d2feb9f, call_b340325d60824b37b99c298bdcdad128]

Issue #7, “quantizing model: undefined symbol: __cxa_call_terminate,” reports a Conda extension-import failure. Reporter async0x42 later reports success after installing cmake and gxx; randoentity suggests conda-forge. These reports do not demonstrate resolution of this workflow's APT dependency problem. [source; call_f5902c0a1a9b4e658b32fc23f23a654b, call_515daf70add74056ac7fc8315db79210, call_b3809e3b922e4173becbd0c89e1ff7e9]

Closed issue #16, “RuntimeError: CUDA error: invalid configuration argument,” concerns conversion on a 3060 and is attributed in its discussion to tokenizer truncation. Any relationship to this task is only an inference from shared CUDA/environment terminology, not a matching APT failure. [inference; call_066cb057311445d9bfc5c23d06fcacda, call_80ccdd4d49e340158ef993881d2feb9f]

<a id="build-release"></a>

## Enable NVIDIA's APT repository before the package workaround

The added Bash step enables errexit, unset-variable checking and pipeline failure propagation. It obtains the Ubuntu release with lsb_release, removes periods, prefixes ubuntu, and fixes the repository architecture to x86_64. These values select a distribution-specific repository rather than a CUDA compute capability. [source; call_80ccdd4d49e340158ef993881d2feb9f]

It creates /usr/share/keyrings, downloads cuda-archive-keyring.gpg there, and writes /etc/apt/sources.list.d/cuda.list with a signed-by reference to that same keyring. It then refreshes APT metadata. The script does not explicitly create /etc/apt/sources.list.d. [source; call_80ccdd4d49e340158ef993881d2feb9f]

The subsequent unchanged workaround refreshes metadata again, requests nvidia-persistenced=575.57.08-0ubuntu1 with downgrades allowed, and requests a hold. That number is the package release constraint, distinct from CUDA 12.8.1. Whole-parent search found these package references only in this workflow and no other apt-get call sites. [source; call_b340325d60824b37b99c298bdcdad128, call_7e2601a6c02a45d18a9e93c7be306fc4, call_f8a9c2cad07042389a4a92ef9030f11b]

Despite the message saying “jimver 0.0.24,” the actual action change is v0.2.25 to v0.2.24. Its inputs remain matrix.cuda, network installation and linux-local-args containing --toolkit. The matrix still requests CUDA 12.8.1. [source; call_80ccdd4d49e340158ef993881d2feb9f, call_b340325d60824b37b99c298bdcdad128]

A bounded Python inspection counted nine matrix rows: five Ubuntu rows selected by the new repository guard, four selected by the existing CUDA provisioning guard, and one CUDA-empty Ubuntu row receiving repository setup alone. Transcribing period removal maps 22.04 to ubuntu2204. [execution; call_4ab06a35e2b14aee8a2fac9fbbbaa2dd]

The broader guard adds a network and package-index prerequisite to source-distribution packaging even though that row does not install CUDA. This is a provisioning-scope expansion, not a demonstrated build failure. [inference; call_80ccdd4d49e340158ef993881d2feb9f, call_b340325d60824b37b99c298bdcdad128]

## Uncertainty and limits

No Bash, PowerShell, APT transaction, GitHub Actions job or CUDA installation was executed. Repository availability, signing-key validity, exact package availability and dependency resolution remain unverified.

The external Jimver action implementations were unavailable for inspection; their behavioral differences and internal prerequisites are unestablished.

The Python check counts parent matrix declarations and transcribes distribution-name construction; it does not execute the added provisioning script.
