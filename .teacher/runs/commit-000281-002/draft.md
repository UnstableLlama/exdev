# 72ef28eb25ab84bab27745eb6191c53e1f343529


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/72ef28eb25ab84bab27745eb6191c53e1f343529) · [Evidence ledger](draft.json)

Adds an exact-version libnvidia-cfg1 installation and hold to the Linux CUDA provisioning workaround; build success remains unverified.

- [Extend the CUDA package workaround to libnvidia-cfg1](#build-release)

## Problem

Attempt #8 extends the existing CUDA provisioning workaround to request and hold libnvidia-cfg1 alongside nvidia-persistenced; the diff does not establish that dependency resolution succeeds. [source; call_f5d665f07489441cabb3798849691e2a]

## Reasoning

The apparent strategy is to establish matching installed package versions before CUDA setup, rather than write an APT preference. This trades unconstrained package selection for an exact-version installation request followed by a hold. [inference; call_f5d665f07489441cabb3798849691e2a, call_b490bf15536143b5890a721916d51e5f]

## Impact

The unchanged guard selects the four Ubuntu CUDA rows, covering Python 3.10–3.13. Windows and the CUDA-empty source-distribution row skip the added commands. [source; call_b490bf15536143b5890a721916d51e5f, call_f5d665f07489441cabb3798849691e2a]

## Source Notes

Read the repository-setup entry and the earlier direct-package-workaround entry. They describe the inherited provisioning sequence and the removal of a PowerShell-incompatible heredoc. [ancestor; call_bb52b839da0b4633bba1d22e040c9ad2, call_11053486107343c6af573107d91d1d30]

That heredoc remains absent. The task retains ordinary package-management commands in the step inheriting pwsh; the preceding repository-registration script separately selects Bash. [source; call_b490bf15536143b5890a721916d51e5f, call_f5d665f07489441cabb3798849691e2a]

Whole-parent searches found no libnvidia or cfg1 references. NVIDIA matches include workflow provisioning, calibration text and native-code documentation links, but no explicit import of this package. This is an OS-package request, not a newly declared Python dependency; dynamic or external library use is not excluded. [source; call_079ca81cf74748d0868ceba0d3b7bff6, call_f96e1be0f7e542f0b0b66f617f2ce446, call_a09833d4bcd0462f9b26c783832081c7]

The supplied issue #8, “RuntimeError: shape '[5120, -1, 128]' is invalid for input of size 776524800,” concerns quantization padding. Turboderp reports adding padding, and both reporters subsequently report success. Its shared number with “Attempt #8” is not evidence that the package workaround fixes that error. [inference; call_f3df7e2fae804bc2a362f1cf9075af61, call_0fcb223b4c6845f990ba994cac9389fc, call_f4dc4a88e47946bdae1f3dfd9880d8e3, call_ba9f794aa6b74c728cf98ea7c2ead564, call_67be9b685291439c97ba95baa400d9f5, call_bdba09fc498d41248dd70574eeb5ee2b, call_7217302bbeb74c6ca2ab39699d9cc1f2, call_f5d665f07489441cabb3798849691e2a]

<a id="build-release"></a>

## Extend the CUDA package workaround to libnvidia-cfg1

After installing and holding nvidia-persistenced, the step now requests libnvidia-cfg1=575.57.08-0ubuntu1 using -y and --allow-downgrades, then requests apt-mark hold libnvidia-cfg1. The numeric string identifies the requested package release, not CUDA 12.8.1. [source; call_f5d665f07489441cabb3798849691e2a, call_b490bf15536143b5890a721916d51e5f]

Whole-parent apt-get search locates only the preceding repository refresh and the existing update/install workaround. The new installation follows that existing call's guard, refreshed indexes and argument pattern, with no new shell override or error-handling construct. [source; call_86b8afebf7934e6bab135be143d76ccd, call_b490bf15536143b5890a721916d51e5f, call_f5d665f07489441cabb3798849691e2a]

The inherited NVIDIA repository registration supplies package-source setup before these exact-version requests. The subsequent Jimver/cuda-toolkit@v0.2.24 action remains configured for network installation, matrix.cuda and --toolkit; this commit changes neither toolkit selection nor build commands. [source; call_b490bf15536143b5890a721916d51e5f, call_f5d665f07489441cabb3798849691e2a]

## Uncertainty and limits

No APT transaction, PowerShell script, CUDA installation or Actions job was executed. Exact package availability, dependency compatibility and successful installation/hold behavior remain unverified.

The external CUDA action implementation and package dependency metadata were not inspected; the necessity of matching these two versions is unestablished.

No useful scalar computation can validate this package-manager workaround; command ordering is source evidence, not a measured provisioning result.
