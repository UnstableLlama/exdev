# 94ef28757e6390261e9a453ad80d11a697d72362


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/94ef28757e6390261e9a453ad80d11a697d72362) · [Evidence ledger](draft.json)

Adds Ko-fi funding metadata and ignores common Python development and build artifacts, including the editable-install native extension.

- [Funding metadata and generated-file exclusions](#repository-configuration)

## Problem

The change adds repository-level configuration for funding and generated-file exclusions. [source; call_22415e5a200c44ab90add9e46fbfd484, call_7124109b183e43e9b61b11e038f2d6c7]

## Reasoning

The ignore list targets packaging outputs, Python caches, local development files and a specifically named compiled extension rather than broadly excluding every shared library. [source; call_7124109b183e43e9b61b11e038f2d6c7]

## Impact

This is repository housekeeping; neither changed file modifies model execution or quantization code. [source; call_22415e5a200c44ab90add9e46fbfd484, call_7124109b183e43e9b61b11e038f2d6c7]

<a id="repository-configuration"></a>

## Funding metadata and generated-file exclusions

The new .github/FUNDING.yml sets ko_fi to turboderp, supplying a funding destination without adding application logic. [source; call_22415e5a200c44ab90add9e46fbfd484]

The new .gitignore lists *.egg-info/, build/, *.pyc, __pycache__/, .idea, venv and dist. It also excludes exllamav3_ext.cpython-*.so, explicitly identified by a comment as produced by pip install -e . [source; call_7124109b183e43e9b61b11e038f2d6c7]

The extension-specific pattern balances excluding local build artifacts against retaining unrelated shared libraries; its wildcard accommodates different CPython suffixes while keeping the extension name fixed. [inference; call_7124109b183e43e9b61b11e038f2d6c7]

## Uncertainty and limits

Git ignore behavior and GitHub funding presentation were not exercised. These declarative settings offer no useful numerical computation to validate.
