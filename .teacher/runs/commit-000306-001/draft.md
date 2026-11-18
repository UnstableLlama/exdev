# 50d7dfd94b8fed3d61c9dc4822008e8033f8ac6f


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/50d7dfd94b8fed3d61c9dc4822008e8033f8ac6f) · [Evidence ledger](draft.json)

Requests float32 gate/up projection results and MLP outputs throughout Cohere2, selecting an existing float activation-and-clamp path while retaining half activation inputs to down projections. Numerical benefits remain unmeasured.

- [Cohere2 MLP precision boundaries](#models)

## Problem

Cohere2 previously left GatedMLP intermediate and output dtypes unspecified. The FP16 backend consequently defaulted its projection outputs to half precision; the change explicitly requests float32 for both. [source; call_6106172d597c4b2b94e66486924d6b5c, call_1d50e228752a4d7eaf259b95888191e1, call_53037c84877c41e4b19051b759f648ab]

## Reasoning

The likely purpose is to reduce overflow in Cohere2 MLP projections and gated activations. Selecting float intermediates also selects an existing activation kernel that clamps its half-precision result, so this is more than a final output cast. [inference; call_6106172d597c4b2b94e66486924d6b5c, call_fdbfa0c3ea9449d3a39021d96718f92f, call_35e2747e928c448183ae9abe06de4f79]

## Impact

Every Cohere2 decoder layer receives the new settings. Checkpoint names, dimensions, weights, attention configuration and final vocabulary projection are unchanged. [source; call_6106172d597c4b2b94e66486924d6b5c, call_a7876656e783433391ebb44a980886cd]

The precision policy uses larger gate/up and down-output buffers, trading activation storage for numerical range. Neither its memory cost nor conversion or inference improvements were measured. [inference; call_1d50e228752a4d7eaf259b95888191e1, call_53037c84877c41e4b19051b759f648ab]

## Source Notes

Read the Cohere2 introduction entry, which establishes the reused parallel decoder and shared calibration labels; the component-selection entry, which records Cohere2's text-component mapping; and the architecture-default chat entry, which concerns an unrelated method in the same file. [ancestor; call_6707cdc666af4af9b41477ffdd9b2926, call_d14a593d5e7c425886b766d4a2f9af3e, call_a2320414d50f45d8920e1f5fce3c4b14]

The padding-control entry records an inherited missing odd-element activation tail. Current source still processes pairs only, but Cohere2 retains the default 128-element projection padding, rather than exposing the entry's unpadded odd-size trigger. [source; call_52a37d651a0f46f6a1b6a8c2cc0edcd2, call_a7876656e783433391ebb44a980886cd, call_1d50e228752a4d7eaf259b95888191e1, call_fdbfa0c3ea9449d3a39021d96718f92f]

Issue #34, “torch._C._LinAlgError on last layer of quant,” reports Cohere2 conversion failure with infinite block.parallel.down inputs. Turboderp described possible post-activation overflow and suggested clamping. Issue #53, “Command A support,” began as a support request and later reported similar conversion failures. Their relationship to this task is inferred from the matching architecture, projection path and numerical symptoms, not an explicit commit reference. [inference; call_35e2747e928c448183ae9abe06de4f79, call_ddfa1ce99f744f65bbb99bf1db4daa46, call_b9fe0afd13804115b1ab3d79345b0820, call_6106172d597c4b2b94e66486924d6b5c]

Issue #52, “Error converting moonshotai/Kimi-Dev-72B,” contains turboderp's recommendation to request float GatedMLP output for a different architecture, followed by the reporter's successful-conversion report. This is an analogous precision remedy, not validation of this Cohere2 change. Issue #42, “converting to 3.0 bpw causes error; block state has 0 inf values and 34 NaN values,” concerns Miqu and Command-R-Plus; its shared Linear path does not establish the same cause. [inference; call_9427004cee0e4395b842928dad7c726a, call_d86797b1a2a1451cb773aa3bde0747ac, call_197ee07fb49c4125956f00d4aff5c61a]

Other shared-file discussions were inspected: #7, “quantizing model: undefined symbol: __cxa_call_terminate,” concerns extension loading; #55, “Possible GLM4 32B regression,” concerns fused-weight construction; and #48, “`RuntimeError` when requesting logprobs with Gemma 3 models,” concerns logits dimensions. Their inferred overlap is through imported modules or shared utility files, not evidence that this precision change remedies them. [inference; call_292a8161146e4e2abad4aa96e791b386, call_5f14b64081014a0da0bd7171ce65dbdd, call_03b2394768064c308b5da6bee482fef8, call_197ee07fb49c4125956f00d4aff5c61a, call_8b62cf78df534ad1bb2abb548006a001]

<a id="models"></a>

## Cohere2 MLP precision boundaries

Cohere2Model.__init__ adds interm_dtype=torch.float and out_dtype=torch.float to each GatedMLP. GatedMLP stores these independently: intermediate dtype configures gate/up Linear outputs, while output dtype configures each down projection and the returned result. [source; call_6106172d597c4b2b94e66486924d6b5c, call_1d50e228752a4d7eaf259b95888191e1]

This does not make the entire MLP float32. ParallelDecoderBlock normalizes its shared branch input to half. Gate/up now produce float outputs, but GatedMLP allocates a separate half activation buffer and computes silu(gate) * up into it. That half buffer feeds down; down outputs and any slice accumulation use the requested float dtype. [source; call_864415ae86904791b8139ad23834f7ab, call_1d50e228752a4d7eaf259b95888191e1]

The two settings protect different boundaries. interm_dtype selects silu_mul's float-input branch, which evaluates activation and multiplication in float, converts to half, then clamps to ±65504. The half-input branch instead uses half2 arithmetic without that clamp. out_dtype separately avoids forcing the down-projection result back into half before residual addition. [source; call_fdbfa0c3ea9449d3a39021d96718f92f, call_1d50e228752a4d7eaf259b95888191e1, call_864415ae86904791b8139ad23834f7ab]

For unquantized LinearFP16, output dtype resolves as call override, stored dtype, then half. With half input and float output, forward selects ext.hgemm rather than its same-dtype torch.matmul branch. hgemm requires half operands and uses cublasGemmEx with float output and CUBLAS_COMPUTE_32F. Thus the change requests wider projection results without changing stored weights to float32. [source; call_53037c84877c41e4b19051b759f648ab, call_20a9d123342e44e88f66a928c1502466, call_197ee07fb49c4125956f00d4aff5c61a]

Linear also forwards its stored output dtype into loaded or newly converted LinearEXL3 instances. LinearEXL3 allocates that dtype in both reconstructed-matmul and direct-quantized routes. Its existing reconstruction selection remains unchanged; this commit changes output precision, not that dispatch rule. [source; call_197ee07fb49c4125956f00d4aff5c61a, call_f5a1acf168ed414893816edb25b77158, call_6106172d597c4b2b94e66486924d6b5c]

The direct consumer, ParallelDecoderBlock.forward, adds the MLP result in place to the existing residual; the new float MLP output does not itself replace the residual with a float tensor. Its prefill shortcut still returns before executing the MLP. The explicit forward dtype override remains supported by to2 and takes priority over the configured return dtype. [source; call_864415ae86904791b8139ad23834f7ab, call_1d50e228752a4d7eaf259b95888191e1, call_8b62cf78df534ad1bb2abb548006a001]

A standard-library scalar check decoded 65504 as the largest finite binary16 value. A modeled gated product of 80000 converted to infinity in half but saturated to 65504 with the float-path clamp. A second example, gate=70000 and up=0, produced NaN after first overflowing the gate to half, versus zero when retaining the gate in wider arithmetic. These illustrate distinct projection and activation hazards; Python arithmetic does not reproduce CUDA's float32 approximations. [execution; call_bb877c96f5a144ce99758855a1aea159]

All three inspected configurations select Cohere2ForCausalLM and silu, so the unconditional settings apply model by model: CohereLabs/c4ai-command-a-03-2025 uses hidden/intermediate widths 12288/36864 and 64 layers; c4ai-command-r7b-12-2024 uses 4096/14336 and 32 layers; c4ai-command-r7b-arabic-02-2025 likewise uses 4096/14336 and 32 layers. Their declared bfloat16 checkpoint dtype does not override these constructor arguments. [source; call_21e868c7a20a4b108598705d3c6eb99b, call_b6e4c07738014ab8bfb7ca19e4de3b08, call_98b97dc226b34086adaba0d52b897abe, call_a7876656e783433391ebb44a980886cd, call_6106172d597c4b2b94e66486924d6b5c]

Representative layer-zero headers contain the unchanged model.layers.0.mlp gate_proj/up_proj weights with shapes [36864,12288] for Command A and [14336,4096] for each R7B; down_proj has the reversed dimensions. These agree with the existing output-row/input-column loading layout. The inspected MLP groups contain no biases or weight_scale_inv tensors, which Linear requests optionally; primary weights exist, so fused fallback is unnecessary. No unused stored tensor was identified in these inspected header subsets. [source; call_9f948b2a043840efb098e22de643954a, call_4626d262dabf4538bb0f7207332c6a82, call_810ae143b6f44707a07468e8958317a1, call_197ee07fb49c4125956f00d4aff5c61a, call_a7876656e783433391ebb44a980886cd]

## Uncertainty and limits

No repository model, checkpoint conversion, inference, PyTorch operation or CUDA kernel was executed. Numerical examples use standard-library scalar transcription, not GPU arithmetic or checkpoint values.

The source establishes buffer dtypes and selected implementations, not elimination of all infinities or NaNs, model quality, performance or successful completion of the reported conversions.

Checkpoint inspection covers representative early-layer headers, not every layer, optional tensor or quantized checkpoint. December R7B configuration identity with the historical official file remains unverified.
