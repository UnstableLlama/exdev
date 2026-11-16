# 5c3ff204c4c5c64dc2bd897582143b116a82b767


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/5c3ff204c4c5c64dc2bd897582143b116a82b767) · [Evidence ledger](draft.json)

Adds per-module deferred loading and handle closure to model comparison, but omits existing sliced-module guards and retains the earlier perplexity indexing issue.

- [Module-scoped deferred loading and handle release](#usage-evaluation)

## Problem

model_diff.py loaded each module directly and left collection file handles open across module comparisons. [source; call_480e64a072574c4fb924bb9e708fa642, call_5bcb9fe25b3e412fb674c20207a10123]

## Reasoning

Both branches now bracket module.load with begin_deferred_load/end_deferred_load and close their collection after forwarding and unloading. Completing deferred reads before forward is essential because deferred get_tensor returns destination storage before populating it. [source; call_12752221fd0b421786659b834d03027a, call_5bcb9fe25b3e412fb674c20207a10123]

## Impact

The change enables batched loading and bounds handle retention to each branch's module processing. It leaves comparison formulas and device selection unchanged; speed and resource savings are not measured. [source; call_12752221fd0b421786659b834d03027a, call_480e64a072574c4fb924bb9e708fa642]

## Source Notes

Read ancestor entries 25d9388 and 9575f7d: they explain the B-state prefix and final-logit diagnostics respectively. The latter records the perplexity-axis observation retained here. [ancestor; call_189798984a15437999fade547628388e, call_ac55ff1b7da746e482bfa95ba7b1a7da]

PR #26, “Superior 3INST parameters,” proposes decoder changes and discusses model_diff.py evaluation. Its relationship to this loading change is only contextual inference from the shared script, not an established fix linkage. [inference; call_c03400b8c9f3488581fd187b6a8fc20e, call_45a3c959104641d6a8fbc18817b00a52, call_12752221fd0b421786659b834d03027a]

Issue #7 reports an undefined __cxa_call_terminate import symbol; issue #34 reports a Cholesky failure during quantization. Neither discussion establishes that this script-loading change addresses its reported failure. [source; call_ff3054c3a5724f9cae365d34870005a1, call_dac76e918aee44129a55d359ed1ff231, call_12752221fd0b421786659b834d03027a]

<a id="usage-evaluation"></a>

## Module-scoped deferred loading and handle release

For the default mt_fread loader, eligible get_tensor calls queue destinations and metadata. end_deferred_load groups requests by file and CPU/CUDA destination, sorts by size, and splits work into chunks capped at 2*1024**2 bytes (2 MiB). It then applies temporary-buffer transformations and clears deferred state. Explicit no_defer requests and the Python loader remain immediate. [source; call_5bcb9fe25b3e412fb674c20207a10123]

close releases populated native handles and sets their entries to None while retaining tensor indexes and headers, allowing later modules to reopen shards. Unlike retaining handles throughout evaluation, this trades potential reopen overhead for earlier release. [source; call_5bcb9fe25b3e412fb674c20207a10123, call_12752221fd0b421786659b834d03027a]

Existing Model._load_single and _load_autosplit guard deferred loading with module.can_defer_load; autosplit also aborts deferred state on exceptions before handling out-of-memory retries. The new script calls omit both the capability guard and recovery. Existing conversion and compilation callers close collections after immediate reads, while Model.load_gen closes after model loading. [source; call_74af6c45fd964861afa360a3baa94815, call_981e77ef842342c1854908b4b4976616, call_12752221fd0b421786659b834d03027a, call_e6322ab78a04464cb9fa58ade0d5ca1d, call_27d90a341b3a4f90ae624609a16c0413, call_2b7d0269a6ff487badfd71c35cb37fed]

## Authoring-time findings — pending review

### unguarded-deferred-sliced-load (suspected; defect)

Unconditional deferred loading bypasses the existing sliced-module safety guard.

Trigger: A compared module contains a sliced unquantized Linear loaded through the normal weight-key path with mt_fread.

Expected: Honor can_defer_load and complete immediate reads before load-time copies of sliced weights.

Actual: Linear.load_fp16 queues the weight, then LinearFP16 copies its still-unpopulated destination into separate storage; end_deferred_load later populates the original destination, not that copy. The inspected reach is the two new main-loop calls when such modules occur, not all models.

Locations: 5c3ff204c4c5c64dc2bd897582143b116a82b767:eval/model_diff.py — main

Source evidence: call_12752221fd0b421786659b834d03027a, call_eea776438e6d4d54b6c27c13b6baf047, call_3356cd7251f24c939b3db2f828e0a9b9, call_fcc5d7b936f942a0aa2c8ee90a7add52

source_inspection: Compared both existing deferred-load callers and the sliced Linear/GatedMLP capability checks with the new unconditional calls and LinearFP16's copy. [call_74af6c45fd964861afa360a3baa94815, call_981e77ef842342c1854908b4b4976616, call_7dafb689be064faf9905ca9de80b6e28, call_b27fd9b4ac9146f29783461b745ece72, call_fcc5d7b936f942a0aa2c8ee90a7add52]. Limits: No sliced model or tensor-library execution was performed.

### inherited-perplexity-axis-bound (suspected; defect)

The previously recorded perplexity vocabulary-versus-sequence bound remains unchanged.

Trigger: The number of prediction positions exceeds vocabulary size.

Expected: Accumulate every prediction position.

Actual: main.ppl bounds its sequence slices by logits_.shape[1], the vocabulary dimension. With 2047 prediction positions and vocabulary 1024 it covers only 1024 positions.

Locations: 5c3ff204c4c5c64dc2bd897582143b116a82b767:eval/model_diff.py — main.ppl

Source evidence: call_480e64a072574c4fb924bb9e708fa642, call_12752221fd0b421786659b834d03027a, call_f00e7495a0ee43708a3b4250f82dd65e

source_inspection: Parent-tree search and script inspection locate the nested helper's direct caller in main's per-model final-logit loop. The task changes loading only, carrying this bound over. [call_f00e7495a0ee43708a3b4250f82dd65e, call_480e64a072574c4fb924bb9e708fa642, call_12752221fd0b421786659b834d03027a]. Limits: Search does not establish external entry points.

scalar_transcription: A standard-library transcription counted 1024 covered and 1023 omitted prediction positions. [call_5038f0da3e094a1fa34a1a1a47aef315]. Limits: Index arithmetic only; repository inference code did not run.

## Uncertainty and limits

No model inference, native loader execution, GPU test or file-handle measurement was performed.

The scalar check models perplexity indexing only, not Torch empty-slice behavior or numerical results.

Exception cleanup is not added: an exception before end_deferred_load or close bypasses those operations.
