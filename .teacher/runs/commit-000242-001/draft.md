# 17f1ab5e59ead2e410854ef53539b2915b304460


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/17f1ab5e59ead2e410854ef53539b2915b304460) · [Evidence ledger](draft.json)

Fixes Pixtral sizing by flooring scaled dimensions before patch alignment and keeping them positive; scalar checks reproduce removal of the inherited bounding-box overflow.

- [Keeping Pixtral resize dimensions within the patch-aligned bound](#vision)

## Problem

Ceiling a floating-point scaled dimension could exceed the bounding box by one pixel; subsequent patch alignment amplified that error. [source; call_389baef6ab3247e1ba4793e674a9e1d1, call_2163d0f8c54e419e8a280e73cc53a0ef]

## Reasoning

The change floors scaled dimensions before upward patch alignment. Its new minimum of one prevents a thin dimension from becoming zero after flooring; these two edits therefore work together. [source; call_2163d0f8c54e419e8a280e73cc53a0ef]

## Impact

The sole direct caller found is Mistral3 vision preprocessing. It uses the returned dimensions to resize the image; embedding construction subsequently derives patch-grid dimensions and position IDs from that resized size. [source; call_a4b9cf447c4848f89b92c2cfcf756874, call_365065fa0e884d8095bf6619f5c9bbbc]

## Source Notes

The helper's introduction entry was read. It records the divisibility precondition and a suspected floating-point overflow. Inspection of the parent and task diff shows that this change replaces the offending ceiling operation rather than carrying it over. [source; call_389baef6ab3247e1ba4793e674a9e1d1, call_2163d0f8c54e419e8a280e73cc53a0ef]

The earlier entry describes the helper as a standalone sizing primitive, initially without model integration. [ancestor; call_88619e797601455497be26dfe12ff51f]

<a id="vision"></a>

## Keeping Pixtral resize dimensions within the patch-aligned bound

The helper retains its assertion that each maximum dimension is divisible by its patch dimension. It scales only when the larger input-to-maximum ratio exceeds one, then rounds each dimension upward using ((d + p - 1) // p) * p. The p - 1 implements integer ceiling division. [source; call_389baef6ab3247e1ba4793e674a9e1d1, call_2163d0f8c54e419e8a280e73cc53a0ef]

Mistral3 supplies a square longest-edge bound and a grid spacing equal to patch size times spatial merge size. Alignment therefore makes the resized image divisible into merged feature tiles. The unchanged no-downscaling branch still permits upward grid rounding, and grid alignment only approximately preserves aspect ratio. [source; call_365065fa0e884d8095bf6619f5c9bbbc, call_389baef6ab3247e1ba4793e674a9e1d1]

A scalar comparison over 90,000 positive input pairs, using maximum (224,192) and patches (16,32), found 2,497 old bounding-box overflows and none with the revised formula. Input (230,1) changed from (240,32) to (224,32). These are synthetic dimensions, not asserted checkpoint defaults. [execution; call_647771a5d5104a828788f273a01cdbe4]

The correction is broader than clipping overflowing outputs: flooring can also reduce a nonlimiting dimension across a patch boundary. In the same scalar sweep, 4,467 output pairs changed. The tradeoff favors staying within the bound over retaining the old upward-rounded resize dimensions. [inference; call_2163d0f8c54e419e8a280e73cc53a0ef, call_647771a5d5104a828788f273a01cdbe4]

## Uncertainty and limits

Validation used a standard-library scalar transcription, not the repository's NumPy implementation, PIL resizing, or GPU inference.

The bounded numerical sweep does not establish correctness for every dimension or invalid input. Literal caller search does not exclude external or dynamic callers.
