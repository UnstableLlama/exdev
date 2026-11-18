# 74812031c539234543e33817d32d332fc76f252c


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/74812031c539234543e33817d32d332fc76f252c) · [Evidence ledger](draft.json)

Disables five build configurations, pins remaining Python 3.13 builds to 3.13.3, and removes inactive CUDA workaround comments; build success remains unverified.

- [Narrow retry builds and pin Python 3.13.3](#build-release)

## Problem

The author reports partial success with local CUDA installation, a log-artifact obstacle to multiple builds, and Python 3.13.4 issues. The diff narrows the build matrix and requests Python 3.13.3; it does not repair artifact handling. [source; call_8e3c723616da4847936cf1834feaed6f, call_ab1829d7da974e0591c16c08201b52f1]

## Reasoning

Commenting out selected configurations is a retry-oriented workaround rather than a general build-system repair. The Python pin and matrix reduction affect different selections; neither supplies a source-visible precondition for the other. [inference; call_8e3c723616da4847936cf1834feaed6f]

## Impact

The remaining configurations are Ubuntu Python 3.11, 3.12 and 3.13.3, plus Windows Python 3.13.3. No active non-CUDA packaging row remains. [source; call_8e3c723616da4847936cf1834feaed6f, call_ab1829d7da974e0591c16c08201b52f1]

## Source Notes

Read ancestor entries ae04741 and b2c3cab. They establish the workflow's introduction, non-isolated build preparation and Linux installer history; neither records a defect directly repaired by this change. [ancestor; call_8026c8c6b7244e64b7a17a6bba3d87c6, call_1f520346bdde429fb9361f5ada7761a6]

The supplied PR #13 evidence concerns conversion without a BOS token: oobabooga reports the failure, async0x42 reports another affected model, and turboderp thanks the contributor. It does not substantiate this workflow change's reported build success. [source; call_3ade2fe8359b4824932ed15178a06938, call_d1bf671d55be4943b8146b59ac9381fa, call_c181a66a436a4b1682019e87770cd725]

Closed issue #43, “Error converting abliterated Qwen3 mlabonne/Qwen3-30B-A3B-abliterated,” concerns invalid conversion states. Closed issue #16, “RuntimeError: CUDA error: invalid configuration argument,” ultimately discusses tokenizer truncation. Neither discussion establishes a connection to the matrix reduction or Python patch-version pin. [source; call_374d0d3eed71458ea33dc27a2e87bd3a, call_21409c8aaf2748b881c23adf92ffbd84, call_e49e82f6e26a4deb9a30f03114d43d7b, call_8e3c723616da4847936cf1834feaed6f]

<a id="build-release"></a>

## Narrow retry builds and pin Python 3.13.3

Five rows become comments: Ubuntu Python 3.10, Windows Python 3.10–3.12, and the Ubuntu non-CUDA sdist row. The build steps themselves remain present, but the sdist branch has no remaining matrix configuration satisfying its empty-CUDA condition. [source; call_8e3c723616da4847936cf1834feaed6f, call_ab1829d7da974e0591c16c08201b52f1]

Both Python 3.13 rows change to 3.13.3. In this workflow matrix.pyver feeds the job display name and setup-uv's python-version input, so the edit requests a specific interpreter patch release rather than changing CUDA or Torch. Whole-parent search also finds matrix.pyver in calibration text, not another active workflow consumer. [source; call_8e3c723616da4847936cf1834feaed6f, call_ab1829d7da974e0591c16c08201b52f1, call_cbd7aaa903ea4ea6b23ec28efbb29d96]

All remaining rows retain CUDA 12.8.1, Torch 2.7.0 and the existing compilation-target list. Linux still selects cuda-toolkit v0.2.24 with method local and --toolkit; Windows retains its separately assembled toolkit. This commit does not introduce local installation. [source; call_ab1829d7da974e0591c16c08201b52f1, call_8e3c723616da4847936cf1834feaed6f]

Deleting the NVIDIA repository and exact-version package workaround removes already-commented text, not an active guard or installation step. The parent already performed local Linux toolkit installation without that workaround. [source; call_ab1829d7da974e0591c16c08201b52f1, call_8e3c723616da4847936cf1834feaed6f]

A bounded standard-library transcription counted nine parent matrix rows, five disabled rows and four remaining rows, reproducing the surviving OS/Python combinations. Four rows still remain, so this is not a conversion to one configuration per run. [execution; call_8d1845f4b92e4d8284da2979f096ae7b]

Release publication remains conditional on release='1' and a parsed package version, selecting ./dist/*.whl. Whole-parent artifact search finds an upload-artifact example in calibration data but no explicit upload-artifact step in this workflow; the reported log-artifact problem cannot be localized to inspected workflow code. [source; call_ab1829d7da974e0591c16c08201b52f1, call_9a41f62cdf3f4061a2a2af0e3e0d7748, call_8e3c723616da4847936cf1834feaed6f]

## Uncertainty and limits

No GitHub Actions job, interpreter installation, CUDA provisioning or wheel build was executed. Successful completed wheels and the reported Python 3.13.4 problem remain unverified.

The inspected workflow has no explicit log-artifact upload. External action internals and any artifact-name collision are unestablished.

The Python computation models matrix edits using text processing; it does not execute YAML, PowerShell or GitHub Actions.
