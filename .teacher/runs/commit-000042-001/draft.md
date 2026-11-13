# 5e46530bee701713b551884be5e5fcf6697a6b63


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/5e46530bee701713b551884be5e5fcf6697a6b63) · [Evidence ledger](draft.json)

Guard BOS and EOS string lookup when their resolved IDs are None, preserving existing lookup behavior for defined IDs.

- [Preserve absent BOS and EOS tokens during initialization](#loading-tokenization)

## Problem

Tokenizer initialization previously passed unresolved BOS or EOS IDs into the backend's id_to_token lookup. The change guards both lookups when the resolved ID is None. [source; call_c141334337754391919dcdfd21be5871, call_a84a102d6fe94a88b6f82d145792a6fe]

## Reasoning

Missing bos_token_id in model configuration does not alone imply this path: the tokenizer first tries bos_token in tokenizer configuration and otherwise defaults to ID 1. Explicit null, unsupported token descriptions, or unresolved token strings can instead leave the ID None. EOS follows the same resolution scheme with default ID 2. [source; call_1a8bba260c9c4f69beb089e2e427cc52, call_a84a102d6fe94a88b6f82d145792a6fe, call_2c58ebf464344d8e94ac0f50527bb909, call_ef98a72b8a1a46c6a787cf5015c9c76c]

## Impact

The guard applies to shared tokenizer construction, not only conversion. Conversion's get_base_model calls Tokenizer.from_config, which directly constructs Tokenizer; parent-tree searches also locate factory calls in examples, evaluation, model initialization and a stress test. [source; call_2a456305295140b9810deceabc86124e, call_a84a102d6fe94a88b6f82d145792a6fe, call_037202fc07324503bf95dbcbf536a5f6, call_9c6d01a0bbef463498940237d211ab17]

## Source Notes

The inspected discussions report different problems: issue 7 concerns an undefined native symbol, issue 8 an invalid quantization reshape, issue 11 a bias datatype assertion, and issue 12 unsupported stop_conditions after conversion, discussed in terms of chat mode selection. PR 4 is a spelling correction. None supplies a reproduction of this None-ID lookup. [source; call_58c630c7fb6643069c0befbc390d12e5, call_bf1f99d76f284898a7b8a92ea56d3b1c, call_d9b76a3f731245f19e68bdf5e67dac46, call_eda60567a14d407582ad4890e495ed4d, call_7a7724c40e984499952c006e39d49060, call_4760df8c06d74d5b88b6a553abe38d74]

<a id="loading-tokenization"></a>

## Preserve absent BOS and EOS tokens during initialization

Tokenizer.__init__ now stores None for each control-token string whose resolved ID is None. For non-None IDs, it retains the original preference for extended_id_to_piece, falling back to backend id_to_token when that mapping is absent or falsey. The explicit identity check also preserves valid ID zero. [source; call_c141334337754391919dcdfd21be5871]

This keeps absence explicit rather than inventing a replacement token. Existing truthiness guards skip adding absent control-token strings to the extended vocabulary, while encode already skips BOS/EOS insertion when the corresponding ID is None. ID resolution and padding fallback are unchanged. [source; call_a84a102d6fe94a88b6f82d145792a6fe, call_c141334337754391919dcdfd21be5871]

A standard-library scalar transcription checked 12 combinations of IDs and extended mappings. All nine non-None cases retained identical results and backend calls; all three None cases avoided the backend call after the change. The backend was a recording stub, not the tokenizers library. [execution; call_1ee0bc4ee0b84dd8a62468c002e087c7]

## Uncertainty and limits

No real tokenizer backend, model conversion or GPU workload was executed; the backend's exact exception for None and end-to-end conversion success remain unverified.

The scalar check models only the changed lookup expressions, not complete tokenizer initialization or downstream padding and generation behavior.
