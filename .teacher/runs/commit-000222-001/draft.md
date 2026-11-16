# 08f7e1b1fcced3ba38e83d5ab1e426051eb02553


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/08f7e1b1fcced3ba38e83d5ab1e426051eb02553) · [Evidence ledger](draft.json)

Adds and exports an unquantized learned-position table that adds consecutive positional vectors to hidden states, with offset and explicit-position support left unfinished.

- [Learned positional vectors added to hidden states](#modules)

## Problem

The change adds a reusable learned-position embedding module, distinct from token-ID embedding lookup. [source; call_dabfc712e93b480cbb4ffd1f02ad1d09, call_2b44ea0a707345c09850309a94036ab5]

## Reasoning

PosEmbedding reuses the embedding-table loading pattern but adds consecutive table rows directly to the hidden states instead of looking up input token IDs. [source; call_dabfc712e93b480cbb4ffd1f02ad1d09, call_2b44ea0a707345c09850309a94036ab5]

## Impact

The package exports PosEmbedding, but this commit adds no model construction site that uses it. [source; call_3a8bd087622948b890bc46b1168fae2c, call_dabfc712e93b480cbb4ffd1f02ad1d09, call_418024e4e69f4ca28ccb4ef9a3304e63]

## Source Notes

The initial modules ancestor entry describes the custom Module interface, embedding loading and dtype precedence on which this implementation builds. [ancestor; call_4a061d0137b844a5b8eee0e31d72f214]

<a id="modules"></a>

## Learned positional vectors added to hidden states

The constructor stores hidden_size, optional vocab_size and output dtype, rejects non-null qmap, and initializes the weight count to vocab_size × hidden_size when known. Module supplies the configuration, tensor key and device-management interface. [source; call_dabfc712e93b480cbb4ffd1f02ad1d09, call_0020181ec7db4967ae55f122eba860d4]

load requests key.weight with float2half=True, derives the positional-table length from weight.shape[0], records its actual element count, and installs the tensor as an nn.Embedding parameter. Forward accesses that parameter directly. get_tensors exports contiguous weight data under the same key; unload clears the embedding and device references. [source; call_dabfc712e93b480cbb4ffd1f02ad1d09]

For conventional [batch, sequence, hidden] activations, forward slices weight[0:sequence] and adds it in place. Zero is the fixed starting position, not a threshold; dimension 1 supplies sequence length. The same positional vectors are shared across batches, and params is unused. [source; call_dabfc712e93b480cbb4ffd1f02ad1d09]

Output conversion happens after the in-place addition. to2 gives the forward-call dtype priority over the constructor dtype and otherwise preserves the input dtype; requesting a different output dtype does not move the preceding addition into that precision. [source; call_dabfc712e93b480cbb4ffd1f02ad1d09, call_0a955c0adeaf4281a04ae63a80e59fcd]

A standard-library scalar transcription with two batches, two positions and two channels produced [[[11,22],[33,44]],[[15,26],[37,48]]], illustrating that both batches receive table rows zero and one. This models the indexing and addition, not execution of the repository implementation. [execution; call_c9675d55079a4acdb4b2a2159a249f32]

## Uncertainty and limits

No PyTorch or GPU execution was performed; the scalar example does not establish broadcasting errors, dtype rounding or device behavior.

Position offsets and explicit position IDs are explicitly unfinished. Every forward call starts at table row zero, so this is not complete chunked-decoding or GPT-2 support.

The implementation assumes compatible activation and table dimensions and sufficient positional rows; no explicit shape or capacity validation is added.

When vocab_size is omitted, weights_numel returns None until loading. Compatibility of pre-load weight accounting with every consumer was not established.
