# 002bd31f288c3bf38786ed2ab8da5d49ce064e08


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/002bd31f288c3bf38786ed2ab8da5d49ce064e08) · [Evidence ledger](draft.json)

Restores the full nine-configuration build matrix and Linux network CUDA installation, while documenting unresolved installer tradeoffs; build success remains unverified.

- [Restore release configurations and network CUDA installation](#build-release)

## Problem

The added comments report two competing provisioning problems: NVIDIA driver dependencies break network installation, while local installation produces identically named log artifacts across jobs. These are author-reported constraints, not demonstrated failures. [source; call_0120ae679a7a44fc966fc06d997e0f9b]

## Reasoning

Restoring the full build matrix together with network installation appears to favor multi-job release preparation over the reported local-install artifact collision. The comments still describe network installation as broken, so this is not evidence that dependency resolution was repaired. [inference; call_0120ae679a7a44fc966fc06d997e0f9b]

## Impact

The change restores five disabled configurations and switches Linux CUDA provisioning from local to network without changing the requested toolkit or installer-action version. [source; call_0120ae679a7a44fc966fc06d997e0f9b]

## Source Notes

Read the workflow-introduction entry and the earlier local-install attempt. They establish the inherited release orchestration and the previous provisioning experiment; neither establishes successful installation. [ancestor; call_23932f9fd02e487b8e3f9d33667f7396, call_3751c4d4c4db4735a3d18dbcb06278b3]

<a id="build-release"></a>

## Restore release configurations and network CUDA installation

The re-enabled rows are Ubuntu/Python 3.10, Windows/Python 3.10–3.12, and the CUDA-empty Ubuntu/Python 3.11 packaging configuration. Existing Python 3.13 rows continue to request 3.13.3. [source; call_0120ae679a7a44fc966fc06d997e0f9b, call_05927082055742199e2fffc9ba5c4d9b]

A bounded Python inspection counted four active parent configurations versus nine after reconstructing the five uncommented rows: eight CUDA configurations, including four Linux configurations, and one CUDA-empty configuration. [execution; call_f5b270170ae947439a6e556e532a15a6]

Jimver/cuda-toolkit remains pinned to v0.2.24 and receives matrix.cuda plus linux-local-args='["--toolkit"]'. The active method becomes network; local remains as a commented alternative. The non-Windows/nonempty-CUDA guard still excludes Windows and the packaging row. [source; call_0120ae679a7a44fc966fc06d997e0f9b, call_05927082055742199e2fffc9ba5c4d9b]

CUDA configurations retain toolkit 12.8.1 and Torch 2.7.0. Downstream commands derive the Torch CUDA index from matrix.cuda, set TORCH_CUDA_ARCH_LIST from the matrix, and invoke a non-isolated wheel build. The architecture list remains compilation-target input rather than evidence of tested GPU compatibility. [source; call_05927082055742199e2fffc9ba5c4d9b, call_0120ae679a7a44fc966fc06d997e0f9b]

The restored CUDA-empty row takes the existing packaging path: install CPU Torch, set EXLLAMA_NOCOMPILE=1, then run python -m build -n. Publication remains conditional on a parsed version and release input '1', and selects only ./dist/*.whl; restoring this row does not add source-archive publication. [source; call_05927082055742199e2fffc9ba5c4d9b, call_0120ae679a7a44fc966fc06d997e0f9b]

## Uncertainty and limits

No GitHub Actions job, installer, package build or release upload ran. Successful dependency resolution and avoidance of artifact collisions remain unverified.

The external Jimver action implementation was unavailable for inspection. Its network/local prerequisites, artifact handling and interpretation of linux-local-args remain unestablished; the NVIDIA forum URL in the comment could not be retrieved from approved evidence.

The Python check counted matrix declarations and reconstructed the uncommented rows; it did not execute GitHub Actions expressions.
