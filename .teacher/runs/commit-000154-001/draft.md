# 5c3ff204c4c5c64dc2bd897582143b116a82b767


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/5c3ff204c4c5c64dc2bd897582143b116a82b767) · [Evidence ledger](draft.json)

Uses deferred tensor loading for each compared module and closes cached file handles afterward, without changing comparison formulas or correcting the inherited perplexity bound issue.

- [Module-scoped deferred loading and handle cleanup](#usage-evaluation)

## Problem

The comparison loop loaded each module directly and unloaded its weights without closing the safetensors collection's cached file handles. [source; call_0fe00079c22144258410593fe80c740f, call_fd7693fb847a4c8f90e1f0a7e3209a4c]

## Reasoning

Bracketing each module load with deferred loading batches its eligible tensor reads, while closing the collection after the forward pass bounds handle retention to the current module. [source; call_b9d29b07e3c6416d925c2ad1bee977cd, call_fd7693fb847a4c8f90e1f0a7e3209a4c]

## Impact

Both model branches receive the same lifecycle change. Device selection, activation propagation and comparison formulas remain unchanged. [source; call_b9d29b07e3c6416d925c2ad1bee977cd]

## Source Notes

PR #26, “Superior 3INST parameters,” proposes decoder changes and discusses using model_diff.py for KLD evaluation. Its relationship to this loading change is inferred only from the shared script; the discussion does not establish the motivation for deferred loading or handle closure. [inference; call_e6cc336afb4840da8ff3add387dccd84, call_0a32af90f6b541a9bb5dc4e6f0423b81, call_b9d29b07e3c6416d925c2ad1bee977cd]

The earlier metrics entry recorded a suspected vocabulary-versus-sequence bound error in the perplexity helper. [ancestor; call_2018820d6c27499dbcf474a9d1bf694f]

<a id="usage-evaluation"></a>

## Module-scoped deferred loading and handle cleanup

For each paired module, main now begins deferred loading, calls load on CPU or cuda:0 according to prefer_cpu, and ends deferred loading before prepare_for_device and forward. After unload it closes that model's collection, then calls free_mem. A completes this sequence before B starts. [source; call_b9d29b07e3c6416d925c2ad1bee977cd]

SafetensorsCollection.get_tensor defers only the mt_fread path when deferred_mode is active and no_defer is false. It allocates destination tensors and queues read descriptions; end_deferred_load groups requests by file and CPU/CUDA destination, sorts by descending byte size, dispatches chunked native workloads, applies temporary-tensor copies for transformations, then clears deferred state. The Python loader and explicit no_defer requests retain immediate reads. [source; call_fd7693fb847a4c8f90e1f0a7e3209a4c]

The existing chunk limit is 2 MiB, not a module-size limit. A standard-library arithmetic check evaluated it as 2,097,152 bytes and showed that a 5 MiB tensor requires three jobs. [execution; call_fd7693fb847a4c8f90e1f0a7e3209a4c, call_633af64282284d17af3a782557b7ef83]

close calls the native closer for every cached open handle and resets those entries to None without discarding tensor metadata. Subsequent loads can reopen the same shard. The tradeoff is shorter handle lifetimes versus repeated opens when successive modules share files; any net speed benefit is an inference, not a measured result. [inference; call_fd7693fb847a4c8f90e1f0a7e3209a4c, call_b9d29b07e3c6416d925c2ad1bee977cd]

Cleanup is placed on the normal sequential path rather than in try/finally. The change does not add exception recovery or alter the inherited perplexity helper's indexing. [source; call_b9d29b07e3c6416d925c2ad1bee977cd, call_0fe00079c22144258410593fe80c740f]

## Authoring-time findings — pending review

### inherited-ppl-axis-bound (suspected; defect)

The inherited perplexity helper bounds sequence slicing by vocabulary size; this change leaves it intact.

Trigger: The number of prediction positions exceeds the vocabulary size.

Expected: Accumulate every next-token prediction exactly once.

Actual: With 2047 prediction positions and vocabulary size 1024, the loop covers only 1024 positions. Larger vocabularies can instead cause trailing empty slices.

Locations: 5c3ff204c4c5c64dc2bd897582143b116a82b767:eval/model_diff.py — main.ppl

Source evidence: call_0fe00079c22144258410593fe80c740f, call_b9d29b07e3c6416d925c2ad1bee977cd, call_580ce6ac52af472293306bcbab3a3ab2

source_inspection: The nested helper slices axis zero but bounds its loop with shape[1]. Whole-parent-tree search found its direct call in main's per-model metrics loop; the other matches name the distinct test_ppl function. The inspected CLI guard invokes main. The task diff changes only loading and closure. [call_580ce6ac52af472293306bcbab3a3ab2, call_0fe00079c22144258410593fe80c740f, call_b9d29b07e3c6416d925c2ad1bee977cd]. Limits: Reach is established for the script's two-model metrics loop, not external or dynamic callers.

scalar_transcription: A Python integer-bound model covered 1024 of 2047 positions for vocabulary 1024, and all 2047 positions in four iterations for vocabulary 32000. [call_633af64282284d17af3a782557b7ef83]. Limits: This did not execute the repository helper or Torch operations.

## Uncertainty and limits

No model inference, native loader execution, file-descriptor measurement or performance benchmark was run. Faster loading and numerical equivalence remain unmeasured.

The scalar checks model integer chunking and slice coverage only, not Torch empty-tensor behavior, native I/O or CUDA synchronization.
