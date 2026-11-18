# 51c2b8d2e69de43546c4a28ea6cd977800262217


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/51c2b8d2e69de43546c4a28ea6cd977800262217) · [Evidence ledger](draft.json)

Adds ordered, sequential list ingestion to Mistral3 while preserving single-image returns and singleton merger execution; Gemma3 gains fixed-size embedding capability metadata.

- [List-based Mistral3 image ingestion](#vision)

## Problem

Mistral3 image ingestion accepted one image at a time; this change adds list input without requiring equal-sized image embeddings. [source; call_4f14a59ee58f407d9ad18a3c85a18000]

## Reasoning

Processing each list member through the existing single-image method preserves image-specific spatial parameters and satisfies Mistral3PatchMerger.forward's batch-size-one assertion. Unlike Gemma3's concatenated batch, this is sequential ingestion. [source; call_4f14a59ee58f407d9ad18a3c85a18000, call_88c36d82ca9c4f5190427a6a27d7361e, call_2134c99de32e4c3ca1cf0f575f599ee1]

## Impact

Single-image calls retain their MMEmbedding return. A list returns an ordered list, including an empty list for empty input, and rejects a supplied text_alias. The existing multimodal example remains compatible because it calls the method separately for each image. [source; call_4f14a59ee58f407d9ad18a3c85a18000, call_c6b31617bc9a4185bfec7f628c6135f0, call_79aa8167daca40b9b6b642d68e3e3905]

## Source Notes

Read the Gemma3 batching and Mistral3 introduction entries. They establish the preceding list interface and the merger's singleton-batch precondition. The Mistral3 introduction also records an inherited resize-overflow observation. [ancestor; call_218684a3ae2946a895922f5828374b75, call_2395a83a148c49db8a7aca6c3a6e42c1]

That recorded overflow mechanism is no longer present in the inspected parent helper: it floors scaled dimensions before patch alignment. The task leaves that helper and its preprocessing caller unchanged. [source; call_178efb3bd11a4044ace57d646e9c215c, call_c6b31617bc9a4185bfec7f628c6135f0, call_4f14a59ee58f407d9ad18a3c85a18000]

Issue #48, “`RuntimeError` when requesting logprobs with Gemma 3 models,” reports vocabulary/logit-width disagreement. Its relationship to this task is inferred solely from the shared gemma3.py path; the image-ingestion edits do not address its reported failure. [inference; call_2b60f89ccfd84b9bb0a377d4e57211ba, call_a0f6764026114dfc9c8f23f9f3c015da]

<a id="vision"></a>

## List-based Mistral3 image ingestion

Mistral3VisionModel.get_image_embeddings now accepts Image | list[Image]. Its list branch asserts that text_alias is None and recursively calls the same method once per member, passing the tokenizer but no alias. The original preprocessing and forward path remains the leaf implementation; no concatenation, padding or batched forward is introduced. [source; call_4f14a59ee58f407d9ad18a3c85a18000, call_c6b31617bc9a4185bfec7f628c6135f0]

Each leaf preprocesses to a singleton BCHW tensor aligned to patch_size times spatial_merge_size. Its own resized height and width determine features_size and rotary position IDs. Forward receives causal=False and those spatial parameters; the merger explicitly requires batch size one. Sequential recursion therefore preserves an existing execution precondition rather than merely accommodating unequal output lengths. [source; call_c6b31617bc9a4185bfec7f628c6135f0, call_88c36d82ca9c4f5190427a6a27d7361e]

After forwarding, each image's embeddings move to CPU. Dividing the patch-grid dimensions by spatial_merge_size gives the merged grid: each row contributes w embedding placeholders and one [IMG_BREAK], followed by one final [IMG_END]. Thus a merged h-by-w grid has h*w vectors and h*(w+1)+1 serialized tokens. Each returned MMEmbedding retains that image's original and preprocessed sizes. [source; call_c6b31617bc9a4185bfec7f628c6135f0]

A standard-library transcription of the inspected sizing and token-count arithmetic produced 1540×1008, 1980 vectors and 2017 serialized tokens for a 1541×1000 image; an 800×600 image produced 812×616, 638 vectors and 661 tokens. The assumed alignment is 28 pixels, from patch size 14 times merge size 2. These examples illustrate unequal token counts and removal of the earlier overflow example, not execution of NumPy, Pillow or the model. [execution; call_5e076af893b5412cb1b51d243c203e49, call_178efb3bd11a4044ace57d646e9c215c, call_c6b31617bc9a4185bfec7f628c6135f0]

The whole-parent-tree get_image_embeddings search found definitions only in Gemma3 and Mistral3, plus the multimodal example's single-image call. That caller builds a flat list of returned objects and reads each text_alias, so its unchanged single-image arguments agree with the retained return form. The new recursive call also uses that retained form. [source; call_d2f32228baea4707a56bb45f2f2832c0, call_79aa8167daca40b9b6b642d68e3e3905, call_4f14a59ee58f407d9ad18a3c85a18000]

Gemma3 additionally advertises caps['fixed_size_image_embeddings']=True. Its existing preprocessing always resizes to one configured size and its list path concatenates inputs for one forward. Mistral3 retains only image_input=True. No parent-tree occurrence of the new capability key was found, so the diff adds discoverable metadata rather than an inspected internal dispatch change. [source; call_a0f6764026114dfc9c8f23f9f3c015da, call_2134c99de32e4c3ca1cf0f575f599ee1, call_88c36d82ca9c4f5190427a6a27d7361e, call_ccc49617d1654ed69420da7f45e041d3, call_d1fc2b21eb4f4173a11647d82baab40d]

The two edits distinguish interface uniformity from execution uniformity: both architectures accept image lists, but only Gemma3 batches them. Mistral3's approach reuses existing spatial handling at the cost of one forward per image; no throughput improvement is established. [inference; call_4f14a59ee58f407d9ad18a3c85a18000, call_2134c99de32e4c3ca1cf0f575f599ee1, call_a0f6764026114dfc9c8f23f9f3c015da]

## Uncertainty and limits

No repository image preprocessing, tensor operations, checkpoint loading or GPU inference were executed; numerical correctness and performance remain unmeasured.

The scalar sizing check assumes longest_edge=1540, patch_size=14 and spatial_merge_size=2; these are illustrative inputs, not independently verified checkpoint preprocessing values.

Whole-tree literal searches establish the inspected direct caller and absence of the new capability key in parent source, not compatibility with dynamic or external consumers.
