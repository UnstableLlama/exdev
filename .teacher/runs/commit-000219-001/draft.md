# 62e8832603ffc3c8089417f384f14d57f3ef6a52


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/62e8832603ffc3c8089417f384f14d57f3ef6a52) · [Evidence ledger](draft.json)

Exposes ordinary MLP projection alignment so pad_to=1 preserves unpadded dimensions, retaining the default 128 alignment. Also adds an activation_fn argument that remains unused.

- [Optional unpadded ordinary MLP projections](#modules)

## Problem

Ordinary MLP projections implicitly used Linear's 128-element alignment. Because both projections disallow input padding, hidden and intermediate widths not divisible by 128 could fail construction. [source; call_27899c0506db4650ae34875e776164c2, call_088845fa60064d13b92923449748037e]

## Reasoning

The change exposes pad_to on MLP and forwards it to both projections. Setting pad_to=1 preserves the requested dimensions without removing Linear's input-padding assertion; the default 128 preserves prior behavior. [source; call_a0af1b039f0941b8a6b1801e5d01c226, call_088845fa60064d13b92923449748037e]

## Impact

This enables callers to construct unpadded ordinary MLPs, rather than changing GatedMLP or automatically selecting unpadded storage for existing models. The whole-parent-tree MLP search found no ordinary MLP construction sites or subclasses. [source; call_a0af1b039f0941b8a6b1801e5d01c226, call_c9cde48334f0414c98112c8538408749]

## Source Notes

The initial modules entry was read. It establishes the original distinction between ordinary down(silu(up(x))) computation and GatedMLP's selectable activation. [ancestor; call_8a2cdb527e5a4811b8f5a26d4106e45b]

Issue #38, “Error converting nvidia/Llama-3_1-Nemotron-Ultra-253B-v1,” reports sliced GatedMLP loading failure. Issues #34, “torch._C._LinAlgError on last layer of quant,” and #42, “converting to 3.0 bpw causes error; block state has 0 inf values and 34 NaN values,” report quantization failures. Their connection here is inferred only from shared mlp.py/linear.py paths; none establishes that this ordinary-MLP change fixes those reports. [inference; call_2e75e6b9af2546d684c276977f6a9613, call_4666d5c28e4a4fe1bbf20051f5c3bb20, call_34ddeb9d3c6e49a5873cb3852a7a75d1, call_a0af1b039f0941b8a6b1801e5d01c226]

<a id="modules"></a>

## Optional unpadded ordinary MLP projections

pad_to is an alignment multiple, not a dtype selector. Linear rounds each dimension with ceil(width/pad_to)*pad_to. Passing the same alignment to up and down keeps their intermediate dimensions consistent; using 1 leaves both hidden and intermediate widths exact. [source; call_a0af1b039f0941b8a6b1801e5d01c226, call_088845fa60064d13b92923449748037e]

For ordinary weights, Linear.load_fp16 passes the resolved dimensions as loader padding targets and constructs LinearFP16 with them. LinearFP16.forward preserves leading dimensions and uses its out_features for the output width, selecting torch.matmul when input and output dtypes agree and ext.hgemm otherwise. The patch changes dimension preparation, not that execution dispatch. [source; call_088845fa60064d13b92923449748037e, call_8a57b4e0edeb465ab0dd2ed562c1b64f, call_a0af1b039f0941b8a6b1801e5d01c226]

A standard-library transcription checked widths 130 and 257: alignment 128 produces 256 and 384 and fails both input-equality conditions; alignment 1 preserves 130 and 257 and satisfies them. It also checked identity for widths 1 through 1024 at alignment 1. [execution; call_46d94011a71b4cc3995e940b2abd6bdb]

MLP.forward remains up → SiLU → down with its existing output-dtype conversion. The newly accepted activation_fn argument is not stored or consumed, unlike GatedMLP's existing activation selector. [source; call_27899c0506db4650ae34875e776164c2, call_a0af1b039f0941b8a6b1801e5d01c226]

## Authoring-time findings — pending review

### ignored-activation (suspected; defect)

The added activation_fn parameter silently has no effect.

Trigger: An external caller constructs an otherwise valid MLP with activation_fn="gelu" and then calls forward.

Expected: Honor the requested activation or explicitly reject unsupported selections.

Actual: The constructor ignores activation_fn and forward unconditionally applies F.silu. No in-tree ordinary MLP constructor caller was found, so demonstrated reach is the exposed API rather than an existing model workflow.

Locations: 62e8832603ffc3c8089417f384f14d57f3ef6a52:exllamav3/modules/mlp.py — MLP.__init__ / MLP.forward

Source evidence: call_a0af1b039f0941b8a6b1801e5d01c226, call_27899c0506db4650ae34875e776164c2, call_c9cde48334f0414c98112c8538408749

source_inspection: Compared the complete patch with the parent constructor and forward method; searched the whole parent tree for MLP references and inspected transformer consumers. [call_a0af1b039f0941b8a6b1801e5d01c226, call_27899c0506db4650ae34875e776164c2, call_c9cde48334f0414c98112c8538408749, call_ff23b92269fb4d12bc35438f9796e6da]. Limits: No runtime activation comparison or external caller inspection.

## Uncertainty and limits

No model, tensor loader, PyTorch operation or GPU kernel was executed. The scalar check establishes dimension arithmetic only, not arbitrary-width FP16 or EXL3 runtime compatibility.

The repository search establishes no ordinary MLP constructor callers; dynamic or external callers remain outside that evidence.
