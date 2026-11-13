# e5f9f22afcc5aae48267b513a9653de54ca058e4


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/e5f9f22afcc5aae48267b513a9653de54ca058e4) · [Evidence ledger](draft.json)

Adds extensible layout names and marks transformer blocks without attention or MLP as no-op during conversion; tokenizer edits are formatting-only.

- [Expose no-op transformer blocks in the conversion layout](#conversion)

## Problem

The conversion layout displayed class names alone, giving empty transformer blocks no explicit no-op label. [source; call_cb72012173f945079bb469c002a0bf0e, call_2cb497107e3949fd8ed47afbc65a88f6]

## Reasoning

A polymorphic get_name() hook preserves ordinary class-name labels while allowing TransformerBlock to append " (no-op)" when both attention and MLP are absent. [source; call_83135579c3c44852bf3e0eb82d6416bb, call_3d595e4f014048debbbd97ce5d8accf9, call_77d9d138ad6a4a26bb8014e15bedd793]

## Impact

Conversion's get_base_model prints the updated layout through its existing get_layout_tree(4) call. The parent-tree search found no other direct callers. [source; call_a2a807d550074a94b74c5a9ea4a2c03f, call_2cb497107e3949fd8ed47afbc65a88f6]

## Source Notes

The preceding entry reports a separate zero-weight bitrate-reporting fix; this change adds structural labeling rather than another arithmetic guard. [ancestor; call_9ac23595785344cf9232c1e4cbfb56ab]

Tokenizer changes only wrap the existing BOS/EOS expressions across lines, preserving their None guards and lookup order. [source; call_c7373d41a77b440c81602354067e0a9d]

Issue #7, “quantizing model: undefined symbol: __cxa_call_terminate,” concerns an extension import failure. Its inferred overlap with this change is the model.py path in its traceback, not the layout-label mechanism; it does not establish motivation for this change. [inference; call_66e8242a5a464ec49c24b9d343ecace0, call_83135579c3c44852bf3e0eb82d6416bb]

<a id="conversion"></a>

## Expose no-op transformer blocks in the conversion layout

get_layout_tree recursively renders registered children and compresses consecutive identical branch strings into multiplicity labels. Replacing direct class-name access with get_name() retains this formatting and grouping mechanism while incorporating specialized labels. [source; call_cb72012173f945079bb469c002a0bf0e, call_83135579c3c44852bf3e0eb82d6416bb]

Both Model and Module provide the default hook because the renderer visits the model root as well as child modules. TransformerBlock overrides only the name, leaving execution and quantization allocation unchanged. [source; call_83135579c3c44852bf3e0eb82d6416bb, call_3d595e4f014048debbbd97ce5d8accf9, call_77d9d138ad6a4a26bb8014e15bedd793]

The label tests branch presence rather than parameter count. With neither branch present, forward skips both residual computations and returns through to2, which can still convert the output dtype. [source; call_77d9d138ad6a4a26bb8014e15bedd793, call_c86235a804b446c4a67ce69d53c9d0af, call_8c0a7aed8cff4b20b9688586a9202af5]

## Uncertainty and limits

No conversion or GPU execution was performed. This display-only change has no numerical algorithm warranting a scalar computation.

The no-op label describes absent attention and MLP branches, not a guarantee of object identity: forward still applies optional output-dtype conversion.
