# 965f5b2f0aa69e8d079cbeaffee59443ba9c8044


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/965f5b2f0aa69e8d079cbeaffee59443ba9c8044) · [Evidence ledger](draft.json)

Adds a bound CUDA page-rotation primitive with one-page scratch and reference tests. Inspection identifies unchecked vector-size constraints and ineffective float32 test coverage.

- [In-place cache-page rotation](#cache-rotate)

## Problem

The change adds a native operation for cyclically moving selected cache pages in place. [source; call_c9324f9c32734247865a3b03d77658ca]

## Reasoning

Saving the first selected page in caller-provided scratch permits each subsequent page to overwrite its predecessor, then restores the saved page into the last position. Scratch storage is one page rather than a full cache copy. [source; call_c9324f9c32734247865a3b03d77658ca]

## Impact

cache_rotate becomes a Python extension entry point. The parent-tree search found no existing callers; the task adds a direct test caller but no generation-path integration. [source; call_19c4aa55df1744b686f266bcf3b46828, call_0354daa0d15e48ec9f350069abe8ee2a, call_e1a2eb99e67347609255d15340854c1d]

## Source Notes

The root runtime chapter was read. It establishes the earlier pybind interface and caller-owned CUDA buffers as architectural context; its recorded elementwise-kernel defects concern functions this change does not modify. [ancestor; call_f9dbfa2b1ab54f3290692a68aa2ce89c]

<a id="cache-rotate"></a>

## In-place cache-page rotation

The declaration and binding expose cache_rotate(cache, order, temp). The wrapper selects the cache device and current CUDA stream, checks cache rank greater than one, one-dimensional int32 order, and scratch byte size equal to one page. Despite the comment saying “long,” the implemented order dtype is kInt, matching the test. [source; call_c6ba134eaf9245d697f6f1bad265dfb9, call_19c4aa55df1744b686f266bcf3b46828, call_c9324f9c32734247865a3b03d77658ca, call_e1a2eb99e67347609255d15340854c1d]

Each of 128 blocks owns a byte interval within every page. Its 512 threads copy uint4 vectors, 16 bytes per transfer, with an 8192-byte thread-loop stride. Each thread follows the complete rotation for its own offsets; this partitions work across page contents rather than across dependent page moves. [source; call_c9324f9c32734247865a3b03d77658ca]

The test compares three successive rotations against sequential PyTorch page copies with exact tolerances. It covers eight shapes and full or quarter-length random permutations on hard-coded cuda:2, but its dtype parameter does not control cache allocation. [source; call_e1a2eb99e67347609255d15340854c1d]

A standard-library scalar check rotated order [4,1,3] over six labeled pages to [0,3,2,4,1,5]. The supplied test shapes produce block lengths from 64 to 8192 bytes, all divisible by 16, so they avoid vector-tail cases. [execution; call_494aa88721cc488083738f6f98ee32c5]

## Authoring-time findings — pending review

### unchecked-vector-partition (suspected; defect)

Accepted page sizes can produce out-of-range vector accesses and unsigned block-length underflow.

Trigger: Call the exposed function with a contiguous uint8 cache shaped (2,129), valid int32 order [0,1], and 129-byte scratch.

Expected: Rotate the two pages without accessing outside their storage, or reject unsupported sizes.

Actual: The wrapper accepts these dimensions. Each block initially receives two bytes, but copies 16-byte vectors. Block 65 begins at byte 130 while its clamped end is 129; unsigned subtraction produces a huge nonzero length instead of skipping the block.

Locations: 965f5b2f0aa69e8d079cbeaffee59443ba9c8044:exllamav3/exllamav3_ext/generator/cache.cu — cache_rotate_kernel

Source evidence: call_c9324f9c32734247865a3b03d77658ca, call_0354daa0d15e48ec9f350069abe8ee2a, call_e1a2eb99e67347609255d15340854c1d

scalar_transcription: Modeled the interval calculation and 64-bit unsigned subtraction; obtained 18446744073709551615 for block 65. Parent search found no callers; the added test uses aligned sizes, so the demonstrated reach is unsupported inputs to the new extension API. [call_494aa88721cc488083738f6f98ee32c5]. Limits: No CUDA memory access was executed; unsigned arithmetic was modeled explicitly.

### unused-test-dtype (suspected; defect)

The apparent float32 test coverage repeats half-precision allocations.

Trigger: Run test_rope with cache_dtype=torch.float.

Expected: Allocate and rotate a float32 cache for that parameter case.

Actual: torch.randn explicitly uses torch.half regardless of cache_dtype, so both dtype cases exercise half storage.

Locations: 965f5b2f0aa69e8d079cbeaffee59443ba9c8044:tests/test_cache_rotate.py — test_rope

Source evidence: call_e1a2eb99e67347609255d15340854c1d

source_inspection: Compared the pytest dtype parametrization with the allocation expression. [call_e1a2eb99e67347609255d15340854c1d]. Limits: Tests were not executed.

## Uncertainty and limits

No extension build, CUDA execution or performance measurement was performed. The Python computation models rotation and address arithmetic only.

The reasons for choosing 128 blocks and 512 threads are not established by the inspected evidence.

The wrapper does not establish contiguity, matching CUDA devices, valid unique page indices, nonempty order or nonaliasing scratch; behavior outside those caller preconditions was not executed.
