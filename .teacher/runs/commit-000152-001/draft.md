# 70056fef5f1f841612023027f6abe6f2b295ce57


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/70056fef5f1f841612023027f6abe6f2b295ce57) · [Evidence ledger](draft.json)

Bumps the shared version from 0.0.1 to 0.0.2, affecting package metadata, conversion provenance and release naming without changing runtime algorithms.

- [Propagating the 0.0.2 release identifier](#build-release)

## Problem

The project still declared version 0.0.1; this release-label change advances it to 0.0.2. [source; call_a0ea4888736a4adca223f06261da55c5]

## Reasoning

Changing the shared version constant updates existing consumers without modifying their implementation. [source; call_a0ea4888736a4adca223f06261da55c5, call_626bdd84489c41a69b1203088ae97ad5]

## Impact

The diff changes release identification, not model computation, dependencies or build configuration. [source; call_a0ea4888736a4adca223f06261da55c5]

## Source Notes

The commit describes a v0.0.2 version bump and carries kingbri's sign-off. [source; call_b2e6529feed545509f763ba7d8675e90]

The inspected discussions concern separate installation reports: #6, “No ROCm runtime is found, using ROCM_HOME='/usr',” includes an extension-build assertion; #17, “ModuleNotFoundError: No module named 'torch' when installing requirements.txt,” concerns PyTorch and Flash-Attention installation. Neither supplies evidence that this version-only change fixes those reports. [source; call_68ae6b178e3645598144ad224fc5b96d, call_087f2c087ac14c5ea9368f2046c0c71e, call_a0ea4888736a4adca223f06261da55c5]

<a id="build-release"></a>

## Propagating the 0.0.2 release identifier

setup.py executes version.py into a dictionary and passes its __version__ value to setup(version=...), so the edited constant supplies the package's new base version. [source; call_d63fab4ffe1645b490f5af85ab330163, call_a0ea4888736a4adca223f06261da55c5]

compile_model imports the same constant and writes it into config.json under quantization_config.version. Newly compiled outputs therefore receive 0.0.2 when that writing path completes; existing artifacts are not rewritten by this commit. [source; call_5c8b857fd19b4ee480b9c0bd1591b22e, call_a0ea4888736a4adca223f06261da55c5]

The manual build workflow reads version.py for its package-version output and derives the release tag and name from it. Upload remains conditional on release input '1' and successful version parsing; changing the constant does not itself launch publication. [source; call_36974921cc0b40538089c545de7b0215, call_a0ea4888736a4adca223f06261da55c5]

## Uncertainty and limits

No package build, conversion or release workflow was executed. This string-only change offers no useful numerical computation to validate.

The version increment alone does not establish compatibility guarantees or successful release publication.
