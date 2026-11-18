# e1484296dd5878d85f782d4b9b36c2917cf2dbcb


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/e1484296dd5878d85f782d4b9b36c2917cf2dbcb) · [Evidence ledger](draft.json)

Explicitly retains special-token text in one base-vocabulary decoding branch, affecting cached piece-table consumers without changing the public decode API.

- [Retain special-token pieces in the base vocabulary](#tokenizer)

## Problem

The commit addresses special-token omission while constructing the base decoded-piece vocabulary. Previously, the single-token decoding branch did not specify skip_special_tokens; the change explicitly passes False. [source; call_873190af280a4c3082a67593223d0a5a]

## Reasoning

This fixes vocabulary construction rather than changing the public decode API: retaining special-token text in the underlying table also makes it available to table consumers that do not request the extended special-token overlay. [inference; call_873190af280a4c3082a67593223d0a5a, call_32ee9cb24fa44ae08d5b3814c459d80f]

## Impact

The change preserves vocabulary indexing and the list-of-strings interface, but can change strings observed by generation, reverse lookup, prefix matching and image-search token masks. [source; call_32ee9cb24fa44ae08d5b3814c459d80f, call_21d27d81480c424d94fc31d8b559f2a0, call_a3227088785d4502a62db84dfb402ec9, call_9adf3f84ecf84c4b8d9cafde1ed20710]

## Source Notes

The root loading-tokenization entry was read. It establishes the earlier design of eagerly cached piece tables and the whitespace-prefix probe on which this change relies. [ancestor; call_0bf7675ea94d4122b80f697fe5443094]

PR #13, “Fix a tokenizer issue while converting models without a bos_token_id defined,” reports a different initialization failure. Issue #16, “RuntimeError: CUDA error: invalid configuration argument,” discusses tokenizer truncation during conversion. Their relationship to this task is only inferred from the shared tokenizer implementation; neither discussion establishes the motivation for this particular decode_batch change. [inference; call_762bead62049406ba531bf63a43a7fde, call_4f4b11083e0d444fb8313050b2d8bba9, call_873190af280a4c3082a67593223d0a5a]

<a id="tokenizer"></a>

## Retain special-token pieces in the base vocabulary

get_fixed_vocab probes the encoding of ' t'. When that produces exactly one token whose decoded text has length two, it batch-decodes each vocabulary ID independently. The constants one and two describe this probe, not vocabulary-size or performance thresholds. Only this branch gains skip_special_tokens=False. [source; call_32ee9cb24fa44ae08d5b3814c459d80f, call_873190af280a4c3082a67593223d0a5a]

The alternate branch prepends the first token encoding a space, decodes each pair, then removes the decoded prefix length. That whitespace-preserving preparation remains unchanged, including its decode_batch arguments. [source; call_32ee9cb24fa44ae08d5b3814c459d80f, call_873190af280a4c3082a67593223d0a5a]

Whole-tree search finds get_id_to_piece_list as the sole direct caller of get_fixed_vocab. Initialization eagerly builds both piece-table variants and the reverse dictionary. The ordinary table takes the fixed vocabulary and appends extended IDs; the special variant copies it and overwrites entries from extended_id_to_piece. Consequently, an existing overlay can already supply a special spelling, whereas this edit repairs the underlying selected-branch decoding. [source; call_5cf48b29717e4a9f8c53d013f144c4ec, call_32ee9cb24fa44ae08d5b3814c459d80f]

Inspected consumers remain structurally compatible: get_piece_to_id_dict reverses strings into IDs; prefix helpers inspect those strings; generation_loop indexes the ordinary table after checking stop conditions; imgsearch builds startswith masks; generator/job.py selects a table using decode_special_tokens and indexes it for output text. In particular, a False selection no longer guarantees empty special-token pieces in the changed branch. Public decode and decode_ are not modified. [source; call_d92dcd1dd72841929e99f689d8ab7b78, call_b6b01643a88445e68683e91bca957cea, call_32ee9cb24fa44ae08d5b3814c459d80f, call_a3227088785d4502a62db84dfb402ec9, call_9adf3f84ecf84c4b8d9cafde1ed20710, call_21d27d81480c424d94fc31d8b559f2a0, call_873190af280a4c3082a67593223d0a5a]

A bounded check extracted get_fixed_vocab and applied the changed keyword against a stub backend assuming a True default. Its two-entry output changed from ['', ' t'] to ['<special>', ' t'], retaining length and position. This demonstrates argument propagation under that assumption, not actual backend decoding. [execution; call_90ebe9b4fdec416092592e2350943991]

## Uncertainty and limits

No real Hugging Face tokenizer or model was executed. The backend's version-specific default and special-token rendering behavior were not independently established.

The alternate whitespace-prefix branch still omits skip_special_tokens. The task therefore does not explicitly enforce special-token retention in both branches.

The bounded check uses an assumed backend default and synthetic token strings; it does not demonstrate checkpoint-specific output or generation behavior.
