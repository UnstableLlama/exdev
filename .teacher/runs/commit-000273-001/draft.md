# 91257162616e3117ad45f848b10c274a93eed713


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/91257162616e3117ad45f848b10c274a93eed713) · [Evidence ledger](draft.json)

Bumps the shared version from 0.0.3 to 0.0.4, updating package metadata, conversion provenance and conditional release naming.

- [Propagating the 0.0.4 release identifier](#build-release)

## Problem

The shared release identifier was 0.0.3; the change advances it to 0.0.4. [source; call_f57197456dac44ce83c7c023ef040e1e]

## Reasoning

Changing the shared constant updates existing metadata consumers without duplicating version edits or changing their implementations. [source; call_6ce2c065113d49ebb7ad5888b108a6dd, call_1fa789ef968b46ff9294e867bc24279a, call_d9ab5ca0901841858e6c21c9f9a694af, call_e5a44ec7de054f6a9f6a40f65c2ba643]

## Impact

The sole edit changes release identification, not inference algorithms, dependencies or build settings. [source; call_f57197456dac44ce83c7c023ef040e1e]

## Source Notes

The earlier 0.0.3 bump entry was read. It establishes the same shared-constant mechanism and conditional publication boundary. [ancestor; call_7c860be7d37c4b9988d27a5752387397]

Issue #33, “Error converting model,” reports a file-opening failure and subsequently a separate GLM4 repeated-token problem. Its connection here is inferred only from the traceback's get_tensors call matching compile_model, which also consumes the version constant; the version edit does not address those mechanisms. [inference; call_bd7916878ed84f64a7b6cb7e49173bca, call_4c87e2272aa7415683cb2aaeb3fa8c43, call_18e4f06d3e1743e58603ea13350e38f0, call_d9ab5ca0901841858e6c21c9f9a694af, call_f57197456dac44ce83c7c023ef040e1e]

Issue #49, “running the QTIP inference code,” discusses installing and comparing QTIP. Any connection to this change is merely inferred from its setup.py references overlapping the inspected packaging consumer, not evidence of motivation for the version bump. [inference; call_22100083e459410fb2e97287a2ce6b99, call_1fa789ef968b46ff9294e867bc24279a]

<a id="build-release"></a>

## Propagating the 0.0.4 release identifier

setup.py executes version.py into a dictionary and passes __version__ to setup(version=...). The changed string therefore supplies 0.0.4 as the package base version. [source; call_1fa789ef968b46ff9294e867bc24279a, call_f57197456dac44ce83c7c023ef040e1e]

compile_model imports __version__ and writes it as quantization_config.version in the output config.json. Conversions reaching that write record 0.0.4; this edit does not rewrite existing artifacts. [source; call_d9ab5ca0901841858e6c21c9f9a694af, call_f57197456dac44ce83c7c023ef040e1e]

The manually dispatched build workflow parses version.py for release naming, yielding tag v0.0.4 and release name 0.0.4. Upload remains conditional on parsing not returning None and the release input being '1'; the input defaults to '0', so the bump itself does not initiate publication. [source; call_e5a44ec7de054f6a9f6a40f65c2ba643, call_f57197456dac44ce83c7c023ef040e1e]

## Uncertainty and limits

No package build, conversion or release workflow was executed; successful publication and compatibility are not established.

This string-only metadata change offers no useful numerical computation to validate.
