# 86753399f5772f7b22d63a34efa235b0f7afd613


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/86753399f5772f7b22d63a34efa235b0f7afd613) · [Evidence ledger](draft.json)

Doubles default autosplit reserve from 256 to 512 MiB per device, including missing list entries, but leaves the old default in the docstring.

- [Increase default autosplit memory headroom](#models)

## Problem

The loader previously reserved 0.25 GiB per device when no reserve was supplied, including unspecified entries in a short reserve list. [source; call_107de4f844ec4f4da2e18362ce3feb98]

## Reasoning

Increasing that reserve trades model-placement capacity for additional headroom. The diff does not establish why 0.5 was chosen. [inference; call_107de4f844ec4f4da2e18362ce3feb98, call_8331a2c4bfff4f5e9a83f2fcae9e7708]

## Impact

Default autosplit loading now reserves 0.5 GiB per device. Explicit scalar reserves and supplied list entries retain their values; use_per_device and explicit single-device loading bypass this default. [source; call_107de4f844ec4f4da2e18362ce3feb98, call_2c998fb50fcf4980b2ac5895fdc67647]

## Source Notes

The root models ancestor entry was read. It describes the existing dummy-forward autosplit mechanism and its out-of-memory retry, which this change retains. [ancestor; call_e88653f24aab4a248de9f24756a3370a]

Issue #50, “RuntimeError: Insufficient VRAM in split for model and cache despite remaining 1GB VRAM (exllamav3 + tabbyAPI),” reports apparent unused VRAM. Its discussion describes transient allocations, dummy forwards and configurable reserves. [source; call_b001a92cb5784217bfc72a9d85e1f915]

Issue #50 is relevant by inference because its error text exactly matches _load_autosplit and its discussion names load/load_gen reserves; it is not evidence that this commit fixes the report. Issues #6 (“No ROCm runtime is found, using ROCM_HOME='/usr'”) and #7 (“quantizing model: undefined symbol: __cxa_call_terminate”) instead report import/build failures. Their inferred connection is only the shared model.py traceback path, not the changed reserve logic. [inference; call_b001a92cb5784217bfc72a9d85e1f915, call_bd162201350843c0b2c07511539c8c1a, call_a2e49cfc3a344a49b57849f7faab392b, call_7dee1893abd24c1e8c3667c788d66fca, call_107de4f844ec4f4da2e18362ce3feb98]

<a id="models"></a>

## Increase default autosplit memory headroom

Both edits are needed for a consistent default: None initializes every device to 0.5, while a short list is extended with 0.5. Values are converted using int(x * 1024**3), so these are GiB despite the docstring's GB terminology. Negative explicit entries still exclude devices. [source; call_107de4f844ec4f4da2e18362ce3feb98, call_2c998fb50fcf4980b2ac5895fdc67647]

A bounded Python scalar calculation gives 268,435,456 bytes for the old default and 536,870,912 for the new one: an additional 256 MiB per defaulted device. [execution; call_abe8ef97af904009ae5454c1d0dd751c]

_load_autosplit passes the byte reserve to set_memory_fraction_reserve when entering a device. That helper touches the device, reads free and total memory, and sets the process memory fraction to (free - reserve) / total; it does not allocate a reserve tensor. Autosplit loads modules and runs dummy forwards, advancing to another device after recognized out-of-memory errors. On normal completion it restores touched devices' fractions. [source; call_bd162201350843c0b2c07511539c8c1a, call_2c998fb50fcf4980b2ac5895fdc67647, call_8331a2c4bfff4f5e9a83f2fcae9e7708]

The larger default can make autosplit advance earlier or exhaust its device list sooner, while leaving more headroom outside the loading budget. Users can retain the old budget with an explicit 0.25 reserve; use_per_device remains a separate budgeting alternative. [inference; call_107de4f844ec4f4da2e18362ce3feb98, call_bd162201350843c0b2c07511539c8c1a, call_8331a2c4bfff4f5e9a83f2fcae9e7708]

The whole-tree load_gen search finds direct calls in examples/loading.py and the Model.load wrapper. Both example generator calls omit memory overrides and therefore select the changed default; the wrapper forwards its caller's arguments. [source; call_87c9e257ad184597a40507a1b66cf85b, call_d3269cf1b4b2448c90ceebd69b25635f, call_2c998fb50fcf4980b2ac5895fdc67647]

## Authoring-time findings — pending review

### stale-reserve-docstring (suspected; defect)

The load_gen docstring retains the old default after both runtime defaults change.

Trigger: A caller consults load_gen's reserve_per_device documentation, also referenced by Model.load.

Expected: Documentation states the new 0.5 GiB default for omitted reserves and missing list entries.

Actual: The unchanged docstring states 0.25 GB, whereas the changed implementation uses 0.5 multiplied by 1024**3.

Locations: 86753399f5772f7b22d63a34efa235b0f7afd613:exllamav3/models/model.py — Model.load_gen

Source evidence: call_107de4f844ec4f4da2e18362ce3feb98, call_2c998fb50fcf4980b2ac5895fdc67647

source_inspection: Compared the complete task diff with the parent docstring and wrapper. Searched the whole parent tree for reserve_per_device and load_gen callers; inspected the direct example calls. The mismatch concerns public documentation, not proof of a runtime failure. [call_041a8c5f9f6243dd81712a95542c3422, call_87c9e257ad184597a40507a1b66cf85b, call_d3269cf1b4b2448c90ceebd69b25635f, call_107de4f844ec4f4da2e18362ce3feb98, call_2c998fb50fcf4980b2ac5895fdc67647]. Limits: No documentation rendering or repository runtime execution.

## Uncertainty and limits

No GPU loading, placement, stability or throughput measurements were performed. The scalar computation checks byte conversion only.

The evidence does not establish an optimal reserve or connect this commit explicitly to issue #50.
