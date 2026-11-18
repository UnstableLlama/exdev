# 162f99ab8bb032be8e4b22adbe0e5ee1f6a25425


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/162f99ab8bb032be8e4b22adbe0e5ee1f6a25425) · [Evidence ledger](draft.json)

Adds AnyPrecision evaluation dispatch and storage accounting, six comparison specifications, and updated Llama-3.2 paths and baseline selection; introduces an unconditional external import requirement.

- [AnyPrecision comparison adapter and model specifications](#usage-evaluation)

## Problem

The comparison runner had no AnyPrecision dispatch entry. This change adds an adapter and six Llama-3.1-8B-Instruct comparison specifications. [source; call_597e675524504e5d91539563080062ce, call_371b2c143276413bac52e9073c2f64d5]

## Reasoning

The adapter preserves the runner's existing interface: loading returns the model, decoder BPW, head BPW and storage bits; forwarding returns logits. Thus AnyPrecision uses the existing dataset, scoring and plotting pipeline rather than a separate evaluator. [source; call_597e675524504e5d91539563080062ce, call_371b2c143276413bac52e9073c2f64d5]

## Impact

The new specifications select 2-, 3- and 4-bit GuidedQuant-LNQ and SqueezeLLM artifacts through local paths. Existing Llama-3.2-1B specifications move from /mnt/str/eval_models to /mnt/str/models; EXL3's lower-bitrate selections also change head labels and directories. A new HF FP16 specification supplies reference-logit output. [source; call_597e675524504e5d91539563080062ce]

## Source Notes

The root usage-evaluation entry was read. It establishes the inherited adapter contract and explains that reported VRAM is decoder-plus-head tensor accounting, not measured peak allocation. [ancestor; call_7c726b2bd6904414a93ae1ed9d473b4d]

PR #26 is titled “Superior 3INST parameters” and proposes codebook-parameter changes. Its connection here is only inferred from the shared comparison tooling and Llama evaluation context; the inspected discussion does not establish that it motivated AnyPrecision support. [inference; call_4fad84551d6e44ea9cfbb24bb5605e4a, call_597e675524504e5d91539563080062ce]

<a id="usage-evaluation"></a>

## AnyPrecision comparison adapter and model specifications

Both dispatch tables gain “anyprecision”. load_anyprecision calls AnyPrecisionForCausalLM.from_quantized(model_dir), computes storage metadata and returns the existing four-item tuple. Its auto and bf16 parameters are unused. fwd_anyprecision moves IDs to cuda:0, invokes the model and returns output.logits; unlike the Transformers loader it does not explicitly establish model device placement or dtype. [source; call_597e675524504e5d91539563080062ce, call_29bc6e203ad74635998c2ded3e7afa72]

get_storage_info counts each AnyPrecisionLinear's qweight plus only the LUT selected by precision 1 through 8. Tensor bytes are multiplied by eight to obtain bits, then divided by the sum of logical in_features × out_features. Consequently decoder BPW includes selected LUT overhead rather than merely reporting the nominal precision. [source; call_597e675524504e5d91539563080062ce]

Ordinary Linear modules with output width at least 90% of config.vocab_size are treated as the head; other ordinary linear weights contribute to decoder accounting. This is a width heuristic, not a structural head lookup. Embeddings, normalization tensors, biases, unused LUTs and runtime allocations are not explicitly included. The copied recursive GPU-tensor scanner is not called by this adapter. [source; call_597e675524504e5d91539563080062ce]

An illustrative standard-library calculation for 1,048,576 logical weights, 262,144 packed bytes and an 8,192-byte LUT produces 2.0625 BPW, including 0.0625 BPW LUT overhead. The runner's bits / 8 / 1024³ conversion reports GiB-sized units despite its GB label. [execution; call_b6bbd39bfe494bc8a66751e0c987f0cf, call_371b2c143276413bac52e9073c2f64d5]

The new AnyPrecision specifications rely jointly on the adapter and both registrations; their labels do not configure precision directly. The directory passed to from_quantized determines the loaded artifact. No AnyPrecision tokenizer is added: the dataset specification continues to select the shared Transformers tokenizer. [source; call_597e675524504e5d91539563080062ce, call_371b2c143276413bac52e9073c2f64d5]

For the new HF specification, main interprets out_logits as a directory, creates it if absent, appends the data-specification hash and .safetensors, and moves that model ahead of the others. test_ppl collects reference logits for the first ten rows; subsequent comparison models read the same resolved filename. This reuses existing behavior rather than introducing a new writer. [source; call_597e675524504e5d91539563080062ce, call_371b2c143276413bac52e9073c2f64d5, call_5588ec2ac07d469d9920e4df5d1df3f9]

## Authoring-time findings — pending review

### unconditional-anyprecision-import (suspected; new_requirement)

Adding the backend also makes its external package an import-time requirement for existing comparison workflows.

Trigger: Run compare_q.py, or import its helpers through compare_q_logits.py, in an environment without the any_precision module.

Expected: A workflow selecting only an existing backend would not need to import AnyPrecision.

Actual: compare_q.py unconditionally imports the new adapter, whose top-level imports require any_precision before model selection or argument parsing.

Locations: 162f99ab8bb032be8e4b22adbe0e5ee1f6a25425:eval/compare_q.py — module imports, 162f99ab8bb032be8e4b22adbe0e5ee1f6a25425:eval/compare_q_anyprecision.py — module imports

Source evidence: call_597e675524504e5d91539563080062ce, call_7d101eae26be4a1dbe5fc55432ccdb81, call_3498e191c00946138c550bf4fb6d1e6a

source_inspection: Whole-parent-tree search found compare_q_logits.py importing get_test_data and save_tensor from compare_q; its source confirms the import occurs at module scope. Parent searches found no AnyPrecision or any_precision occurrences. [call_7d101eae26be4a1dbe5fc55432ccdb81, call_3498e191c00946138c550bf4fb6d1e6a, call_0c8d1b712fe14916816095a311c3b4ca, call_fad6fcaab709417ea659edaf853142b8]. Limits: Import failure was not executed. Reach is established for these two evaluation entry points, not for unrelated package workflows or dynamic external callers.

## Uncertainty and limits

No model loading, GPU forwarding, perplexity evaluation or filesystem-library execution was performed. External AnyPrecision implementation, version compatibility and default device placement remain unverified.

Storage accounting assumes the external modules expose qweight, precision and the selected lut1–lut8 attribute. No checkpoint tensors were inspected to validate those assumptions.

The scalar computation illustrates the inspected accounting formula with hypothetical tensor sizes; it neither measures a checkpoint nor executes repository code.

Only the initial portion of the lengthy PR #26 discussion was inspected; no task-specific provenance is established from it.
