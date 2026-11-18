# 1be81eed6839845877d192b2ac1fc84f66f569f6


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/1be81eed6839845877d192b2ac1fc84f66f569f6) · [Evidence ledger](draft.json)

Adds a manually selected EXAONE4 chat template with role markers, no added BOS, and token-ID and text stops. If the tokenizer lacks an exact end-of-turn ID, the literal stop does not prevent Job construction from failing.

- [Format EXAONE4 turns in the interactive chat example](#chat)

## Problem

The interactive chat example had no EXAONE prompt mode. The parent registry has no `exaone` entry, and whole-tree literal searches found no `exaone` or `EXAONE` references. [source; call_dd3c8fe2661c48db84b013df49c94768, call_a469cf6bb54140199aabbf0cc6a25299, call_6e17d3b169f44d5b91dc49a9b8f5a1ca]

## Reasoning

The class supplies the prompt text, BOS policy and stop conditions; the registry entry makes those methods reachable without a new CLI branch. Keeping the change in the chat registry reuses the existing history, tokenizer and generation loop rather than adding a model loader or selecting a template from checkpoint metadata. [source; call_c3a49e3041b149c6b92534533a223bea, call_1e01b8cf08ab480a9a489a285977c3ed]

## Impact

`python examples/chat.py -m <model_dir> --mode exaone` selects the new formatter, and `--modes` lists it as `EXAONE (EXAONE4)`. Existing chat modes and model loading are unchanged. HumanEval has a separate prompt registry and does not gain this mode. [source; call_c3a49e3041b149c6b92534533a223bea, call_1e01b8cf08ab480a9a489a285977c3ed, call_ec1516edc33b47069c7ab1beb888a940, call_3c795896ac7c4e6abaa9fa5d3d36d86c]

## Source Notes

The root usage chapter describes the original chat registry and history-to-Job flow. The SmolLM3 entry documents the shared `default_system_prompt(think)` interface. The Dots and Command-A entries describe the same optional-system and open-assistant pattern, and note that their exact stop-token lookups are unguarded. [ancestor; call_f0c51e2bdd8f4692934ec8a3c8c1a55f, call_765115dc35214612905d7455624d0c04, call_0c09d754b51943ec9d7c50604ae0fbb7, call_52408dfca11443a2a92dc8c32f8c3915]

Issue #12, “Qwen2.5 Coder 0.5B Instruct | ValueError: Unsupported type in stop_conditions,” reports a crash after selecting `llama3` for a converted Qwen model. The traceback reaches the same `chat.py` Job construction and the same constructor error string found in the parent. That makes it an analogy for the stop-list failure, not evidence of an EXAONE failure or a fix for the report. [inference; call_35013176ad354cc999251a637aa2112a, call_1870ee429df54ba296d2af2a79577bc8, call_1e01b8cf08ab480a9a489a285977c3ed, call_5b3a8f5c1f6c4e48adb935cff6528997]

Issue #52, “Error converting moonshotai/Kimi-Dev-72B,” reports a conversion failure; a later comment suggests `examples/chat.py -mode chatml` to diagnose separate Qwen output and BOS concerns. The shared CLI and BOS decision are the only inferred connection. Issue #48, “`RuntimeError` when requesting logprobs with Gemma 3 models,” reaches the inspected `job.py` logits-append line, not the constructor's stop-list validation. Neither discussion establishes an EXAONE relationship. [inference; call_07a80243008748b7a093e8d64db1584b, call_2176806ec8284282843093552140832a, call_1e01b8cf08ab480a9a489a285977c3ed, call_38ffb6a4e66f41e9b44fefa02f20067d]

<a id="chat"></a>

## Format EXAONE4 turns in the interactive chat example

`PromptFormat_exaone.format` emits a system turn only for a truthy system prompt. It writes `[|system|]`, `[|user|]` and `[|assistant|]` with a newline after each role marker. The system prompt, each user message and each completed assistant reply are followed immediately by `[|endofturn|]`. A pending `(user, None)` leaves the assistant prefix open for generation; an empty-string reply still closes the turn. [source; call_c3a49e3041b149c6b92534533a223bea, call_1e01b8cf08ab480a9a489a285977c3ed]

The default is `You are a helpful AI assistant.` regardless of `think`; a truthy custom system prompt takes precedence. The class inherits `<think>` and `</think>` from `PromptFormat`, so the existing `--think` path can still append the opening tag when no reply prefix is supplied, and `--no_think` still passes both tags as banned strings. The formatter uses fixed role markers, not the configured console names. [source; call_c3a49e3041b149c6b92534533a223bea, call_d787e66a576e45199b5dc5d5fd6fed66, call_1e01b8cf08ab480a9a489a285977c3ed]

`chat.py` appends the pending exchange, formats the history and calls `Tokenizer.encode` with `encode_special_tokens=True`. The template returns `False` for `add_bos`, so the tokenizer wrapper does not prepend its configured BOS ID. After generation, the chat loop replaces the pending answer with the streamed reply for the next formatting pass. [source; call_c3a49e3041b149c6b92534533a223bea, call_1e01b8cf08ab480a9a489a285977c3ed, call_ed901b94886a4a52aa1236cc3215fccb]

The stop list contains the tokenizer EOS ID, the exact ID for `[|endofturn|]`, and the literal marker. `Job` separates integer stops from string stops: it checks sampled IDs directly and separately matches buffered output text. Like the parent ChatML and Dots templates, EXAONE passes the exact lookup result without checking it. The string stop is therefore an additional match route, not a fallback that makes a missing ID safe. [source; call_c3a49e3041b149c6b92534533a223bea, call_d787e66a576e45199b5dc5d5fd6fed66, call_ed901b94886a4a52aa1236cc3215fccb, call_5b3a8f5c1f6c4e48adb935cff6528997, call_38ffb6a4e66f41e9b44fefa02f20067d]

The bounded Python transcription checked the exact output for a system prompt, one completed exchange and one pending exchange: four end markers, with the final assistant prefix left open. It also checked that an empty system prompt is omitted and an empty completed reply still gets an end marker. [execution; call_96340cb302574145ac70f3dbf06c6202]

## Authoring-time findings — pending review

### exaone-missing-stop-token-id (suspected; defect)

The new EXAONE template carries over the unguarded exact-ID stop pattern. The whole-parent search found `examples/chat.py` as the direct template stop-list caller; its interactive CLI forwards the list unchanged to `Job`. Other callers of `Tokenizer.single_id` do not call the new formatter by virtue of sharing that helper.

Trigger: Select `--mode exaone`, load a tokenizer that has a valid EOS ID but no exact `[|endofturn|]` entry in either lookup dictionary, and submit a prompt that reaches Job construction.

Expected: If literal matching is to remain usable without an exact token ID, the stop list should omit the missing ID. If the ID is required, the mode could instead reject the tokenizer explicitly and name the missing marker.

Actual: `Tokenizer.single_id` returns `None`. The formatter inserts it between EOS and the literal stop string, and `Job.__init__` raises `ValueError: Unsupported type in stop_conditions` before the job is enqueued.

Locations: 1be81eed6839845877d192b2ac1fc84f66f569f6:examples/chat_templates.py — PromptFormat_exaone.stop_conditions, 5cb70f591b8286a7df902eb7a642f39a8fc80029:examples/chat.py — main, 5cb70f591b8286a7df902eb7a642f39a8fc80029:exllamav3/generator/job.py — Job.__init__

Source evidence: call_c3a49e3041b149c6b92534533a223bea, call_3652b9d2742c48dca2c6c8f5b6765b8c, call_dcda2ecc047b4d4e9aa4e3feba91c964, call_1e01b8cf08ab480a9a489a285977c3ed, call_ed901b94886a4a52aa1236cc3215fccb, call_5b3a8f5c1f6c4e48adb935cff6528997

source_inspection: Traced the exact-token lookup miss through the new stop list, the chat caller and the existing Job type check. [call_c3a49e3041b149c6b92534533a223bea, call_ed901b94886a4a52aa1236cc3215fccb, call_1e01b8cf08ab480a9a489a285977c3ed, call_5b3a8f5c1f6c4e48adb935cff6528997]. Limits: The inspected code establishes the conditional path, not whether a particular EXAONE checkpoint lacks the marker. The literal caller search does not cover external or dynamic consumers.

scalar_transcription: With empty lookup dictionaries and EOS ID 2, the model produced `[2, None, '[|endofturn|]']`; the transcribed type check raised the expected ValueError. [call_96340cb302574145ac70f3dbf06c6202]. Limits: This used Python dictionaries and a transcribed validation loop, not the repository tokenizer or Job constructor.

## Uncertainty and limits

No authoritative EXAONE4 chat template or checkpoint tokenizer was inspected. The comment about the Hugging Face template using two BOS tokens is unverified; the added formatter itself writes no BOS marker and requests no BOS insertion.

The bounded Python check transcribed string assembly and stop-list validation. It did not run the patched chat application, the checkpoint tokenizer, the generator or model inference.
