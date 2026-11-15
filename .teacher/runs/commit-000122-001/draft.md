# a65386545773f0e1dc66146e7050f6c0f5a9e3e4


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/a65386545773f0e1dc66146e7050f6c0f5a9e3e4) · [Evidence ledger](draft.json)

Adds a tiny positive repetition-factor offset to preserve masked logits at zero penalty weight; full-weight masked logits retain a suspected NaN endpoint.

- [Preserving masked logits during repetition penalties](#sampling)

## Problem

Repetition-penalty interpolation can turn a masked negative-infinity logit into NaN when its history factor is zero: the penalized logit remains negative infinity but is multiplied by zero. [source; call_bb8f7c08d7fa47da891dd0eb0d6eb58c]

## Reasoning

The patch adds 1e-30 to the history factor before interpolation, avoiding the zero multiplier for tokens receiving no repetition penalty without adding a conditional branch. [source; call_2aa27bc75c6f48969799c55755968ee4]

## Impact

A scalar FP32 transcription preserves negative infinity at factor zero after the change, but still produces NaN at factor one. The correction therefore addresses only one endpoint of the interpolation. [execution; call_056567d4201846928f944d9f41a3e7aa]

## Source Notes

The earlier penalty entry describes strongest-recency weighting and FP32 output. The current source retains those mechanisms. [ancestor; call_62a3d882cb204d64b8af13dfe1e2b865]

Issue #8, “RuntimeError: shape '[5120, -1, 128]' is invalid for input of size 776524800,” concerns conversion-time vocabulary padding and reports successful fixes. It does not establish a relationship to this repetition-penalty change. [source; call_9b936f43b9314dc6a5cef19cb6e4391e]

Whole-parent-tree searching for NaN also finds calibration diagnostics, a quantization utility comment and calibration text; those occurrences do not establish the same sampling failure. [source; call_b35b815975ee4961aa886168f1616da4]

<a id="sampling"></a>

## Preserving masked logits during repetition penalties

The kernel initializes per-token factors to zero, assigns one for occurrences inside the sustain window, and otherwise takes the maximum linearly decaying contribution. It computes w as v/rep_p for positive logits and v*rep_p otherwise, then interpolates v*(1-f)+w*f. The patch changes only f, not history scanning or the sign-dependent penalty. [source; call_bb8f7c08d7fa47da891dd0eb0d6eb58c, call_2aa27bc75c6f48969799c55755968ee4]

The 1e-30 constant is a small positive offset, not a history threshold. The scalar check represents it as approximately 1.000000003e-30 in FP32, above the smallest normal FP32 value, while adding it to 0.5 or 1 rounds back to the original factor. [execution; call_056567d4201846928f944d9f41a3e7aa]

SS_RepP.run directly invokes the native wrapper either with initial logits and newly allocated FP32 output or in place on existing logits. Its alternative selects a no-op for rep_p=1 or a nonpositive combined history window. The native wrapper supports batch size one and dispatches half-input or float-input kernel specializations; both receive the correction. [source; call_0dde504411cb4a70b1cbd931456db2db, call_f2ab4dcc06f147adabeeac92a89d4664, call_bb8f7c08d7fa47da891dd0eb0d6eb58c, call_2aa27bc75c6f48969799c55755968ee4]

The offset is a branch-free mitigation rather than complete nonfinite handling. Explicit endpoint selection could avoid evaluating the unused infinity-times-zero term at both endpoints; that alternative is not implemented here. [inference; call_2aa27bc75c6f48969799c55755968ee4, call_056567d4201846928f944d9f41a3e7aa]

## Authoring-time findings — pending review

### masked-full-penalty-endpoint (suspected; defect)

The existing full-penalty endpoint still permits masked logits to become NaN.

Trigger: An enabled repetition penalty receives v=-inf for a token appearing within the sustain window, giving factors[i]=1, with a positive finite rep_p.

Expected: The masked logit remains negative infinity.

Actual: Adding 1e-30 leaves the stored float factor equal to one; v*(1-f) remains negative infinity times zero. The scalar transcription produces NaN before and after the patch.

Locations: a65386545773f0e1dc66146e7050f6c0f5a9e3e4:exllamav3/exllamav3_ext/generator/rep_pen.cu — apply_rep_pens_kernel

Source evidence: call_bb8f7c08d7fa47da891dd0eb0d6eb58c, call_2aa27bc75c6f48969799c55755968ee4, call_0dde504411cb4a70b1cbd931456db2db, call_f2ab4dcc06f147adabeeac92a89d4664

source_inspection: Inspected factor construction, the task diff and both SS_RepP.run call sites found by whole-parent-tree search. The endpoint is carried over and reachable through initial-logit and in-place penalty calls. [call_bb8f7c08d7fa47da891dd0eb0d6eb58c, call_2aa27bc75c6f48969799c55755968ee4, call_0dde504411cb4a70b1cbd931456db2db, call_f2ab4dcc06f147adabeeac92a89d4664]. Limits: Search establishes direct callers, not universal workflow reach.

scalar_transcription: Ran standard-library arithmetic with explicit FP32 rounding for factors zero, one-half and one, using v=-inf and rep_p=1.2. [call_056567d4201846928f944d9f41a3e7aa]. Limits: This models the expression rather than executing the CUDA implementation.

## Uncertainty and limits

No CUDA kernel or repository test was executed. The scalar transcription rounds intermediate operations to FP32 but does not reproduce CUDA compiler contraction, optimization or GPU execution.

The inspected callers establish reach through SS_RepP, not that every generation workflow supplies masked logits or enables repetition penalties.
