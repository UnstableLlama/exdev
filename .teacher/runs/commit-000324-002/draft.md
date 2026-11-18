# 6171f9af3d4b477ccd43fdf8d7172d40fc770a38


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/6171f9af3d4b477ccd43fdf8d7172d40fc770a38) · [Evidence ledger](draft.json)

Replaces ChatML in the Dots, dense Ernie and MoE Ernie single-turn helpers with each family's prompt format. Interactive chat modes are unchanged, and the Dots helper still omits the system block supplied by the pinned checkpoint templates.

- [Format single-turn Dots and Ernie prompts without ChatML](#chat)

## Problem

All three model-level `default_chat_prompt` overrides returned ChatML-style `im_start`/`im_end` blocks. The pinned Dots templates instead use dedicated system, user and response markers; the pinned Ernie PT templates use a begin-of-sentence marker and `User: `/`Assistant: ` labels. The mismatch was in the single-request helper, not in the existing interactive chat modes. [source; call_f8823f58596a4cce8c10dc2eb2f9dfb4, call_27de021cf5f74b859c045d30c9b36b26, call_a27ff80d77994795bb947f8d94919689, call_92bea65e507240bba577fc0a08d58628, call_55b5e30bb3214099b326685cf695f232, call_d2ce101610b0407dadd092b128e7947d]

## Reasoning

The new strings match the existing interactive formatters for a single pending turn given the same system text. That supports reading the fix as alignment with each family's prompt syntax, not as an attempt to reproduce every checkpoint's template policy. The base helper explicitly documents that it does not consult the checkpoint's Jinja template. [inference; call_150f676cc9da49dbad9fbb985e8224ef, call_f8823f58596a4cce8c10dc2eb2f9dfb4, call_27de021cf5f74b859c045d30c9b36b26, call_a27ff80d77994795bb947f8d94919689, call_d2ce101610b0407dadd092b128e7947d, call_d9d699e0c4a442abbdbd09310e801ba7]

## Impact

Direct callers of the three overrides get different prompt strings with the same signature and return type. The only literal call found in the whole parent tree was `examples/imgsearch.py`: it formats an image alias plus a stripped question, then passes the text and image embeddings to the tokenizer. That script first requires a `vision` component; all three affected configurations expose only `text`, so its normal path does not reach these overrides. The literal search does not establish reach for dynamic or external callers. [source; call_b68a7d5e164e4a87bb77bf98e98393f6, call_405fff31d1304c41b6432f63b5a0d5da, call_15f7b30aebf9466480746a766f94d2e5, call_8f611d1d094c42819eea327ec125b261, call_1f0bebf402584ef593ed84697f341d95, call_a9eb49be5b7a4f6783dbc93a2f4128c2]

`examples/chat.py --mode dots` and `--mode ernie` already select separate history-aware formatters. The loop uses their special-token encoding, BOS settings and stop conditions, not the model helper. This patch changes none of those settings, nor model loading, tensor lookup or architecture dispatch. [source; call_767af39fce1a48a6a650d1fd8330d3ca, call_d2ce101610b0407dadd092b128e7947d, call_f8823f58596a4cce8c10dc2eb2f9dfb4, call_27de021cf5f74b859c045d30c9b36b26, call_a27ff80d77994795bb947f8d94919689]

## Source Notes

The Dots and Ernie model introduction entries recorded the ChatML mismatch; the separate Dots and Ernie chat-template entries described the pending-turn convention already in use. The later Ernie routed-expert precision entry concerns forward computation, not prompt construction. [ancestor; call_c76e70b0026542bfbc9696719aeb65e4, call_0ed0c13bd8244359a5e143e681d8e1db, call_f214a3d54dd64038ac71d933df61f060, call_842cf0c1fe2f4b6a9ddbf141ea864fdc, call_97131878a75f4003a36ce34a4f3666b5]

Issue #51, “dots.llm1 support,” is louiehelm's architecture-support request; turboderp's reply reports implementation support and a first-layer quantization workaround. The shared Dots model is an inferred connection, not a report of this prompt defect. Closed issue #61, “Run ERNIE-4.5-300B-A47B-PT 2.25bpw with 5x20G 3080 got 'Insufficient VRAM',” is buliaoyin's loading report. The inferred connection is the Ernie MoE family and the explicit `examples/chat.py -mode ernie` command. Its traceback stops at model loading, before prompt formatting, and the reporter says the allocator workaround suggested by turboderp worked. [inference; call_d49c00582dc94bd2906fda0414316366, call_2007db842d544d8c976a34eea28ce033, call_767af39fce1a48a6a650d1fd8330d3ca, call_a9eb49be5b7a4f6783dbc93a2f4128c2]

Issue #7, “quantizing model: undefined symbol: __cxa_call_terminate,” reports a native-extension import error; the overlap is the `models/model.py` import traceback, not prompt behavior. Issue #52, “Error converting moonshotai/Kimi-Dev-72B,” begins as a conversion failure; a later comment suggests `examples/chat.py -mode chatml` to investigate a separate Qwen generation complaint. The inferred overlap is the same example and its independent template dispatch, not a Dots or Ernie reproduction. [inference; call_8fb2c9b13e0c4f44948edf6cb3a41a97, call_a1866869807741caba711f5cf806fc72, call_15f7b30aebf9466480746a766f94d2e5, call_767af39fce1a48a6a650d1fd8330d3ca]

<a id="chat"></a>

## Format single-turn Dots and Ernie prompts without ChatML

`Dots1Model.default_chat_prompt` encloses a truthy system prompt in `<|system|>…<|endofsystem|>`, wraps the user text in `<|userprompt|>…<|endofuserprompt|>`, and ends at `<|response|>`. It inserts no whitespace. Both pinned Dots tokenizer templates use these delimiters, but the helper still omits the system block for a missing or empty system prompt. The base checkpoint emits an empty block when no system message is supplied; the instruction checkpoint inserts “You are a helpful assistant.” [source; call_f8823f58596a4cce8c10dc2eb2f9dfb4, call_2f49bfd69a574d46875feba6f395b6be, call_92bea65e507240bba577fc0a08d58628]

`Ernie4_5Model.default_chat_prompt` and `Ernie4_5MoEModel.default_chat_prompt` now build identical strings: `<|begin_of_sentence|>`, then truthy system text followed by a newline, then `User: ` plus the user text and a newline, then `Assistant: ` with its trailing space. That is the pending-turn form in the ERNIE-4.5-0.3B-PT, ERNIE-4.5-21B-A3B-PT and ERNIE-4.5-300B-A47B-PT templates with no system message or a nonempty one. An explicitly empty system message contributes a newline in those templates but not in the helper. The tokenizer metadata distinguishes the begin-of-sentence marker (`cls_token`) from BOS (`<s>`); the helper emits the former as text and does not add the latter as a token. [source; call_27de021cf5f74b859c045d30c9b36b26, call_a27ff80d77994795bb947f8d94919689, call_55b5e30bb3214099b326685cf695f232, call_3e98517d655d4746ba12d61829225135, call_91214fed24d84b02b9babdb9a0e79fed]

A standard-library transcription compared the new strings against the corresponding single-turn template branches. With nonempty system text both families matched. With no system message, Ernie matched and Dots instruction did not. With an explicitly empty system message both differed. This checked text and whitespace, not token IDs. [execution; call_db5fe0011c994f5f9fbc4fec1cba107f]

The pinned configs for `dots-studio/dots.llm1.base` and `dots-studio/dots.llm1.inst` each map to the same Dots text class: both specify width 4096, 32 query and KV heads, and 62 layers. Both use the head-width fallback and override the dense-prefix, shared-expert and selected-expert defaults. The formatter does not branch on these dimensions or on their different configured EOS IDs. [source; call_1951b5e458f9497f9ba007860d66e851, call_82215676ce714faa8766ac8dc26d65ff, call_8f611d1d094c42819eea327ec125b261, call_f8823f58596a4cce8c10dc2eb2f9dfb4]

The pinned `baidu/ERNIE-4.5-0.3B-Base-PT`, `-Base-Paddle`, `-PT` and `-Paddle` configs each map to the dense class: width 1024, 16 query/two KV heads, 18 layers, explicit head width 128 rather than the fallback, and tied embeddings. None of those values is read by the formatter. [source; call_2c9741df2da24384b892dc9f9355efbe, call_26cb37df6c244f1397eb5ed1974900b2, call_283f7f7b786d423ab4b78b35b9e24cf6, call_e2afabdb4f794c3bad24ecd7c85ac185, call_1f0bebf402584ef593ed84697f341d95, call_27de021cf5f74b859c045d30c9b36b26]

The pinned `baidu/ERNIE-4.5-21B-A3B-Base-PT`, `-Base-Paddle`, `-PT` and `-Paddle` configs each map to the MoE class with width 2560, 20 query/four KV heads, 28 layers, one dense-prefix layer and two shared experts. The pinned `baidu/ERNIE-4.5-300B-A47B-2Bits-Paddle`, `-Base-PT`, `-Base-Paddle`, `-FP8-Paddle`, `-PT`, `-Paddle` and `-W4A8C8-TP4-Paddle` configs each map to that class with width 8192, 64 query/eight KV heads, 54 layers, three dense-prefix layers and the zero shared-expert default. All omit `head_dim` and use the same fallback rule. The MoE helper is independent of these values and does not add support for any format declared by the quantized configs. [source; call_6b2ef8db0b504f7d82a137e691b8409f, call_81483394e0654956bf7fa520dc7076b2, call_caab878a2e004968bf701e3672c04afa, call_c3fe9248411f49b5899fe5eb5f488be4, call_5a5e7ed2c8534a7a886f8442bc352cdc, call_a107007159ee4c10b4e5ea432b1c19db, call_bd121c23ec4b4ddd869470832a61481a, call_05457700e1024574a939ba7c28650007, call_e12f8b569a474b35abcadc6e302a0e96, call_601a5515f73c433fbde6be3e62b414db, call_9a6d94eecd164bfb9a6989ceb4e03644, call_a9eb49be5b7a4f6783dbc93a2f4128c2, call_a27ff80d77994795bb947f8d94919689]

## Authoring-time findings — pending review

### dots-system-default-still-differs (suspected; external_compatibility)

The Dots fix removes the ChatML marker mismatch but does not reproduce either pinned checkpoint's system block when no system prompt is supplied.

Trigger: Call `Dots1Model.default_chat_prompt("U")` and compare with the pinned Dots single-user-message template with generation prompting enabled.

Expected: For checkpoint-template parity, the base variant would prefix `<|system|><|endofsystem|>` and the instruction variant would prefix `<|system|>You are a helpful assistant.<|endofsystem|>`.

Actual: The helper begins directly with `<|userprompt|>`. This is reachable through a direct call to the helper, but the only repository caller found by literal search requires a vision component that Dots does not provide. The interactive Dots formatter does not use the helper.

Locations: 6171f9af3d4b477ccd43fdf8d7172d40fc770a38:exllamav3/models/dots1.py — Dots1Model.default_chat_prompt

Source evidence: call_f8823f58596a4cce8c10dc2eb2f9dfb4, call_2f49bfd69a574d46875feba6f395b6be, call_92bea65e507240bba577fc0a08d58628, call_b68a7d5e164e4a87bb77bf98e98393f6, call_405fff31d1304c41b6432f63b5a0d5da, call_8f611d1d094c42819eea327ec125b261, call_15f7b30aebf9466480746a766f94d2e5, call_767af39fce1a48a6a650d1fd8330d3ca

source_inspection: Compared the unchanged truthiness guard with both checkpoint template branches and inspected the direct caller and interactive formatter path. [call_f8823f58596a4cce8c10dc2eb2f9dfb4, call_2f49bfd69a574d46875feba6f395b6be, call_92bea65e507240bba577fc0a08d58628, call_d9d699e0c4a442abbdbd09310e801ba7]. Limits: The base API does not promise Jinja parity. This observation is a concrete output difference, not an observed generation failure.

## Uncertainty and limits

The Python check modeled string construction only. No repository model, tokenizer, Jinja renderer or generation loop was run; token sequences, stopping behavior and generation quality were not measured.

Checkpoint-template comparison covered the two pinned Dots variants and the three pinned Ernie PT instruction variants named in the chapter. Architecture config matches do not establish equivalent tokenizer templates or weight-format compatibility for other variants. The changed helper does not use checkpoint tensors.
