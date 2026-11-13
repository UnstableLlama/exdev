# bcc096667169d8f34c602ce495b372e3fc9afd2b


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/bcc096667169d8f34c602ce495b372e3fc9afd2b) · [Evidence ledger](draft.json)

Implements native GPTJ adjacent-pair RoPE while retaining existing dispatch and position handling; the Torch alternative and partial-frequency bounds concern remain.

- [Adjacent-pair GPTJ rotary execution](#modules)

## Problem

GPTJ rotary style was already selectable, but its CUDA specialization contained only a TODO and wrote no rotated output. [source; call_4fa0c19373f541aaa9fc1ec5ee6abbec, call_784b029bd92f4df2af378719cc7b9b95]

## Reasoning

The change implements adjacent-channel rotation within the existing kernel rather than adding another positional-frequency pipeline. [source; call_7192cb6d99994abe81198d9f5cd607dd]

## Impact

Native GPTJ calls now rotate Q and optional K; this does not register a GPT-J model architecture or complete the Torch reference implementation. [source; call_7192cb6d99994abe81198d9f5cd607dd, call_3cf749b4802a4f598c4e3d6676af849c, call_784b029bd92f4df2af378719cc7b9b95]

## Source Notes

The earlier modules entry identified the empty GPTJ branch and partial-rotation frequency-read concern. Inspection of this patch shows the former implemented and the latter carried over. [inference; call_d9b57de42b0b4d2eb3a61d797b9f1e41, call_4fa0c19373f541aaa9fc1ec5ee6abbec, call_7192cb6d99994abe81198d9f5cd607dd]

Issue #7, “quantizing model: undefined symbol: __cxa_call_terminate,” includes util/rope.py in its import traceback. Its connection here is only an inferred file overlap: the reporter describes an environment/compiler remedy, not GPTJ rotation. The reviewed reports of incoherent low-bitrate output (#15), invalid CUDA configuration (#16), and missing torch during requirements installation (#17) do not establish motivation for this patch. [inference; call_39fed8ee10a64f1caf00bd750af26079, call_5f35cf1e899441a29055dae3799818e4, call_fb3ada9f39004aa386e6639003341bb2, call_a95c4863d1c246b7a0cf72cbe9b0b877, call_7192cb6d99994abe81198d9f5cd607dd]

<a id="modules"></a>

## Adjacent-pair GPTJ rotary execution

For pair index t, GPTJ addresses channels 2t and 2t+1 and computes (u·cos−v·sin, v·cos+u·sin), with float intermediates and round-to-nearest half outputs. NEOX instead pairs t with t+partial_head_dim/2. Both modes share position selection, inverse frequencies and attention-factor scaling. [source; call_7192cb6d99994abe81198d9f5cd607dd, call_4fa0c19373f541aaa9fc1ec5ee6abbec]

partial_head_dim is twice the inverse-frequency count. GPTJ rotates pairs below that count and copies remaining adjacent pairs using half2. The launch still uses head_dim/2 threads along x and at most 1024 threads per block, distributing Q and K heads along y with a strided loop. The NEOX copy rewrite preserves its original address arithmetic. [source; call_7192cb6d99994abe81198d9f5cd607dd, call_4fa0c19373f541aaa9fc1ec5ee6abbec]

Named dispatch constants preserve GPTJ=1 and NEOX=2 rather than changing selection semantics. RoPE.apply makes inputs contiguous, chooses allocated or in-place outputs and forwards the configured style to ext.rope. Inspected attention callers consume its returned Q/K before SDPA or FlashAttention. [source; call_7192cb6d99994abe81198d9f5cd607dd, call_784b029bd92f4df2af378719cc7b9b95, call_70ede631d93e4913acd35cf6c15dfb2c]

The new _rotate_half_gptj helper constructs interleaved (−odd, even) channels, but no call site is added. apply_torch still uses split-half rotation; its TODO now explicitly mentions GPTJ and partial rotary factors. Existing test parametrization enables only NEOX. [source; call_3cf749b4802a4f598c4e3d6676af849c, call_784b029bd92f4df2af378719cc7b9b95, call_526fc5d10f9c4f40a1c716adc713a282]

A scalar transcription checked adjacent-pair destination coverage for head/rotary dimensions 8/8, 8/4, 128/128 and 128/64. Every channel was covered once. A four-channel rotation preserved squared norm within 3.6e−15 while differing from the unchanged split-half formula. [execution; call_b23cd757206f48db9136f1fcc0cfceed]

The accompanying Hadamard edit widens the device annotation to torch.device | str without changing its conversion, scaling or caching implementation. [source; call_76045bea15f8409c812228b49e0d8ea3]

## Authoring-time findings — pending review

### partial-frequency-read (suspected; defect)

The inherited unconditional frequency read remains outside the partial-rotation guard.

Trigger: A partial rotary frequency array shorter than head_dim/2 reaches rope_kernel.

Expected: Threads copying unrotated channels should not read beyond the frequency array.

Actual: All x threads evaluate inv_freq[t] before the rotation/copy branch. For head_dim=128 and rotary_dim=64, 32 source-level frequency indices exceed the 32-element array. Actual GPU consequences are untested.

Locations: bcc096667169d8f34c602ce495b372e3fc9afd2b:exllamav3/exllamav3_ext/rope.cu — rope_kernel

Source evidence: call_4fa0c19373f541aaa9fc1ec5ee6abbec, call_7192cb6d99994abe81198d9f5cd607dd, call_784b029bd92f4df2af378719cc7b9b95

source_inspection: The parent-tree search locates ext.rope in RoPE.apply and three attention callers of self.rope.apply. Their reach is conditional on supplying partial frequencies; it is not evidence that every model uses them. The task diff leaves the shared read and launch unchanged. [call_3966534e7632463eb4e1e01b6a23df8c, call_9867f6c103474b51b58b50314cc4be32, call_70ede631d93e4913acd35cf6c15dfb2c, call_7192cb6d99994abe81198d9f5cd607dd]. Limits: Source-level bounds concern, not a measured CUDA fault.

scalar_transcription: Counted launched frequency indices outside the partial array for two bounded examples. [call_b23cd757206f48db9136f1fcc0cfceed]. Limits: Integer indexing model only.

### torch-gptj-reference (suspected; defect)

The Torch alternative remains incompatible with general GPTJ adjacent-pair rotation.

Trigger: Calling RoPE.apply_torch with GPTJ style on a four-or-more-channel head at a nontrivial angle.

Expected: Use adjacent even/odd channel pairs, matching the newly implemented native GPTJ path.

Actual: compute_sincos repeats adjacent coefficients, but the application helpers still call split-half _rotate_half rather than the newly added _rotate_half_gptj.

Locations: bcc096667169d8f34c602ce495b372e3fc9afd2b:exllamav3/util/rope.py — RoPE.apply_torch

Source evidence: call_784b029bd92f4df2af378719cc7b9b95, call_3cf749b4802a4f598c4e3d6676af849c

source_inspection: Whole-parent search finds the direct apply_torch caller in tests/test_rope.py, whose active styles include only NEOX. Inspected attention paths use native apply instead. [call_ca4553eb93904e999312dc175beda93d, call_526fc5d10f9c4f40a1c716adc713a282, call_70ede631d93e4913acd35cf6c15dfb2c]. Limits: External callers are not covered by repository search.

scalar_transcription: Compared adjacent-pair and split-half formulas for [1,2,3,4] with angle 0.7; outputs differed. [call_b23cd757206f48db9136f1fcc0cfceed]. Limits: Executed scalar formulas, not Torch or CUDA implementations.

## Uncertainty and limits

No CUDA compilation, kernel execution, model inference or performance measurement was performed.

The scalar check uses Python double precision, not CUDA fast trigonometry, float intermediates or FP16 rounding; it cannot establish device-memory behavior.
