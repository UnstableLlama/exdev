# 823fd8db8502c9dabb0828ddb51ef519637a1689


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/823fd8db8502c9dabb0828ddb51ef519637a1689) · [Evidence ledger](draft.json)

Adds a manually selected Command-A chat template with a default preamble, response-boundary markers and template-controlled BOS and stopping behavior.

- [Command-A formatting through the existing chat interface](#chat)

## Problem

The chat registry offered a Cohere template but no distinct Command-A template. [source; call_81a939b9d0e0448c96a642a690550c1d, call_0af599f397c74118aa69ca59ac6b52c3]

## Reasoning

Adding the commanda registry entry reuses the existing chat selection, history, tokenization and generation pipeline rather than adding a separate application. [source; call_0af599f397c74118aa69ca59ac6b52c3, call_1f1aafa947dc4ffb9866546117b61063]

## Impact

Selecting --mode commanda supplies Command-A-specific prompt text, response delimiters and stop conditions. The existing cohere option remains unchanged; this patch adds no model architecture. [source; call_0af599f397c74118aa69ca59ac6b52c3, call_1f1aafa947dc4ffb9866546117b61063]

## Source Notes

The earlier Cohere entry establishes the role-delimited formatter this addition closely follows. The SmolLM3 entry records the shared required think argument and chat caller interface. Both entries were read. [ancestor; call_2207e403b43a432ba230e3a1a941f845, call_75d0774b627441be8eef8acda0742a99]

Issue #53, “Command A support,” requests the model and subsequently discusses quantization failures. Its relationship to this template is inferred only from the shared Command A identifier; it does not establish that this patch fixes conversion. Issue #52, “Error converting moonshotai/Kimi-Dev-72B,” also discusses chat.py and BOS selection, but its connection is merely the shared chat entry point, not Command-A formatting. [inference; call_173d03fe30be47d8b9bb06c55cff50a1, call_bf2c9bb8895344af87f247f2ffbdd1f8, call_24e4645237044ac68b9668604d3e8e69, call_0af599f397c74118aa69ca59ac6b52c3]

<a id="chat"></a>

## Command-A formatting through the existing chat interface

PromptFormat_commanda follows the Cohere SYSTEM/USER/CHATBOT turn structure, adding <|START_RESPONSE|> after every chatbot prefix and <|END_RESPONSE|> before each completed chatbot turn ends. None leaves the response open for generation; an empty-string answer still closes it. [source; call_0af599f397c74118aa69ca59ac6b52c3, call_81a939b9d0e0448c96a642a690550c1d]

A truthy system prompt causes the formatted text to begin with literal <BOS_TOKEN> and a SYSTEM turn. add_bos also returns True. chat.py enables special-token encoding, and Tokenizer.encode independently prepends its configured BOS ID when present. Thus two initial BOS tokens depend on the literal marker being recognized as BOS; a falsey system prompt omits the literal marker. [source; call_0af599f397c74118aa69ca59ac6b52c3, call_1f1aafa947dc4ffb9866546117b61063, call_3aff0e3b5aa74719ad0d1691c2a4c258]

The abridged default preamble identifies Command and Cohere, labels the information cutoff June 2024, and supplies conversational, formatting and reasoning instructions. June 2024 and the ten-item list limit are prompt content, not runtime checks. The required think argument is accepted but unused; a truthy custom --system_prompt replaces the default. The inherited think tags remain available to chat.py. [source; call_0af599f397c74118aa69ca59ac6b52c3, call_81a939b9d0e0448c96a642a690550c1d, call_1f1aafa947dc4ffb9866546117b61063]

Stopping supplies EOS, exact IDs for END_RESPONSE and END_OF_TURN_TOKEN, and the literal end-of-turn string. Like existing template callers, it performs single_id lookups without a token-existence guard. single_id returns None when neither dictionary contains the marker, so these ID entries require a suitable tokenizer; the string entry does not replace the lookups. [source; call_0af599f397c74118aa69ca59ac6b52c3, call_7c351c6aad614a96a84ec4fa8c7b8c0a, call_81a939b9d0e0448c96a642a690550c1d, call_3aff0e3b5aa74719ad0d1691c2a4c258]

The inspected chat caller builds history as user/answer pairs, appends a pending pair, formats and encodes it, then passes the template's stop conditions to Job. The new class agrees with that existing interface; it does not require changes to the caller or existing subclasses. [source; call_38a4d34a24a5448c9261dd7fa9be4e96, call_1f1aafa947dc4ffb9866546117b61063, call_81a939b9d0e0448c96a642a690550c1d, call_0af599f397c74118aa69ca59ac6b52c3]

A bounded scalar transcription checked a system turn, completed exchange and pending exchange: one literal BOS, five turn starts, four turn ends, two response starts and one response end. It also checked omission of the literal BOS for an empty system prompt and closure of an empty-string answer. [execution; call_4465852f4d1d4113b3a2947b51a55532]

## Uncertainty and limits

No Command-A tokenizer, authoritative checkpoint template or model inference was executed or inspected. The comment asserting that the HF template uses double BOS is not independently verified.

The Python check transcribed string serialization only; it did not execute the patched class, tokenizer, stop handling or generation pipeline.
