# 7989c93b6a476a918dbfff0a0b96954a79111662


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/7989c93b6a476a918dbfff0a0b96954a79111662) · [Evidence ledger](draft.json)

Adds architecture-default single-round prompt formatting without changing existing chat callers. The Gemma implementations appear to lose supplied system content and omit user-turn closure.

- [Architecture-default single-round chat formatting](#chat-templates)

## Problem

Single-request scripts lacked a model-level chat formatter. The new convenience API selects a fixed architecture-associated template, explicitly ignoring the checkpoint's actual Jinja template. [source; call_449530873adc425bbfe722fcb5b93e2b, call_e2eeb10c3ff248e19d914a7e5eb8f6d8]

## Reasoning

Putting the interface on Model permits polymorphic formatting without duplicating architecture selection in scripts. Explicit MiMo, Mistral and Qwen2 overrides also prevent those Llama subclasses from inheriting the newly added Llama3 syntax. [inference; call_e2eeb10c3ff248e19d914a7e5eb8f6d8, call_aacdc722ea5c440c8614160133b7f549, call_dd3c403510d445a9be7a81cc714c8a27, call_1f7b0f5b9e8d417f91f3a907680b8bb1, call_137f61c073e44d5a998fbe0b427d7a38]

## Impact

The change adds string-formatting methods, not automatic chat generation, tokenization or stop-condition selection. No existing default_chat_prompt callers were found in the whole parent tree, and the diff adds none. [source; call_449530873adc425bbfe722fcb5b93e2b, call_e2eeb10c3ff248e19d914a7e5eb8f6d8, call_aacdc722ea5c440c8614160133b7f549]

## Source Notes

The root usage-evaluation entry describes the original application-side chat templates and their BOS/stop policies. The Cohere-template entry records optional system turns and an open chatbot prefix. These entries establish earlier formatting interfaces, not independent validation of the new methods. [ancestor; call_9ae8527ac13543379ddd8a4ba1222cce, call_f8df80b5ebf94ad2a793cd18dbab1559]

Discussion #7, “quantizing model: undefined symbol: __cxa_call_terminate,” and closed #6, “No ROCm runtime is found, using ROCM_HOME='/usr',” report import/build failures. Issue #48, “`RuntimeError` when requesting logprobs with Gemma 3 models,” reports incompatible logits dimensions. Their relationship to this task is only an inferred shared-file overlap: their text names model.py or gemma3.py, but none describes the added formatting methods. [inference; call_c0bbb00d4a1b40718e82a042a1b333f9, call_7aa68092384343d39797c6420a47b30a, call_5de133f260464296a86c6322aaa5f710, call_e2eeb10c3ff248e19d914a7e5eb8f6d8, call_5e3f9019f8484675b921278eb8b8bd37]

<a id="chat-templates"></a>

## Architecture-default single-round chat formatting

Model.default_chat_prompt(prompt, system_prompt=None) defines the interface and raises NotImplementedError by default. Concrete implementations return text containing one user request and an unfinished assistant prefix. System content is conditional on truthiness, so None and an empty string both omit it; no default system message is supplied. [source; call_e2eeb10c3ff248e19d914a7e5eb8f6d8, call_550495a1ca2f43f8973317208ccbe6eb, call_aacdc722ea5c440c8614160133b7f549, call_137f61c073e44d5a998fbe0b427d7a38]

Cohere and Cohere2 prepend <BOS_TOKEN>, delimit system/user turns with START_OF_TURN_TOKEN and END_OF_TURN_TOKEN, and leave CHATBOT_TOKEN open. Llama uses the explicitly labelled Llama3 format: begin_of_text, role headers and eot_id after completed turns. [source; call_550495a1ca2f43f8973317208ccbe6eb, call_c88f5a60fd6c4493ac78cd0b795bab22, call_aacdc722ea5c440c8614160133b7f549]

MiMo, Qwen2, Qwen3 and Qwen3MoE use the same ChatML construction: optional system message, user message, and assistant opening, with im_end closing supplied messages. They do not prepend a BOS spelling. [source; call_dd3c403510d445a9be7a81cc714c8a27, call_137f61c073e44d5a998fbe0b427d7a38, call_1e25e84f637642f68fd838448ae5153c, call_a410231b263140ae942b990ee37d4481]

Mistral and Mixtral use <s>[INST], placing optional system text before the user text within the instruction block. Mistral3 instead puts optional system content in SYSTEM_PROMPT delimiters before its INST block. DeciLM uses <s> and Markdown-style System/User/Assistant headings; Phi3 uses <s>, role markers and end markers; GLM4 uses [gMASK]<sop> followed by role markers. [source; call_1f7b0f5b9e8d417f91f3a907680b8bb1, call_0fce228f50cb4a48a449e8592be2fe4b, call_d039e3ca382e454593876fe9eb3559ed, call_2651bb7becff407cb21ea7c780f26d98, call_62db754aa5004b49a2b1dea34e5484d9, call_9f639417db4c404e9dfb889997cd555f]

Gemma2 and Gemma3 prepend <bos> and open user/model turns. Gemma3TextModel inherits the Gemma3 implementation unchanged. The separate Gemma3VisionModel and Mistral3VisionModel are direct Model subclasses, not subclasses of the text-model implementations; this diff supplies them no chat override. [source; call_c79a289702e1430ba1ae31087ea37c52, call_5e3f9019f8484675b921278eb8b8bd37, call_4e0471cd4551444384e6348121233b96, call_0c85f824e08345d9b9b817e4c6912532]

The existing interactive chat path remains an alternative, not a consumer of this API: it chooses PromptFormat from the mode registry, formats conversation history, explicitly enables special-token encoding, supplies the template's BOS policy and separately obtains stop conditions. In contrast, callers of the new methods must arrange those steps themselves. Tokenizer.encode defaults to treating special-token spellings as text, and add_bos independently prepends a BOS ID when available. [source; call_cb14ce8684db471ab13fd4251fe94848, call_8118811f13a94ecbbacc90921d0fd030, call_3576a2374da44f3485dda89eab75cf0e, call_e2eeb10c3ff248e19d914a7e5eb8f6d8]

The convenience tradeoff is simpler single-round scripting versus checkpoint-specific fidelity and conversation management. The existing formatter registry supports history and separate stopping policies; the new interface only returns a fixed architecture-associated string. [inference; call_e2eeb10c3ff248e19d914a7e5eb8f6d8, call_8118811f13a94ecbbacc90921d0fd030, call_cb14ce8684db471ab13fd4251fe94848]

## Authoring-time findings — pending review

### gemma-system-interpolation (suspected; defect)

Both Gemma formatters append a literal placeholder instead of the supplied system text.

Trigger: Call Gemma2Model.default_chat_prompt or Gemma3Model.default_chat_prompt with a nonempty system_prompt; Gemma3TextModel inherits the latter.

Expected: Include the supplied system content in the returned prompt.

Actual: The ordinary string "{system_prompt}\n\n" is appended, so the supplied content is absent and the placeholder is visible. Whole-parent-tree search found no existing callers, so the established reach is direct use of the new API, not existing chat workflows.

Locations: 7989c93b6a476a918dbfff0a0b96954a79111662:exllamav3/models/gemma2.py — Gemma2Model.default_chat_prompt, 7989c93b6a476a918dbfff0a0b96954a79111662:exllamav3/models/gemma3.py — Gemma3Model.default_chat_prompt

Source evidence: call_c79a289702e1430ba1ae31087ea37c52, call_5e3f9019f8484675b921278eb8b8bd37, call_449530873adc425bbfe722fcb5b93e2b, call_4e0471cd4551444384e6348121233b96

scalar_transcription: Transcribed the identical Gemma string construction with None, empty and nonempty system prompts. The nonempty case retained {system_prompt} and omitted 'Follow safety rules'. [call_a80078dda88d4adc823fa7f0246923e1]. Limits: Standard-library Python string check, not execution of either repository class or a model.

### gemma-user-turn-closure (suspected; defect)

The new Gemma prompts omit the user-turn end marker present in the existing Gemma formatter.

Trigger: Format any request through the new Gemma2 or Gemma3 default_chat_prompt methods, including inherited Gemma3TextModel use.

Expected: Close the user turn with <end_of_turn> before starting the model turn, as the existing PromptFormat_gemma.format does.

Actual: The new methods append only a newline after user content and immediately start the model turn. A scalar transcription produced two turn starts and zero turn ends. No parent-tree callers of the new API were found; model-output consequences are untested.

Locations: 7989c93b6a476a918dbfff0a0b96954a79111662:exllamav3/models/gemma2.py — Gemma2Model.default_chat_prompt, 7989c93b6a476a918dbfff0a0b96954a79111662:exllamav3/models/gemma3.py — Gemma3Model.default_chat_prompt

Source evidence: call_c79a289702e1430ba1ae31087ea37c52, call_5e3f9019f8484675b921278eb8b8bd37, call_8118811f13a94ecbbacc90921d0fd030, call_449530873adc425bbfe722fcb5b93e2b

source_inspection: Compared the new methods with PromptFormat_gemma.format, which emits user content followed by <end_of_turn> and then the model prefix. [call_8118811f13a94ecbbacc90921d0fd030, call_c79a289702e1430ba1ae31087ea37c52, call_5e3f9019f8484675b921278eb8b8bd37]. Limits: Repository-local format comparison, not checkpoint-specific template validation.

scalar_transcription: Counted turn markers in the transcribed new construction for three system-prompt cases. [call_a80078dda88d4adc823fa7f0246923e1]. Limits: Checks string structure only, not tokenizer recognition or generation behavior.

## Uncertainty and limits

No model, tokenizer backend or generation pipeline was executed. The Python check transcribed the Gemma string construction only.

Checkpoint-specific template compatibility and output quality remain unverified; architecture defaults deliberately do not consult checkpoint Jinja templates.

The whole-tree literal search found no existing callers of the new method; it does not establish external or dynamically constructed usage.
