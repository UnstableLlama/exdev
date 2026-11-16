# 3873d40ae2734261f72aa85261ac06b6e307c1e4


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/3873d40ae2734261f72aa85261ac06b6e307c1e4) · [Evidence ledger](draft.json)

Adds persisted reference logits and KLD plotting alongside perplexity, plus loader and example-spec adjustments; inspection identifies regressions in no-reference evaluation and cache invalidation.

- [Reference-logit comparison alongside perplexity](#usage-evaluation)

## Problem

The comparison evaluator previously reported perplexity but did not compare output distributions against a reference model. [source; call_f5d2f2aa254f4df5bdc47c07ba21e969]

## Reasoning

The change reuses the evaluation forward passes to collect reference logits or compare against them, adding a distribution-level metric without replacing next-token perplexity. [source; call_2cab5598aade44d0aaa7ac023b4ac4ad]

## Impact

KLD evaluation is activated by an out_logits model specification, not by --kld. The flag selects the plotted metric. Runs without a reference specification encounter an unconditional zero-denominator calculation. [source; call_2cab5598aade44d0aaa7ac023b4ac4ad]

## Source Notes

An earlier entry describes argument-keyed evaluation caching and the then-working --clear_cache path. This change adds an argument to evaluation but not to cache invalidation. [ancestor; call_918c09e296d54276a86ba88fc72a88ae]

Issue #7, “quantizing model: undefined symbol: __cxa_call_terminate,” reports a native-extension import failure and a reporter-supplied environment workaround. Its traceback includes the inspected model.py, but that shared path does not establish a relationship to this evaluation change. [inference; call_3dfdf7dc4a404b25920a8891d8554912, call_06d9ef803679473da45de6f8449129b6]

<a id="usage-evaluation"></a>

## Reference-logit comparison alongside perplexity

main selects the last specification containing out_logits, creates that directory if needed, constructs a filename from SHA-256 of the sorted JSON data specification, and moves the selected reference model first. test_ppl writes a list of CPU logits as tensor.0, tensor.1, and so on; consumers load that same filename. The filename identifies the dataset specification rather than reference-model contents. [source; call_2cab5598aade44d0aaa7ac023b4ac4ad]

Only the first ten dataset rows contribute to KLD. Each row is one token sequence, and the comparison includes every output position, unlike perplexity, which discards the last position and scores shifted targets. Candidate and reference logits are softmaxed separately, then truncated to their smaller vocabulary width without renormalization. The KL call receives log(candidate probability + 1e-10) and reference probabilities, sums across vocabulary, and averages across positions. The epsilon avoids taking log of zero but perturbs the quantity. [source; call_2cab5598aade44d0aaa7ac023b4ac4ad, call_f5d2f2aa254f4df5bdc47c07ba21e969]

Reference collection increments the denominator once per collected row without accumulating divergence, producing a zero reference result rather than performing a self-comparison. Perplexity still processes all dataset rows. [source; call_2cab5598aade44d0aaa7ac023b4ac4ad]

The new transformers_auto_bf16 loader requests automatic device placement and bfloat16; existing loaders retain float16 by default. The supplied HF reference specification selects transformers_auto, so it remains FP16, not BF16. The unchanged forward adapter transfers input IDs to cuda:0. [source; call_87f9c19575c04147b774498bfac2767e, call_1c19185d9e46409a927439f1cfb624ac, call_aee844b71afa4312a9a3f2c4cc504803]

ExLlamaV3 loading raises max_output_factor from three to seven while retaining a 2048-token output estimate. The autosplit implementation allocates factor-minus-one extra output-shaped tensors during its placement probe; this changes two extra copies to six. It is a placement allowance, not an increase in model dimensions or an observed VRAM measurement. [source; call_11cf49bcecd34bf0abc8e9d2abcc5e9b, call_06d9ef803679473da45de6f8449129b6]

The larger placement allowance plausibly accommodates the additional float32 logits and probability tensors used by KLD, trading tighter placement for more temporary-output headroom. [inference; call_2cab5598aade44d0aaa7ac023b4ac4ad, call_06d9ef803679473da45de6f8449129b6]

The AQLM, EXL2, EXL3, GGUF, HF and VPTQ example specifications relocate model paths from /mnt/str/eval_models to /mnt/str/models. The HF specification additionally supplies the reference-logit directory. [source; call_c8e90d95e5094050a5f4b01d224ca870, call_3820e4884a234270aaa73d9db374efb6, call_7319cd6b15444969b8e173a83df9070f, call_7fbbd985c2ef43d89d54f1e92d345ec2, call_1c19185d9e46409a927439f1cfb624ac, call_b64ca43a07db481eaa528e1dfe8fc0b8]

## Authoring-time findings — pending review

### no-reference-finalization (suspected; defect)

The formerly valid perplexity-only path now reaches an unconditional KLD division with a zero denominator.

Trigger: An uncached evaluation with nonempty valid data and no model specification containing out_logits.

Expected: Return perplexity without requiring a reference model.

Actual: main passes None as logits_file; the KLD branch never increments kl_div_count, so finalization evaluates 0.0 / 0.0. collect_logits is also initialized only inside the reference branch, although division fails first.

Locations: 3873d40ae2734261f72aa85261ac06b6e307c1e4:eval/compare_q.py — test_ppl

Source evidence: call_2cab5598aade44d0aaa7ac023b4ac4ad, call_ac1f3092530b4e15bb47e9075a2a9999, call_f5d2f2aa254f4df5bdc47c07ba21e969

source_inspection: Whole-parent-tree search found main as the sole direct test_ppl caller; the task updates it to pass the optional reference filename. The CLI therefore reaches this path independently of --kld. [call_ac1f3092530b4e15bb47e9075a2a9999, call_2cab5598aade44d0aaa7ac023b4ac4ad]. Limits: Reach is established for the inspected repository caller, not external callers.

scalar_transcription: A standard-library calculation of the final zero-over-zero expression raised ZeroDivisionError. [call_166a977fec8244ed9dab00538e161e62]. Limits: The evaluation function and model forward pass were not executed.

### cache-clear-argument-mismatch (suspected; defect)

--clear_cache no longer targets the keys used by test_ppl.

Trigger: A cached result exists for the new three-argument test_ppl call and the user requests --clear_cache.

Expected: Invalidate the selected result and recompute it.

Actual: Invalidation still serializes two arguments, whereas evaluation serializes data_spec, spec and logits_file. The distinct key leaves the new cached result intact.

Locations: 3873d40ae2734261f72aa85261ac06b6e307c1e4:eval/compare_q.py — main

Source evidence: call_2cab5598aade44d0aaa7ac023b4ac4ad, call_890679db394046338e982eb1f2bacb93, call_9289fad5303b4dc6bef25f5d95ec07b1

source_inspection: Inspected main and both cache helpers. Whole-parent-tree search found this main call as the only disk_lru_cache_clear caller. [call_f5d2f2aa254f4df5bdc47c07ba21e969, call_890679db394046338e982eb1f2bacb93, call_9289fad5303b4dc6bef25f5d95ec07b1]. Limits: No shelve database was opened.

scalar_transcription: Reimplemented the inspected JSON key construction and verified that two-argument invalidation and three-argument evaluation produce unequal keys. [call_166a977fec8244ed9dab00538e161e62]. Limits: This checks serialization identity, not repository cache execution.

## Uncertainty and limits

No model inference, PyTorch KL calculation, GPU memory measurement, or safetensors round trip was executed.

The added PNG payloads were not inspected; no quantitative benchmark conclusions are drawn from them.

The ten-row sampling cap and exact choice of memory factor seven have no experimentally established rationale in the inspected evidence.

The scalar checks model Python arithmetic and cache-key construction, not repository evaluation execution.
