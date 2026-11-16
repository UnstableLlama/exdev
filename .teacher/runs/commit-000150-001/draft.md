# 1e1754787e52f416252a36ea3ebf7177d2e11f2a


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/1e1754787e52f416252a36ea3ebf7177d2e11f2a) · [Evidence ledger](draft.json)

Makes HumanEval BOS handling template-specific, retaining automatic insertion only for explicit raw mode.

- [Template-specific HumanEval BOS handling](#usage-evaluation)

## Problem

HumanEval previously requested automatic BOS insertion for every prompt format, including Gemma's template, which already begins with <bos>. [source; call_100acfe017194c2e8c4234c442d1511e]

## Reasoning

The change moves BOS selection into model-specific prompt text rather than applying one tokenizer-level policy to all formats. [inference; call_b269d990842b4a8483ffdd1ce9a36bef]

## Impact

Automatic BOS insertion remains enabled only for explicit --prompt_format raw. Omitting the option selects the separate unwrapped-completion path and now disables automatic BOS insertion. [source; call_b269d990842b4a8483ffdd1ce9a36bef, call_100acfe017194c2e8c4234c442d1511e]

## Source Notes

The parent entry describes the earlier Qwen3 preset integration with BOS still requested during encoding. [ancestor; call_0f274fbdd62d4f789331d414c983af06]

Closed issue #16, “RuntimeError: CUDA error: invalid configuration argument,” concerns conversion and tokenizer truncation, not HumanEval BOS placement; it supplies no direct validation of this change. [source; call_4f0e3bca90824ddeb41c9e6c3b24435e]

<a id="usage-evaluation"></a>

## Template-specific HumanEval BOS handling

The templates gain these leading markers: granite and reka use <|endoftext|>; llama and mistral use <s>; llama3 uses <|begin_of_text|>; deepseek uses <｜begin▁of▁sentence｜>. Gemma retains its existing <bos>, while chatml and qwen3 gain no BOS text. [source; call_b269d990842b4a8483ffdd1ce9a36bef, call_100acfe017194c2e8c4234c442d1511e]

main substitutes the problem into the selected template, encodes it once, and passes the resulting input_ids to each sample Job. Special-token encoding stays enabled. Tokenizer.encode routes this through encode_special, whose underlying tokenizer call disables automatic special-token addition; the wrapper independently prepends bos_token_id only when add_bos is true and that ID exists. [source; call_100acfe017194c2e8c4234c442d1511e, call_b269d990842b4a8483ffdd1ce9a36bef, call_166e39fadc4d4369ae705a6843959404]

This removes the extra wrapper-inserted BOS from Gemma and avoids imposing one on ChatML/Qwen3. For the six newly prefixed templates, preservation of the old token sequence depends on the literal marker encoding to the same configured BOS ID; source inspection alone cannot establish that equivalence. [inference; call_b269d990842b4a8483ffdd1ce9a36bef, call_166e39fadc4d4369ae705a6843959404]

A standard-library check extracted the parent templates and modeled the patch: all problem-placeholder counts were preserved, and only explicit raw retained automatic BOS. The no-option path remained distinct from raw. [execution; call_d20b3becc3ed455798f1ceb6d14ab47f]

## Uncertainty and limits

No real tokenizer, model generation or HumanEval scoring was executed. Recognition of each literal marker depends on the selected tokenizer.

The bounded Python check models template edits and flag selection; it does not establish token IDs, token counts or score improvements.
