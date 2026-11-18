# b2c3cabdbbce0413a1d9297380323f2ebc2a3b6e


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/b2c3cabdbbce0413a1d9297380323f2ebc2a3b6e) · [Evidence ledger](draft.json)

Removes unused explicit sentencepiece installation from build jobs and updates the Linux CUDA toolkit action to v0.2.24, without establishing that builds now succeed.

- [Trim build dependencies and update the Linux CUDA installer](#build-release)

## Problem

The workflow explicitly installed sentencepiece in both build branches and selected cuda-toolkit v0.2.23 for Linux. The change removes those installs and updates the action to v0.2.24; the reported CUDA fix remains an attempt, not a demonstrated result. [source; call_3bc4e2a32fcb4ca1aa583c0fcb3bcbd8]

## Reasoning

Removing sentencepiece is consistent with the inspected tokenizer using tokenizers.HFTokenizer and setup.py not declaring sentencepiece. Whole-parent searches found no sentencepiece imports: remaining textual occurrences are calibration-data examples, not active dependency declarations. [source; call_3827ffb4e83b4ad494ac17a7ce1a7b8c, call_808dee99ceba49b2a6ffe541469c573c, call_fde708b725474abfb0d02a3450d805e3, call_87214cfd9e324d2c9cf5681420a3ce97, call_adcec11cb3e94e93a0f92a94e1d3cb6d]

## Impact

The dependency removal affects CUDA builds on both operating systems and the non-CUDA packaging branch. The action update affects only non-Windows CUDA jobs; Windows retains its manually assembled toolkit. Neither CUDA versions nor action inputs change. [source; call_3bc4e2a32fcb4ca1aa583c0fcb3bcbd8, call_e0759afac448458ba0a3570f30454f6d]

## Source Notes

Read ancestor entries ae04741 and 1022264. They describe the introduction and integration of this manual build workflow, including its non-isolated builds and optional publication; neither records a defect directly repaired here. [ancestor; call_b60666da5c844c71aa10fa554d98124f, call_58d43e09df4c49d8acb29f21255ae6e8]

Issue #21, “Build Failure on Windows: CUDA 12.4 / PyTorch 2.7.0+cu126 / VS 2022,” closed without a solution. Its relationship here is only inferred from shared build-toolchain context: this task updates the Linux installer, not the reported Windows compilation path. Issue #49, “running the QTIP inference code,” discusses installing QTIP and fast-hadamard-transform, not this workflow's CUDA action. [inference; call_8ee326869c0d4308bfccbbdc02ced3af, call_f04e34f4da444907b186e55539e40115, call_3bc4e2a32fcb4ca1aa583c0fcb3bcbd8]

<a id="build-release"></a>

## Trim build dependencies and update the Linux CUDA installer

Linux CUDA installation retains the matrix-provided toolkit version, network method and linux-local-args=['--toolkit']; only the action release changes. The installer remains guarded by runner.os != 'Windows' and a nonempty CUDA value. [source; call_e0759afac448458ba0a3570f30454f6d, call_3bc4e2a32fcb4ca1aa583c0fcb3bcbd8]

Both build branches still install Torch first, then build tooling, safetensors, tokenizers and numpy, with setuptools pinned to 69.5.1. Removing sentencepiece changes environment preparation rather than tokenizer implementation or package metadata. The subsequent python -m build -n commands retain their explicitly prepared environments. [source; call_e0759afac448458ba0a3570f30454f6d, call_3bc4e2a32fcb4ca1aa583c0fcb3bcbd8, call_87214cfd9e324d2c9cf5681420a3ce97]

A bounded standard-library check counted nine matrix rows, eight specifying CUDA 12.8.1, and modeled the existing transformation of that version to the PyTorch index suffix 128. The task does not alter those selections. [execution; call_adcec11cb3e94e93a0f92a94e1d3cb6d]

The two edits address separate preparation stages: Python dependency installation across both branches and toolkit provisioning on Linux CUDA jobs. Source inspection shows neither edit supplies a new precondition required by the other. [inference; call_e0759afac448458ba0a3570f30454f6d, call_3bc4e2a32fcb4ca1aa583c0fcb3bcbd8]

## Uncertainty and limits

No Actions job, package installation, PowerShell command or native build was executed. The behavior change inside cuda-toolkit v0.2.24 and whether it resolves the reported dependency problem are unestablished.

Literal dependency searches do not exclude dynamic imports or external consumers.

The Python check counted workflow rows and transcribed CUDA string processing; it did not execute the workflow or validate binary compatibility.
