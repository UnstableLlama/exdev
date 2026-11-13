# 00bbb58384359ced00025238360cdcdcafad7c3c


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/00bbb58384359ced00025238360cdcdcafad7c3c) · [Evidence ledger](draft.json)

Adds a Python-exposed CUDA diagnostic that compares normalized input and exhaustive 3INST codebook histograms using a single shared-memory block.

- [CUDA distribution comparison diagnostic](#quantizer)

## Problem

The change adds a diagnostic for comparing a tensor's value distribution with the procedural codebook, rather than changing quantization itself. [source; call_d9709749784742469850627572a7dba6]

## Reasoning

A single CUDA block reuses a shared histogram: first counting every 16-bit codebook state, then counting input elements. Separate normalization produces comparable probability masses despite different sample counts. [source; call_d9709749784742469850627572a7dba6]

## Impact

Python gains the extension entry point test_distribution(input, dist_output, ref_output, min_value, max_value), which writes into caller-provided outputs. The parent-tree search finds no existing callers, and the diff adds no workflow integration. [source; call_2e4ff436f8754160a18d7d28aace6cff, call_d98b679676ba4c3cb7d69f87b3728880, call_9eb73fb693b74792a055a9dba68094b9, call_d9709749784742469850627572a7dba6]

## Source Notes

The inspected discussions report an undefined __cxa_call_terminate symbol (#7), incoherent Cogito output at bpw <= 2.5 (#15), an invalid CUDA configuration during conversion (#16), and missing torch during installation (#17). None explicitly connects its report to this histogram addition. [source; call_242066abe80e42bf8c82cbcd1fcbdbdf, call_69d24f530c234360b3df20824c550ee3, call_5f03a84dff9b44b4b1103f5aef74a09e, call_53808808ae04445bb12195f317a10105]

<a id="quantizer"></a>

## CUDA distribution comparison diagnostic

The wrapper selects the input device and current CUDA stream, checks that input is float32, derives the bin count from ref_output.numel(), and launches one block of 1024 threads. MAX_BINS=1024 bounds the shared integer histogram; the source explicitly describes the routine as not optimized. [source; call_d9709749784742469850627572a7dba6]

Each sample is transformed by (value-min_value)/(max_value-min_value)*num_bins, converted to an integer and clamped into the end bins. Thus out-of-range values contribute to endpoint mass rather than being discarded. Counts are divided by sample count, not bin width, so the outputs are normalized histograms rather than probability densities. [source; call_d9709749784742469850627572a7dba6]

The reference enumerates 65,536 states, the complete uint16_t domain, through decode_3inst_f. That function converts the half-precision 3INST result to float; the existing decode_pcb_f also selects 3INST, while 2MAD remains a commented-out alternative. The diagnostic hardcodes 3INST rather than following the generic decoder selector. [source; call_d9709749784742469850627572a7dba6, call_e1355c70e4de46f29fe86ce72f49b94f]

A standard-library scalar transcription enumerated all 65,536 states, yielding extrema -3.95703125 and 3.97265625. With 16 bins over [-4,4], counts totaled 65,536 and normalized mass totaled 1.0. The launch divides reference enumeration into 64 states per thread and uses 4096 bytes for 1024 four-byte counters. [execution; call_40724d7f504e439eb68ba8fff184c195]

Reusing one shared histogram avoids a multi-block reduction, but limits parallelism and concentrates atomic updates within one block. This is consistent with a simple diagnostic implementation, not evidence of a performance improvement. [inference; call_d9709749784742469850627572a7dba6]

## Authoring-time findings — pending review

### unchecked-output-capacity (suspected; defect)

The newly exposed diagnostic does not validate the destination histogram capacity.

Trigger: Call test_distribution with valid contiguous CUDA float32 input, ref_output containing N bins where 1 <= N <= 1024, and dist_output containing fewer than N float32 elements.

Expected: Reject the mismatched output capacity before launching the kernel.

Actual: The wrapper derives N solely from ref_output; write_histogram writes N floats through dist_output's raw pointer without checking its size, potentially writing beyond its allocation. Reach is direct extension callers; no parent-tree callers or new workflow call sites were found.

Locations: 00bbb58384359ced00025238360cdcdcafad7c3c:exllamav3/exllamav3_ext/quant/quantize.cu — test_distribution

Source evidence: call_d9709749784742469850627572a7dba6, call_9eb73fb693b74792a055a9dba68094b9, call_2e4ff436f8754160a18d7d28aace6cff

source_inspection: Traced ref_output.numel() through the launch argument to both output-writing loops and inspected the complete wrapper checks and caller search. [call_d9709749784742469850627572a7dba6, call_9eb73fb693b74792a055a9dba68094b9]. Limits: No malformed invocation was executed; memory corruption or a specific CUDA error was not observed.

## Uncertainty and limits

No extension build or GPU execution was performed; CUDA synchronization, launch success and performance remain unmeasured.

The scalar check models unsigned 32-bit decoder arithmetic and binary16 rounding, but uses Python arithmetic for histogram indexing; it does not establish CUDA behavior for nonfinite values, invalid ranges or integer overflow.

The caller search establishes absence of literal parent-tree references, not absence of external or dynamically constructed calls.
