# 4f9851616c46007d83dcd5b75b6d0907874471ee


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/4f9851616c46007d83dcd5b75b6d0907874471ee) · [Evidence ledger](draft.json)

Adds opt-in suffix-logit computation by narrowing hidden states immediately before flagged output heads; existing callers retain full-output behavior.

- [Selecting suffix hidden states before logits projection](#models)

## Problem

Model.forward previously projected every token's hidden state into logits, even when a caller needed only a suffix. [source; call_366df40eeac74145811cab2131a32f4e, call_4845eb62814e460d80234ab0b30254d3]

## Reasoning

Selecting hidden states immediately before the logits-output module can avoid projecting unwanted positions without shortening the preceding transformer computation. [inference; call_4845eb62814e460d80234ab0b30254d3, call_12758edb302143a1b6907de46900d4fb]

## Impact

The option is opt-in through params["last_tokens_only"], not a new forward keyword argument. No existing parent-tree caller supplies the key. [source; call_4845eb62814e460d80234ab0b30254d3, call_15ebd099389a4d9db450192a15639dc4]

## Source Notes

The root models ancestor entry was read. It establishes the shared sequential model boundary, logits head, and separate prefill path on which this change builds. [ancestor; call_6f64b9d976174031b008fbe860ec384e]

Issue #7, “quantizing model: undefined symbol: __cxa_call_terminate,” reports an extension import failure; issue #6, “No ROCm runtime is found, using ROCM_HOME='/usr',” reports an installation-time traceback ending in an assertion. [source; call_ce76af9c05144fdfa74c5669262a9a71, call_94fb8ade50ff490e82df7baa37a67a5e]

Their connection to this task is only inferred from traceback references to models/model.py. Neither discussion establishes a motivation for suffix-logit selection, and the diff does not alter imports or extension loading. [inference; call_ce76af9c05144fdfa74c5669262a9a71, call_94fb8ade50ff490e82df7baa37a67a5e, call_4845eb62814e460d80234ab0b30254d3]

<a id="models"></a>

## Selecting suffix hidden states before logits projection

Inside Model.forward's module loop, a truthy module.caps["logits_output"] and truthy params["last_tokens_only"] now trigger x[..., -num:, :].contiguous(). This selects the final num positions on the penultimate axis while retaining leading dimensions and all hidden features. The selection happens before prepare_for_device and module.forward; params and the original input IDs are not shortened. [source; call_4845eb62814e460d80234ab0b30254d3, call_366df40eeac74145811cab2131a32f4e]

In LlamaModel the flagged module is the final Linear lm_head, after embedding, transformer blocks and final normalization. Module.prepare_for_device moves its input when devices differ. Linear.forward still delegates to its existing inner implementation and applies any configured softcap or post-scale. Thus the change narrows the head's input rather than slicing already-computed logits or changing the attention path. [source; call_12758edb302143a1b6907de46900d4fb, call_de1c89ef3e6c46e3bc5304385116b5a4, call_ae93086b07f44a97981f8230f8059081, call_4845eb62814e460d80234ab0b30254d3]

The parent constructors for Cohere, Cohere2, DeciLM, Gemma2, Gemma3, GLM4, Llama, Mistral3, Mixtral, Phi3, Qwen3 and Qwen3Moe all mark their Linear logits heads with this capability. Whole-tree AST inspection found no Model subclass overriding forward, including the Llama-derived Mistral, Qwen2 and MiMo classes. The two other forward definitions in models belong to image-processing modules, not Model overrides. [source; call_44fd5249af58454e88ee3f9ae0f53b01, call_decba5de548f4e6c96753da9b77b5310, call_bcbf75cbc72c48949d512f95996cef04]

Missing, None or zero values leave the sequence unchanged because the condition tests truthiness. For a positive integer num and sequence length T, suffix indexing retains min(num, T) positions; num=1 means the last position, not an empty or squeezed sequence. No matching last_tokens_only key existed in the parent tree, and near-spelling searches found no competing option. [source; call_4845eb62814e460d80234ab0b30254d3, call_15ebd099389a4d9db450192a15639dc4, call_5f70cfceeab9458c952b4e952edfb966, call_818610970c1544d39af3be6f458a8f7a, call_af170bc22e3148c09570f8fef1261e04]

A standard-library scalar transcription checked a six-position sequence: counts 1 and 2 retained [5] and [4,5], while counts 6 and 9 retained all positions. None and zero bypassed selection. It also exposed the literal unchecked behavior: -2 selected positions [2,3,4,5], and True behaved as one. For an illustrative batch of two, six positions and output width eleven, selecting two positions reduced modeled logits elements from 132 to 44. This did not execute tensor slicing, contiguous copies or the model. [execution; call_8b6d123b2a874a9fb5f3420f8ec13fd3]

Existing callers remain on their original full-output path: compare_q_exllamav3 supplies only its attention mode; ppl consumes logits aligned with shifted targets; generation_loop supplies a single input position; generator.py's draft and main calls supply cache metadata without the new key. Gemma3 and Mistral3 image-embedding calls likewise omit it. Their inspected argument dictionaries therefore require no migration. [source; call_6200674764274ab98ee37e70bb9ac02f, call_bcbf75cbc72c48949d512f95996cef04, call_4845eb62814e460d80234ab0b30254d3]

Model.prefill and autosplit sizing remain separate mechanisms. Prefill stops at the last KV-cache module; autosplit already limits dummy logits-layer input using max_output_size. The new runtime option neither changes that load-time estimate nor automatically enables itself in generation. [source; call_366df40eeac74145811cab2131a32f4e, call_4845eb62814e460d80234ab0b30254d3, call_bcbf75cbc72c48949d512f95996cef04]

The tradeoff is a potentially smaller logits projection and, across device boundaries, smaller head-input transfer, in exchange for making the suffix contiguous before projection. Earlier transformer work remains full-length. This is an expected resource benefit, not measured acceleration. [inference; call_4845eb62814e460d80234ab0b30254d3, call_12758edb302143a1b6907de46900d4fb, call_de1c89ef3e6c46e3bc5304385116b5a4]

## Uncertainty and limits

No model forward, GPU operation, output-equivalence test, or performance benchmark was executed. The scalar check models Python suffix indexing and element counts only.

The new option has no explicit type or positivity validation. Its intended contract for negative counts or non-integer values is not documented by this diff.

Whole-tree literal and AST searches cover inspected static definitions and call sites, not dynamic invocation or external callers.
