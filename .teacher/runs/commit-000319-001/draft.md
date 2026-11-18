# 5cb70f591b8286a7df902eb7a642f39a8fc80029


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/5cb70f591b8286a7df902eb7a642f39a8fc80029) · [Evidence ledger](draft.json)

Adds three opt-in safetensors exports to model_diff.py: the shared input IDs and each model’s final logits. The exports reuse the comparison’s tensors without changing its metrics. The named logits files are not directly readable as compare_q.py references, and the inherited perplexity axis-bound issue remains.

- [Save the input IDs and final logits from a model comparison](#usage-evaluation)

## Problem

The parent version of eval/model_diff.py prints layerwise and final-output diagnostics but does not save the inputs or outputs used to compute them. The patch implements the commit message’s stated change: optional exports of input token IDs and each model’s final logits. [source; call_0d053c4c0f864562ba524b20d1eacf99, call_13cfd8165e5c4814a0162ea95b7884c0]

## Reasoning

The export points reuse data already in memory. Saving IDs before the paired forward loop captures the exact batch given to both models. Saving logits after that loop captures the final states before the metrics slice off the last position for next-token scoring or turn scores into probabilities. The patch adds no extra forward pass. [source; call_0d053c4c0f864562ba524b20d1eacf99, call_13cfd8165e5c4814a0162ea95b7884c0]

Full tensors support offline analysis without rerunning either model, but are much larger than the printed summaries. A Python calculation gives 13,107,200,000 payload bytes (about 12.21 GiB) for one illustrative 100 × 2048 × 32,000 tensor at two bytes per element. This is shape arithmetic, not a measured file size or peak memory figure. [execution; call_f790a30e44cd409cbf8e741fa7c06372, call_0d053c4c0f864562ba524b20d1eacf99, call_13cfd8165e5c4814a0162ea95b7884c0]

## Impact

The three filename options are independent and default to None, so existing CLI invocations request no writes. The parser supplies all three attributes that main now reads directly. The parent-tree search found no textual model_diff references identifying another caller; a programmatic caller using a pre-change argument object would need to supply the new attributes. [source; call_13cfd8165e5c4814a0162ea95b7884c0, call_0d053c4c0f864562ba524b20d1eacf99, call_3c7219acbd904f2cbbed872e5a1deefa]

The exports are standalone artifacts, not drop-in reference files for compare_q.py. Its reference reader recognizes only tensor or a numbered tensor.0, tensor.1, … series, not the new logits key. model_diff.py adds no read-back path of its own. [source; call_13cfd8165e5c4814a0162ea95b7884c0, call_75213686ba7a49539ffa55083f3b8b53, call_f0cfb4e100664ec590f2636b6f30b17d]

## Source Notes

The initial usage/evaluation entry introduces model_diff.py as a paired, layerwise divergence diagnostic. The keep_b entry documents replacement of A’s state over a prefix. The deferred-loading and device-selection entries describe module-scoped loading and a shared device with a CPU-preferred branch. The final-metrics entry introduces the nested perplexity helper and records its vocabulary-axis bound issue, also noted by the later loading and device entries. [ancestor; call_e734641f4f09473cad3f19a1104459fd, call_e37a61b065ba4ce2b2bf47f311433ddc, call_2744c385f2ec4f67872f3743bdd114a1, call_feb52b34ff894688b1d98e7b66ab68ae, call_20109b924af645c1a5a600dc6fa7046d]

The earlier compare_q.py reference-logit entry documents the numbered CPU-logit format and recorded then-existing problems with no-reference finalization and cache invalidation. [ancestor; call_27f275df5ff2497cb71a8c3e674e385d]

In the inspected parent, compare_q.py already guards KL finalization on logits_file, initializes collect_logits outside that guard, and passes logits_file to both evaluation and cache invalidation. Those earlier observations do not describe the parent’s current wiring. By contrast, the model_diff.py perplexity axis issue is carried over: the patch adds exports before the metrics and does not change the helper or its call. [source; call_75213686ba7a49539ffa55083f3b8b53, call_cde255bcd7e842aeb912f433d6a04138, call_0d053c4c0f864562ba524b20d1eacf99, call_13cfd8165e5c4814a0162ea95b7884c0]

PR #26, “Superior 3INST parameters,” proposes a decoder multiplier and discusses model_diff.py as a starting point for KL evaluation. Issue #33, “Error converting model,” starts with a Qwen3 conversion file-open failure and later shows model_diff.py runs investigating GLM4 output. Issue #58, “linalg.cholesky error converting OpenBuddy (Qwen3) 32B QAT,” reports NaNs and a conversion failure that the participants later could not reproduce; turboderp posted a model_diff.py comparison and the reporter asked about compare_q.py for plotting KL divergence. The connection to this patch is inferred from those explicit script references. None of these discussions establishes why the export flags were added or verifies their behavior. [inference; call_311e731d267c4cf6a1ed63c4af58e7a1, call_a88b8d3ef5274cfaacbea46e167310ef, call_f53de61ad8554a8a8181141b157abc4b, call_815e9f4da84b4b9497afdcaeb7599542, call_19e94f53f179437cb15245784dd39a0b, call_13cfd8165e5c4814a0162ea95b7884c0]

Other discussion matches are contextual, not evidence of an export defect or motivation. Issue #8, “RuntimeError: shape '[5120, -1, 128]' is invalid for input of size 776524800,” concerns head quantization and reported padding fixes. PR #25, “Language layers for Mistral Small 3.1 and InternVL3,” discusses language-only conversion and checkpoint naming. Issue #34, “torch._C._LinAlgError on last layer of quant,” #42, “converting to 3.0 bpw causes error; block state has 0 inf values and 34 NaN values,” and #52, “Error converting moonshotai/Kimi-Dev-72B,” report conversion failures; #53, “Command A support,” starts as a request for model support. Their overlap is with inspected conversion code or terms such as logits and safetensors, not the new save sites. Issue #49, “running the QTIP inference code,” discusses QTIP setup and evaluation; its requirements-file mention does not establish a connection to the added safetensors import. [inference; call_0dbaed55ff0e4440b5dca522d88d6a7f, call_c7ced1c83b034091b8ae6d5bbf311073, call_501c4d1b32434cb9ad168d83e9693e35, call_a80c537a55634488b3fa616cbcd1b179, call_c6eec3dc4c524869af425c9513744e5f, call_3adde5def8d34d99853dce9cf1e25756, call_4d1e3f16a14f4e59a2856d1392b3b5a0, call_f0bcd462e0274e44b0745a38aca27a19, call_5c3596eecb40499cb11e083a4c47dc92, call_7b7a8800c2884a1b95fdc896a0b690c7, call_13cfd8165e5c4814a0162ea95b7884c0]

<a id="usage-evaluation"></a>

## Save the input IDs and final logits from a model comparison

Pass -si / --save_input_ids FILE to save input_ids, -sla / --save_logits_a FILE to save A’s logits, and -slb / --save_logits_b FILE to save B’s logits. Each requested write is a separate safetensors call. A and B use the same key, logits, in their respective files. The helper passes the filename through unchanged: it neither creates parent directories nor checks for path collisions, and it has no local write-error handler. [source; call_13cfd8165e5c4814a0162ea95b7884c0]

The shared input batch comes from model A’s tokenizer applied to Wikitext-2 raw test text. The script takes 2048-token windows every 512 tokens and caps the batch at --rows (default 100). It forwards that batch through zipped module lists, without checking that they have matching lengths or that the last paired outputs are both language-model heads. The exports are the states at that boundary, not independently recomputed predictions. A positive --keep_b replaces A’s state with a clone of B’s over the selected prefix, so the A export reflects that replacement and can be B’s output if the prefix covers every pair. [source; call_0d053c4c0f864562ba524b20d1eacf99, call_13cfd8165e5c4814a0162ea95b7884c0]

The task’s save_tensor passes dictionary keys through, names list entries tensor.0 onward, and wraps a single tensor under the supplied name or tensor. All three new call sites use the single-tensor branch. They do not move values to CPU, cast dtypes, make tensors contiguous, or attach model or tokenizer metadata. Saving IDs occurs before the first paired forward; saving A then B occurs after layerwise reporting but before perplexity, top-K and KL reporting. An exception from a save therefore stops the run at that point. [source; call_13cfd8165e5c4814a0162ea95b7884c0, call_0d053c4c0f864562ba524b20d1eacf99]

The eager save_file import adds no declared package: the parent requirements already list safetensors. The analogous compare_q.py writer collects CPU logits for its first ten rows in reference-collection mode; compare_q_logits.py runs configurable batches, moves outputs to CPU, and saves a list split into single rows. Both use numbered keys. The conversion writer instead joins paths under work_dir, saves per-module dictionaries, and saves checkpoint state after creating a staging directory. Its compiler creates the output directory and explicitly makes shard tensors contiguous before writing. None of those preparation steps is added to model_diff.py’s export path. [source; call_ccab596ba519432dabb14f9dfdddf566, call_8393acc3f27c4d69af905717947a8dcb, call_49c8b46315434b1c80424ea72df00375, call_75213686ba7a49539ffa55083f3b8b53, call_9909218058b040b8967595fb21764111, call_7b7a8800c2884a1b95fdc896a0b690c7, call_17e1da41835e4d25940704ae29be883d, call_13cfd8165e5c4814a0162ea95b7884c0]

A named-key reader can select logits or input_ids explicitly; using these outputs as compare_q.py references would instead require adapting the reader or repackaging logits under its accepted keys. Format compatibility alone would not align datasets: compare_q.py gets inputs from its own data specification, whereas model_diff.py uses A’s tokenizer and its own windows. [inference; call_75213686ba7a49539ffa55083f3b8b53, call_0d053c4c0f864562ba524b20d1eacf99, call_13cfd8165e5c4814a0162ea95b7884c0]

## Authoring-time findings — pending review

### inherited-perplexity-vocabulary-bound (suspected; defect)

The unchanged perplexity helper uses vocabulary width as the bound for sequence-position slices.

Trigger: A model_diff.py run reaches the per-model perplexity loop with more scored positions than vocabulary entries, for example 2047 positions and 1024 entries.

Expected: Accumulate every next-token prediction in the row once.

Actual: The loop ends at the vocabulary width and would cover only the first 1024 positions in that example. At width 32000, the same bounds cover all 2047 positions but issue three further empty sequence slices.

Locations: 5cb70f591b8286a7df902eb7a642f39a8fc80029:eval/model_diff.py — main.ppl

Source evidence: call_0d053c4c0f864562ba524b20d1eacf99, call_13cfd8165e5c4814a0162ea95b7884c0, call_9f5938882cc544b39a366b6a59607cc2

source_inspection: The only direct ppl call found is inside main’s row-by-model metrics loop, after the new exports; the CLI guard calls main. The other whole-tree matches are the distinct compare_q.py test_ppl. The caller removes the final position; the helper still slices axis zero using a loop bound from axis one. [call_9f5938882cc544b39a366b6a59607cc2, call_0d053c4c0f864562ba524b20d1eacf99, call_13cfd8165e5c4814a0162ea95b7884c0]. Limits: Reach is conditional on the script getting through the forward pass and any requested writes.

scalar_transcription: Modeled the chunk expression and Python sequence slices. With 2047 positions the slice lengths were [1024] at width 1024 and [2047, 0, 0, 0] at width 32000. The positive-width chunk expression simplifies to 10240. [call_f790a30e44cd409cbf8e741fa7c06372]. Limits: No Torch slicing, gathering, or metric execution.

### named-logits-not-compatible-with-reference-reader (suspected; external_compatibility)

The new named logits export is not recognized by the existing comparison evaluator’s reference reader.

Trigger: An uncached compare_q.py evaluation with nonempty data uses a successfully written model_diff.py logits file as --logits_file for a spec without out_logits.

Expected: If used as a reference artifact, the file would provide one logit row per corresponding input row.

Actual: The reader finds neither tensor nor tensor.0, so it returns an empty list. The first reference-row lookup in test_ppl then indexes that empty list.

Locations: 5cb70f591b8286a7df902eb7a642f39a8fc80029:eval/model_diff.py — main, 4265c9e1937a735861190229a524726fbd112156:eval/compare_q.py — load_tensor

Source evidence: call_13cfd8165e5c4814a0162ea95b7884c0, call_75213686ba7a49539ffa55083f3b8b53, call_cde255bcd7e842aeb912f433d6a04138, call_f0cfb4e100664ec590f2636b6f30b17d

source_inspection: The parent-tree search found compare_q.py’s test_ppl as the direct caller of its load_tensor; main passes through an explicit --logits_file. The conversion load_tensor is a separate checkpoint reader under work_dir and is not connected to the export. [call_f0cfb4e100664ec590f2636b6f30b17d, call_75213686ba7a49539ffa55083f3b8b53, call_cde255bcd7e842aeb912f433d6a04138, call_7b7a8800c2884a1b95fdc896a0b690c7]. Limits: This is an interoperability boundary, not a documented promise of the export flags or a failure when using a reader that selects logits explicitly.

scalar_transcription: A standard-library model of the reader’s key tests recognized tensor and tensor.0 but selected no entries for logits or input_ids. [call_f790a30e44cd409cbf8e741fa7c06372]. Limits: No safetensors file was opened or written.

## Uncertainty and limits

No repository inference, CUDA, or safetensors round trip ran. Device transfers inside the serializer, layout acceptance, missing-directory and existing-file behavior, write cost, and peak host or device memory were not established.

The scalar checks model key recognition, slice bounds, and payload arithmetic only. They do not establish Torch behavior on empty tensors or validate perplexity on a model.

Literal searches do not establish external or dynamic callers. No particular checkpoint with a vocabulary narrower than the scored sequence was verified.
