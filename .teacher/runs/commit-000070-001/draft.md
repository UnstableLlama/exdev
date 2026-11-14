# 9849c92b3603f7f61ca169e52d3ec1ae7fac09c0


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/9849c92b3603f7f61ca169e52d3ec1ae7fac09c0) · [Evidence ledger](draft.json)

Reduces perplexity-scoring temporaries through in-place logit offsets and earlier release of standalone log probabilities; actual VRAM savings were not measured.

- [Reduce temporary storage during perplexity scoring](#usage-evaluation)

## Problem

Both perplexity evaluators formed an out-of-place addition after converting logits to float32. The standalone evaluator also retained log_probs across row boundaries. [source; call_894a23724b734c21b69cec064a71c2f2, call_17822cb931734a2183763599c7e29dc2, call_e94dd376169c4bbb863f984c265940b3]

## Reasoning

Replacing the addition with += targets a full-sized temporary allocation; deleting log_probs after scoring shortens its lifetime before the next forward pass. [inference; call_894a23724b734c21b69cec064a71c2f2, call_17822cb931734a2183763599c7e29dc2]

## Impact

The changes preserve next-token alignment, log-softmax, target gathering and exp(-mean_log_prob). They do not change model selection or the standalone evaluator's max_output_factor=5. [source; call_e94dd376169c4bbb863f984c265940b3, call_6b986644957b4d9e9376652261f7e938, call_894a23724b734c21b69cec064a71c2f2, call_17822cb931734a2183763599c7e29dc2]

## Source Notes

An earlier entry describes per-row cleanup and CUDA cache clearing in compare_q.py. This change extends that memory-lifetime approach rather than adding a new scoring algorithm. [ancestor; call_528d5ba9430b48c7862622fa93c43a4a]

Issue #7, “quantizing model: undefined symbol: __cxa_call_terminate,” reports an extension import failure. Issue #15, “`cogito-v1-preview-qwen-32B` generates incoherent output for bpw <= 2.5,” concerns quantization quality and discusses regularization. Neither discussion establishes a connection to this evaluator-memory change. [source; call_254530ba02d742a0a861adb1d7ebb88c, call_b37a7d13fec848c1b8a2f094d927b005]

<a id="usage-evaluation"></a>

## Reduce temporary storage during perplexity scoring

Both loops discard the final prediction position, convert remaining logits to float32, and now add the existing 1e-10 offset in place. ppl.py additionally crops to tokenizer.actual_vocab_size; compare_q.py retains the backend's full vocabulary dimension. [source; call_894a23724b734c21b69cec064a71c2f2, call_17822cb931734a2183763599c7e29dc2, call_e94dd376169c4bbb863f984c265940b3, call_6b986644957b4d9e9376652261f7e938]

The 1e-10 constant is a uniform logit offset, not a probability floor. In exact arithmetic such a shift cancels in log-softmax; its original rationale is not documented in these files. [inference; call_e94dd376169c4bbb863f984c265940b3, call_6b986644957b4d9e9376652261f7e938]

For the standalone evaluator's default 2048-token row, a retained float32 scoring tensor has 2047×V elements, or 8188×V bytes. A bounded standard-library calculation verified that arithmetic and found zero difference for log-softmax of [-2, 0, 3] with versus without the uniform offset in Python float64. [execution; call_33383f181b664ebab6b1dbb86289b591]

ppl.py now deletes log_probs after accumulating the gathered target scores and before empty_cache(). Previously the local reference survived into the next iteration. compare_q.py already deleted log_probs immediately after gathering, so its only change is the in-place offset. [source; call_17822cb931734a2183763599c7e29dc2, call_e94dd376169c4bbb863f984c265940b3, call_6b986644957b4d9e9376652261f7e938, call_894a23724b734c21b69cec064a71c2f2]

The patch favors reusing the converted logits buffer and releasing completed scoring tensors, while retaining the existing out-of-place log-softmax. The standalone file's TODO for an in-place softmax remains an alternative, not an implemented optimization. [source; call_e94dd376169c4bbb863f984c265940b3, call_17822cb931734a2183763599c7e29dc2]

## Uncertainty and limits

No PyTorch evaluator or CUDA workload was executed; peak VRAM savings, allocator behavior and runtime effects remain unmeasured.

The scalar check uses Python float64, not float32 tensor arithmetic, and does not establish bitwise score equivalence or GPU allocation behavior.

In-place addition can mutate shared storage when .float() does not require a conversion; backend-specific aliasing effects were not tested.
