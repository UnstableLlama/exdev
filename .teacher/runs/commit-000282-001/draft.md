# 7ba1d4989ba7eb9d0eabf3cfa4d93beaa7ed271e


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/7ba1d4989ba7eb9d0eabf3cfa4d93beaa7ed271e) · [Evidence ledger](draft.json)

Removes the explicit libnvidia-cfg1 versioned installation while retaining its hold before Linux CUDA setup; dependency resolution and build success remain unverified.

- [Retain the libnvidia-cfg1 hold without an explicit installation](#build-release)

## Problem

The CUDA provisioning workaround explicitly installed libnvidia-cfg1 at 575.57.08-0ubuntu1 before holding it. This attempt removes that installation request while retaining the hold. [source; call_966fd1d33988472ca46966f6936c6ba3]

## Reasoning

The edit trades explicit version selection for reliance on the runner's package state and preceding dependency resolution. Calling this “pinning without installing” describes the apparent strategy, not proof that the desired package version is present. [inference; call_966fd1d33988472ca46966f6936c6ba3, call_569b188281fc4602bf5ace0de67ae05d]

## Impact

The changed step remains restricted to non-Windows rows with a nonempty CUDA value. Windows provisioning and the CUDA-empty source-distribution row do not execute it. [source; call_569b188281fc4602bf5ace0de67ae05d, call_966fd1d33988472ca46966f6936c6ba3]

## Source Notes

Read the workflow-introduction and NVIDIA-repository-setup ancestor entries. They establish the inherited build orchestration and repository prerequisite; neither establishes successful dependency resolution. [ancestor; call_4de31dd074cf435897af17b76afb73a7, call_221aa67e4f29448f8230996182227668]

The supplied issue #9 discussion concerns reusing quantization measurements. Nrgte asks about reuse, turboderp says jobs cannot reuse that work, and the remaining replies acknowledge the exchange. It supplies no evidence for this APT change. [source; call_03f4c2a007d9443a9021746862ff0c17, call_4ebdc309bfb041dbb2602ed678d31f50, call_ad33529d03284c91a3b78f9d1838762e, call_f27973c5d022433b9d8a06913f237fbb]

<a id="build-release"></a>

## Retain the libnvidia-cfg1 hold without an explicit installation

The sole deletion removes apt-get install -y --allow-downgrades libnvidia-cfg1=575.57.08-0ubuntu1. That command explicitly requested a package release and permitted downgrading; no replacement command guarantees that release. The remaining apt-mark command names only libnvidia-cfg1. [source; call_966fd1d33988472ca46966f6936c6ba3]

The surrounding sequence still refreshes APT metadata, requests nvidia-persistenced=575.57.08-0ubuntu1 with downgrades allowed, holds nvidia-persistenced, then holds libnvidia-cfg1. Consequently, this is not a removal of all package installation: the earlier persistenced transaction remains consequential. [source; call_569b188281fc4602bf5ace0de67ae05d, call_966fd1d33988472ca46966f6936c6ba3]

NVIDIA repository setup still precedes the workaround, and Jimver/cuda-toolkit@v0.2.24 follows it with matrix.cuda, network installation and --toolkit. The package release 575.57.08-0ubuntu1 is distinct from the matrix's CUDA toolkit version 12.8.1. [source; call_569b188281fc4602bf5ace0de67ae05d, call_966fd1d33988472ca46966f6936c6ba3]

Whole-parent searches locate libnvidia references and both apt-mark calls only in this workflow. The existing comparison is the immediately preceding persistenced hold, which retains its explicit installation; the cfg1 hold loses that preparation. This establishes a source-level difference, not that either hold succeeds or fails. [source; call_6a254133f0e247c3974edef946620e89, call_565f19f4d7534e60b3189c413658ccee, call_966fd1d33988472ca46966f6936c6ba3]

## Uncertainty and limits

No APT transaction, PowerShell step, CUDA installation or GitHub Actions build was executed. Package availability, transitive installation and the retained hold's behavior on the runner remain unverified.

The inspected workflow no longer explicitly selects a libnvidia-cfg1 version; the resulting installed version cannot be established from this source.

A scalar computation would not meaningfully validate this package-manager state transition; no numerical emulation was substituted for provisioning execution.
