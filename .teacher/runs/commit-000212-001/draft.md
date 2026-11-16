# 56e9d038dee07aa1657b8febb7f6a259f7eda11c


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/56e9d038dee07aa1657b8febb7f6a259f7eda11c) · [Evidence ledger](draft.json)

Bumps the shared version from 0.0.2 to 0.0.3, updating package identification, conversion provenance and release naming without changing runtime algorithms.

- [Propagating the 0.0.3 release identifier](#build-release)

## Problem

The shared release identifier remained 0.0.2; this change advances it to 0.0.3. [source; call_5aa60a6c411c4db69de918492b469740]

## Reasoning

Updating the shared constant propagates the release identifier through existing consumers without changing their implementations. [source; call_5af93df9d6074dd5bcb3b6a6c3c00442, call_45e88888106a4bf7880a68fa0c46b082, call_5709115d1c6e4e0e94d2b37a469afed3, call_9f9bf4e4564942fd9f050a9d80f1436e]

## Impact

The sole edit changes release metadata, not inference algorithms, dependencies or build settings. [source; call_5aa60a6c411c4db69de918492b469740]

## Source Notes

The earlier 0.0.2 bump entry was read; it documents the same shared-constant mechanism and conditional release publication. [ancestor; call_dcc0d9bd83a944999dd5e6ecfc7fec82]

Issue #33, “Error converting model,” reports a file-opening failure and later a separate GLM4 repeated-token problem. Its relevance here is only inferred from its traceback matching compile_model's tensor-loading call, a function that also consumes the version constant; it does not establish that this version-only edit fixes either report. [inference; call_0a5208065add4384a48a6995a2e9d077, call_fc71c18adcb54ba990aa4308ca896e68, call_5709115d1c6e4e0e94d2b37a469afed3, call_5aa60a6c411c4db69de918492b469740]

<a id="build-release"></a>

## Propagating the 0.0.3 release identifier

setup.py executes version.py into a dictionary and supplies __version__ to setup(version=...), making 0.0.3 the new package base version. [source; call_45e88888106a4bf7880a68fa0c46b082, call_5aa60a6c411c4db69de918492b469740]

compile_model imports the constant and writes it under quantization_config.version in the output config.json. Outputs reaching that write now record 0.0.3; the edit does not rewrite existing artifacts. [source; call_5709115d1c6e4e0e94d2b37a469afed3, call_5aa60a6c411c4db69de918492b469740]

The manually dispatched build workflow parses version.py and derives the release tag and name from it. Upload remains conditional on successful parsing and release input '1'; the constant change does not itself initiate publication. [source; call_9f9bf4e4564942fd9f050a9d80f1436e]

## Uncertainty and limits

No build, conversion or release workflow was executed. This string-only edit offers no useful numerical computation to validate.

The version increment does not establish compatibility guarantees or successful release publication.
