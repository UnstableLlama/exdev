# 93cb21ca9b23d22164f38c1d91d968a3c25538b7


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/93cb21ca9b23d22164f38c1d91d968a3c25538b7) · [Evidence ledger](draft.json)

Corrects wrapper and vision-preprocessing documentation and removes a sampling TODO without changing executable behavior; the documented Mistral3 size bound retains an inherited rounding exception.

- [Clarifying existing wrappers and vision preprocessing](#comments)

## Problem

Comments retained an outdated DynamicJob name and described Mistral3 preprocessing as targeting Siglip. The change corrects these descriptions and removes a sampling TODO. [source; call_c44307e5211f46629ad30a27d2d9c0ce, call_f579319aecdf42ccb0e10d3964b99f3d, call_a0874dbad94846c2902321c2d42a4835]

## Reasoning

All four edits affect comments or docstrings, not executable operations. They clarify existing interfaces rather than implementing a new preprocessing or sampling strategy. [source; call_c44307e5211f46629ad30a27d2d9c0ce, call_a0874dbad94846c2902321c2d42a4835, call_44def8a91944415c86cdca07ac9aea33, call_f579319aecdf42ccb0e10d3964b99f3d]

## Impact

The revised Mistral3 bounding-box description expresses the intended sizing contract, but the unchanged rounding helper does not guarantee that bound for every input. [source; call_f579319aecdf42ccb0e10d3964b99f3d, call_5b0ad51112314baea2f8d0827edd2a31, call_6f90181763164b56bc985484e3d8bfa5]

## Source Notes

The Gemma3 vision introduction and Mistral3 architecture entries were read. They establish the existing preprocessing pipelines; the Mistral3 entry also records the inherited sizing overflow. [ancestor; call_db5263e6914e468e98ca56eafdac1fab, call_7faaf86a9ee84416b5bea61230688e9e]

Issue #48, “`RuntimeError` when requesting logprobs with Gemma 3 models,” reports mismatched logits dimensions. Its relationship to this task is inferred only from the shared gemma3.py path: this task edits a preprocessing docstring, not logits handling. PR #35, “humaneval.py: fix top_k type, remove rep_p, add qwen3,” concerns evaluation and sampling failures; it does not establish a reason for deleting this sampling TODO. [inference; call_0f6c8865ca1d4c9092da476ed3d70079, call_6ef0a950853842b7952ff7fe2b82b937, call_44def8a91944415c86cdca07ac9aea33, call_a0874dbad94846c2902321c2d42a4835]

<a id="comments"></a>

## Clarifying existing wrappers and vision preprocessing

AsyncJob already imports and constructs Job, forwards its arguments to that constructor, and enqueues the wrapper. Replacing DynamicJob with Job makes the docstring point to the actual underlying class without changing queue or cancellation behavior. [source; call_ddde4633ec0a4bd0981293fc9bb6e737, call_c44307e5211f46629ad30a27d2d9c0ce]

SS_Sample.run loses only the suggestion to evaluate multinomial sampling over sorted probabilities. The fused Gumbel-noise-plus-argmax TODO remains; no alternative algorithm is selected by this edit. [source; call_a0874dbad94846c2902321c2d42a4835]

Gemma3's addition of “format” covers existing RGB conversion, float32 rescaling and channel normalization, followed by channels-first half-precision conversion with a batch dimension. Its fixed-size resize remains unchanged. [source; call_44def8a91944415c86cdca07ac9aea33, call_c19f541753de44a4b99371ac5c1e5606, call_863934a8923748ddb391b774048355b1]

Mistral3 prepares a square bounding limit from longest_edge and aligns each output dimension to patch_size × spatial_merge_size. This alignment supplies complete patch neighborhoods for merging. It then performs RGB conversion, rescaling, normalization and BCHW half conversion; get_image_embeddings derives the feature grid from the returned size and divides its dimensions by spatial_merge_size for image-token serialization. Grid rounding means aspect-ratio preservation is approximate, not exact. [source; call_6f90181763164b56bc985484e3d8bfa5, call_5b0ad51112314baea2f8d0827edd2a31, call_f579319aecdf42ccb0e10d3964b99f3d]

## Authoring-time findings — pending review

### inherited-bounding-box-overflow (suspected; defect)

The newly documented bounding-box guarantee remains vulnerable to inherited floating-point ceiling overflow; this comment-only change carries the behavior over.

Trigger: Mistral3VisionModel.get_image_embeddings receives a 1541×1000 image with longest_edge=1540, patch_size=14 and spatial_merge_size=2.

Expected: Produce patch-aligned dimensions no larger than 1540 on either axis.

Actual: Scalar transcription produces 1568×1008. Division leaves the limiting dimension slightly above 1540, ceiling yields 1541, and alignment to 28 pixels increases it to 1568. Neither the helper nor preprocess clamps the result. Whole-parent-tree search finds the helper's sole direct call in Mistral3 preprocess; get_image_embeddings directly calls that preprocessing method.

Locations: 98964cbdae78ddcc85b0eefef2f4b13c6a606fbd:exllamav3/util/vision.py — size_to_longest_edge_and_patch_size, 93cb21ca9b23d22164f38c1d91d968a3c25538b7:exllamav3/models/mistral3.py — Mistral3VisionModel.preprocess

Source evidence: call_5b0ad51112314baea2f8d0827edd2a31, call_944f1d2839e04c9ab3a2f55717e125e8, call_6f90181763164b56bc985484e3d8bfa5, call_f579319aecdf42ccb0e10d3964b99f3d

scalar_transcription: Computed the inspected ratio, ceiling and 28-pixel alignment with standard-library Python; output was (1568, 1008). [call_1169a120ef5a48b085f376da93776b10]. Limits: Does not execute the repository helper, NumPy, Pillow or downstream vision kernels.

## Uncertainty and limits

No repository image processing, model inference or sampling implementation was executed. The arithmetic check uses Python floats and math.ceil rather than NumPy and Pillow.

The overflow example assumes longest_edge=1540, patch_size=14 and spatial_merge_size=2; these are test inputs, not newly verified checkpoint settings.
