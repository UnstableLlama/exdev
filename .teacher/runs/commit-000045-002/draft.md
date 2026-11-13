# 3d51a39d1338d7538853ac03ec641b435b2c66ab


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/3d51a39d1338d7538853ac03ec641b435b2c66ab) · [Evidence ledger](draft.json)

Guard zero-weight bitrate calculation and print no_weights for retained identity blocks, addressing the DeciLM empty-block conversion hazard without changing serialization.

- [Handle weightless blocks without bitrate division](#conversion)

## Problem

The converter computed bits per weight unconditionally, dividing by zero for a weightless module if its preceding serialization completed. [source; call_dba262fba8b0439ba9c1f07e9636523f, call_c232479de483409cac713da1c4f1a971]

## Reasoning

The patch represents an undefined bitrate as None rather than inventing a denominator, and prints no_weights instead of formatting that value numerically. [source; call_4b05a82b036f447287714ed9245282eb]

## Impact

Zero-weight modules can pass the bitrate-reporting step; serialization, state advancement and checkpoint handling remain in the conversion loop. [source; call_4b05a82b036f447287714ed9245282eb, call_dba262fba8b0439ba9c1f07e9636523f]

## Source Notes

Issue 7, “quantizing model: undefined symbol: __cxa_call_terminate,” reports an extension import failure, not zero-weight bitrate calculation. It supplies no evidence that this patch fixes that reported failure. [source; call_f31802e20e36446982f82fffb06825f0, call_4b05a82b036f447287714ed9245282eb]

<a id="conversion"></a>

## Handle weightless blocks without bitrate division

Whole-parent searches found no literal no-op occurrence but located no_op handling in DeciLMModel.__init__. When both attention.no_op and ffn.no_op are true, both branches and their norms become None, while a TransformerBlock is still appended under the original layer index. [source; call_0b86b2248a984d5c83cb26620f59b60f, call_ce8ca81432cf4e9fac766969859805fc, call_b0c484e4cd674497bcf6763f90e23c51]

register_submodule ignores None. Consequently this block has no children, weights_numel() returns sum([]), get_qmaps() is empty, and iteration yields only the block, whose get_tensors() returns {}. Its forward method skips both branches and returns the input through dtype conversion. [source; call_c232479de483409cac713da1c4f1a971, call_2040b8e93537417ca78f3029a3b7a487]

The DeciLM ancestor entry identified this construction and its converter division hazard. It reported fully disabled blocks beginning at index 9 in both nvidia/Llama-3_1-Nemotron-Ultra-253B-CPT-v1 and nvidia/Llama-3_1-Nemotron-Ultra-253B-v1, but none in nvidia/Llama-3_1-Nemotron-51B-Instruct or nvidia/Llama-3_3-Nemotron-Super-49B-v1. [ancestor; call_539a5b3900f841789f95dc6675c72bf9]

Fresh inspection of the pinned Ultra CPT config confirms that block 9 disables both branches. It therefore supplies a concrete configuration example for the weightless construction, not proof of successful end-to-end conversion. [source; call_3545cde8f2664f0392a1eabca4f85a86, call_b0c484e4cd674497bcf6763f90e23c51]

main skips calibration capture and quantization allocation for this block because there are no qmaps or Linear targets. It still passes an empty tensor dictionary to save_file at work_dir/qtensors/model.layers.<index>.safetensors; prepare_env creates the qtensors directory. The patch does not change that save operation. [source; call_dba262fba8b0439ba9c1f07e9636523f, call_c232479de483409cac713da1c4f1a971, call_4b05a82b036f447287714ed9245282eb]

dsize counts tensor payload bytes, not file overhead; multiplication by 8 converts those bytes to bits. The new conditional removes the inherited zero-denominator calculation while preserving the ratio for nonzero weight counts. It does not remove the block from processing. [source; call_9e97fba90c744e169d1d394290fd2265, call_4b05a82b036f447287714ed9245282eb]

After state advancement, feedback retains the Quantized label and padded module key, prints no_weights instead of bpw, then rfn: 0.000000 and elapsed seconds. For this block, error stays zero because error accumulation requires Linear targets; this is not a measured reconstruction comparison. [source; call_dba262fba8b0439ba9c1f07e9636523f, call_4b05a82b036f447287714ed9245282eb]

A scalar transcription reproduced ZeroDivisionError for the old empty-block expression and None plus no_weights for the patched expression. A nonzero-denominator example retained its numeric bitrate. [execution; call_1cfbd890b0204933aa197ae4a0d9e78b]

The unchanged compiler reads work_dir/qtensors and skips modules whose tensor-size list is empty when allocating output shards. Thus the source path does not manufacture weight tensors for identity blocks. [source; call_9e97fba90c744e169d1d394290fd2265]

## Uncertainty and limits

No model conversion, GPU execution or safetensors serialization was run. Successful writing and reading of an empty tensor dictionary remain unestablished.

The Python check transcribed scalar arithmetic and formatting; it did not execute the converter.

Only the Ultra CPT configuration was freshly inspected for an example; statements about the other reference models are explicitly attributed to ancestor prose.
