# 6693b5010504364efbfd099fdc839aab971e7708


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/6693b5010504364efbfd099fdc839aab971e7708) · [Evidence ledger](draft.json)

Adds adjacent-pair GPTJ reference rotation and float intermediates, but breaks optional-K calls; existing tests neither enable GPTJ nor compare returned outputs.

- [Style-correct reference RoPE](#modules)

## Problem

The Torch reference generated adjacent GPTJ sine/cosine coefficients but applied NEOX split-half rotation, leaving its existing GPTJ rotation helper unused. [source; call_a2c542775282416e81fa3e416c56a7fc]

## Reasoning

The change pairs style-specific coefficient layouts with style-specific rotation helpers and moves reference arithmetic to float before converting results to half. [source; call_fd170c9e76d543ff81989d85272829e9]

## Impact

Adds GPTJ rotation to the reference path, not a new GPT-J model architecture or native kernel. It also introduces an unconditional conversion of optional K that prevents query-only reference calls. [source; call_fd170c9e76d543ff81989d85272829e9, call_a2c542775282416e81fa3e416c56a7fc]

## Source Notes

Read the initial modules entry and the native-GPTJ entry. They establish the reference implementation's origins and record its previously unused GPTJ helper and incomplete partial-rotation support. [ancestor; call_0f69ac2376e64006924a9d042d1dccc9, call_53134a9db20e4850a5fe8b067bbc5878]

The connection to issue #7, “quantizing model: undefined symbol: __cxa_call_terminate,” and closed issue #6, “No ROCm runtime is found, using ROCM_HOME='/usr',” is inferred solely from their rope.py import traceback lines. They describe installation failures, not rotary arithmetic. Issue #29, “Auto-YaRN for Qwen3? Maybe even set it dynamically?”, concerns scaling policy in the same file; that file overlap does not establish motivation for this change. [inference; call_00a9b5c7f2e744a7b96e4d3f033024a1, call_d5fc4efec0ff42deaa358b1b4ccf497a, call_9231e86321674892a908d4cd36b2155e, call_fd170c9e76d543ff81989d85272829e9]

<a id="modules"></a>

## Style-correct reference RoPE

NEOX splits the last dimension into halves and rotates corresponding channels; GPTJ slices even and odd channels and interleaves their rotated values. Both implement (u cos − v sin, v cos + u sin), but with different channel pairings. The new Q/K wrappers reuse the corresponding single-tensor helper for each tensor. [source; call_fd170c9e76d543ff81989d85272829e9, call_a2c542775282416e81fa3e416c56a7fc]

compute_sincos already duplicated frequency coefficients by concatenation for NEOX and repeat-interleave for GPTJ. Dispatching apply_torch to the matching helper supplies the missing pairing agreement; every non-NEOX style takes the GPTJ branch. [source; call_a2c542775282416e81fa3e416c56a7fc, call_fd170c9e76d543ff81989d85272829e9]

Position IDs are explicitly converted to float before the frequency outer product. Removing the half conversion retains float coefficients in the reference cache, while Q/K are converted to float for rotation and then to half. Cache expansion still uses 2048-position allocation increments, not a rotary threshold. Non-in-place results are now explicitly half; in-place mode copies those rounded results into the original tensors. [source; call_fd170c9e76d543ff81989d85272829e9, call_a2c542775282416e81fa3e416c56a7fc]

Whole-tree searches found compute_sincos consumed only by expand_cache, and cached coefficients consumed locally by apply_torch. Renamed application and rotation helpers have no other matched callers. The sole matched direct apply_torch caller is tests/test_rope.py; no RoPE subclass appeared in the whole-tree RoPE search. [source; call_0ce03097da444fe7b4dc2f911769f588, call_d9a7b21c3edd442a9b071ea5b6216bfe, call_b7341b21183247e1b529a6dd55da9671, call_6f933b713f684352b7defce522d6a625, call_2e07d7a4f90149b1a9e221ba246391fe, call_cb5a198a6272410d9bafa9f7479e5295]

A scalar transcription for four channels and two distinct angles matched adjacent-pair rotation exactly, differed from the old split-half application by up to 3.2211, and preserved squared norm within 7.11e−15. This checks the pairing algebra, not repository execution. [execution; call_3afaaec943b64d09af1c281c4d56ca86]

The earlier GPTJ reference mismatch is removed for full-width Q/K inputs. The partial-rotation limitation remains: neither new helper separates an unrotated tail before multiplying by shorter coefficients. [source; call_a2c542775282416e81fa3e416c56a7fc, call_fd170c9e76d543ff81989d85272829e9]

## Authoring-time findings — pending review

### optional-k-conversion (suspected; defect)

The new precision conversions bypass the optional-K guards.

Trigger: Call RoPE.apply_torch(q, None).

Expected: Rotate Q and return a None K through the existing query-only branch.

Actual: k.float() raises before that branch; the later k.half() is also unconditional. Four existing test shapes supply None K.

Locations: 6693b5010504364efbfd099fdc839aab971e7708:exllamav3/util/rope.py — RoPE.apply_torch

Source evidence: call_fd170c9e76d543ff81989d85272829e9, call_d9c1694b8c604d8abf23369e12e653a3

source_inspection: Whole-parent search found the test helper as the sole direct caller; it supplies optional K without a guard. The diff introduces the dereference before existing None-aware handling. [call_2e07d7a4f90149b1a9e221ba246391fe, call_d9c1694b8c604d8abf23369e12e653a3, call_fd170c9e76d543ff81989d85272829e9]. Limits: Not executed; external callers are outside the search.

### reference-test-discarded-results (suspected; defect)

The unchanged comparison test discards both implementations' returned tensors.

Trigger: Run test_rope with non-None K so reference conversion can proceed.

Expected: Compare rotated reference outputs with native outputs.

Actual: Both calls use the default in_place=False and ignore their returns; assertions compare reproducibly regenerated input tensors. Active parametrization also excludes GPTJ.

Locations: 6693b5010504364efbfd099fdc839aab971e7708:tests/test_rope.py — test_rope

Source evidence: call_d9c1694b8c604d8abf23369e12e653a3, call_a2c542775282416e81fa3e416c56a7fc

source_inspection: Inspected the parametrized test and both methods' allocation/return behavior; the task changes neither test nor in-place default. [call_d9c1694b8c604d8abf23369e12e653a3, call_a2c542775282416e81fa3e416c56a7fc, call_fd170c9e76d543ff81989d85272829e9]. Limits: Test weakness established by source inspection, not a measured passing run.

### partial-reference-width (suspected; defect)

Partial rotary dimensions remain unsupported by the reference application.

Trigger: Pass full-width Q/K with head_dim=128 and partial_rotary_factor=0.5 to apply_torch.

Expected: Rotate the first 64 channels and retain the remaining channels.

Actual: Frequency construction produces 64-wide expanded coefficients, while both style helpers multiply the entire 128-wide tensor, producing incompatible last dimensions.

Locations: 6693b5010504364efbfd099fdc839aab971e7708:exllamav3/util/rope.py — RoPE.apply_torch

Source evidence: call_a2c542775282416e81fa3e416c56a7fc, call_fd170c9e76d543ff81989d85272829e9

source_inspection: Compared frequency construction with both new full-vector helpers. The sole matched direct caller sets partial_rotary_factor=1.0, so the inspected test does not exercise this inherited limitation. [call_2e07d7a4f90149b1a9e221ba246391fe, call_d9c1694b8c604d8abf23369e12e653a3, call_a2c542775282416e81fa3e416c56a7fc, call_fd170c9e76d543ff81989d85272829e9]. Limits: No tensor execution.

## Uncertainty and limits

No Torch implementation, CUDA kernel or repository test was executed. The scalar check uses Python double precision, not float intermediates and half rounding.

Whole-tree literal searches establish the inspected repository callers, not dynamic or external consumers.
