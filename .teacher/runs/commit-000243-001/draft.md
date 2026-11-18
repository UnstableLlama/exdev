# 64ef2a379213f88671e04d71a45f18ae8590e079


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/64ef2a379213f88671e04d71a45f18ae8590e079) · [Evidence ledger](draft.json)

Batches vocabulary decoding and caches tokenizer lookup construction, with unmeasured speed benefits, shared-list extension risk, and a removed ordinal-getter return.

- [Batching and caching tokenizer lookup construction](#loading-tokenization)

## Problem

Tokenizer construction eagerly builds lookup tables using per-token decoding and repeated backend vocabulary-size queries. The change replaces these operations with batched decoding and cached helpers. [source; call_d380f428399c423d86ad9b05de1c76bc, call_c63c8e37f42f452e9f1c1a514ab559d7]

## Reasoning

Reducing Python/backend crossings plausibly explains the claimed faster initialization, but the inspected evidence contains no timing comparison. [inference; call_c63c8e37f42f452e9f1c1a514ab559d7]

## Impact

The optimization also changes cache ownership and the ordinal getter's return behavior; it is not strictly a performance-only substitution. [source; call_c63c8e37f42f452e9f1c1a514ab559d7, call_84774abb51104d59b9d8d4b620be95b1]

## Source Notes

The root loading-tokenization entry describes eager vocabulary construction, the whitespace probe, and inherited decode-filter limitations. [ancestor; call_edad02c3b728473fa1c1975ab8f27aee]

PR #13, “Fix a tokenizer issue while converting models without a bos_token_id defined,” reports a separate None-valued BOS failure. Its relationship here is contextual inference based on the shared tokenizer file, not evidence motivating this optimization; the parent already guards that BOS lookup. [inference; call_573351c4e42547729f046195800215f4, call_d380f428399c423d86ad9b05de1c76bc]

<a id="loading-tokenization"></a>

## Batching and caching tokenizer lookup construction

raw_vocab_size caches the backend size and supplies actual_vocab_size calculation, decode filtering, and table construction. Initialization remains eager: it builds ordinals, special and ordinary piece lists, and the reverse map before returning. [source; call_c63c8e37f42f452e9f1c1a514ab559d7, call_d380f428399c423d86ad9b05de1c76bc]

get_fixed_vocab preserves the existing ' t' probe. One token decoding to the probe's two-character length selects singleton sequences; otherwise each ID is decoded after a space-prefix token, whose decoded character length is sliced away. Both paths now issue decode_batch rather than one decode call per ID. The nonempty-probe assertion remains, as does the unguarded indexing of the separately encoded space. [source; call_c63c8e37f42f452e9f1c1a514ab559d7, call_d380f428399c423d86ad9b05de1c76bc]

The table getters replace attribute-based early returns with lru_cache. synchronized still surrounds their cache access using the utility's reentrant lock, allowing the special-list getter to call the ordinary getter recursively. get_fixed_vocab and raw_vocab_size themselves have no synchronized decorator. [source; call_c63c8e37f42f452e9f1c1a514ab559d7, call_707eee569ac743eca6704d212af4f9be]

get_id_to_ord_list now initializes base entries as range(raw_vocab_size), rather than round-tripping through id_to_token and token_to_id. Appended entries retain hexadecimal-byte parsing, single-character ordinals up to 255, and -1 for unsupported pieces or gaps. Thus base entries remain ID-like rather than becoming a general byte decoder. [source; call_c63c8e37f42f452e9f1c1a514ab559d7, call_d380f428399c423d86ad9b05de1c76bc]

Whole-parent searches found no ordinal-table consumer beyond construction. Piece-list consumers remain list-compatible: generation_loop indexes sampled IDs; Job indexes completion, healing and stop-token strings; prefix helpers scan or index the list. single_id still consumes the reverse dictionary. However, their shared table construction can duplicate appended entries, as recorded in the finding. [source; call_401d009eaff341fda397753e97c9fef1, call_9b3a599c07b84a6d9d62a9039da73b26, call_56109dfed9994f76a7cd4e207eea5a2d, call_ea53c7090d3340a889e36085b48038bf, call_1de7019ddd034b63a6110648956f7409, call_4c24e04395f048dc9e71cc2f151853dc, call_d380f428399c423d86ad9b05de1c76bc]

A bounded Python transcription reproduced separate default/explicit-False cache computations mutating one cached vocabulary list: the ordinary table contained two copies of the appended token while the special copy contained one. It also reproduced the ordinal getter returning None despite setting its attribute. [execution; call_84774abb51104d59b9d8d4b620be95b1]

## Authoring-time findings — pending review

### shared-vocabulary-extension (suspected; defect)

The cached decoded vocabulary is mutated by separately cached ordinary-list calls, duplicating appended vocabulary entries during construction.

Trigger: A tokenizer has actual_vocab_size greater than raw_vocab_size. Construction calls get_id_to_piece_list(True), which invokes the no-argument form, then calls get_id_to_piece_list(False).

Expected: Each appended ID occupies exactly one table position, and the reverse map points to that ID.

Actual: Both ordinary computations obtain the same get_fixed_vocab list and append the extension again. The special copy predates the second append; the reverse dictionary enumerates the duplicated list and can map an extended piece to its later, incorrect index.

Locations: 64ef2a379213f88671e04d71a45f18ae8590e079:exllamav3/tokenizer/tokenizer.py — Tokenizer.get_id_to_piece_list

Source evidence: call_c63c8e37f42f452e9f1c1a514ab559d7, call_d380f428399c423d86ad9b05de1c76bc, call_56109dfed9994f76a7cd4e207eea5a2d, call_9b3a599c07b84a6d9d62a9039da73b26

scalar_transcription: Modeled constructor call order, lru_cache argument distinctions, cached-list aliasing and extension. [call_84774abb51104d59b9d8d4b620be95b1]. Limits: Synthetic two-token vocabulary with one extension; no tokenizer backend executed.

### ordinal-return-removed (suspected; behavior_change)

get_id_to_ord_list no longer returns its populated list.

Trigger: A caller uses the getter's return value.

Expected: Return the ordinal list, as the parent implementation did.

Actual: The function falls through and its cache stores None. self.id_to_ord is still populated. Whole-parent search found only the constructor call, which discards the return, so no inspected internal consumer fails on this change.

Locations: 64ef2a379213f88671e04d71a45f18ae8590e079:exllamav3/tokenizer/tokenizer.py — Tokenizer.get_id_to_ord_list

Source evidence: call_c63c8e37f42f452e9f1c1a514ab559d7, call_401d009eaff341fda397753e97c9fef1

source_inspection: Compared removed return statement with the complete parent function and searched callers. [call_c63c8e37f42f452e9f1c1a514ab559d7, call_d380f428399c423d86ad9b05de1c76bc, call_401d009eaff341fda397753e97c9fef1]. Limits: External callers were not available.

### inherited-eos-filter (suspected; defect)

The touched decode_ path carries over the earlier entry's ineffective EOS truncation.

Trigger: decode receives ordinary tokens both before and after EOS with special rendering disabled.

Expected: The explicit EOS-truncation branch would discard tokens after EOS.

Actual: Filtering removes EOS first, making that branch unreachable; post-EOS tokens remain. Only the vocabulary-size query changes in this commit. Direct callers are the rank-one and rank-two branches of decode; Job also uses decode for incomplete-character recovery, but this does not establish that its stop handling reaches this trigger.

Locations: 64ef2a379213f88671e04d71a45f18ae8590e079:exllamav3/tokenizer/tokenizer.py — Tokenizer.decode_

Source evidence: call_c63c8e37f42f452e9f1c1a514ab559d7, call_d380f428399c423d86ad9b05de1c76bc, call_fb95b995600f4552be90295a36bf5f39, call_1de7019ddd034b63a6110648956f7409

scalar_transcription: Applied the inspected filter to [11,2,12,0,99] with EOS 2, PAD 0 and vocabulary size 50; result was [11,12]. [call_84774abb51104d59b9d8d4b620be95b1]. Limits: Filtering only; no backend decoding or generation execution.

## Uncertainty and limits

No real Hugging Face tokenizer, initialization benchmark, model generation, or concurrent execution was run. Batched-versus-individual decoding equivalence remains unmeasured.

The scalar check models inspected Python cache and list behavior; it does not execute the repository implementation.

Replacing token-to-string-to-ID round trips with range assumes dense, round-tripping backend IDs. Compatibility with sparse or unusual tokenizer vocabularies is unestablished.
