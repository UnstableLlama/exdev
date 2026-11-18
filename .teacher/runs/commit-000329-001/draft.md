# 5cada8cd004b876b7f7f5fae21fc32aaa8d2f240


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/5cada8cd004b876b7f7f5fae21fc32aaa8d2f240) · [Evidence ledger](draft.json)

Adds nine Torch 2.8.0 configurations to the manual release workflow alongside the nine Torch 2.7.0 configurations. The patch expands build coverage without changing runtime code or dependency minimums; successful builds and release uploads are unverified.

- [Build release packages against Torch 2.8 alongside 2.7](#build-release)

## Problem

kingbri’s commit message says “Actions: Add Torch 2.8 support.” The parent release workflow requests Torch 2.7.0 in every row; the patch adds 2.8.0 as a second build target rather than replacing 2.7.0 or changing the library’s minimum version. [source; call_5a3909ae40d44d0181e673aa5e3efa98, call_2248d300bea74af28b6f59808205165e, call_f912dffe8e034b6daba2a607f71c8908, call_c112220d064845c092d1f806aa007891, call_5878117feee24cc18a1f70e69a78ee0a]

## Reasoning

The existing workflow already uses matrix.torch in the job name, both Torch install commands, and the CUDA wheel build tag. Adding rows is therefore enough to request the new dependency version and distinguish the CUDA builds without duplicating build steps. Retaining the old rows preserves the 2.7.0 build targets at the cost of doubling the matrix. [inference; call_97fa7decea62458fbedb66c43a79b9be, call_2248d300bea74af28b6f59808205165e, call_f912dffe8e034b6daba2a607f71c8908]

## Impact

A standard-library Python check read the parent matrix rows and modeled the one-for-one additions shown in the diff. It counted 9 → 18 rows: 4 → 8 Ubuntu CUDA wheel rows, 4 → 8 Windows CUDA wheel rows, and 1 → 2 Ubuntu non-CUDA packaging rows. Transcribing the CUDA string transformation produced the same cu128 index for both Torch versions and distinct +cu128-torch2.7.0 and +cu128-torch2.8.0 build-tag inputs. [execution; call_98600e5a448548daaf3edd88e65a21f2, call_2248d300bea74af28b6f59808205165e, call_f912dffe8e034b6daba2a607f71c8908]

## Source Notes

The workflow-introduction entry (ae04741) explains the original manual dispatch, the split between CUDA precompilation and non-precompiled packaging, and the opt-in release guard. Entries 7481203 and 002bd31 describe the Python 3.13.3 pin and the reported tradeoff between Linux network-install dependency failures and local-install log-name collisions. [ancestor; call_53065d89ef7e4fbda111d10ca9c0da3d, call_bde05cc394794a938d0538300dd0a078, call_33bd4f0d7c074808b2ea02141b297fba]

The inherited Linux CUDA step still selects Jimver/cuda-toolkit v0.2.24 with method: network for non-Windows, nonempty-CUDA rows. The new Ubuntu CUDA rows meet that guard and inherit the same provisioning prerequisite; the diff neither fixes the driver dependency problem reported in the comment nor activates the commented local alternative. [source; call_2248d300bea74af28b6f59808205165e, call_f912dffe8e034b6daba2a607f71c8908]

The whole-parent literal search found no 2.8.0 match. Other 2.8 matches include CUDA 12.8 references and unrelated evaluation values; the README already discusses selecting PyTorch for installation, but the patch does not edit those instructions. [source; call_9e3e35bd3f284775a16b9091bdcc7554, call_d99ddf0c989b46e29ed6a8e2d7fb904f, call_bb74bb99750847c8a69a4f95cbcb825f, call_f912dffe8e034b6daba2a607f71c8908]

Closed issue #17, “ModuleNotFoundError: No module named 'torch' when installing requirements.txt,” is relevant as installation context: the report concerns FlashAttention and choosing CPU versus CUDA Torch, while the workflow explicitly selects a Torch index before packaging. The issue’s suggested CUDA 12.4 install and Windows FlashAttention wheel are not evidence that these Torch 2.8.0 builds work. [inference; call_0ff4ef8f5d0448a790231ddba1fd7562, call_2248d300bea74af28b6f59808205165e]

Closed issue #57, “Batch process interrupted,” shares Windows and CUDA 12.8 with the wheel rows, but reports a translation example crashing during job creation and discusses virtual-memory use and bounded queueing. That is a runtime report, not a report about building these wheels. [inference; call_10d9f2b7c5b342c6b1b731c28b78292c, call_7bbabf1a589a467d94d07ec0c842c7cb, call_f912dffe8e034b6daba2a607f71c8908]

Issue #49, “running the QTIP inference code,” also discusses installing Torch and Ninja before building native code, but the instructions are for QTIP and fast-hadamard-transform, neither of which the edited workflow builds. Issue #34, “torch._C._LinAlgError on last layer of quant,” and issue #64, “Can not capture graph with torch.compile (dynamo),” concern a Cholesky failure during conversion and tracing a native GEMM binding, respectively. Their overlap with this change is the Torch dependency, not the packaging path that changed. [inference; call_d0ddebbab86747e59fdacbd238536fa8, call_c9ae861bd9ce400eb51937b86c6bd9ec, call_1af26bd27db4486e88b83299ce8de978, call_2248d300bea74af28b6f59808205165e, call_f912dffe8e034b6daba2a607f71c8908]

<a id="build-release"></a>

## Build release packages against Torch 2.8 alongside 2.7

The eight added CUDA rows cover ubuntu-22.04 and windows-2022, each with Python 3.10, 3.11, 3.12 and 3.13.3. They keep CUDA 12.8.1, empty ROCm fields, and the existing TORCH_CUDA_ARCH_LIST value `8.0 8.6 8.9 9.0 10.0 12.0+PTX`. These values are compilation targets, not hardware test results. [source; call_f912dffe8e034b6daba2a607f71c8908, call_2248d300bea74af28b6f59808205165e]

The wheel path installs the exact matrix Torch version from PyTorch’s CUDA index, then runs a non-isolated wheel build. The index suffix comes from stripping the final component and dots from 12.8.1; the separate build-tag argument uses both that suffix and the matrix Torch version. setup.py registers the CUDA extension when Torch is present and EXLLAMA_NOCOMPILE is unset. [source; call_2248d300bea74af28b6f59808205165e, call_c112220d064845c092d1f806aa007891, call_f912dffe8e034b6daba2a607f71c8908]

The ninth addition is Ubuntu/Python 3.11 with empty CUDA and ROCm fields. Those fields, not the sdist label, select the packaging branch: it installs CPU Torch 2.8.0, sets EXLLAMA_NOCOMPILE=1 to suppress extension registration, and runs python -m build -n. That exercises packaging with CPU Torch present, not CPU inference. The release step still requires release='1' and a parsed package version, and only selects ./dist/*.whl. [source; call_f912dffe8e034b6daba2a607f71c8908, call_2248d300bea74af28b6f59808205165e, call_c112220d064845c092d1f806aa007891, call_e27e5a00bde144dd91a7d28f0f02e4f6]

## Authoring-time findings — pending review

### non-cuda-release-asset-name-collision (suspected; defect)

The new non-CUDA row can contend with the existing non-CUDA row for a release asset name. Unlike the CUDA wheel command, the non-CUDA command passes no Torch-specific build tag, and the upload step allows overwrite.

Trigger: Dispatch with release='1' and a parseable package version, with both Ubuntu/Python 3.11 non-CUDA builds producing a wheel under the same filename.

Expected: If the non-CUDA jobs publish separate outputs, those outputs should have distinct asset names; if they are duplicate builds of one package, only one job needs to publish it.

Actual: Both jobs select ./dist/*.whl and target the same versioned release with overwrite enabled. The workflow supplies no per-Torch discriminator or single-publisher guard on this path. No collision is implied if neither job emits a wheel or publication is disabled.

Locations: 5cada8cd004b876b7f7f5fae21fc32aaa8d2f240:.github/workflows/build.yml — jobs.build_wheels.strategy.matrix.include, 1c8378a5c1a48eb76bf2a2000406d61479d4b65d:.github/workflows/build.yml — jobs.build_wheels.steps: Build sdist; Upload files to GitHub release

Source evidence: call_f912dffe8e034b6daba2a607f71c8908, call_2248d300bea74af28b6f59808205165e, call_c112220d064845c092d1f806aa007891

source_inspection: Compared both non-CUDA rows with the build and upload steps. A whole-parent search for matrix.torch found Torch-dependent naming only in the job display name and the CUDA build tag, not in the non-CUDA build or upload naming. [call_f912dffe8e034b6daba2a607f71c8908, call_2248d300bea74af28b6f59808205165e, call_97fa7decea62458fbedb66c43a79b9be]. Limits: Conditional on the backend emitting same-named wheels. Neither wheel generation nor concurrent upload behavior was tested.

## Uncertainty and limits

The Python check counted rows and reproduced string transformations; it did not execute GitHub Actions, PowerShell, the installer, the packaging backend, or the release uploader.

Torch wheel availability for each runner and interpreter, successful native compilation and import, final asset names, and runtime or cross-version compatibility are unverified.

The non-CUDA build invokes python -m build -n without an explicit distribution selector. Its exact output set and how the release action handles concurrent uploads with the same asset name were not established.
