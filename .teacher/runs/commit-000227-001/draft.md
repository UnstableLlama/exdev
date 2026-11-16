# 0e8ad5418d234678e82fd3265da45e102a2b2324


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/0e8ad5418d234678e82fd3265da45e102a2b2324) · [Evidence ledger](draft.json)

Removes multimodal support from the README’s missing-feature lists, aligning documentation with the existing Gemma3 example.

- [Updating multimodal feature status](#readme)

## Problem

The README still listed multimodal support as missing in both the opening caveats and the feature backlog, despite the existing Gemma3 image-generation example. [source; call_89ea0d79eb3a45168623877b38163a0a, call_dc5e884cc99b41f3a29e5d30fef90e9f]

## Reasoning

Removing both mentions reconciles the two status lists with the existing example; this is documentation catch-up rather than a new multimodal implementation. [inference; call_89ea0d79eb3a45168623877b38163a0a, call_dc5e884cc99b41f3a29e5d30fef90e9f]

## Impact

Only README.md changes. Tensor parallelism remains listed as missing, and no executable behavior or dependency changes. [source; call_89ea0d79eb3a45168623877b38163a0a]

## Source Notes

The parent entry records the addition of the Gemma3 multimodal example. The original usage-evaluation entry supplies the README's early-preview context and cautions that examples require local model paths and device configuration. [ancestor; call_8cd7d82c00dd418c9766993e813ddd84, call_2819bad2b3df41d1ab4eb7b824535359]

Issue #12, “Qwen2.5 Coder 0.5B Instruct | ValueError: Unsupported type in stop_conditions,” concerns chatbot prompt-mode selection. Its README.md occurrence is in a copied model-file listing; that provides no substantive connection to this multimodal status edit. [inference; call_44671207c4a243299cc12d6cf65a6732, call_586a8ab08ebe4c4aa4b0bee4fc461a94, call_89ea0d79eb3a45168623877b38163a0a]

<a id="readme"></a>

## Updating multimodal feature status

The example already loads a separate vision component, obtains image embeddings, inserts their text aliases into the prompt, and supplies those embeddings to tokenization and a streaming Job or to generate(). This supplies concrete source context for removing the blanket “not yet added” wording. [source; call_dc5e884cc99b41f3a29e5d30fef90e9f, call_89ea0d79eb3a45168623877b38163a0a]

The edit removes stale status claims without replacing them with model-specific instructions or a compatibility guarantee. [source; call_89ea0d79eb3a45168623877b38163a0a]

## Uncertainty and limits

No inference or GPU tests were run. The inspected example supports the narrower claim of an implemented Gemma3 integration, not universal multimodal compatibility or production readiness.

No useful scalar computation applies to these prose deletions; arithmetic would not validate multimodal execution.
