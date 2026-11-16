# 16df3fd1810c4f0747ff4fd5fbcc1dc94c4d6628


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/16df3fd1810c4f0747ff4fd5fbcc1dc94c4d6628) · [Evidence ledger](draft.json)

Adds patch-aligned image-size calculation with proportional downscaling; scalar inspection exposes a suspected floating-point bounding-box overflow.

- [Bounding image dimensions on a patch grid](#vision)

## Problem

Adds a reusable image-size calculation combining a maximum bounding box with patch-grid alignment. [source; call_17c57986a1dd4e4797a9aee7511340cb]

## Reasoning

Requiring maximum dimensions to be patch multiples makes upward grid rounding compatible with the bounding box in exact arithmetic. Floating-point scaling introduces an exception. [inference; call_17c57986a1dd4e4797a9aee7511340cb, call_d05e036eb3c74e63a3d0d5a38be97288]

## Impact

The change adds only the helper, not a resizing operation or model integration. A whole-parent-tree literal search found no existing reference to its name. [source; call_17c57986a1dd4e4797a9aee7511340cb, call_86597b999c464906a796ea782ed9e67d]

## Source Notes

Read the earlier vision-utilities entry, which establishes RGB conversion and normalization as preprocessing primitives with caller-managed pixel scaling. [ancestor; call_8f91452593f6402489bb474a00fa097a]

The inspected parent implementation retains those helpers unchanged; the new function reuses the existing NumPy import. [source; call_6817895c913b45eebc0fc063aeb6a701, call_17c57986a1dd4e4797a9aee7511340cb]

The cataloged PR “humaneval.py: fix top_k type, remove rep_p, add qwen3” concerns evaluation and generation failures, not image sizing; no substantive connection to this change is established. [inference; call_6b8b86cfacf84d3a8688c37b735b5ed5, call_17c57986a1dd4e4797a9aee7511340cb]

<a id="vision"></a>

## Bounding image dimensions on a patch grid

size_to_longest_edge_and_patch_size takes input, maximum and patch dimension tuples. It asserts pairwise divisibility of maximum dimensions by patch dimensions, then computes the larger input-to-maximum ratio. Only ratios above 1 trigger proportional reduction; smaller inputs are not proportionally enlarged. [source; call_17c57986a1dd4e4797a9aee7511340cb]

After ceiling reduced dimensions to integers, the helper rounds each dimension upward with ((d + p - 1) // p) * p. The p - 1 implements integer ceiling division. This alignment can enlarge smaller inputs and changes aspect ratio, so the docstring's aspect-ratio preservation is approximate rather than exact. [source; call_17c57986a1dd4e4797a9aee7511340cb]

A scalar sweep of 90,000 positive input pairs, with maximum (224,192) and patches (16,32), found 2,497 bounding-box overflows in the transcribed algorithm. The first was (230,1), producing intermediate (225,1) and final (240,32). [execution; call_d05e036eb3c74e63a3d0d5a38be97288]

## Authoring-time findings — pending review

### floating-ceiling-overflow (suspected; defect)

Floating-point division followed by ceiling can push a limiting dimension above its maximum, and patch alignment amplifies the overshoot.

Trigger: Call the new helper with input_size=(230,1), max_size=(224,192), patch_size=(16,32).

Expected: Return patch-aligned dimensions no larger than (224,192), as promised by the bounding-box contract.

Actual: The scalar transcription produces (240,32): the computed limiting dimension rounds up to 225 before alignment. The source has no final clamp. No repository callers were found in the parent, and the diff introduces none, so reach is limited to direct prospective or external use.

Locations: 16df3fd1810c4f0747ff4fd5fbcc1dc94c4d6628:exllamav3/util/vision.py — size_to_longest_edge_and_patch_size

Source evidence: call_17c57986a1dd4e4797a9aee7511340cb, call_86597b999c464906a796ea782ed9e67d

scalar_transcription: Swept input dimensions 1 through 300 using the inspected scaling and alignment formulas. [call_d05e036eb3c74e63a3d0d5a38be97288]. Limits: Used standard-library math.ceil rather than NumPy ceil; did not execute the repository helper or image resizing.

## Uncertainty and limits

No repository implementation or NumPy operation was executed. The numerical check transcribed the algorithm using Python floats and math.ceil.

No integrated caller establishes dimension ordering or input validation. Literal searches do not exclude external or dynamic callers.
