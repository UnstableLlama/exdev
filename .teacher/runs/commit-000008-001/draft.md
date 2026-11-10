# f579de4923ac13ce05ae4cabe45c276e4558b768


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/f579de4923ac13ce05ae4cabe45c276e4558b768) · [Evidence ledger](draft.json)

Points the README’s EXL3 model link directly to the Hugging Face EXL3 models collection.

- [Direct navigation to the EXL3 model collection](#documentation-navigation)

## Problem

The README’s EXL3 model-selection link pointed to the general turboderp Hugging Face profile. [source; call_9fc594041a934d0aa38ca74b44f267a8]

## Reasoning

The change replaces that profile URL with the EXL3 models collection URL while preserving the link label and surrounding sentence. [source; call_9fc594041a934d0aa38ca74b44f267a8]

## Impact

Readers following the model-selection link are directed to a collection-specific destination rather than the general profile; no executable code changes. [source; call_9fc594041a934d0aa38ca74b44f267a8]

<a id="documentation-navigation"></a>

## Direct navigation to the EXL3 model collection

README.md changes the Hugging Face target from https://huggingface.co/turboderp to https://huggingface.co/collections/turboderp/exl3-models-67f2dfe530f05cb9f596d21a. The visible “🤗 Hugging Face” label remains unchanged. [source; call_9fc594041a934d0aa38ca74b44f267a8]

## Uncertainty and limits

The destination’s availability and collection contents were not verified. No useful numerical computation or runtime test applies to this URL-only documentation change.
