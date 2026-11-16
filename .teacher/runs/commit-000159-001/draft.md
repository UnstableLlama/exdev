# d1e3b2b20e7591ee613c049701a46973e9e5bf86


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/d1e3b2b20e7591ee613c049701a46973e9e5bf86) · [Evidence ledger](draft.json)

Refreshes README maturity and roadmap wording without changing implementation or establishing release-build or TabbyAPI availability.

- [Refresh project-status wording](#documentation)

## Problem

The README still called ExLlamaV3 an early preview, said release builds were unavailable, and named Mixtral, Cohere and Deepseek as forthcoming architectures. [source; call_4d76dce2f6ef4ce8b7ee27c4916005c2]

## Reasoning

Removing the named architecture examples is consistent with the parent registry already including MixtralModel, CohereModel and Cohere2Model. That registry does not establish Deepseek support. [source; call_ba6db346f49e47f0a13d8659a06d822c, call_4d76dce2f6ef4ce8b7ee27c4916005c2]

## Impact

Only README wording changes; the patch adds no runtime functionality, release artifacts or integration code. [source; call_4d76dce2f6ef4ce8b7ee27c4916005c2]

## Source Notes

Issue #12, “Qwen2.5 Coder 0.5B Instruct | ValueError: Unsupported type in stop_conditions,” concerns chat prompt-mode selection and mode-listing arguments. Its README.md occurrence is a model-conversion copy log; this does not establish a connection to the documentation update. [inference; call_2268ebdc90d7416ca2df53993b4bceed, call_7d03e6ccc3cb4067a698345a45fae740, call_4d76dce2f6ef4ce8b7ee27c4916005c2]

<a id="documentation"></a>

## Refresh project-status wording

The opening now says ExLlamaV3 is “still in development” rather than an “early preview release.” The patch removes both the no-release-builds warning and the conditional TabbyAPI integration plan. [source; call_4d76dce2f6ef4ce8b7ee27c4916005c2]

The architecture roadmap becomes the open-ended “Support for more architectures.” This avoids retaining specific forthcoming examples while preserving the broader development goal. [inference; call_4d76dce2f6ef4ce8b7ee27c4916005c2, call_ba6db346f49e47f0a13d8659a06d822c]

The diff retains the surrounding performance, ROCm, FlashAttention-2 and missing-feature caveats, along with the warning that ExLlamaV3 is not yet a viable ExLlamaV2 replacement. These are retained documentation statements, not independently verified runtime conclusions. [source; call_4d76dce2f6ef4ce8b7ee27c4916005c2]

## Uncertainty and limits

Deleting the release-build and TabbyAPI bullets does not establish that builds became available or integration was completed.

No runtime tests were run. This prose-only change offers no meaningful numerical computation; architecture registration is not model-execution validation.
