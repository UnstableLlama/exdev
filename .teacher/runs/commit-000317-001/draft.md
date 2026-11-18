# c09f809876902c2cd9eedad463eecfa2c97977ed


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/c09f809876902c2cd9eedad463eecfa2c97977ed) · [Evidence ledger](draft.json)

Adds `-l` / `--length` to standalone perplexity evaluation, keeping the 2048-token default and 512-token stride. The flag changes scoring windows, but not the loader's memory estimate or LongRoPE length override, and it does not validate unusable widths.

- [Choose the token window length for standalone perplexity evaluation](#usage-evaluation)

## Problem

The standalone Wikitext-2 perplexity CLI let users set the number of rows, but not the number of tokens per row. Its token-window helper already accepted a width; the CLI always used the helper's 2048-token default. [source; call_49ec2c61864f4b02ae61a06943d08e72, call_1b673ffe0b6547b79c4476c7f68b9eda]

## Reasoning

The patch implements turboderp's stated change, “ppl.py: Add length argument,” by forwarding the integer `-l` / `--length` value as `eval_len`. The new CLI default is the old helper default, so omitting the flag preserves the window selection. The flag changes the evaluation window, not the model's configured context capacity. [source; call_0f26c0b599e64c18b5da145554c280d5, call_1b673ffe0b6547b79c4476c7f68b9eda, call_49ec2c61864f4b02ae61a06943d08e72]

## Impact

A different length changes both the context available to each prediction and the mix of corpus positions scored. Keep length and row count fixed when comparing model scores under the same windowing protocol; matching the row count alone does not match the number or weighting of targets. [inference; call_49ec2c61864f4b02ae61a06943d08e72, call_1b673ffe0b6547b79c4476c7f68b9eda, call_9370f4aa012a459c93e72012573417ca]

The script's parser always supplies `args.length`, but a programmatic caller passing an old namespace without `length` would now fail at the dataset call, after model initialization. Whole-parent literal searches for `get_test_tokens`, `ppl.py`, `eval.ppl`, and `import ppl` found the script's own call and separate helpers in other scripts, not an in-tree importer or external caller. [source; call_1b673ffe0b6547b79c4476c7f68b9eda, call_49ec2c61864f4b02ae61a06943d08e72, call_8be93422adf74b158c5600ee35845211, call_2fd7cea374bc447e9190be1b7e9fbe0c, call_eff494645e114c5a994a79ebab4e61b5, call_512513cf3c39456ca9205f69db0c5924]

## Source Notes

The initial preview's evaluation chapter records the original 2048-token, stride-512 Wikitext protocol and its repeated scoring of overlapping targets. The later evaluator-memory entry records in-place logit addition and earlier release of `log_probs`, not a new perplexity formula. [ancestor; call_b1f0ad873a7848db88fea5ae7e6d44c5, call_6d8b1a4c47be42d38c2b2d9bfe3a0112]

Issue #50, “RuntimeError: Insufficient VRAM in split for model and cache despite remaining 1GB VRAM (exllamav3 + tabbyAPI),” reports a TabbyAPI loading failure. Its error text matches the raise in `Model._load_autosplit`, and the discussion describes the dummy forward that the standalone evaluator also uses via the loader. That is shared loader context, not evidence that `ppl.py --length` reproduces the report. [inference; call_42dade58b5444cf0be2de8da5ced388c, call_0c2fb9cfe8cf4661b96536a18fd044b6, call_e67ccc6dac8c42b88b557168139151f9, call_49ec2c61864f4b02ae61a06943d08e72]

Issue #29, “Auto-YaRN for Qwen3? Maybe even set it dynamically?”, discusses static versus per-request YaRN and quotes `override_max_position_embeddings`. That exact field is relevant to the inspected LongRoPE path, but the patch neither changes Qwen3 YaRN nor forwards the CLI length to the override. [inference; call_b401b265ea064a838d1469cd850efb35, call_ec2857bbed7c403785aa54cdebe9ac62, call_618271708388446f8b79f42c0a57d2b8, call_1b673ffe0b6547b79c4476c7f68b9eda]

PR #22, “OpenAI compatible API example,” proposes a chat endpoint and quotes the shared `model_init.add_args` cache option. The common parser helper explains the overlap, but this evaluator passes `cache=False`; the API discussion does not describe its new window option. [inference; call_d47ca9a625174604855ef031da77bf2a, call_2a2bcfa7a2f844fbaedaac33dd3fdad0, call_e67ccc6dac8c42b88b557168139151f9, call_1b673ffe0b6547b79c4476c7f68b9eda]

PR #26, “Superior 3INST parameters,” proposes a trellis-decoder multiplier, reports perplexity comparisons, and mentions `eval/model_diff.py` as a starting point for KLD testing. Issue #33, “Error converting model,” reports a file-open failure during conversion compilation. Neither the evaluation-script overlap nor the conversion discussion establishes a link to the CLI length change. [inference; call_a05ac1c924624c6eb32ba8e84f0db0b7, call_9bca9f8b93bd48f78512eda93ddae27c, call_ba3c18e2b89d40f196da19980abd0998, call_1b673ffe0b6547b79c4476c7f68b9eda]

Issue #7, “quantizing model: undefined symbol: __cxa_call_terminate,” reports a native extension import failure and names the inspected model/config/RoPE files in its traceback. PR #4, “chore: update config.py,” describes a spelling correction. The shared paths do not connect either discussion to evaluation-window selection. [inference; call_982f7b3ba1bd42079d1b49322648ddd1, call_2c674a94504542179f81ef4203607f3a, call_758ac8e592104e1481ca4b2ed4059d29, call_1b673ffe0b6547b79c4476c7f68b9eda]

<a id="usage-evaluation"></a>

## Choose the token window length for standalone perplexity evaluation

`eval/ppl.py` tokenizes the Wikitext-2 raw test text with the loaded model's tokenizer. A window starting at token `a` contains `eval_tokens[:, a:a+L]`, where `L` is the requested length. Starts still advance by 512 tokens, and `--rows` still caps the number of windows at 100 by default. The stride is not a CLI option. [source; call_49ec2c61864f4b02ae61a06943d08e72, call_1b673ffe0b6547b79c4476c7f68b9eda]

Each row still goes through one cacheless forward pass. The scorer drops the last prediction position, crops to the actual vocabulary, takes float32 log-softmax, and gathers the following token's log probability. For a valid row of length `L`, this yields `L-1` targets. The script pools log probabilities across all rows and reports `exp(-sum_logprob / target_count)`, with no deduplication of overlapping targets. The in-place `1e-10` logit offset and per-row cleanup recorded by the memory entry remain in the parent source and are untouched by this diff. [source; call_49ec2c61864f4b02ae61a06943d08e72, call_1b673ffe0b6547b79c4476c7f68b9eda]

With 60,000 synthetic token positions and a cap of 100 rows, a Python transcription counted 51,100 target occurrences at length 512, all distinct. At length 2048 it counted 204,700 occurrences over 52,735 distinct positions, with some positions counted four times. Length 4096 raised the maximum multiplicity to eight; this is an indexing result, not evidence that 4096 runs on a model. [execution; call_9370f4aa012a459c93e72012573417ca, call_49ec2c61864f4b02ae61a06943d08e72]

`model_init.init` still receives `override_dynamic_seq_len=2048`, `max_output_size=2048`, and `max_output_factor=5`. It passes the output settings to `Model.load`; the split loader uses a default dummy chunk of 2048 tokens, narrows the dummy state at the logit layer, and allocates four extra output-shaped tensors for the factor of five. This is a load-time memory estimate, not a runtime truncation rule. `Model.forward` only narrows the logit input for `last_tokens_only`, which this evaluator does not set. The base config's dynamic-length override is a no-op; `Phi3Config` stores it for LongRoPE, which chooses long versus short factors by comparing the override to the original context limit. [source; call_49ec2c61864f4b02ae61a06943d08e72, call_1b673ffe0b6547b79c4476c7f68b9eda, call_e67ccc6dac8c42b88b557168139151f9, call_a10b3ac0881e4e968e5726c1bf72d62b, call_0c2fb9cfe8cf4661b96536a18fd044b6, call_758ac8e592104e1481ca4b2ed4059d29, call_ec2857bbed7c403785aa54cdebe9ac62, call_618271708388446f8b79f42c0a57d2b8]

`eval/model_diff.py` calls its own helper with `(tokenizer, args.rows)` and still uses length 2048. `eval/prequant_test.py` calls a separate BOS-aware helper with `(tokenizer, args.rows, bos)` and also keeps its own 2048 default. Neither call consumes the changed `ppl.py` namespace. [source; call_8be93422adf74b158c5600ee35845211, call_ba3c18e2b89d40f196da19980abd0998, call_9e015822710b433cb7b20e7cc63a078a, call_47a828b48792442b8ff68b4061fbf9fe, call_1b673ffe0b6547b79c4476c7f68b9eda]

## Authoring-time findings — pending review

### length-without-next-token-targets (suspected; defect)

The new integer flag exposes window widths that cannot supply a next-token target.

Trigger: Invoke standalone `eval/ppl.py` with `--length 1`, successful model initialization, and more than one encoded corpus token. Zero and negative widths are also accepted by the parser without semantic validation.

Expected: Reject widths below two before model work, since scoring requires a token and its successor.

Actual: A one-token row reaches scoring with both prediction and target slices empty. If tensor operations succeed, the target count remains zero and the mean divides by zero. Zero and negative widths likewise reach slicing instead of getting an argument error; their downstream failures were not tested.

Locations: c09f809876902c2cd9eedad463eecfa2c97977ed:eval/ppl.py — main

Source evidence: call_1b673ffe0b6547b79c4476c7f68b9eda, call_49ec2c61864f4b02ae61a06943d08e72, call_8be93422adf74b158c5600ee35845211

scalar_transcription: The slice calculation gave 100 one-token windows and zero target positions. [call_9370f4aa012a459c93e72012573417ca]. Limits: The check did not run the tensor or model operations that precede the division.

### window-ending-at-corpus-boundary-skipped (suspected; defect)

The inherited exclusive range bound omits a complete final window and does not handle an empty window list.

Trigger: Select `--length` equal to the encoded corpus length. More generally, a valid final window is omitted when its start is on the 512-token grid and the row cap has not already been reached. A length greater than the corpus also produces no windows.

Expected: Include a full window that ends exactly at the corpus boundary, and report a clear error when no full window can fit.

Actual: The range excludes start `num_tokens - eval_len`. At equality it yields no rows, so the standalone evaluator's helper calls `torch.cat` on an empty list rather than scoring the one available full row.

Locations: c09f809876902c2cd9eedad463eecfa2c97977ed:eval/ppl.py — get_test_tokens

Source evidence: call_1b673ffe0b6547b79c4476c7f68b9eda, call_49ec2c61864f4b02ae61a06943d08e72, call_8be93422adf74b158c5600ee35845211

scalar_transcription: At length 2048, the range produced no starts for 2048 corpus tokens, one for 2560, and two for 2561. [call_9370f4aa012a459c93e72012573417ca]. Limits: This checked the range and target counts, not the PyTorch exception.

### longer-window-outgrows-load-estimate (suspected; defect)

The new window width can exceed the token dimensions used to plan model placement.

Trigger: Run the standalone evaluator with a valid corpus window longer than 2048 tokens and a model that loads through the split loader.

Expected: Size the load estimate for the requested forward width, or reject widths outside the supported configuration.

Actual: Model placement is planned with the same 2048-token dummy chunk and output estimate, then `main` forwards the whole longer row and requests logits at every position. Conversely, a shorter window does not reduce the load-time estimate.

Locations: c09f809876902c2cd9eedad463eecfa2c97977ed:eval/ppl.py — main, 2b3d8b54af2de96d1ca956eb95f80b3f3e5b1042:exllamav3/models/model.py — Model._load_autosplit

Source evidence: call_1b673ffe0b6547b79c4476c7f68b9eda, call_49ec2c61864f4b02ae61a06943d08e72, call_e67ccc6dac8c42b88b557168139151f9, call_a10b3ac0881e4e968e5726c1bf72d62b, call_0c2fb9cfe8cf4661b96536a18fd044b6

source_inspection: Traced the fixed load arguments and the variable-width forward separately. Changing the estimate would require adjusting both chunk and output size: the dummy logit width is bounded by both. [call_49ec2c61864f4b02ae61a06943d08e72, call_1b673ffe0b6547b79c4476c7f68b9eda, call_a10b3ac0881e4e968e5726c1bf72d62b, call_0c2fb9cfe8cf4661b96536a18fd044b6]. Limits: The mismatch does not prove any particular GPU will run out of memory or that a given model accepts the longer context.

### length-can-cross-longrope-tier (suspected; defect)

On the Phi3 LongRoPE path, the evaluation width can disagree with the load-time width used to choose rotary factors.

Trigger: Use a Phi3 LongRoPE configuration and a valid evaluation length on the opposite side of its original-context threshold from 2048; for example, choose a width above the threshold when the threshold is at least 2048.

Expected: For a context-length evaluation, choose factors using the requested width, or explicitly constrain the evaluation to the intended tier.

Actual: The evaluator still passes 2048 into `Phi3Config.override_dynamic_seq_len`; LongRoPE selects its factors using that override, not the requested window width. In the example trigger it selects short factors even though the requested row exceeds the threshold.

Locations: c09f809876902c2cd9eedad463eecfa2c97977ed:eval/ppl.py — main, 2b3d8b54af2de96d1ca956eb95f80b3f3e5b1042:exllamav3/util/rope.py — _rope_params_longrope

Source evidence: call_1b673ffe0b6547b79c4476c7f68b9eda, call_49ec2c61864f4b02ae61a06943d08e72, call_e67ccc6dac8c42b88b557168139151f9, call_4f67fc31ed4b4e38ae7bcdac009d33cf, call_ec2857bbed7c403785aa54cdebe9ac62, call_618271708388446f8b79f42c0a57d2b8

source_inspection: Followed the override from the evaluator to the config field and compared it with the LongRoPE `a_override > b` condition. [call_49ec2c61864f4b02ae61a06943d08e72, call_e67ccc6dac8c42b88b557168139151f9, call_ec2857bbed7c403785aa54cdebe9ac62, call_618271708388446f8b79f42c0a57d2b8]. Limits: This is conditional on the LongRoPE path and a crossed threshold; no checkpoint or score was tested.

## Uncertainty and limits

Only window and target indexing were executed, using synthetic integer positions in standard-library Python. No Wikitext download, tokenization, PyTorch scoring, model loading, or GPU forward was run. Perplexity, VRAM usage, and supported maximum length remain unmeasured.

Literal parent-tree searches do not rule out dynamic imports or out-of-tree callers. The commit message gives no reason for leaving the loader and position settings fixed.
