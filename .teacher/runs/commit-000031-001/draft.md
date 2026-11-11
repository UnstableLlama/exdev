# 40fb78fa4cc156e8b8a79d7470bc5062a02ea29c


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/40fb78fa4cc156e8b8a79d7470bc5062a02ea29c) · [Evidence ledger](draft.json)

Replaces manual special-token splitting with whole-text backend encoding, enabling backend-controlled token handling while leaving compatibility and inherited decoding limitations unresolved.

- [Delegate special-token encoding to the backend](#loading-tokenization)

## Problem

The special-token encoding path split text around literal token spellings and inserted mapped IDs itself, withholding those tokens and their surrounding context from the backend tokenizer. [source; call_21228fafc8c64a948a14bf95b05982d6]

## Reasoning

Passing the complete input to the backend delegates token recognition and whitespace handling to that engine rather than duplicating recognition with a regular expression. The retained TODO explicitly leaves the necessity of the old SentencePiece-oriented workaround unresolved. [source; call_6b4434947cc54510b3654e82f700f55a]

## Impact

encode_special now returns one backend encoding with add_special_tokens=False. Explicit BOS/EOS insertion and batch padding remain in encode; the change does not alter decoding. [source; call_6b4434947cc54510b3654e82f700f55a, call_21228fafc8c64a948a14bf95b05982d6]

## Source Notes

The earlier loading-tokenization entry identifies the manual path's lack of AddedToken whitespace rules and reports Phi configurations with rstrip=true. That is historical explanatory context, not a fresh inspection of those model artifacts. [ancestor; call_815bf842cc9f4ffd882503e8794a0777]

The whole-parent Phi search found a Phi3/Phi4 prompt formatter alongside incidental calibration-text matches. The formatter places newlines after role and end markers, making token-adjacent whitespace locally relevant without establishing a reproduced Phi failure. [source; call_ebd3ca892fa949c38b70a0e5387bb3a1, call_322d4cdf3123465d85277bfb862459fb]

<a id="loading-tokenization"></a>

## Delegate special-token encoding to the backend

Previously, encode_special lazily compiled escaped extended-vocabulary spellings into a capturing regex, encoded the intervening fragments separately, and inserted special IDs directly. The patch comments out that implementation and encodes the entire text once instead. [source; call_6b4434947cc54510b3654e82f700f55a]

The backend is loaded from tokenizer.json. Separate added_tokens.json and special added_tokens_decoder entries still populate wrapper lookup dictionaries, but the new encode_special no longer consults those dictionaries. Correct special-token recognition therefore depends on the backend's loaded definitions rather than wrapper-side ID substitution. [source; call_21228fafc8c64a948a14bf95b05982d6, call_6b4434947cc54510b3654e82f700f55a]

The direct caller is encode_special_or_unspecial when special is true; encode reaches it for both scalar and batched input through encode_special_tokens. The ordinary branch is unchanged and already delegates directly when its unspecial mapping is empty. [source; call_bdd35ddfcda5441ca1cfc4ef616c69e0, call_21228fafc8c64a948a14bf95b05982d6]

A scalar transcription using '<|user|>\nhello<|end|>\n' produced ordinary fragments '\nhello' and '\n' under the old split. This demonstrates that the old wrapper sent those newlines separately from the special tokens; it does not establish what the backend emits for the replacement whole-text call. [execution; call_7bc883eb00214d9ba0676d09ff09ec70]

The tradeoff is removal of manual token-boundary enforcement in favor of backend semantics. This gives the backend complete context but does not prove equivalence for tokens represented only in the wrapper's auxiliary mappings. [inference; call_21228fafc8c64a948a14bf95b05982d6, call_6b4434947cc54510b3654e82f700f55a]

Inspection against the task diff shows that inherited decoding limitations remain: EOS filtering precedes attempted truncation, extended IDs outside backend vocabulary are filtered, and rank-two decoding returns a list even for one row. The padding fallback, ordinal-table construction, and ordinary encoding branch also remain unchanged; this patch is not a general tokenizer compatibility repair. [source; call_21228fafc8c64a948a14bf95b05982d6, call_6b4434947cc54510b3654e82f700f55a]

## Authoring-time findings — pending review

### inherited-decode-filtering (suspected; defect)

Unchanged decode_ filtering prevents its EOS truncation branch from working and discards extended IDs outside backend vocabulary before special rendering.

Trigger: Decode a sequence containing EOS followed by ordinary tokens, or request special rendering of a mapped ID at or beyond backend vocabulary size.

Expected: The explicit EOS truncation branch should discard the suffix; special rendering should retain a mapped extended token.

Actual: EOS is removed before truncation can find it, while the vocabulary-bound filter removes extended IDs before dictionary rendering.

Locations: 40fb78fa4cc156e8b8a79d7470bc5062a02ea29c:exllamav3/tokenizer/tokenizer.py — Tokenizer.decode_

Source evidence: call_21228fafc8c64a948a14bf95b05982d6, call_6b4434947cc54510b3654e82f700f55a, call_0a7e433416b34bbebdb7e15f238efa19

source_inspection: Whole-parent search finds direct calls from both rank-one and rank-two branches of decode. Both pass through the inspected filters, which the task leaves unchanged. [call_0a7e433416b34bbebdb7e15f238efa19, call_21228fafc8c64a948a14bf95b05982d6, call_6b4434947cc54510b3654e82f700f55a]. Limits: Broader generation workflows were not traced; no backend decoding ran.

scalar_transcription: With EOS=2, PAD=0 and vocabulary size 50, the filter transformed [11,2,12,0,99] into [11,12], retaining the token after EOS. [call_7bc883eb00214d9ba0676d09ff09ec70]. Limits: Python list filtering only, not repository execution.

### inherited-decode-return-contract (suspected; defect)

decode retains its mismatch between the documented one-sequence return type and rank-two handling.

Trigger: Pass a rank-two tensor with one row to Tokenizer.decode.

Expected: Its docstring promises a string when batch size is one.

Actual: The rank-two branch returns a one-element list. The internal recursive call for list inputs also uses this rank-dependent behavior.

Locations: 40fb78fa4cc156e8b8a79d7470bc5062a02ea29c:exllamav3/tokenizer/tokenizer.py — Tokenizer.decode

Source evidence: call_21228fafc8c64a948a14bf95b05982d6, call_6b4434947cc54510b3654e82f700f55a

source_inspection: Compared the docstring and rank-two return branch with the task's encode_special-only edit. [call_21228fafc8c64a948a14bf95b05982d6, call_6b4434947cc54510b3654e82f700f55a]. Limits: No tensor execution or inventory of external decode callers was performed; reach is limited here to the public method's stated input contract.

## Uncertainty and limits

No Hugging Face tokenizer, model-specific tokenization, or generation test was executed. Actual lstrip/rstrip behavior and compatibility across tokenizer files remain unverified.

The standard-library check models regex segmentation and decoding filters only; it does not execute the repository tokenizer.

The broad Phi search was truncated by calibration-text matches and does not establish an exhaustive inventory of related source.
