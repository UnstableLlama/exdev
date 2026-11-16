# a19538cf1e3b3f46ccdb347ff076fd4838a4910b


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/a19538cf1e3b3f46ccdb347ff076fd4838a4910b) · [Evidence ledger](draft.json)

Corrects ExLlamaV3 comparison head accounting and padded-logit normalization, and runs the comparison entry point in inference mode.

- [Correct head accounting and vocabulary normalization](#usage-evaluation)

## Problem

The comparison adapter classified only the exact key lm_head as the output head and passed all output columns into perplexity normalization, including any padding. [source; call_bf44fbdacef24504a44bc0f598d8524d, call_bc7cad2e5c394690bcc57124c01d5d6e]

## Reasoning

The patch broadens head recognition, masks out-of-vocabulary logits, and decorates the comparison entry point with torch.inference_mode(). These address accounting, scoring, and evaluation context independently. [source; call_4f8ca40724b348d3b67b65a6ff50c674, call_ee6e57891c104570bedcb02034afe839]

## Impact

Existing cached results can bypass the corrected evaluation: the disk cache keys results by arguments rather than implementation. The existing --clear_cache option clears the selected test_ppl entries before evaluation. [source; call_fa1da573fa4349d5be9c21882e4d156e, call_bc7cad2e5c394690bcc57124c01d5d6e]

## Source Notes

The earlier evaluator entry notes that compare_q.py retained the backend's full vocabulary dimension. This patch changes the ExLlamaV3 adapter's contribution without changing the shared scoring formula. [ancestor; call_e1cc32ee0fbb48269ad94d2fd3d249ac]

Issue #34, “torch._C._LinAlgError on last layer of quant,” reports a conversion-time Cholesky failure and includes linear.py in its traceback. That shared source path does not establish a relationship to these evaluation changes. [inference; call_753d61ad76e44f2291e0c7c647bb4f64, call_ee6e57891c104570bedcb02034afe839]

<a id="usage-evaluation"></a>

## Correct head accounting and vocabulary normalization

get_storage_info now tests module.key.endswith("lm_head") before its general Linear branch. A prefixed head therefore contributes to head_bpw and head_numel rather than decoder totals. Tensor storage is counted in bits as eight times element size times element count; the returned layer bitrate remains total decoder bits divided by decoder weight count. [source; call_ee6e57891c104570bedcb02034afe839, call_bf44fbdacef24504a44bc0f598d8524d]

fwd_exllamav3 retains CPU input transfer and flash_attn_nc forwarding, then overwrites output[..., config.vocab_size:] with negative infinity. It preserves the output shape while excluding those columns from the shared log-softmax denominator. The boundary is the configured vocabulary size, not a tokenizer-derived count. [source; call_ee6e57891c104570bedcb02034afe839, call_bf44fbdacef24504a44bc0f598d8524d, call_5fb51071ab834a9690231a5c9b475cc9, call_bc7cad2e5c394690bcc57124c01d5d6e]

Linear rounds dimensions upward to multiples of 128 by default; 128 is an alignment unit, not a vocabulary limit. Masking rather than slicing leaves this padded representation intact while preventing finite padded logits from competing with valid tokens. [inference; call_b4df0cb8c2ab4a4e81d82b8cb3a1cfb3, call_ee6e57891c104570bedcb02034afe839]

A bounded scalar example used vocabulary size 129, padded width 256, and zero logits. Masking the 127 extra columns changed one-token perplexity from approximately 256 to 129. The same check confirmed that model.lm_head changes classification while lm_head remains recognized. [execution; call_012d5a2d5ace416f94cd1fdba81722f6]

The inference-mode decorator is applied to main, whose evaluation loop invokes test_ppl for each model specification. It is not added to test_ppl or the adapter itself, so direct calls to those functions do not acquire this new context through their own decorators. [source; call_4f8ca40724b348d3b67b65a6ff50c674, call_bc7cad2e5c394690bcc57124c01d5d6e, call_bf44fbdacef24504a44bc0f598d8524d]

## Uncertainty and limits

No PyTorch or GPU evaluation was executed; inference-mode memory savings and model-level perplexity changes remain unmeasured.

The numerical check models normalization using Python float64, not tensor execution, CUDA precision, or model outputs.

Suffix matching supports prefixed head names, but the inspected model declarations use the exact lm_head key; a concrete affected prefixed checkpoint was not established.
