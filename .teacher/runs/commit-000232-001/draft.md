# 3637103e2ff4a736544774606ddc964fc4f71362


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/3637103e2ff4a736544774606ddc964fc4f71362) · [Evidence ledger](draft.json)

Exposes GatedMLP padding control while preserving existing defaults; unpadded odd-sized intermediates expose an inherited activation-tail limitation.

- [Controlling GatedMLP projection padding](#modules)

## Problem

GatedMLP previously inherited Linear's fixed default padding to multiples of 128, without exposing the padding control already available on ordinary MLP. [source; call_e8cdd3658bf4405aaf61895a0bda049f, call_e091bd97b55640bcbbb2a7d126b415d4]

## Reasoning

The change appends pad_to=128 to GatedMLP's constructor and passes it to every gate, up and down projection. Applying the same setting to all three preserves agreement between the gated intermediate width and the down projection's input width. [source; call_bd6fe2c3517449a994c9c3fb7d385669, call_e8cdd3658bf4405aaf61895a0bda049f]

## Impact

Callers can request unpadded dimensions with pad_to=1; existing callers retain 128-element alignment. This changes dimension preparation, not the activation or matrix-multiplication implementation. [source; call_bd6fe2c3517449a994c9c3fb7d385669, call_e091bd97b55640bcbbb2a7d126b415d4, call_c60c91d9d924471eb93be1574d4b98c9]

## Source Notes

The initial implementation's modules entry was read. It describes the gate/up activation-multiply pipeline and records that native activation kernels process half2 pairs without an odd-element tail. Inspection of the parent kernel and task diff shows that limitation is carried over, while disabling padding exposes it to odd-sized intermediates. [source; call_9ea15bef772842f584d3b3945ac891c5, call_a8f589daa7364e07b185c9d2de5c4d36, call_bd6fe2c3517449a994c9c3fb7d385669]

Issue #38, “Error converting nvidia/Llama-3_1-Nemotron-Ultra-253B-v1,” reports a sliced-weight loading mismatch; #34, “torch._C._LinAlgError on last layer of quant,” and #42, “converting to 3.0 bpw causes error; block state has 0 inf values and 34 NaN values,” concern conversion numerical failures. Their relevance here is inferred only from shared GatedMLP/Linear paths. None establishes that this padding-parameter change fixes its reported failure. [inference; call_b1a18c3c89a349aaa836cf5f9200155c, call_5df0adec043d4b8ca5b84d05f092c2f8, call_94b37018724d44e782719bd7ddc65646, call_bd6fe2c3517449a994c9c3fb7d385669]

<a id="modules"></a>

## Controlling GatedMLP projection padding

Linear rounds each input and output dimension using (dimension + pad_to - 1) // pad_to * pad_to. Thus 128 is an alignment quantum, not a token threshold; 1 disables rounding. Gate/up retain their input-padding assertion, while down retains allow_input_padding=True. The change supplies a configurable quantum rather than removing those checks. [source; call_e091bd97b55640bcbbb2a7d126b415d4, call_bd6fe2c3517449a994c9c3fb7d385669]

The FP16 path uses the resolved dimensions for weight loading and output allocation. GatedMLP still computes down(activation(gate(x)) * up(x)), overwrites the up result with the gated product and sums slice outputs. Its slicing calculation still aligns ordinary slices to 128 independently of pad_to, and its prohibition on combining fused gate/up weights with slicing remains unchanged. [source; call_e091bd97b55640bcbbb2a7d126b415d4, call_c60c91d9d924471eb93be1574d4b98c9, call_e8cdd3658bf4405aaf61895a0bda049f, call_bd6fe2c3517449a994c9c3fb7d385669]

Whole-tree GatedMLP search and inspection found constructors in Cohere, Cohere2, DeciLM, Gemma2, Gemma3, GLM4, Llama, Phi3 and Qwen3. Each uses named arguments and omits pad_to, so each retains the old default. No subclass appeared in that search. TransformerBlock and ParallelDecoderBlock consume the existing forward result and projection lists without a changed interface. [source; call_0753846c3ea744b5bcd9f01a47672c7e, call_3bf4e3122909424180de4e8d34977e82, call_83e4f29976614c9b82d8515b88407a6b]

A scalar check with hidden width 128 and intermediate width 129 produced intermediate widths 256 under pad_to=128 and 129 under pad_to=1. Modeling the native pairwise activation indexing covered only 128 of 129 elements, leaving index 128 untouched. [execution; call_94a9fc138a214c3aa25a88cb709dee16]

## Authoring-time findings — pending review

### unpadded-odd-activation-tail (suspected; defect)

Disabling padding can expose the inherited activation kernel's missing odd-element tail.

Trigger: A direct GatedMLP caller selects pad_to=1 and runs FP16 projections with an odd total intermediate element count, for example one token, hidden_size=128 and intermediate_size=129.

Expected: Every intermediate element becomes activation(gate) multiplied by up before the down projection.

Actual: act_mul_kernel processes only numel // 2 half2 pairs. With 129 elements, the last up element remains ungated and is consumed by down. No even-element guard is added. The inspected model constructors retain padding, so this observation concerns opt-in callers rather than all existing model workflows.

Locations: 3637103e2ff4a736544774606ddc964fc4f71362:exllamav3/modules/mlp.py — GatedMLP.__init__, 16df3fd1810c4f0747ff4fd5fbcc1dc94c4d6628:exllamav3/exllamav3_ext/activation.cu — act_mul_kernel

Source evidence: call_bd6fe2c3517449a994c9c3fb7d385669, call_e8cdd3658bf4405aaf61895a0bda049f, call_a8f589daa7364e07b185c9d2de5c4d36, call_0753846c3ea744b5bcd9f01a47672c7e, call_3bf4e3122909424180de4e8d34977e82

source_inspection: Traced configurable dimensions through LinearFP16 output allocation to GatedMLP's in-place activation call and subsequent down projection. [call_e091bd97b55640bcbbb2a7d126b415d4, call_c60c91d9d924471eb93be1574d4b98c9, call_e8cdd3658bf4405aaf61895a0bda049f, call_a8f589daa7364e07b185c9d2de5c4d36]. Limits: No GPU execution or loaded checkpoint.

scalar_transcription: Enumerated the kernel's pairwise coverage for 129 elements; index 128 was not written. [call_94a9fc138a214c3aa25a88cb709dee16]. Limits: Integer indexing model only; does not execute CUDA or reproduce FP16 arithmetic.

## Uncertainty and limits

No model, PyTorch projection or CUDA kernel was executed. The bounded computation models integer dimension rounding and kernel coverage only.

The new parameter does not establish arbitrary unpadded EXL3 compatibility or validate all padding values. Quantized backend constraints were not evaluated.
