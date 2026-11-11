# 07b9e59ddb02e035119b98dcffaf319f1f3ee6b8


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/07b9e59ddb02e035119b98dcffaf319f1f3ee6b8) · [Evidence ledger](draft.json)

Corrects Model.load's usage-budget example to pass use_per_device instead of reserve_per_device, without changing runtime logic.

- [Distinguish usage budgets from reserved memory](#models)

## Problem

The use_per_device example mistakenly passed reserve_per_device, selecting memory reservation rather than the documented per-device usage limits. [source; call_a56ae276fad546d4a14020b7dd63e2c1, call_0e379d0928ac4a2e9706f2629401b1ab]

## Reasoning

Changing the example's keyword aligns it with the existing loader: positive usage entries select devices, whereas nonnegative reservation entries retain devices. [source; call_a56ae276fad546d4a14020b7dd63e2c1, call_0e379d0928ac4a2e9706f2629401b1ab]

## Impact

The correction changes guidance for callers copying the example; it does not change executable loading logic or defaults. [source; call_a56ae276fad546d4a14020b7dd63e2c1]

<a id="models"></a>

## Distinguish usage budgets from reserved memory

Model.load now illustrates use_per_device=[23, 0, 23]. Its usage branch converts entries to bytes and selects only positive entries, so the example selects cuda:0 and cuda:2, excluding cuda:1 and omitted devices. [source; call_a56ae276fad546d4a14020b7dd63e2c1, call_0e379d0928ac4a2e9706f2629401b1ab]

The alternative reserve_per_device interface keeps nonnegative entries active and pads omitted devices with a 0.25 reserve. Thus zero does not exclude a device in that interface. _load_autosplit dispatches the resulting budgets to distinct reservation or usage memory-limit helpers. [source; call_0e379d0928ac4a2e9706f2629401b1ab, call_9214528ce71244f793be8677c1dfcd1c]

Although the docstring says GB, normalization multiplies by 1024³, making 23 a 23-GiB budget. A scalar transcription produced 24,696,061,952 bytes and active devices [0, 2]; the old reservation example retained all four devices in a four-device scenario. [execution; call_0e379d0928ac4a2e9706f2629401b1ab, call_6051d60ebba749eabab4db008993d10c]

## Uncertainty and limits

The scalar check models argument normalization and device selection only; no model loading, CUDA allocation, or enforcement of memory limits was executed.
