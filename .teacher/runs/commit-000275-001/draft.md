# 1fa77542243550a22d15454cad1b9b5461685f45


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/1fa77542243550a22d15454cad1b9b5461685f45) · [Evidence ledger](draft.json)

Attempts to pin nvidia-persistenced before Linux CUDA installation, but unindented command lines appear to invalidate the workflow; dependency resolution remains untested.

- [Attempted Linux CUDA dependency pin](#build-release)

## Problem

The change attempts a temporary workaround for a CUDA dependency error by pinning nvidia-persistenced before Linux toolkit installation. [source; call_3c6a85056d0a49469d84f21967ed524b]

## Reasoning

Placing the preference before the existing network-based CUDA installer would make package selection policy available before installation, rather than changing CUDA compilation or Python dependencies. [inference; call_3c6a85056d0a49469d84f21967ed524b, call_87d5b0b09ea2490482148e07c7b3413a]

## Impact

The new condition targets the four Ubuntu CUDA matrix rows, excluding Windows and the CUDA-empty packaging row. However, malformed indentation appears to prevent the workflow from being accepted at all. [source; call_3c6a85056d0a49469d84f21967ed524b, call_87d5b0b09ea2490482148e07c7b3413a]

## Source Notes

The introduction and merge entries were read. They establish the inherited manual build matrix, PowerShell command default and opt-in release publication; neither records a defect directly affected by this pin. [ancestor; call_01355953d356400db3b12afb80902107, call_99c9fec3a8d34b46993f1a55b60e05e8]

Issue #2, “Error: setup script specifies an absolute path,” reports a wheel-build failure involving setup.py paths. Its reported error differs from this change's package-selection workaround; the issue does not establish the CUDA dependency diagnosis. [source; call_9f047d0ef3b94cbeaa8e5d6d0c3c8768, call_3c6a85056d0a49469d84f21967ed524b]

Whole-parent searches found no nvidia-persistenced or apt-get occurrences. A broader CUDA search also found documentation, calibration text and native code, but was truncated; those occurrences do not independently identify this dependency failure. [source; call_a0e2f2e5d6ce4b79b7f72b1417509179, call_9bd5ad3012d14d9abede5c12b4d69eb9, call_d08581a98c1f496892b1128168880dec]

<a id="build-release"></a>

## Attempted Linux CUDA dependency pin

The added step intends to write an APT preference for Package: nvidia-persistenced, version 570.148.08-1ubuntu1, priority 1001, to /etc/apt/preferences.d/99-nvidia-persistenced, then refresh package indexes. It does not explicitly install that package. [source; call_3c6a85056d0a49469d84f21967ed524b]

The existing next step invokes Jimver/cuda-toolkit@v0.2.24 with CUDA 12.8.1, network installation and --toolkit. Both steps use the same non-Windows, nonempty-CUDA condition. The workflow retains its default pwsh shell. [source; call_87d5b0b09ea2490482148e07c7b3413a, call_3c6a85056d0a49469d84f21967ed524b]

The workaround trades unrestricted package selection for one hard-coded distribution version. Its comment calls this temporary, but the source supplies no fallback or package-availability check. [source; call_3c6a85056d0a49469d84f21967ed524b]

A standard-library Python transcription measured indentation of 10, 0, 0 and 10 spaces for the four command lines. This confirms the textual indentation discrepancy, not YAML parsing or installer behavior. [execution; call_24305cce2dfd4cd7a46d575d10162820]

## Authoring-time findings — pending review

### unindented-pin-lines (suspected; defect)

The added multiline command contains two unindented lines that escape the YAML run block, apparently invalidating the workflow before its conditional steps can run.

Trigger: GitHub Actions loads the modified build.yml workflow.

Expected: All lines of the preference-writing command remain inside the run scalar, allowing the workflow to schedule its jobs.

Actual: Pin: and Pin-Priority: begin at column zero, ending the indented run scalar; the following indented apt-get command does not restore the intended workflow structure. The suspected reach is the entire workflow, not only Linux CUDA jobs.

Locations: 1fa77542243550a22d15454cad1b9b5461685f45:.github/workflows/build.yml — jobs.build_wheels.steps: Pin nvidia-persistenced 570.148.08

Source evidence: call_3c6a85056d0a49469d84f21967ed524b

source_inspection: Compared the new run block with the enclosing workflow indentation and inherited job structure. [call_3c6a85056d0a49469d84f21967ed524b, call_87d5b0b09ea2490482148e07c7b3413a]. Limits: No YAML parser or Actions validation was run.

scalar_transcription: Counted leading spaces in the four added command lines. [call_24305cce2dfd4cd7a46d575d10162820]. Limits: Text measurement only; not execution of the repository workflow.

## Uncertainty and limits

No YAML parser, GitHub Actions job, PowerShell command or APT installation was executed. The indentation check only measured a transcription of the added text.

The linked NVIDIA forum was unavailable through approved evidence. Package availability, the dependency conflict and the precise APT semantics of priority 1001 remain unverified.
