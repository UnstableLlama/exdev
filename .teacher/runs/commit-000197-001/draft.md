# 9be91d644d8272db7bfd5e759084b74bc08704ae


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/9be91d644d8272db7bfd5e759084b74bc08704ae) · [Evidence ledger](draft.json)

Adds default-on idle-queue cache defragmentation using prefix-chain planning and in-place CUDA copy schedules. Inspection identifies missing draft-cache relocation and carried-over kernel/test limitations; performance remains unmeasured.

- [Idle-queue cache defragmentation](#cache-defragmentation)

## Problem

Cached prefix pages could remain physically scattered after jobs released them; PageTable.defrag was a stub. This change implements idle-queue cache reordering. [source; call_772a7039cd094d69b38b9f4c585a7039, call_0e7aa0d01c5c401c91b6119a2c17afca]

## Reasoning

The edits form one mechanism: cache layers expose their backing tensors, the page table constructs a physical permutation, the CUDA primitive executes its copy schedule, and page metadata receives the resulting indices. Visualization must consequently index usage by physical page_index rather than list position. [source; call_9611cf9702fc4fb19f357f32b5861605, call_0e7aa0d01c5c401c91b6119a2c17afca, call_5632406deded4d54bae23b6cd27f1851, call_627306c3536b4c11a0cac516aeecd89f]

## Impact

Defragmentation defaults on and runs after completion or cancellation empties the queue, including the existing clear_queue call. It is not a timer or an operation performed while jobs remain active. [source; call_627306c3536b4c11a0cac516aeecd89f, call_bd1e22560f184c6093840b1240aadd65]

## Source Notes

The cache-rotation ancestor entry establishes the earlier single-cycle API and records vector-boundary and dtype-test concerns. The root generation chapter establishes prefix hashing, reference ownership and the original no-op defragmenter. [ancestor; call_88fda29f37ae4527a61690cd4b9c1670, call_6ac6919ec8a84fcb9b754985077814e8, call_7c348d2e39834dcea84a408cd5eadac5]

Whole-parent searches found one CachePage construction site, updated by this diff, and two direct CacheLayer subclasses, both given get_tensors implementations. The sole existing Python cache_rotate caller is its test, also migrated to the new pair representation. [source; call_c0dc66000c9843e9887fb90fc37ede2d, call_2733dbdf157e4931a41f7752cc029718, call_82299790a2a94f0b888523217b0fd508, call_d0c041c32a584729a3ab957ef74c1805, call_1e87528993904b258dd2e70ff22150c4, call_27bffe9e70064eac984d93807f969456]

<a id="cache-defragmentation"></a>

## Idle-queue cache defragmentation

enable_defrag gates the operation. A second gate requires access_serial to advance by max_pages since the previous attempt, then asserts there are no referenced pages. Allocation increments this serial per page assignment, including reuse: the comment about every page having been touched is stronger than the implemented aggregate counter. The attempt timestamp advances even when the later movement threshold skips copying. [source; call_0e7aa0d01c5c401c91b6119a2c17afca, call_772a7039cd094d69b38b9f4c585a7039]

The planner links pages through prev_hash, measures descendant chain lengths and orders children longest-first. Roots are sorted by ascending access_serial; secondary branches become additional roots. Recoverable chains receive consecutive proposed indices. Orphans retain physical-index ordering while sorted access serials are reassigned among them, affecting subsequent oldest-page replacement. [source; call_0e7aa0d01c5c401c91b6119a2c17afca, call_772a7039cd094d69b38b9f4c585a7039]

The most common proposed displacement becomes a global circular shift adjustment, keeping that displacement group stationary. Copying proceeds only when moved pages exceed max(max_pages // 10, 2): this is an approximately ten-percent movement threshold with a two-page floor, not a measured fragmentation score. Circular wrapping can split a physically contiguous chain at the cache boundary. [source; call_0e7aa0d01c5c401c91b6119a2c17afca]

Each nontrivial permutation cycle becomes destination/source pairs with -1 denoting one-page scratch. The native interface now interprets order as signed int32 pairs rather than a list of cycle indices, and synchronizes threads after each copy. Blocks partition page bytes; threads transfer 16-byte uint4 vectors with a 512×16-byte stride. [source; call_5632406deded4d54bae23b6cd27f1851, call_2b617257a6eb4980b07a7e8c51b433e4]

FP16 layers expose K and V; quantized layers expose packed K/V and both scale tensors, avoiding decompression for relocation. The planner caches order tensors per device and scratch by page shape, device and dtype during one defrag call. Existing test callers likewise allocate page-shaped scratch; the new caller constructs valid permutation cycles itself. [source; call_1e87528993904b258dd2e70ff22150c4, call_27bffe9e70064eac984d93807f969456, call_9ea9d647d87b4cb4b4b51da9f01a1a40, call_0e7aa0d01c5c401c91b6119a2c17afca, call_a4ffff52d1964e70be379ff5c861cdd7]

Updating page_index after relocation preserves logical page objects and hash dictionaries. Later sequence allocation rebuilds block_index_tensor from those indices; the idle-only guard avoids relocating pages underneath existing active block tables. [source; call_772a7039cd094d69b38b9f4c585a7039, call_0e7aa0d01c5c401c91b6119a2c17afca]

A standard-library transcription verified the cycle-to-copy schedule for all 5,913 permutations of sizes one through seven. This checks destination/source direction and scratch reuse, not GPU execution. [execution; call_bc91113dce6d4fdcb1f3fdf394e7ac82]

The rotation test adopts the pair-based reference and repeats partial schedules. The stress script forces queue depth to zero every third scheduling cycle to exercise defragmentation opportunities; its draft model remains disabled and quantized-cache settings remain commented out. [source; call_d0c041c32a584729a3ab957ef74c1805, call_180418f1ac924bca9f34169a290e91ef]

## Authoring-time findings — pending review

### draft-cache-not-relocated (suspected; defect)

Defragmentation relocates main-cache storage but not the draft cache sharing its physical page indices.

Trigger: Draft decoding is enabled, a qualifying defragmentation moves valid cached pages, and a later job reuses those pages.

Expected: Relocate both caches consistently, or invalidate draft-cache reuse.

Actual: defrag enumerates only self.cache tensors, then changes shared page_index metadata. Draft prefill and generation use block tables derived from those new indices against unmoved draft storage. Existing partial-prefix copying explicitly handles both caches, unlike defrag.

Locations: 9be91d644d8272db7bfd5e759084b74bc08704ae:exllamav3/generator/pagetable.py — PageTable.defrag

Source evidence: call_0e7aa0d01c5c401c91b6119a2c17afca, call_bd1e22560f184c6093840b1240aadd65, call_b22fa260e85f497d8ffc00606a1264cf, call_06de7254bec048f18e09c2a7663923a0

source_inspection: Compared main-only tensor enumeration with draft block-table consumers and dual-cache prefix copying. Defrag callers are queue clearing, cancellation and completed-job cleanup. [call_626c41248756469c9138373a76d7afc8, call_627306c3536b4c11a0cac516aeecd89f]. Limits: No speculative generation was run; downstream output effects are unmeasured.

### inherited-vector-boundary (suspected; defect)

The inherited vector-boundary problem remains; changing !block_size to block_size <= 0 does not prevent unsigned underflow.

Trigger: Call cache_rotate with a contiguous uint8 cache of shape (2,129), 129-byte scratch and a valid pair schedule such as [-1,0,0,1,1,-1].

Expected: Reject unsupported page sizes or copy within each allocation.

Actual: Two-byte block partitions still issue 16-byte transfers. Block 65 starts at byte 130, beyond the clamped end of 129; unsigned subtraction produces a huge positive length that passes the new guard.

Locations: 9be91d644d8272db7bfd5e759084b74bc08704ae:exllamav3/exllamav3_ext/generator/cache.cu — cache_rotate_kernel

Source evidence: call_2b617257a6eb4980b07a7e8c51b433e4, call_5632406deded4d54bae23b6cd27f1851

scalar_transcription: Modeled block 65 with 64-bit unsigned subtraction, obtaining 18446744073709551615. [call_bc91113dce6d4fdcb1f3fdf394e7ac82]. Limits: No GPU access executed. Existing test shapes avoid this case; this concrete trigger concerns the exposed native API, not a demonstrated model-cache shape.

### inherited-unused-test-dtype (suspected; defect)

The updated test retains ineffective float32 parametrization.

Trigger: Pytest selects cache_dtype=torch.float for test_rope.

Expected: Exercise float32 cache storage.

Actual: The unchanged allocation hard-codes torch.half, so both dtype cases exercise half storage.

Locations: 9be91d644d8272db7bfd5e759084b74bc08704ae:tests/test_cache_rotate.py — test_rope

Source evidence: call_a4ffff52d1964e70be379ff5c861cdd7, call_d0c041c32a584729a3ab957ef74c1805

source_inspection: Compared parametrization and allocation with the task's reference-loop changes; the allocation is unchanged. [call_a4ffff52d1964e70be379ff5c861cdd7, call_d0c041c32a584729a3ab957ef74c1805]. Limits: Tests were not run.

## Uncertainty and limits

No repository tests, CUDA kernels or model generation were executed; the scalar check validates only permutation scheduling and modeled unsigned arithmetic.

Latency improvements and the tuning rationale for the defragmentation thresholds, 128 blocks and 512 threads are unmeasured.

The native wrapper still relies on callers for valid indices, contiguous compatible device storage and suitable vector alignment; arbitrary external callers were not inspected.
