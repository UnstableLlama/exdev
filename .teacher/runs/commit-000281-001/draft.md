# 72ef28eb25ab84bab27745eb6191c53e1f343529


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/72ef28eb25ab84bab27745eb6191c53e1f343529) · [Evidence ledger](draft.json)

Adds exact-version libnvidia-cfg1 installation and hold before Linux CUDA setup, extending the existing nvidia-persistenced workaround without establishing build success.

- [Extend the CUDA package workaround to libnvidia-cfg1](#build-release)

## Problem

The workflow identifies an ongoing CUDA dependency issue. This attempt extends its existing exact-version installation workaround to libnvidia-cfg1. [source; call_b2c53f8ef3fb461a94479bf50e1da7c2, call_6b519379ebe24537b05faa5976df9d75]

## Reasoning

Requesting the same package release for libnvidia-cfg1 and nvidia-persistenced appears intended to constrain package resolution before CUDA setup; the available source does not establish the underlying dependency conflict. [inference; call_6b519379ebe24537b05faa5976df9d75, call_b2c53f8ef3fb461a94479bf50e1da7c2]

## Impact

Only the guarded Linux CUDA provisioning step changes. Windows provisioning and the CUDA-empty source-distribution path retain their previous commands. [source; call_6b519379ebe24537b05faa5976df9d75, call_b2c53f8ef3fb461a94479bf50e1da7c2]

## Source Notes

Read the earlier workaround entry, which records restoring exact-version nvidia-persistenced installation and hold. It provides historical context, not proof of successful package resolution. [ancestor; call_d346166d6d264cda848ef6f622098b3f]

Whole-parent searches found no libnvidia occurrences. NVIDIA matches include workflow provisioning, calibration text and CUDA documentation references; none establishes a Python import name for this system package. Dynamic loading and external use are not ruled out. [source; call_a3272b33be1e4655b1f68d6a01c9e2c3, call_b2c53f8ef3fb461a94479bf50e1da7c2, call_6b519379ebe24537b05faa5976df9d75]

Supplied issue #8 reports an invalid tensor reshape during model quantization. Its discussion attributes that problem to missing padding and reports subsequent success. Those reports do not verify this APT workaround. [source; call_1afe2c75e1a943589b3959aaaeed1c1b, call_eda1334edaea4add8c68f1e75eaaf78d, call_e98185258d2a41b78543e639621ce9f0, call_6448608eeb8349fdae7d0fe89f123042, call_e8d6227b6aae451cb454c63da42a6f1f, call_3834b71f375a4cb5912480e0147b637e, call_451143f696d34ed4a6204e75957de47e]

<a id="build-release"></a>

## Extend the CUDA package workaround to libnvidia-cfg1

After installing and holding nvidia-persistenced, the step now requests libnvidia-cfg1=575.57.08-0ubuntu1 using apt-get install -y --allow-downgrades, then requests apt-mark hold libnvidia-cfg1. The numeric string selects a package release, not a CUDA toolkit version. No APT preference file is added. [source; call_6b519379ebe24537b05faa5976df9d75]

The new commands reuse the existing step's non-Windows/nonempty-CUDA guard and inherited pwsh shell. They follow APT repository setup and index refresh, and precede Jimver/cuda-toolkit@v0.2.25 with matrix.cuda, network installation and --toolkit. The task changes neither that action nor its inputs. [source; call_b2c53f8ef3fb461a94479bf50e1da7c2, call_6b519379ebe24537b05faa5976df9d75]

A bounded Python inspection counted nine parent matrix rows, including four Ubuntu CUDA rows covering Python 3.10–3.13. These rows request CUDA 12.8.1. [execution; call_3c698d51e70444739246b8fd8dfb0f39]

The installation and hold are coupled: installation requests the exact release first, while the following hold seeks to retain the installed package selection. This extends the existing constrained-package strategy rather than changing toolkit selection, trading flexibility for a more specific provisioning environment. [inference; call_6b519379ebe24537b05faa5976df9d75, call_b2c53f8ef3fb461a94479bf50e1da7c2]

## Uncertainty and limits

No APT transaction, PowerShell script, GitHub Actions job or wheel build was executed; package availability and successful dependency resolution remain unverified.

The external CUDA action and linked NVIDIA forum explanation were not inspected.

The Python check counted matrix declarations; it did not execute workflow conditions or provisioning.
