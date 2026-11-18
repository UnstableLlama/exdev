# 754450f6ad4de88dce348f67099a61de14072237


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/754450f6ad4de88dce348f67099a61de14072237) · [Evidence ledger](draft.json)

Requests FP32 down-projection outputs throughout Llama's shared constructor. The existing FP32 residual stream preserves the wider result through block addition; backend execution and conversion success were not independently tested.

- [Keep Llama down-projection results wide through the residual stream](#models)

## Problem

Llama's gated MLP previously left down-projection output at the linear backends' FP16 default. Widening that result only after projection cannot recover a value already overflowed during FP16 output storage. [source; call_0940ed7aa3f94007a0cb63fcf32185de, call_d029f6676b294405ad07b4f50d918020, call_b7016771323a488d9cb2ce48d157966e, call_4e10dc2e257044d79a0509724b42e2e2]

## Reasoning

The one-line change requests torch.float at GatedMLP construction. Existing plumbing carries this choice into every down projection before its output is allocated, rather than merely casting the completed MLP result. [source; call_af5f80db7c6142d992160849f685e6f2, call_d029f6676b294405ad07b4f50d918020, call_2639054d91a648ab9ce16e66054e3bc7]

## Impact

This is a targeted numerical behavior change: down outputs and sliced-down accumulation become FP32, while gate/up computation, attention output precision and the already-FP32 residual stream are unchanged. [source; call_af5f80db7c6142d992160849f685e6f2, call_d029f6676b294405ad07b4f50d918020, call_63874a9c58c9434d876cb16be08380f6, call_adc86504442b4808b03f2bd3c200eebe, call_ca2ecd4e0b8743eca69aab2abee4ae85]

## Source Notes

Read the initial commit's models and modules chapters and the cache-construction entry 4fa0e686. They establish the shared constructor, module sequence, FP32 embedding default and residual-storage design. The initial models chapter also records a Mistral sliding-window mapping gap; inspection of the current Mistral/Llama constructors and this diff shows that omission is carried over, not corrected by this precision change. [ancestor; call_9b21fe72a58140e793b0857c5911a1db, call_b5d23e517ef043359c228540d9e732b5, call_3e01ae6a180747fbaa70503a228fba84]

The task changes only the GatedMLP constructor argument. Mistral still supplies no sliding-window adaptation, and Llama's Attention construction still omits sliding_window, whose default is -1. [source; call_bf4ab54222034bd39cfedeb313ba3802, call_0940ed7aa3f94007a0cb63fcf32185de, call_ca2ecd4e0b8743eca69aab2abee4ae85, call_af5f80db7c6142d992160849f685e6f2]

Other inspected discussions have different framing: “torch._C._LinAlgError on last layer of quant” concerns Command-A and suspected activation overflow; “converting to 3.0 bpw causes error; block state has 0 inf values and 34 NaN values” includes Midnight-Miqu and Command-R+ reports. Their relationship to this task is inference from shared conversion errors and linear.py references, not evidence of an identical cause. “quantizing model: undefined symbol: __cxa_call_terminate” reports an extension-import/toolchain problem; “`RuntimeError` when requesting logprobs with Gemma 3 models” reports a tensor-size mismatch. Neither establishes a down-output overflow. [inference; call_a1ba874c7a1b4beaab5ac0ec358a6792, call_f393d2d63dc74a52ba60f712409c620c, call_65fbac544961449e955869944a434eb7, call_3e9148dbade74670b08811ff46092b75, call_da803cd3f6a84932bb679ea3afbb12f5]

<a id="models"></a>

## Keep Llama down-projection results wide through the residual stream

LlamaModel.__init__ adds out_dtype=torch.float to the GatedMLP created for every configured transformer layer. GatedMLP stores that argument and passes it to each Linear in self.downs, including sliced projections. Gate and up projections instead use interm_dtype, which this constructor leaves unset. During forward, each slice produces d_; the first becomes d and subsequent slices accumulate with d += d_. The final to2 preserves the configured float output unless explicitly overridden. [source; call_af5f80db7c6142d992160849f685e6f2, call_0940ed7aa3f94007a0cb63fcf32185de, call_d029f6676b294405ad07b4f50d918020, call_e6c78f4fbd304e74923cec49eccbdf2a]

Slicing is an existing mechanism, not a new restriction: the default intermediate-width limit is 55,296. Above it, GatedMLP divides the intermediate axis into slices, aligning ordinary slice widths to 128 and assigning the remainder to the last slice. Every slice's down output receives the new dtype, so both individual partial outputs and their sum avoid FP16 output storage. [source; call_7b05f1b5757744178eb3e839a520ae52, call_d029f6676b294405ad07b4f50d918020, call_af5f80db7c6142d992160849f685e6f2]

Linear forwards its stored output dtype when loading ordinary weights, loading EXL3 weights, or replacing an ordinary backend during convert_exl3. LinearFP16.forward allocates the requested output dtype; with half input and float output it selects ext.hgemm instead of the same-dtype torch.matmul branch. The native hgemm accepts half operands and float output, selecting cublasGemmEx with FP32 computation and output. This is not an FP16 result followed by a float cast. [source; call_2639054d91a648ab9ce16e66054e3bc7, call_b7016771323a488d9cb2ce48d157966e, call_6e8485a989524260a7f040383ea358f5]

LinearEXL3.forward likewise allocates its result in the requested dtype in both execution routes. The reconstruction route uses half transformed inputs and reconstructed half weights, hgemm into the requested output, then an output Hadamard transform. The direct route passes the float output buffer to exl3_gemm, whose wrapper accepts half input and float or half output and passes the output-type flag to kernel selection. The existing default selects reconstruction above 32 flattened input rows, unless params['reconstruct'] overrides it; this patch does not change that threshold. [source; call_4e10dc2e257044d79a0509724b42e2e2, call_b74f51ac433e4610bfd5a3a2a0b7e762, call_6e8485a989524260a7f040383ea358f5]

The receiving tensor in TransformerBlock.forward is x, not the normalized branch tensor y. Llama leaves Embedding.out_dtype at its torch.float default, so ordinary model execution starts the residual stream in FP32. Device preparation moves x without requesting another dtype. Each block normalizes x into a separate half-precision y for attention and again for the MLP; neither normalization replaces the residual tensor. Llama supplies no branch post-normalizations and no block output dtype. [source; call_0940ed7aa3f94007a0cb63fcf32185de, call_63874a9c58c9434d876cb16be08380f6, call_27855ad7ba20461fa29293f44bfdc94e, call_adc86504442b4808b03f2bd3c200eebe]

Attention returns an FP16 result for this constructor: no output dtype is supplied to Attention or its o_proj, and both linear backends default to half. The block combines it with FP32 x using x += y. Under the in-place tensor-add semantics expressed here, the half operand is combined into the destination's FP32 storage; the operation does not turn x into half. After this patch, the MLP addition combines FP32 y with FP32 x. Thus the widened down result is not immediately narrowed at the residual addition. Actual mixed-dtype execution was not tested. [inference; call_0940ed7aa3f94007a0cb63fcf32185de, call_ca2ecd4e0b8743eca69aab2abee4ae85, call_b7016771323a488d9cb2ce48d157966e, call_4e10dc2e257044d79a0509724b42e2e2, call_adc86504442b4808b03f2bd3c200eebe, call_63874a9c58c9434d876cb16be08380f6]

The block returns FP32 x on the normal path because neither forward nor constructor requests an output conversion. Model.forward passes it to the next block, whose input RMSNorm produces half branch input while retaining FP32 residual storage. After the last block, model.norm consumes that FP32 state and explicitly produces half output for lm_head. Consequently, a finite down result needing more than FP16 range can retain that range through residual combination and into the next normalization. Compared with the parent, the residual dtype is unchanged; the correction removes the earlier FP16 down-output bottleneck. This is a numerical bugfix, not evidence of a residual-narrowing defect. [inference; call_adc86504442b4808b03f2bd3c200eebe, call_e6c78f4fbd304e74923cec49eccbdf2a, call_8d1245850f754e53aa25f998f26647da, call_8254ebe27ccb46d581e0eb3f9a7c88b4, call_0940ed7aa3f94007a0cb63fcf32185de, call_af5f80db7c6142d992160849f685e6f2]

A bounded standard-library storage-range check decoded binary16's largest finite value as 65,504. It represented 70,000 in binary32 and modeled adding it to a binary32 residual of 1,000 as 71,000; two binary32 sliced partials of 40,000 summed to 80,000. Binary16 packing of 70,000 raised OverflowError. These examples illustrate the removed storage bottleneck, not execution of either backend or PyTorch's addition. [execution; call_06b29fa9a645410b9633c0d724e72168]

Whole-parent-tree LlamaModel search finds MistralModel, Qwen2Model and MiMoModel as subclasses. Each inspected constructor delegates directly to LlamaModel.__init__, so each inherits this change. Other independently constructed model classes are not covered merely because they also use GatedMLP. [source; call_705942d084054fc8b07dff1f1257b3a5, call_bf4ab54222034bd39cfedeb313ba3802, call_3be3f5d631a04a5780ad9a67e6966873, call_0cfb9b3224bb43e2aceae8e03a7d1225]

Reference configs read were TinyLlama-1.1B-Chat-v1.0, Qwen2.5-0.5B, Mistral-7B-v0.1 and MiMo-7B-Base, -RL, -RL-0530, -RL-Zero and -SFT. Each names the corresponding shared-constructor architecture and SiLU activation. TinyLlama has hidden/intermediate widths 2048/5632; Qwen2.5 has 896/4864; Mistral has 4096/14336. Each MiMo variant has 4096/11008 and 36 layers. All these intermediate widths stay below the slicing limit. Their declared bfloat16 checkpoint dtype does not override the constructor's FP32 down-output choice; this does not establish complete compatibility with their other configuration features. [source; call_ee4351f8b001479785bcad13f71e0f25, call_ca7d6c3d196649fcbf58a5d0a4de8e26, call_a7f68dfac97f43a28659d4a9276bc93e, call_8a152d7b578c4016a24e78d6d99f9f9a, call_326c37d4d01c421f8de85810c04c9fae, call_7a25cd46c23c46d9b65931acb6b124a6, call_a43e3f2a3d6d4d71bb2971898b5fdf18, call_b9a000d7c38b4471a728e9ce0023c049, call_d029f6676b294405ad07b4f50d918020]

The strongest discussion connection is inferential but specific: “Error converting moonshotai/Kimi-Dev-72B” reports Qwen2ForCausalLM conversion failures and a NaN after the final normalization. Task author turboderp proposed exactly out_dtype=torch.float at Llama's GatedMLP call, explaining suspected last-layer overflow; reporter artus-dev subsequently reported a successful conversion with that proposal. This matches the task's exact edit. The reporter and fix author are different contributors, and the report is not a conversion executed in this session. [inference; call_955c03794fe249d9a2b7f7caea98f42b, call_af5f80db7c6142d992160849f685e6f2, call_3be3f5d631a04a5780ad9a67e6966873]

The targeted tradeoff is wider down-result buffers and accumulation without widening gate/up activations or the whole attention branch. Casting only the final MLP return would be too late; the existing backend output-allocation mechanism is essential. Source inspection supports that data-flow explanation, but not a measured memory cost, speed change, or universal prevention of nonfinite values. [inference; call_d029f6676b294405ad07b4f50d918020, call_b7016771323a488d9cb2ce48d157966e, call_4e10dc2e257044d79a0509724b42e2e2, call_af5f80db7c6142d992160849f685e6f2]

## Uncertainty and limits

No repository model, PyTorch mixed-dtype addition, CUDA kernel or conversion was executed. Runtime success, numerical accuracy and performance remain unmeasured.

The scalar check models storage range with Python struct, not GPU arithmetic. Its FP16 overflow raises OverflowError rather than reproducing CUDA's overflow conversion.

Wider down outputs do not protect against nonfinite gate/up activations, attention outputs, or values exceeding FP32 range. Explicit forward dtype overrides and manually supplied block inputs can differ from the normal constructor-driven path.

Reference configurations establish configuration values, not checkpoint numerical behavior or complete architectural equivalence.
