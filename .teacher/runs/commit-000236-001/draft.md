# 9a24e0ce520af941a309765338bf291f3d2b9e97


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/9a24e0ce520af941a309765338bf291f3d2b9e97) · [Evidence ledger](draft.json)

Defaults the multimodal example to Mistral3 and adds matching EOS stopping, while retaining Gemma3 selection and an inherited Mistral prompt-template typo.

- [Selecting Mistral3 in the image-description example](#multimodal)

## Problem

The multimodal example selected only Gemma3. Selecting Mistral also needed a stop-condition branch: the existing prompt formatter supported Mistral, but get_stop_conditions did not. [source; call_43dff8bcba374b9784921d6ea6ff2bc6, call_4f6b8d8f61a0419788a1f69cceaeea88]

## Reasoning

The edits work together: the new default selects mistral3, its branch selects the mistral prompt format and a local Mistral Small 3.1 checkpoint, and the shared helper now returns tokenizer EOS for that format. Gemma3 remains selectable. [source; call_7ecec67429af44e5b7079b1399ce08a2, call_4f6b8d8f61a0419788a1f69cceaeea88]

## Impact

Both streaming Job creation and non-streaming generate receive the new EOS list. The other discovered helper callers—banned_strings.py, dynamic_gen.py, generation_loop.py and generator.py—select llama3 and retain their existing results. [source; call_6f9b181415b64adcab1304e034d17858, call_fa1c1ce048ef4bc4baec928249f159b1, call_528503d0b2e04bddb4d98433fae07319, call_537408dedcc64ac3a98859fea5bb8580, call_f7e36c0a1b984d9583d7ca3a2bd3d167, call_1d48d25878b048bd8cb1af3dd8e0b6fb]

## Source Notes

The original multimodal entry establishes the paired image-alias/embedding flow. The original usage entry records both the missing Mistral stop branch and an extra literal 'n' in its prompt template. This change fixes the former but carries over the latter. [ancestor; call_c522b67789ba4950bea39898d62063ea, call_4844f7e5c21546d4b8248a58248899ca]

PR #25, “Language layers for Mistral Small 3.1 and InternVL3,” discusses language-only support and concerns about preserving future multimodal components. Its relationship to this example update is contextual inference from the shared Mistral Small 3.1/component-model subject, not an explicit upstream link. [inference; call_eeafd92f97b64aa9981219364ff7a265, call_4f6b8d8f61a0419788a1f69cceaeea88]

<a id="multimodal"></a>

## Selecting Mistral3 in the image-description example

The unchanged pipeline loads text and vision components from one configuration, turns each image into an embedding object, and places its text alias before the instruction. Streaming supplies the embeddings to both tokenizer.encode and Job; non-streaming passes them to generate. The 8192-token cache and 500-new-token cap remain example settings. [source; call_6f9b181415b64adcab1304e034d17858, call_4f6b8d8f61a0419788a1f69cceaeea88]

The existing Mistral3 vision implementation preprocesses images, forwards them noncausally with spatial positions and precomputed rotary frequencies, and packages projected vectors with [IMG_BREAK] row separators and [IMG_END]. Configuration requires PixtralImageProcessorFast and matching model/preprocessor patch sizes; selecting this example does not add architecture support or relax those requirements. [source; call_7dd3fa03ceba48978f598f678ad7323f, call_4f6b8d8f61a0419788a1f69cceaeea88]

Unlike the Gemma helper, the selected Mistral template includes the supplied system prompt. It also retains the literal 'n' before the image-alias/instruction string. [source; call_43dff8bcba374b9784921d6ea6ff2bc6, call_6f9b181415b64adcab1304e034d17858]

Executing the parent common.py helper with synthetic strings produced '<s>[INST] SYS\n\n nIMAGE\nDescribe the image.[/INST]'; its parent Mistral stop lookup returned None. [execution; call_617a9c74ed4c4bfdbbf74c4c98271ba6]

## Authoring-time findings — pending review

### mistral-template-prefix (suspected; defect)

The newly selected Mistral prompt path carries over an unintended-looking literal 'n' before user content.

Trigger: Run multimodal.main with the new mistral3 default and reach prompt formatting.

Expected: Insert the supplied image aliases and instruction without an unrelated character prefix.

Actual: format_prompt returns a space and literal 'n' immediately before the supplied user content. This affects both generation branches; the other discovered example callers currently select llama3.

Locations: 9a24e0ce520af941a309765338bf291f3d2b9e97:examples/common.py — format_prompt

Source evidence: call_43dff8bcba374b9784921d6ea6ff2bc6, call_4f6b8d8f61a0419788a1f69cceaeea88, call_6f9b181415b64adcab1304e034d17858, call_6ac8e9117b394dd38c8a1a8c440a9ede

repository_execution: Executed the unchanged parent prompt formatter with synthetic system and image/instruction strings. [call_617a9c74ed4c4bfdbbf74c4c98271ba6]. Limits: Confirms string construction only, not tokenizer behavior or model-quality impact.

## Uncertainty and limits

No checkpoint loading, image preprocessing, tokenization or GPU generation was executed. The local checkpoint path and its compatibility remain unverified.

The bounded execution checks the parent prompt helper only; it does not establish generated response quality or successful EOS termination.
