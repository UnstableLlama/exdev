# 4db952592d65b6d40a78132850f80c63eed1bc3d


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/4db952592d65b6d40a78132850f80c63eed1bc3d) · [Evidence ledger](draft.json)

Repairs the YAML indentation of the CUDA apt pin, but introduces a heredoc incompatible with the inherited PowerShell shell; successful dependency resolution remains unverified.

- [Repair the CUDA pin block without changing its shell](#build-release)

## Problem

The parent workflow leaves two lines of the apt preference outside the indented run block. The change repairs that indentation while attempting to address the reported CUDA dependency error. [source; call_816a2ceb8aac4792b0173d384c21c7d0, call_3f1d0005016b41859e3f04cd089c830e]

## Reasoning

The replacement uses a quoted shell heredoc rather than multiline echo, preserving the package, exact version and priority while suppressing tee's stdout. However, the step still inherits PowerShell rather than selecting a shell supporting this heredoc syntax. [source; call_3f1d0005016b41859e3f04cd089c830e, call_816a2ceb8aac4792b0173d384c21c7d0]

## Impact

The pin step remains limited to non-Windows CUDA jobs and precedes the unchanged network CUDA installer. Windows CUDA provisioning and the non-CUDA packaging row do not run this step. [source; call_816a2ceb8aac4792b0173d384c21c7d0, call_3f1d0005016b41859e3f04cd089c830e]

## Source Notes

Read the workflow introduction entry ae04741 and installer-update entry b2c3cab. They establish the inherited PowerShell command environment and the preceding update to cuda-toolkit v0.2.24; neither establishes successful dependency resolution. [ancestor; call_ccb241d755c54b508a306e7d41c26855, call_4dc0d1e4c3e14a39a232d499f2f8fff8]

The supplied PR #3 evidence concerns an absolute-path setup error: its body links issue #2, another contributor reports success, and turboderp acknowledges an oversight. These statements do not verify this workflow's CUDA pinning change. [source; call_0637a1b3d5d6431cb0af5b1dc194609d, call_e96877304bb34cf4bb86beb077c9ff93, call_3a59d31968134de2b62ace9ceb72aecb]

<a id="build-release"></a>

## Repair the CUDA pin block without changing its shell

The preference still names nvidia-persistenced, version 570.148.08-1ubuntu1 and priority 1001. These are package-selection inputs, not CUDA compute capability values. The writer still targets /etc/apt/preferences.d/99-nvidia-persistenced and then invokes apt-get update; this is not a location change. [source; call_3f1d0005016b41859e3f04cd089c830e]

Indenting the preference body and EOF consistently supplies the YAML block structure needed to deliver the whole script to a shell. A bounded Python inspection found the parent's Pin and Pin-Priority lines at column zero and showed the replacement heredoc after stripping ten indentation spaces. [execution; call_1dfc92d6bfb849f4ae6939e80a1e60c8]

The indentation repair and heredoc replacement are coupled: the new delimiter and body must survive YAML block extraction together. This repairs script delivery but does not supply the compatible shell needed by the replacement syntax. [inference; call_3f1d0005016b41859e3f04cd089c830e, call_816a2ceb8aac4792b0173d384c21c7d0]

## Authoring-time findings — pending review

### pin-heredoc-powershell (suspected; defect)

The replacement introduces POSIX heredoc syntax into a step that inherits PowerShell.

Trigger: A non-Windows matrix job with a nonempty CUDA value reaches the pin step.

Expected: Write the three-line apt preference and refresh package metadata before CUDA installation.

Actual: The script contains <<'EOF', but the job default is shell: pwsh and this step has no override. Source inspection indicates a shell syntax failure rather than execution of the intended heredoc.

Locations: 4db952592d65b6d40a78132850f80c63eed1bc3d:.github/workflows/build.yml — jobs.build_wheels

Source evidence: call_3f1d0005016b41859e3f04cd089c830e, call_816a2ceb8aac4792b0173d384c21c7d0

source_inspection: Compared the changed run block with the inherited job shell and matrix guard. Reach is the four Ubuntu CUDA rows, not Windows or the source-distribution row. [call_816a2ceb8aac4792b0173d384c21c7d0, call_3f1d0005016b41859e3f04cd089c830e]. Limits: PowerShell parsing and Actions execution were not run.

## Uncertainty and limits

No Actions job, YAML parser, PowerShell interpreter, apt transaction or CUDA installation was executed.

The exact package version's availability and apt priority 1001's resolver behavior were not established by eligible documentation or execution.

The bounded Python check inspected indentation and transcribed block stripping; it did not validate shell execution.
