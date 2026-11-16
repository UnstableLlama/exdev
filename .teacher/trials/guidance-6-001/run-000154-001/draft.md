# 5c3ff204c4c5c64dc2bd897582143b116a82b767


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/5c3ff204c4c5c64dc2bd897582143b116a82b767) · [Evidence ledger](draft.json)

Uses deferred tensor loading and closes file handles after each compared module, without changing comparison metrics; an inherited perplexity indexing issue remains.

- [Module-scoped deferred loading and handle cleanup](#usage-evaluation)

## Problem

model_diff.py loaded tensors directly and retained collection file handles across module comparisons, despite unloading each module. [source; call_0ba255faa9114b21ac991326be4e922f, call_3aa24c4ed12d46dcad75fcb9b8c6d032]

## Reasoning

The change brackets each model's module.load with begin_deferred_load/end_deferred_load, then closes that model's collection after forwarding and unloading. Completing deferred reads before forwarding is essential because deferred get_tensor returns allocated destinations before filling them. [source; call_07608162fe924cb38aa9c2fa5540adc9, call_3aa24c4ed12d46dcad75fcb9b8c6d032]

## Impact

The normal comparison path now batches eligible tensor reads within each module and releases file handles between modules; comparison formulas and device selection remain unchanged. [source; call_07608162fe924cb38aa9c2fa5540adc9]

## Source Notes

The root usage-evaluation entry establishes the original module-at-a-time diagnostic. The later metrics entry records the final-logit diagnostics and a vocabulary-versus-sequence bound observation. [ancestor; call_c53e7f3f1de141ad952fe189cbec8d74, call_2a5a6dea6c4d4821a5ad7db593ff0fa7]

PR #26, “Superior 3INST parameters,” proposes decoder changes; its discussion includes turboderp announcing KLD evaluation in model_diff.py. Its relationship to this loading change is inferred only from the shared script, not an explicit commit link or a reported loading failure. [inference; call_8ecc5694a9fa47ac81b520db386c8876, call_be7f638302c6479b93e8bf41c9fef755, call_07608162fe924cb38aa9c2fa5540adc9]

<a id="usage-evaluation"></a>

## Module-scoped deferred loading and handle cleanup

Both A and B follow the same sequence: begin deferred loading, load the module, finish deferred loading, prepare and forward activations, unload, close collection handles, then free memory. A finishes this sequence before B begins. [source; call_07608162fe924cb38aa9c2fa5540adc9, call_0ba255faa9114b21ac991326be4e922f]

Deferral applies to the default mt_fread backend unless get_tensor requests no_defer. The Python backend remains immediate. end_deferred_load groups requests by file and CPU/CUDA destination, sorts by decreasing byte size, dispatches chunked native workloads, performs required temporary-to-destination copies, and clears deferred state. [source; call_3aa24c4ed12d46dcad75fcb9b8c6d032]

close closes nonempty native handles and resets their slots to None without discarding tensor metadata. Later loads can reopen the same files. This trades persistent handle reuse for module-bounded handle retention; any speed or resource benefit remains an inference rather than a measurement. [inference; call_3aa24c4ed12d46dcad75fcb9b8c6d032, call_07608162fe924cb38aa9c2fa5540adc9]

The earlier perplexity bound observation carries over unchanged: this diff does not alter the nested ppl helper or its caller. [source; call_0ba255faa9114b21ac991326be4e922f, call_07608162fe924cb38aa9c2fa5540adc9, call_a97e25eee3344020829149d7161dc6af]

## Authoring-time findings — pending review

### inherited-ppl-axis-bound (suspected; defect)

The unchanged perplexity helper bounds sequence-axis slicing by vocabulary size.

Trigger: Prediction-position count exceeds vocabulary size; larger vocabularies instead cause trailing empty slices.

Expected: Accumulate every next-token prediction exactly once.

Actual: For 2047 prediction positions and vocabulary size 1024, only 1024 positions are included. The direct caller is main's per-model final-logit loop, reachable through this script's CLI.

Locations: 5c3ff204c4c5c64dc2bd897582143b116a82b767:eval/model_diff.py — main.ppl

Source evidence: call_0ba255faa9114b21ac991326be4e922f, call_07608162fe924cb38aa9c2fa5540adc9, call_a97e25eee3344020829149d7161dc6af

source_inspection: Whole-parent-tree search located the nested helper and its direct caller. Inspection shows shape[1] controlling slices along axis zero; the task leaves both unchanged. [call_a97e25eee3344020829149d7161dc6af, call_0ba255faa9114b21ac991326be4e922f, call_07608162fe924cb38aa9c2fa5540adc9]. Limits: Literal search does not establish external or dynamic callers.

scalar_transcription: A standard-library model counted 1024 positions in one pass for vocabulary 1024, and all 2047 positions in four passes for vocabulary 32000. [call_ba6624e3621b4d41a7c45502cd3f3f8a]. Limits: Models integer bounds only; does not execute the repository helper or Torch.

## Uncertainty and limits

No model inference, native loader execution, file-handle measurement or throughput benchmark was performed.

The scalar check models inherited perplexity indexing only; it does not establish Torch behavior on empty slices or numerical metric values.

The added cleanup is on the normal path, not protected by exception-handling cleanup.
