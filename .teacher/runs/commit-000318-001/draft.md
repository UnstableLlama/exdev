# 4265c9e1937a735861190229a524726fbd112156


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/4265c9e1937a735861190229a524726fbd112156) · [Evidence ledger](draft.json)

Adds a standalone Transformers perplexity evaluator that reuses ExLlamaV3 tokenization and the native WikiText-2 scoring protocol. Loading and memory behavior differ: three native CLI options are ignored, window edge cases carry over, and the new loop retains the previous row's log probabilities into the next forward.

- [Run the native perplexity protocol with a Transformers model](#usage-evaluation)

## Problem

The commit message calls the new Transformers perplexity test “equivalent to eval/ppl.py.” The diff adds a standalone counterpart to the native ExLlamaV3 evaluator. The parent already had a Transformers backend in eval/compare_q.py, so the addition is a simpler entry point with the native evaluator's scoring protocol, not the repository's first Transformers comparison. [source; call_7fa81d77509f4ee8b9070c64bcd1278f, call_8d5ce4c9343542babc42bf24e8ba8581, call_e1cabd4c2ed1427e9a498a12d02f93a8, call_e7891cd825f14449a5fe6d8e73438623]

## Reasoning

The two standalone scripts use the same corpus, token-window rules, and next-token statistic. That controls important comparison variables when the model directories yield the same token IDs and vocabulary cutoff. It does not make model loading, precision, attention behavior, memory use, or perplexity values equivalent. [inference; call_8d5ce4c9343542babc42bf24e8ba8581, call_e1cabd4c2ed1427e9a498a12d02f93a8]

## Impact

`python eval/ppl_transformers.py -m <model_dir>` adds a single-checkpoint WikiText-2 evaluation. It reports the directory, the Transformers backend, actual row count and width, and perplexity to six decimal places instead of the native evaluator's decoder/head bitrate report. No existing evaluator, package initializer, or dependency declaration changes. [source; call_8d5ce4c9343542babc42bf24e8ba8581, call_e1cabd4c2ed1427e9a498a12d02f93a8]

## Source Notes

The root usage-evaluation entry describes the original native WikiText-2 protocol and the comparison runner's separate backend adapters. The later memory-optimization entry explains why the native evaluator changed its logit offset to an in-place operation and explicitly released `log_probs` before the next row. [ancestor; call_19aacc37da4549808e7c636382b85fd2, call_5322c6ae33b74502b0fdd743e9f0280c]

The Transformers adapter's introduction entry describes explicit EXL3 registration, plus older concerns about eager imports, packaging, and omitted decoder multipliers. [ancestor; call_bb36785ba5814711a1d866668d7731e8, call_e26dcdc881d743ad9399c81d040228ea]

At this task boundary the package initializer no longer imports the adapter, so the earlier eager-adapter import path is not carried over; the new evaluator imports Transformers directly. The explicit package list still omits the adapter, and adapter finalization still passes neither `mcg` nor `mul1`. The new script does not register the adapter or call its finalizer, so those adapter issues are not evidence that an ordinary Transformers checkpoint fails in this script. [source; call_848e2746fce84fdc8b9a40adee615f26, call_0c20384cc2d14e6785a97b96306fc484, call_52ecf3cfd1504f10b24f5a9f74690d5d, call_8d5ce4c9343542babc42bf24e8ba8581]

Closed issue #58, “linalg.cholesky error converting OpenBuddy (Qwen3) 32B QAT,” reports NaN activations during conversion, not a failure of the new evaluator. Downtown-Case reported separate Transformers and native prequant checks; turboderp reported a successful retry and posted `eval/model_diff.py` perplexities. The inferred connection is the use of model evaluation as a diagnostic, including the inspected `model_diff.py` workflow. The discussion does not say that it prompted this commit or that the new script fixes the conversion failure. [inference; call_bde6768e6acf4df6a1447c2aa6005e82, call_a885bb183f4d4af296e8257cf1f6a1ad, call_8d5ce4c9343542babc42bf24e8ba8581]

PR #26, “Superior 3INST parameters,” reports perplexity comparisons for a proposed decoder multiplier and mentions `eval/model_diff.py`; that is an inferred overlap in evaluation practice, not a link to this new script. Issue #7, “quantizing model: undefined symbol: __cxa_call_terminate,” instead shows an extension import failure through `exllamav3/__init__.py` and `models/config.py`. The new evaluator's use of the same package is an inferred import-path overlap, not evidence of a reproduced failure. PR #4, “chore: update config.py,” is a spelling correction; its inferred overlap is only the inspected configuration file. [inference; call_d4b380bd60bf472c897e1ef0caf94fe4, call_827ada65916f4318bf8352b995ac72d2, call_56e8d328a45940108c33fdfd166e86ca, call_920c1aff27f640db9d13c51d704d489d, call_43bc83a8c340467b9228fd23cfe382b8, call_8d5ce4c9343542babc42bf24e8ba8581]

Issue #33, “Error converting model,” opens with a file-open failure during conversion compilation. Issues #34, “torch._C._LinAlgError on last layer of quant,” and #52, “Error converting moonshotai/Kimi-Dev-72B,” report Cholesky failures during quantization. Issue #42, “converting to 3.0 bpw causes error; block state has 0 inf values and 34 NaN values,” reports a bitrate-specific conversion failure. Issue #53, “Command A support,” opens as a request for support or an available quant. The inferred overlaps are references to inspected conversion or diagnostic files, not to the new evaluator's forward pass. [inference; call_57834f86d0654031afb5e7025a47d3b5, call_f874293d842c48ab865ea24d5758541d, call_a5f84722315a4d7fa742d99b95108d1a, call_0f98c19775164102bd7b9315bb4cfaa6, call_9c8528114ae24bfc952957ea28f07ef8, call_e3a30c4331354f009e5860f7ed00c580, call_8d5ce4c9343542babc42bf24e8ba8581]

Issue #49, “running the QTIP inference code,” offers installation advice for QTIP; the inferred overlap is packaging and evaluation terminology, not a shared setup procedure. Issue #50, “RuntimeError: Insufficient VRAM in split for model and cache despite remaining 1GB VRAM (exllamav3 + tabbyAPI),” quotes the exact error in the inspected native model loader. That is an inferred connection to the native loading path that the new script does not call, not evidence about Transformers auto placement. [inference; call_276d01106c8f4b0e92c62833ccac53ce, call_20bb29b9823647349e7116c5adea63b0, call_e3a30c4331354f009e5860f7ed00c580, call_8d5ce4c9343542babc42bf24e8ba8581]

<a id="usage-evaluation"></a>

## Run the native perplexity protocol with a Transformers model

Only the model forward is handed over to Transformers. `main` first calls ExLlamaV3's `Config.from_directory` and `Tokenizer.from_config`. The directory must pass ExLlamaV3's single, registered architecture check and provide a usable `tokenizer.json`; there is no fallback to Transformers tokenization. The tokenizer call uses the default no-BOS/no-EOS settings. Its `actual_vocab_size` is one above the highest ID implied by the raw and extended vocabularies, and bounds the logits slice. [source; call_8d5ce4c9343542babc42bf24e8ba8581, call_43bc83a8c340467b9228fd23cfe382b8, call_1bbca26c102d4dca99e298dc72e7bbaa, call_e3a30c4331354f009e5860f7ed00c580, call_52ecf3cfd1504f10b24f5a9f74690d5d, call_9abdfb5dee4048d2bc6e421296ee7a79]

The script always requests `device_map="auto"`. `-t/--tight` requests `torch.half` at load and then calls `model.half()` between two calls to `free_mem`, which runs garbage collection and CUDA cache cleanup. Without `--tight` it passes `torch_dtype=None` and skips the post-load cast. The comparison adapter instead explicitly selects FP16 or BF16, chooses auto placement or `cuda:0`, and computes storage statistics; the integration example patches Transformers before loading EXL3 and puts prompt IDs on `model.device`. The new evaluator does neither: it moves all evaluation IDs to CUDA without specifying a device, calls `model.forward` directly, and moves each target slice to the log-probability device before gather. [source; call_8d5ce4c9343542babc42bf24e8ba8581, call_4331731ecb404461ab92de888226e203, call_237ea39fa4094074bc1c72b099c26fc3, call_166b4d01897c47b09ec3b4c42cb8b5ea, call_e3a30c4331354f009e5860f7ed00c580]

Dataset preparation loads the raw WikiText-2 test split and joins its text with double newlines. The named shelf caches the joined text, not token IDs or scores. When the evaluators are run as scripts from the same checkout, the helper resolves `__disk_lru_cache__/get_dataset_text.lru` beside the entry script, using the same serialized `{"dataset": "wiki2"}` key as `ppl.py`, `model_diff.py`, and `prequant_test.py`. Each defines its own helper. `prequant_test.py` can prepend BOS per row; `compare_q.py` instead selects a tokenizer from its spec and caches tokenized data under `get_dataset`. [source; call_8d5ce4c9343542babc42bf24e8ba8581, call_e1cabd4c2ed1427e9a498a12d02f93a8, call_1cbe983a8cdd47e884a224ff9a121bfc, call_b5645f53ef8d42be86b17d43e2c4bb81, call_a885bb183f4d4af296e8257cf1f6a1ad, call_811a37d559914c7589403c759ceb166b, call_52ecf3cfd1504f10b24f5a9f74690d5d]

The evaluator tokenizes the joined text once and takes up to `-r/--rows` windows (default 100), each `-l/--length` tokens wide (default 2048), with a fixed 512-token stride. For a valid window of length L, it drops the last logit position and gathers the probability of each following token, giving L−1 targets. It crops vocabulary logits before float32 log-softmax, pools the gathered log probabilities over all rows, and exponentiates the negative mean. The constant `1e-10` shifts every retained logit equally; it cancels in exact log-softmax and is not a probability floor. The native evaluator uses the same formula but forwards through `flash_attn_nc`. [source; call_8d5ce4c9343542babc42bf24e8ba8581, call_e1cabd4c2ed1427e9a498a12d02f93a8]

A Python transcription of the window and target indices, given enough tokens for 100 default windows, counted 204,700 scored occurrences over 52,735 distinct corpus positions, with maximum multiplicity four. Overlap therefore changes the weight of individual corpus positions; it does not add 204,700 distinct targets. The same check computed 8,188 bytes per vocabulary column for one default row's float32 log probabilities and observed zero log-softmax difference in a three-logit scalar example with the uniform offset. [execution; call_d96b30017da146a1834a074d513082c0]

The shared CLI helper requires `-m/--model_dir` and suppresses native cache flags here. It also exposes native loading options that this script does not consume. The progress helper takes absolute completed counts: tokenization reports windows collected, while evaluation reports the zero-based row index and then sets completion to the requested count, even when fewer windows exist. The printed evaluated shape is taken from the actual tensor. [source; call_8d5ce4c9343542babc42bf24e8ba8581, call_880473878f864603acbcc7d2634ab174, call_45c706419a13409ca3d3b3419c3016d2]

## Authoring-time findings — pending review

### native-loader-flags-ignored (suspected; defect)

The new CLI advertises three native loading controls it does not use.

Trigger: Invoke the new script with `--gpu_split`, `--load_metrics`, or `--override`.

Expected: An accepted loading option should take effect as advertised or be rejected as unsupported by this backend.

Actual: The shared parser accepts all three, but the script unconditionally asks Transformers for automatic placement and never reads those arguments. The native evaluator calls `model_init.init`, which parses the split, prints metrics on request, and installs tensor overrides. The discrepancy reaches the new standalone CLI, not the existing native CLI.

Locations: 4265c9e1937a735861190229a524726fbd112156:eval/ppl_transformers.py — main and __main__ parser

Source evidence: call_8d5ce4c9343542babc42bf24e8ba8581, call_880473878f864603acbcc7d2634ab174, call_e1cabd4c2ed1427e9a498a12d02f93a8

source_inspection: Compared options registered by the shared helper with both standalone entry points and the native init consumer. [call_8d5ce4c9343542babc42bf24e8ba8581, call_880473878f864603acbcc7d2634ab174, call_e1cabd4c2ed1427e9a498a12d02f93a8]. Limits: No CLI invocation or model load was executed.

### exclusive-window-bound (suspected; defect)

The copied window loop omits a full window ending exactly at the last token.

Trigger: The final valid start `num_tokens - eval_len` is stride-aligned and the row limit would permit it; in particular, the corpus has exactly `eval_len` tokens.

Expected: Include a full window whose end equals the token count; if no complete window fits, report that explicitly.

Actual: The exclusive range stops before that start. At exact corpus/window equality the function passes an empty list to `torch.cat`, so no evaluation rows are produced. The new `main` calls this local helper; the parent search finds separate helpers in `ppl.py`, `model_diff.py`, and `prequant_test.py` with the same range, not calls into the new file.

Locations: 4265c9e1937a735861190229a524726fbd112156:eval/ppl_transformers.py — get_test_tokens

Source evidence: call_8d5ce4c9343542babc42bf24e8ba8581, call_f1fcccbb326a4bd08d23850d03e7f6d2, call_e1cabd4c2ed1427e9a498a12d02f93a8, call_a885bb183f4d4af296e8257cf1f6a1ad, call_811a37d559914c7589403c759ceb166b

scalar_transcription: The copied range emits zero starts for 2048 tokens at length 2048, and only start zero for 2560 tokens at length 2048 and stride 512. [call_d96b30017da146a1834a074d513082c0]. Limits: Only indexing was run; no tensor concatenation, tokenization, or dataset load was executed.

### one-token-length-no-targets (suspected; defect)

The CLI admits a one-token window that cannot contribute to next-token perplexity.

Trigger: Run with `--length 1`, enough corpus tokens to produce a row, and a backend that completes the forward and empty-target scoring operations.

Expected: Reject a window length below two or report that there are no scorable targets.

Actual: Target slices are empty, the count stays zero, and `main` divides by zero if it reaches the mean calculation. The copied native scoring loop has the same unchecked denominator.

Locations: 4265c9e1937a735861190229a524726fbd112156:eval/ppl_transformers.py — main

Source evidence: call_8d5ce4c9343542babc42bf24e8ba8581, call_e1cabd4c2ed1427e9a498a12d02f93a8, call_52256bd846f0443aa4e79c7ad616a836

scalar_transcription: The index check produced one row and zero next-token targets for a 10-token input and length one. [call_d96b30017da146a1834a074d513082c0]. Limits: No backend was run; a backend may fail before the mean calculation.

### nonpositive-row-count-still-appends (suspected; defect)

The row limit is checked only after appending.

Trigger: Pass `--rows 0` or a negative row count with at least one available window, assuming progress setup succeeds.

Expected: Reject an invalid count, or honor a zero-row request without scoring an unintended row.

Actual: The local helper appends one window and only then stops because `len(seqs) >= rows`. Its direct caller `main` loops over the returned shape, not the request, so it can score that row. The separate parent comparison helper checks a truthy `max_rows`, giving zero a different meaning there: no cap.

Locations: 4265c9e1937a735861190229a524726fbd112156:eval/ppl_transformers.py — get_test_tokens

Source evidence: call_8d5ce4c9343542babc42bf24e8ba8581, call_f1fcccbb326a4bd08d23850d03e7f6d2, call_52ecf3cfd1504f10b24f5a9f74690d5d

scalar_transcription: The copied loop returned start zero with a requested count of zero and an available 2048-token window. [call_d96b30017da146a1834a074d513082c0]. Limits: The check did not run Rich or the model; it isolates the append-and-stop logic.

### scoring-buffer-retained (suspected; behavior_change)

The new scoring loop does not preserve the native evaluator's tighter temporary lifetimes.

Trigger: Score at least two rows successfully, so that an earlier row has left a `log_probs` tensor bound when the next forward starts.

Expected: Release the completed row's log-probability reference before cache cleanup and the next forward, as `eval/ppl.py` does.

Actual: The reference survives the cache-cleanup call and remains bound through the next forward until the next `log_softmax` result is assigned. Separately, `.float() + 1e-10` is an out-of-place addition rather than the parent's `+=`, so it can require another full scoring-sized tensor during the addition.

Locations: 4265c9e1937a735861190229a524726fbd112156:eval/ppl_transformers.py — main

Source evidence: call_8d5ce4c9343542babc42bf24e8ba8581, call_e1cabd4c2ed1427e9a498a12d02f93a8, call_52256bd846f0443aa4e79c7ad616a836

source_inspection: Compared the assignments and deletions across both row loops. The task diff reaches the new loop through its own CLI; the parent search found no reference to the new script. [call_8d5ce4c9343542babc42bf24e8ba8581, call_e1cabd4c2ed1427e9a498a12d02f93a8, call_52256bd846f0443aa4e79c7ad616a836]. Limits: The reference lifetime is source-visible; allocator behavior, peak memory and any out-of-memory consequence were not measured.

## Uncertainty and limits

Only standard-library scalar checks and source reads were performed. No evaluator, model load, dataset fetch, PyTorch operation, or CUDA workload ran. No perplexity agreement, speed, or peak VRAM result is established.

Transformers' version-specific dtype resolution, return format, auto-placement hooks, KV-cache defaults, and support for whole-model `.half()` on particular checkpoints or dispatched models were not verified. The script does not use `AutoTokenizer`, set `use_cache=False`, or check that model logits and tokenizer IDs are compatible.

The scalar log-softmax example uses Python double precision, not the evaluator's float32 tensor arithmetic. The cache-path comparison is by source inspection; no shelf was opened and no concurrent cache behavior was tested.
